import os
from database import get_db_connection

statements = """
INSERT INTO DOCTORS VALUES ('DR-0001', 'Dr. Rajesh Sharma', 'Cardiology', '+91-9876543210', 15, 1500.00, 'ACTIVE');
INSERT INTO DOCTORS VALUES ('DR-0002', 'Dr. Priya Mehta', 'Pediatrics', '(022) 2567-8901', 12, 1000.00, 'ACTIVE');
INSERT INTO DOCTORS VALUES ('DR-0003', 'Dr. Amit Kumar', 'Orthopedics', '9988776655', 20, 1800.00, 'ACTIVE');
INSERT INTO DOCTORS VALUES ('DR-0004', 'Dr. Sneha Patel', 'Dermatology', '+91-8877665544', 8, 1200.00, 'ACTIVE');
INSERT INTO DOCTORS VALUES ('DR-0005', 'Dr. Vikram Singh', 'General Medicine', '7766554433', 25, 800.00, 'ACTIVE');
INSERT INTO DOCTORS VALUES ('DR-0006', 'Dr. Ananya Reddy', 'ENT', '+91-9876501234', 10, 1100.00, 'ON_LEAVE');
INSERT INTO DOCTORS VALUES ('DR-0007', 'Dr. Karthik Rao', 'Neurology', '8899001122', 18, 2000.00, 'ACTIVE');
INSERT INTO DOCTORS VALUES ('DR-0008', 'Dr. Meera Desai', 'Gynecology', '+91-9988112233', 14, 1300.00, 'ACTIVE');

INSERT INTO PATIENTS VALUES ('PT-0001', 'Ramesh Kumar', TO_DATE('1985-05-15', 'YYYY-MM-DD'), 'MALE', '9876543210', 'ramesh.k@gmail.com', 'O+', TO_DATE('2023-01-10', 'YYYY-MM-DD'));
INSERT INTO PATIENTS VALUES ('PT-0002', 'Sita Sharma', TO_DATE('1990-08-22', 'YYYY-MM-DD'), 'FEMALE', '9876543211', 'sita.sharma@yahoo.com', 'A+', TO_DATE('2023-02-15', 'YYYY-MM-DD'));
INSERT INTO PATIENTS VALUES ('PT-0003', 'Arun Patel', TO_DATE('1978-12-05', 'YYYY-MM-DD'), 'MALE', '9876543212', 'arun.patel@outlook.com', 'B+', TO_DATE('2023-03-20', 'YYYY-MM-DD'));
INSERT INTO PATIENTS VALUES ('PT-0004', 'Lakshmi Iyer', TO_DATE('1995-03-18', 'YYYY-MM-DD'), 'FEMALE', '9876543213', 'lakshmi.i@gmail.com', 'AB+', TO_DATE('2023-04-05', 'YYYY-MM-DD'));
INSERT INTO PATIENTS VALUES ('PT-0005', 'Suresh Reddy', TO_DATE('1982-07-30', 'YYYY-MM-DD'), 'MALE', '9876543214', 'suresh.reddy@mail.com', 'O-', TO_DATE('2023-05-12', 'YYYY-MM-DD'));
INSERT INTO PATIENTS VALUES ('PT-0006', 'Kavita Singh', TO_DATE('1988-11-25', 'YYYY-MM-DD'), 'FEMALE', '9876543215', 'kavita.singh@gmail.com', 'A-', TO_DATE('2023-06-18', 'YYYY-MM-DD'));
INSERT INTO PATIENTS VALUES ('PT-0007', 'Deepak Gupta', TO_DATE('1975-04-08', 'YYYY-MM-DD'), 'MALE', '9876543216', 'deepak.g@yahoo.in', 'B-', TO_DATE('2023-07-22', 'YYYY-MM-DD'));
INSERT INTO PATIENTS VALUES ('PT-0008', 'Pooja Nair', TO_DATE('1992-09-14', 'YYYY-MM-DD'), 'FEMALE', '9876543217', 'pooja.nair@gmail.com', 'O+', TO_DATE('2023-08-30', 'YYYY-MM-DD'));
INSERT INTO PATIENTS VALUES ('PT-0009', 'Rajiv Malhotra', TO_DATE('1980-01-20', 'YYYY-MM-DD'), 'MALE', '9876543218', 'rajiv.m@hotmail.com', 'A+', TO_DATE('2023-09-10', 'YYYY-MM-DD'));
INSERT INTO PATIENTS VALUES ('PT-0010', 'Anjali Verma', TO_DATE('1987-06-12', 'YYYY-MM-DD'), 'FEMALE', '9876543219', 'anjali.verma@gmail.com', 'AB-', TO_DATE('2023-10-15', 'YYYY-MM-DD'));
INSERT INTO PATIENTS VALUES ('PT-0011', 'Manoj Yadav', TO_DATE('1993-02-28', 'YYYY-MM-DD'), 'MALE', '9876543220', 'manoj.yadav@mail.com', 'B+', TO_DATE('2024-01-08', 'YYYY-MM-DD'));
INSERT INTO PATIENTS VALUES ('PT-0012', 'Divya Krishnan', TO_DATE('1991-10-05', 'YYYY-MM-DD'), 'FEMALE', '9876543221', 'divya.k@gmail.com', 'O-', TO_DATE('2024-02-20', 'YYYY-MM-DD'));

INSERT INTO APPOINTMENTS VALUES ('APT-00001', 'PT-0001', 'DR-0001', TO_DATE('2024-01-15', 'YYYY-MM-DD'), '09:00', 'COMPLETED', 'Hypertension - regular checkup', 1500.00);
INSERT INTO APPOINTMENTS VALUES ('APT-00002', 'PT-0002', 'DR-0002', TO_DATE('2024-01-15', 'YYYY-MM-DD'), '10:00', 'COMPLETED', 'Child vaccination', 1000.00);
INSERT INTO APPOINTMENTS VALUES ('APT-00003', 'PT-0003', 'DR-0003', TO_DATE('2024-01-16', 'YYYY-MM-DD'), '09:30', 'COMPLETED', 'Knee pain - arthritis suspected', 1800.00);
INSERT INTO APPOINTMENTS VALUES ('APT-00004', 'PT-0001', 'DR-0005', TO_DATE('2024-01-18', 'YYYY-MM-DD'), '11:00', 'COMPLETED', 'Follow-up for hypertension', 800.00);
INSERT INTO APPOINTMENTS VALUES ('APT-00005', 'PT-0004', 'DR-0004', TO_DATE('2024-01-20', 'YYYY-MM-DD'), '14:00', 'COMPLETED', 'Acne treatment', 1200.00);
INSERT INTO APPOINTMENTS VALUES ('APT-00006', 'PT-0005', 'DR-0001', TO_DATE('2024-02-05', 'YYYY-MM-DD'), '09:00', 'COMPLETED', 'Chest pain evaluation', 1500.00);
INSERT INTO APPOINTMENTS VALUES ('APT-00007', 'PT-0006', 'DR-0007', TO_DATE('2024-02-08', 'YYYY-MM-DD'), '10:30', 'COMPLETED', 'Migraine consultation', 2000.00);
INSERT INTO APPOINTMENTS VALUES ('APT-00008', 'PT-0007', 'DR-0005', TO_DATE('2024-02-10', 'YYYY-MM-DD'), '09:00', 'COMPLETED', 'Diabetes management', 800.00);
INSERT INTO APPOINTMENTS VALUES ('APT-00009', 'PT-0001', 'DR-0001', TO_DATE('2024-02-15', 'YYYY-MM-DD'), '09:30', 'COMPLETED', 'Hypertension follow-up', 1500.00);
INSERT INTO APPOINTMENTS VALUES ('APT-00010', 'PT-0008', 'DR-0008', TO_DATE('2024-02-18', 'YYYY-MM-DD'), '11:00', 'COMPLETED', 'Prenatal checkup', 1300.00);
INSERT INTO APPOINTMENTS VALUES ('APT-00011', 'PT-0003', 'DR-0003', TO_DATE('2024-03-01', 'YYYY-MM-DD'), '10:00', 'COMPLETED', 'Knee pain follow-up', 1800.00);
INSERT INTO APPOINTMENTS VALUES ('APT-00012', 'PT-0009', 'DR-0002', TO_DATE('2024-03-05', 'YYYY-MM-DD'), '14:00', 'COMPLETED', 'Child fever consultation', 1000.00);
INSERT INTO APPOINTMENTS VALUES ('APT-00013', 'PT-0010', 'DR-0004', TO_DATE('2024-03-08', 'YYYY-MM-DD'), '15:00', 'COMPLETED', 'Skin allergy', 1200.00);
INSERT INTO APPOINTMENTS VALUES ('APT-00014', 'PT-0007', 'DR-0005', TO_DATE('2024-03-10', 'YYYY-MM-DD'), '09:00', 'COMPLETED', 'Diabetes follow-up', 800.00);
INSERT INTO APPOINTMENTS VALUES ('APT-00015', 'PT-0001', 'DR-0001', TO_DATE('2024-03-15', 'YYYY-MM-DD'), '10:00', 'COMPLETED', 'Hypertension checkup', 1500.00);
INSERT INTO APPOINTMENTS VALUES ('APT-00016', 'PT-0005', 'DR-0007', TO_DATE('2024-03-18', 'YYYY-MM-DD'), '11:30', 'COMPLETED', 'Headache assessment', 2000.00);
INSERT INTO APPOINTMENTS VALUES ('APT-00017', 'PT-0011', 'DR-0005', TO_DATE('2024-03-20', 'YYYY-MM-DD'), '09:30', 'COMPLETED', 'General checkup', 800.00);
INSERT INTO APPOINTMENTS VALUES ('APT-00018', 'PT-0012', 'DR-0008', TO_DATE('2024-03-22', 'YYYY-MM-DD'), '14:00', 'COMPLETED', 'Gynec consultation', 1300.00);
INSERT INTO APPOINTMENTS VALUES ('APT-00019', 'PT-0006', 'DR-0007', TO_DATE('2024-03-25', 'YYYY-MM-DD'), '10:00', 'SCHEDULED', NULL, NULL);
INSERT INTO APPOINTMENTS VALUES ('APT-00020', 'PT-0001', 'DR-0001', TO_DATE('2024-03-28', 'YYYY-MM-DD'), '09:00', 'SCHEDULED', NULL, NULL);
INSERT INTO APPOINTMENTS VALUES ('APT-00021', 'PT-0003', 'DR-0003', TO_DATE('2024-03-30', 'YYYY-MM-DD'), '11:00', 'SCHEDULED', NULL, NULL);
INSERT INTO APPOINTMENTS VALUES ('APT-00022', 'PT-0002', 'DR-0002', TO_DATE('2024-02-20', 'YYYY-MM-DD'), '10:00', 'CANCELLED', NULL, NULL);
INSERT INTO APPOINTMENTS VALUES ('APT-00023', 'PT-0004', 'DR-0004', TO_DATE('2024-03-12', 'YYYY-MM-DD'), '15:00', 'CANCELLED', NULL, NULL);
INSERT INTO APPOINTMENTS VALUES ('APT-00024', 'PT-0010', 'DR-0007', TO_DATE('2024-03-23', 'YYYY-MM-DD'), '09:00', 'COMPLETED', 'Neurological assessment', 2000.00);
INSERT INTO APPOINTMENTS VALUES ('APT-00025', 'PT-0007', 'DR-0001', TO_DATE('2024-03-23', 'YYYY-MM-DD'), '14:00', 'COMPLETED', 'Cardiac screening', 1500.00);

INSERT INTO PRESCRIPTIONS VALUES ('RX-00001', 'APT-00001', 'Amlodipine', '5mg', 'Once daily', 30, 'Take with food');
INSERT INTO PRESCRIPTIONS VALUES ('RX-00002', 'APT-00001', 'Aspirin', '75mg', 'Once daily', 30, 'Take after breakfast');
INSERT INTO PRESCRIPTIONS VALUES ('RX-00003', 'APT-00002', 'Paracetamol', '250mg', 'SOS (if fever)', 3, 'For fever management');
INSERT INTO PRESCRIPTIONS VALUES ('RX-00004', 'APT-00003', 'Diclofenac', '50mg', 'Twice daily', 7, 'Take after meals');
INSERT INTO PRESCRIPTIONS VALUES ('RX-00005', 'APT-00003', 'Calcium supplement', '500mg', 'Once daily', 30, 'Take with milk');
INSERT INTO PRESCRIPTIONS VALUES ('RX-00006', 'APT-00004', 'Amlodipine', '5mg', 'Once daily', 30, 'Continue existing dose');
INSERT INTO PRESCRIPTIONS VALUES ('RX-00007', 'APT-00005', 'Clindamycin gel', '1%', 'Apply twice daily', 14, 'Clean face before application');
INSERT INTO PRESCRIPTIONS VALUES ('RX-00008', 'APT-00005', 'Vitamin A', '5000IU', 'Once daily', 30, 'Take with food');
INSERT INTO PRESCRIPTIONS VALUES ('RX-00009', 'APT-00006', 'Atorvastatin', '10mg', 'Once daily', 30, 'Take at bedtime');
INSERT INTO PRESCRIPTIONS VALUES ('RX-00010', 'APT-00006', 'Ecosprin', '75mg', 'Once daily', 30, 'Blood thinner');
INSERT INTO PRESCRIPTIONS VALUES ('RX-00011', 'APT-00007', 'Sumatriptan', '50mg', 'SOS (during attack)', 10, 'Take at onset of headache');
INSERT INTO PRESCRIPTIONS VALUES ('RX-00012', 'APT-00007', 'Propranolol', '40mg', 'Twice daily', 30, 'Preventive medication');
INSERT INTO PRESCRIPTIONS VALUES ('RX-00013', 'APT-00008', 'Metformin', '500mg', 'Twice daily', 30, 'Take with meals');
INSERT INTO PRESCRIPTIONS VALUES ('RX-00014', 'APT-00008', 'Glimepiride', '1mg', 'Once daily', 30, 'Take before breakfast');
INSERT INTO PRESCRIPTIONS VALUES ('RX-00015', 'APT-00009', 'Amlodipine', '5mg', 'Once daily', 30, 'Continue medication');
INSERT INTO PRESCRIPTIONS VALUES ('RX-00016', 'APT-00009', 'Aspirin', '75mg', 'Once daily', 30, 'Continue medication');
INSERT INTO PRESCRIPTIONS VALUES ('RX-00017', 'APT-00010', 'Folic acid', '5mg', 'Once daily', 30, 'Important for fetal development');
INSERT INTO PRESCRIPTIONS VALUES ('RX-00018', 'APT-00010', 'Iron supplement', '100mg', 'Once daily', 30, 'Take with vitamin C');
INSERT INTO PRESCRIPTIONS VALUES ('RX-00019', 'APT-00011', 'Glucosamine', '500mg', 'Twice daily', 60, 'Joint health supplement');
INSERT INTO PRESCRIPTIONS VALUES ('RX-00020', 'APT-00011', 'Diclofenac', '50mg', 'SOS (if pain)', 10, 'Pain relief as needed');
INSERT INTO PRESCRIPTIONS VALUES ('RX-00021', 'APT-00012', 'Paracetamol syrup', '5ml', 'Every 6 hours if fever', 3, 'Monitor temperature');
INSERT INTO PRESCRIPTIONS VALUES ('RX-00022', 'APT-00012', 'Amoxicillin', '250mg', 'Thrice daily', 5, 'Complete full course');
INSERT INTO PRESCRIPTIONS VALUES ('RX-00023', 'APT-00013', 'Cetirizine', '10mg', 'Once daily', 7, 'Antihistamine');
INSERT INTO PRESCRIPTIONS VALUES ('RX-00024', 'APT-00013', 'Hydrocortisone cream', '1%', 'Apply twice', 7, 'On affected areas');
INSERT INTO PRESCRIPTIONS VALUES ('RX-00025', 'APT-00014', 'Metformin', '500mg', 'Twice daily', 30, 'Continue medication');
INSERT INTO PRESCRIPTIONS VALUES ('RX-00026', 'APT-00015', 'Amlodipine', '5mg', 'Once daily', 30, 'Regular dose');
INSERT INTO PRESCRIPTIONS VALUES ('RX-00027', 'APT-00016', 'Paracetamol', '500mg', 'SOS', 10, 'For pain relief');
INSERT INTO PRESCRIPTIONS VALUES ('RX-00028', 'APT-00017', 'Multivitamin', '1 tablet', 'Once daily', 30, 'General health');
INSERT INTO PRESCRIPTIONS VALUES ('RX-00029', 'APT-00018', 'Iron supplement', '100mg', 'Once daily', 30, 'For anemia');
INSERT INTO PRESCRIPTIONS VALUES ('RX-00030', 'APT-00024', 'Vitamin B12', '1000mcg', 'Once daily', 30, 'Nerve health');
"""

def insert_data():
    conn = get_db_connection()
    if conn is None:
        print("Failed to connect to database.")
        return

    cursor = conn.cursor()
    success_count = 0
    error_count = 0
    for stmt in statements.split(';'):
        stmt = stmt.strip()
        if stmt:
            try:
                cursor.execute(stmt)
                success_count += 1
            except Exception as e:
                print(f"Error executing statement: {stmt}\nError: {e}")
                error_count += 1

    try:
        conn.commit()
    except Exception as e:
        print(f"Error committing transaction: {e}")
    finally:
        cursor.close()
        conn.close()
        print(f"Insertion complete. {success_count} statements succeeded. {error_count} failed.")

if __name__ == "__main__":
    insert_data()
