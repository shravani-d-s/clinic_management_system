import os
import uuid
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from database import get_db_connection, fetch_all_dict, fetch_one_dict
from models import LoginRequest, PatientCreate, AppointmentCreate, PrescriptionCreate, ConsultationCreate, PaymentUpdate
import oracledb

app = FastAPI(title="Clinic Management System API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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

def generate_id(prefix: str):
    return f"{prefix}-{uuid.uuid4().hex[:5].upper()}"

@app.get("/")
def read_root():
    return {"message": "Welcome to Clinic Management System API"}

# --- AUTH API ---
@app.post("/api/auth/login")
def login(req: LoginRequest, db = Depends(get_db)):
    cursor = db.cursor()
    if req.role == "doctor":
        cursor.execute(
            "SELECT doctor_id, first_name, last_name, email FROM Doctors WHERE (email = :1 OR phone = :2) AND password = :3",
            (req.email_or_phone, req.email_or_phone, req.password)
        )
        user = fetch_one_dict(cursor)
        if not user:
            raise HTTPException(401, "Invalid credentials")
        return {"id": user["doctor_id"], "name": f"Dr. {user['first_name']} {user['last_name']}", "role": "doctor"}
    elif req.role == "patient":
        cursor.execute(
            "SELECT patient_id, first_name, last_name FROM Patients WHERE (email = :1 OR phone = :2) AND password = :3",
            (req.email_or_phone, req.email_or_phone, req.password)
        )
        user = fetch_one_dict(cursor)
        if not user:
            raise HTTPException(401, "Invalid credentials")
        return {"id": user["patient_id"], "name": f"{user['first_name']} {user['last_name']}", "role": "patient"}
    raise HTTPException(400, "Invalid role")


# --- PATIENTS API ---
@app.post("/api/patients", status_code=201)
def register_patient(patient: PatientCreate, db = Depends(get_db)):
    try:
        cursor = db.cursor()
        pid = generate_id("PT")
        sql = """
            INSERT INTO Patients (patient_id, first_name, last_name, dob, gender, phone, email, address, password)
            VALUES (:1, :2, :3, TO_DATE(:4, 'YYYY-MM-DD'), :5, :6, :7, :8, :9)
        """
        cursor.execute(sql, (
            pid, patient.first_name, patient.last_name, patient.dob, patient.gender,
            patient.phone, patient.email, patient.address, patient.password
        ))
        db.commit()
        return {"patient_id": pid, "message": "Patient registered successfully"}
    except oracledb.IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Patient with this phone already exists.")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/patients")
def list_patients(db = Depends(get_db)):
    try:
        cursor = db.cursor()
        cursor.execute("SELECT patient_id, first_name, last_name, TO_CHAR(dob, 'YYYY-MM-DD') as dob, gender, phone, email, address FROM Patients ORDER BY patient_id DESC")
        return fetch_all_dict(cursor)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/patients/{patient_id}/consultations")
def patient_consultations(patient_id: str, db = Depends(get_db)):
    try:
        cursor = db.cursor()
        sql = """
            SELECT mr.record_id, mr.symptoms, mr.treatment, p.prescription_id, p.notes, 
                   TO_CHAR(a.appointment_date, 'YYYY-MM-DD') as appointment_date,
                   d.first_name || ' ' || d.last_name as doctor_name
            FROM Medical_Records mr
            JOIN Appointments a ON mr.appointment_id = a.appointment_id
            JOIN Doctors d ON a.doctor_id = d.doctor_id
            LEFT JOIN Prescriptions p ON a.appointment_id = p.appointment_id
            WHERE a.patient_id = :1
            ORDER BY a.appointment_date DESC
        """
        cursor.execute(sql, (patient_id,))
        consultations = fetch_all_dict(cursor)
        for c in consultations:
            if c['prescription_id']:
                cursor.execute("SELECT name, dosage, frequency, duration FROM Medications WHERE prescription_id = :1", (c['prescription_id'],))
                c['medications'] = fetch_all_dict(cursor)
            else:
                c['medications'] = []
        return consultations
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --- DOCTORS API ---
@app.get("/api/doctors")
def list_doctors(db = Depends(get_db)):
    try:
        cursor = db.cursor()
        sql = """
            SELECT d.doctor_id, d.first_name, d.last_name, dept.name as department_name
            FROM Doctors d
            JOIN Departments dept ON d.department_id = dept.department_id
        """
        cursor.execute(sql)
        return fetch_all_dict(cursor)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --- APPOINTMENTS API ---
@app.post("/api/appointments", status_code=201)
def book_appointment(appointment: AppointmentCreate, db = Depends(get_db)):
    try:
        cursor = db.cursor()
        aid = generate_id("APT")
        sql = """
            INSERT INTO Appointments (appointment_id, patient_id, doctor_id, appointment_date, start_time, end_time, status)
            VALUES (:1, :2, :3, TO_DATE(:4, 'YYYY-MM-DD'), :5, :6, 'Scheduled')
        """
        cursor.execute(sql, (
            aid, appointment.patient_id, appointment.doctor_id, appointment.appointment_date,
            appointment.start_time, appointment.end_time
        ))
        db.commit()
        return {"appointment_id": aid, "message": "Appointment scheduled successfully"}
    except oracledb.DatabaseError as e:
        db.rollback()
        error_obj, = e.args
        if error_obj.code == 20001:
            raise HTTPException(status_code=409, detail=error_obj.message)
        raise HTTPException(status_code=400, detail=error_obj.message)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/appointments")
def list_appointments(patient_id: str = None, doctor_id: str = None, db = Depends(get_db)):
    try:
        cursor = db.cursor()
        sql = """
            SELECT a.appointment_id, p.first_name || ' ' || p.last_name as patient_name,
                   d.first_name || ' ' || d.last_name as doctor_name,
                   TO_CHAR(a.appointment_date, 'YYYY-MM-DD') as appointment_date,
                   a.start_time, a.end_time, a.status,
                   p.patient_id, d.doctor_id
            FROM Appointments a
            JOIN Patients p ON a.patient_id = p.patient_id
            JOIN Doctors d ON a.doctor_id = d.doctor_id
            WHERE 1=1
        """
        params = {}
        if patient_id:
            sql += " AND a.patient_id = :pat_id"
            params['pat_id'] = patient_id
        if doctor_id:
            sql += " AND a.doctor_id = :doc_id"
            params['doc_id'] = doctor_id
            
        sql += " ORDER BY a.appointment_date DESC, a.start_time DESC"
        
        cursor.execute(sql, params)
        return fetch_all_dict(cursor)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/appointments/{appointment_id}")
def cancel_appointment(appointment_id: str, db = Depends(get_db)):
    try:
        cursor = db.cursor()
        # First check status
        cursor.execute("SELECT status FROM Appointments WHERE appointment_id = :1", (appointment_id,))
        row = fetch_one_dict(cursor)
        if not row:
            raise HTTPException(404, "Appointment not found")
        
        # We can either delete or cancel. Let's do a hard delete as requested.
        # But we must delete Billing first because of fk_bill_app
        cursor.execute("DELETE FROM Billing WHERE appointment_id = :1", (appointment_id,))
        cursor.execute("DELETE FROM Appointments WHERE appointment_id = :1", (appointment_id,))
        
        db.commit()
        return {"message": "Appointment deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(500, str(e))


# --- CONSULTATIONS API ---
@app.post("/api/consultations", status_code=201)
def create_consultation(consultation: ConsultationCreate, db = Depends(get_db)):
    try:
        cursor = db.cursor()
        
        # 1. Insert Medical Record (Mandatory)
        record_id = generate_id("MR")
        record_sql = """
            INSERT INTO Medical_Records (record_id, appointment_id, symptoms, treatment)
            VALUES (:1, :2, :3, :4)
        """
        cursor.execute(record_sql, (record_id, consultation.appointment_id, consultation.symptoms, consultation.treatment))

        # 2. Insert Prescription (Optional)
        presc_id = None
        if consultation.notes or consultation.medications:
            presc_id = generate_id("RX")
            presc_sql = """
                INSERT INTO Prescriptions (prescription_id, appointment_id, notes)
                VALUES (:1, :2, :3)
            """
            cursor.execute(presc_sql, (presc_id, consultation.appointment_id, consultation.notes))

            # 3. Insert Medications
            if consultation.medications:
                med_sql = """
                    INSERT INTO Medications (medication_id, prescription_id, name, dosage, frequency, duration)
                    VALUES (:1, :2, :3, :4, :5, :6)
                """
                for m in consultation.medications:
                    mid = generate_id("MED")
                    cursor.execute(med_sql, (mid, presc_id, m.name, m.dosage, m.frequency, m.duration))
        
        # 4. Update appointment status to Completed
        cursor.execute("UPDATE Appointments SET status = 'Completed' WHERE appointment_id = :1", (consultation.appointment_id,))
        
        db.commit()
        return {"record_id": record_id, "prescription_id": presc_id, "message": "Consultation recorded and appointment completed"}
    except oracledb.IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Consultation for this appointment may already exist")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# --- BILLING API ---
@app.get("/api/billing/report")
def billing_report(doctor_id: str = None, db = Depends(get_db)):
    try:
        cursor = db.cursor()
        
        # Modify billing report query to optionally filter by doctor
        doc_filter = " WHERE a.doctor_id = :1 " if doctor_id else ""
        doc_params = (doctor_id,) if doctor_id else ()
        
        status_sql = f"""
            SELECT b.payment_status, SUM(b.amount) as total_amount 
            FROM Billing b
            JOIN Appointments a ON b.appointment_id = a.appointment_id
            {doc_filter}
            GROUP BY b.payment_status
        """
        cursor.execute(status_sql, doc_params)
        status_summary = fetch_all_dict(cursor)

        dept_sql = """
            SELECT dept.name as department_name, count(a.appointment_id) as appointment_count
            FROM Appointments a
            JOIN Doctors d ON a.doctor_id = d.doctor_id
            JOIN Departments dept ON d.department_id = dept.department_id
            GROUP BY dept.name
        """
        cursor.execute(dept_sql)
        dept_summary = fetch_all_dict(cursor)

        bills_sql = f"""
            SELECT b.bill_id, p.first_name || ' ' || p.last_name as patient_name,
                   TO_CHAR(a.appointment_date, 'YYYY-MM-DD') as appt_date,
                   b.amount, b.payment_status, b.payment_mode
            FROM Billing b
            JOIN Appointments a ON b.appointment_id = a.appointment_id
            JOIN Patients p ON a.patient_id = p.patient_id
            {doc_filter}
            ORDER BY b.bill_id DESC
        """
        cursor.execute(bills_sql, doc_params)
        latest_bills = fetch_all_dict(cursor)

        return {
            "status_summary": status_summary,
            "department_summary": dept_summary,
            "latest_bills": latest_bills
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/billing/{bill_id}/pay")
def pay_bill(bill_id: str, payment: PaymentUpdate, db = Depends(get_db)):
    try:
        cursor = db.cursor()
        cursor.execute(
            "UPDATE Billing SET payment_mode = :1 WHERE bill_id = :2 AND payment_status = 'Pending'",
            (payment.payment_mode, bill_id)
        )
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Bill not found or already paid")
        db.commit()
        return {"message": "Payment updated successfully"}
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, reload_excludes=["venv/*", ".env/*"])
