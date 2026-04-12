from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from database import get_db_connection, fetch_all_dict, fetch_one_dict
from models import PatientCreate, AppointmentCreate, PrescriptionCreate, PaymentUpdate
import oracledb

app = FastAPI(title="Clinic Management System API")

# Update CORS for Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    try:
        yield conn
    finally:
        conn.close()

@app.get("/")
def read_root():
    return {"message": "Welcome to Clinic Management System API"}

# --- Patients API ---

@app.post("/api/patients", status_code=201)
def register_patient(patient: PatientCreate, db = Depends(get_db)):
    try:
        cursor = db.cursor()
        sql = """
            INSERT INTO Patients (first_name, last_name, dob, gender, phone, email, address)
            VALUES (:1, :2, TO_DATE(:3, 'YYYY-MM-DD'), :4, :5, :6, :7)
            RETURNING patient_id INTO :8
        """
        patient_id_var = cursor.var(oracledb.NUMBER)
        cursor.execute(sql, (
            patient.first_name, patient.last_name, patient.dob, patient.gender,
            patient.phone, patient.email, patient.address, patient_id_var
        ))
        patient_id = int(patient_id_var.getvalue()[0])
        return {"patient_id": patient_id, "message": "Patient registered successfully"}
    except oracledb.IntegrityError as e:
        raise HTTPException(status_code=400, detail="Patient with this phone already exists.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/patients")
def list_patients(db = Depends(get_db)):
    try:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Patients ORDER BY patient_id DESC")
        patients = fetch_all_dict(cursor)
        return patients
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- Doctors API ---
@app.get("/api/doctors")
def list_doctors(db = Depends(get_db)):
    try:
        cursor = db.cursor()
        # Join with department to get department name
        sql = """
            SELECT d.doctor_id, d.first_name, d.last_name, dept.name as department_name
            FROM Doctors d
            JOIN Departments dept ON d.department_id = dept.department_id
        """
        cursor.execute(sql)
        doctors = fetch_all_dict(cursor)
        return doctors
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- Appointments API ---
@app.post("/api/appointments", status_code=201)
def book_appointment(appointment: AppointmentCreate, db = Depends(get_db)):
    try:
        cursor = db.cursor()
        sql = """
            INSERT INTO Appointments (patient_id, doctor_id, appointment_date, start_time, end_time)
            VALUES (:1, :2, TO_DATE(:3, 'YYYY-MM-DD'), :4, :5)
            RETURNING appointment_id INTO :6
        """
        appointment_id_var = cursor.var(oracledb.NUMBER)
        cursor.execute(sql, (
            appointment.patient_id, appointment.doctor_id, appointment.appointment_date,
            appointment.start_time, appointment.end_time, appointment_id_var
        ))
        appt_id = int(appointment_id_var.getvalue()[0])
        return {"appointment_id": appt_id, "message": "Appointment scheduled successfully"}
    except oracledb.DatabaseError as e:
        error_obj, = e.args
        # -20001 is our custom error from the trigger for double booking
        if error_obj.code == 20001:
            raise HTTPException(status_code=409, detail=error_obj.message)
        raise HTTPException(status_code=400, detail=error_obj.message)

@app.get("/api/appointments")
def list_appointments(db = Depends(get_db)):
    try:
        cursor = db.cursor()
        sql = """
            SELECT a.appointment_id, p.first_name || ' ' || p.last_name as patient_name,
                   d.first_name || ' ' || d.last_name as doctor_name,
                   TO_CHAR(a.appointment_date, 'YYYY-MM-DD') as appointment_date,
                   a.start_time, a.end_time, a.status
            FROM Appointments a
            JOIN Patients p ON a.patient_id = p.patient_id
            JOIN Doctors d ON a.doctor_id = d.doctor_id
            ORDER BY a.appointment_date DESC, a.start_time DESC
        """
        cursor.execute(sql)
        return fetch_all_dict(cursor)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- Prescriptions API ---
@app.post("/api/prescriptions", status_code=201)
def create_prescription(prescription: PrescriptionCreate, db = Depends(get_db)):
    # Requires manual transaction management due to multiple inserts
    try:
        cursor = db.cursor()
        
        # 1. Insert Prescription
        presc_sql = """
            INSERT INTO Prescriptions (appointment_id, notes)
            VALUES (:1, :2)
            RETURNING prescription_id INTO :3
        """
        presc_id_var = cursor.var(oracledb.NUMBER)
        cursor.execute(presc_sql, (prescription.appointment_id, prescription.notes, presc_id_var))
        presc_id = int(presc_id_var.getvalue()[0])

        # 2. Insert Medications
        if prescription.medications:
            med_sql = """
                INSERT INTO Medications (prescription_id, name, dosage, frequency, duration)
                VALUES (:1, :2, :3, :4, :5)
            """
            med_data = [
                (presc_id, m.name, m.dosage, m.frequency, m.duration) for m in prescription.medications
            ]
            cursor.executemany(med_sql, med_data)
        
        # 3. Update appointment status to Completed
        cursor.execute("UPDATE Appointments SET status = 'Completed' WHERE appointment_id = :1", (prescription.appointment_id,))
        
        return {"prescription_id": presc_id, "message": "Prescription created and appointment completed"}
    except oracledb.IntegrityError as e:
        raise HTTPException(status_code=400, detail="Prescription for this appointment may already exist")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- Billing API ---
@app.get("/api/billing/report")
def billing_report(db = Depends(get_db)):
    try:
        cursor = db.cursor()
        # Provide aggregated data for charting
        # e.g., Total pending vs paid amount, and revenue by department
        
        # Status summary
        cursor.execute("SELECT payment_status, SUM(amount) as total_amount FROM Billing GROUP BY payment_status")
        status_summary = fetch_all_dict(cursor)

        # Appointments count per department
        sql_dept = """
            SELECT dept.name as department_name, count(a.appointment_id) as appointment_count
            FROM Appointments a
            JOIN Doctors d ON a.doctor_id = d.doctor_id
            JOIN Departments dept ON d.department_id = dept.department_id
            GROUP BY dept.name
        """
        cursor.execute(sql_dept)
        dept_summary = fetch_all_dict(cursor)

        # Latest Bills
        sql_bills = """
            SELECT b.bill_id, p.first_name || ' ' || p.last_name as patient_name,
                   b.amount, b.payment_status, b.payment_mode
            FROM Billing b
            JOIN Appointments a ON b.appointment_id = a.appointment_id
            JOIN Patients p ON a.patient_id = p.patient_id
            ORDER BY b.bill_id DESC
        """
        cursor.execute(sql_bills)
        latest_bills = fetch_all_dict(cursor)

        return {
            "status_summary": status_summary,
            "department_summary": dept_summary,
            "latest_bills": latest_bills
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/billing/{bill_id}/pay")
def pay_bill(bill_id: int, payment: PaymentUpdate, db = Depends(get_db)):
    try:
        cursor = db.cursor()
        cursor.execute(
            "UPDATE Billing SET payment_mode = :1 WHERE bill_id = :2 AND payment_status = 'Pending'",
            (payment.payment_mode, bill_id)
        )
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Bill not found or already paid")
        return {"message": "Payment updated successfully, Trigger executed state change to 'Paid'"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    # Make sure to specify the reload_excludes or reload_dirs
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True, 
        reload_excludes=["venv/*", ".env/*"] 
    )
