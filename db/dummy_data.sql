--------------------------------------------------
-- DEPARTMENTS
--------------------------------------------------
INSERT INTO Departments VALUES ('D001','Cardiology',NULL);
INSERT INTO Departments VALUES ('D002','Pediatrics',NULL);
INSERT INTO Departments VALUES ('D003','Orthopedics',NULL);
INSERT INTO Departments VALUES ('D004','Dermatology',NULL);
INSERT INTO Departments VALUES ('D005','General Medicine',NULL);
INSERT INTO Departments VALUES ('D006','ENT',NULL);
INSERT INTO Departments VALUES ('D007','Neurology',NULL);
INSERT INTO Departments VALUES ('D008','Gynecology',NULL);

--------------------------------------------------
-- DOCTORS
--------------------------------------------------
INSERT INTO Doctors VALUES ('DR-0001','D001','Rajesh','Sharma','rajesh@clinic.com','9876543210','doc_rajesh');
INSERT INTO Doctors VALUES ('DR-0002','D002','Priya','Mehta','priya@clinic.com','9876543211','doc_priya');
INSERT INTO Doctors VALUES ('DR-0003','D003','Amit','Kumar','amit@clinic.com','9988776655','doc_amit');
INSERT INTO Doctors VALUES ('DR-0004','D004','Sneha','Patel','sneha@clinic.com','8877665544','doc_sneha');
INSERT INTO Doctors VALUES ('DR-0005','D005','Vikram','Singh','vikram@clinic.com','7766554433','doc_vikram');
INSERT INTO Doctors VALUES ('DR-0006','D006','Ananya','Reddy','ananya@clinic.com','9876501234','doc_ananya');
INSERT INTO Doctors VALUES ('DR-0007','D007','Karthik','Rao','karthik@clinic.com','8899001122','doc_karthik');
INSERT INTO Doctors VALUES ('DR-0008','D008','Meera','Desai','meera@clinic.com','9988112233','doc_meera');

--------------------------------------------------
-- SET HEAD DOCTORS
--------------------------------------------------
UPDATE Departments SET head_doctor_id='DR-0001' WHERE department_id='D001';
UPDATE Departments SET head_doctor_id='DR-0002' WHERE department_id='D002';
UPDATE Departments SET head_doctor_id='DR-0003' WHERE department_id='D003';
UPDATE Departments SET head_doctor_id='DR-0004' WHERE department_id='D004';

--------------------------------------------------
-- PATIENTS
--------------------------------------------------
INSERT INTO Patients VALUES ('PT-0001','Ramesh','Kumar',DATE '1985-05-15','Male','9876543210','ramesh@gmail.com','Mumbai','pat_ramesh');
INSERT INTO Patients VALUES ('PT-0002','Sita','Sharma',DATE '1990-08-22','Female','9876543211','sita@gmail.com','Mumbai','pat_sita');
INSERT INTO Patients VALUES ('PT-0003','Arun','Patel',DATE '1978-12-05','Male','9876543212','arun@gmail.com','Mumbai','pat_arun');
INSERT INTO Patients VALUES ('PT-0004','Lakshmi','Iyer',DATE '1995-03-18','Female','9876543213','lakshmi@gmail.com','Mumbai','pat_lakshmi');
INSERT INTO Patients VALUES ('PT-0005','Suresh','Reddy',DATE '1982-07-30','Male','9876543214','suresh@gmail.com','Mumbai','pat_suresh');
INSERT INTO Patients VALUES ('PT-0006','Kavita','Singh',DATE '1988-11-25','Female','9876543215','kavita@gmail.com','Mumbai','pat_kavita');
INSERT INTO Patients VALUES ('PT-0007','Deepak','Gupta',DATE '1975-04-08','Male','9876543216','deepak@gmail.com','Mumbai','pat_deepak');
INSERT INTO Patients VALUES ('PT-0008','Pooja','Nair',DATE '1992-09-14','Female','9876543217','pooja@gmail.com','Mumbai','pat_pooja');

--------------------------------------------------
-- APPOINTMENTS
--------------------------------------------------
INSERT INTO Appointments VALUES ('APT-00001','PT-0001','DR-0001',DATE '2024-01-15','09:00','09:30','Completed');
INSERT INTO Appointments VALUES ('APT-00002','PT-0002','DR-0002',DATE '2024-01-15','10:00','10:30','Completed');
INSERT INTO Appointments VALUES ('APT-00003','PT-0003','DR-0003',DATE '2024-01-16','09:30','10:00','Completed');
INSERT INTO Appointments VALUES ('APT-00004','PT-0001','DR-0005',DATE '2024-01-18','11:00','11:30','Completed');
INSERT INTO Appointments VALUES ('APT-00005','PT-0004','DR-0004',DATE '2024-01-20','14:00','14:30','Completed');
INSERT INTO Appointments VALUES ('APT-00006','PT-0005','DR-0001',DATE '2024-02-05','09:00','09:30','Completed');
INSERT INTO Appointments VALUES ('APT-00007','PT-0006','DR-0007',DATE '2024-02-08','10:30','11:00','Completed');
INSERT INTO Appointments VALUES ('APT-00008','PT-0007','DR-0005',DATE '2024-02-10','09:00','09:30','Completed');
INSERT INTO Appointments VALUES ('APT-00009','PT-0001','DR-0001',DATE '2024-02-15','09:30','10:00','Completed');
INSERT INTO Appointments VALUES ('APT-00010','PT-0008','DR-0008',DATE '2024-02-18','11:00','11:30','Completed');

-- Scheduled (trigger will auto-create billing)
INSERT INTO Appointments VALUES ('APT-00011','PT-0002','DR-0002',DATE '2024-03-01','10:00','10:30','Scheduled');
INSERT INTO Appointments VALUES ('APT-00012','PT-0003','DR-0003',DATE '2024-03-02','11:00','11:30','Scheduled');

--------------------------------------------------
-- MEDICAL RECORDS
--------------------------------------------------
INSERT INTO Medical_Records VALUES ('MR-001','APT-00001','Hypertension','Medication prescribed');
INSERT INTO Medical_Records VALUES ('MR-002','APT-00002','Fever','Paracetamol given');
INSERT INTO Medical_Records VALUES ('MR-003','APT-00003','Knee pain','Pain relief treatment');
INSERT INTO Medical_Records VALUES ('MR-004','APT-00004','BP follow-up','Continue medication');
INSERT INTO Medical_Records VALUES ('MR-005','APT-00005','Skin acne','Topical treatment');

--------------------------------------------------
-- PRESCRIPTIONS
--------------------------------------------------
INSERT INTO Prescriptions VALUES ('RX-00001','APT-00001','Take medicines regularly');
INSERT INTO Prescriptions VALUES ('RX-00002','APT-00002','Complete full course');
INSERT INTO Prescriptions VALUES ('RX-00003','APT-00003','Avoid heavy activity');
INSERT INTO Prescriptions VALUES ('RX-00004','APT-00004','Monitor BP daily');

--------------------------------------------------
-- MEDICATIONS
--------------------------------------------------
INSERT INTO Medications VALUES ('MED-001','RX-00001','Amlodipine','5mg','Once daily','30 days');
INSERT INTO Medications VALUES ('MED-002','RX-00001','Aspirin','75mg','Once daily','30 days');
INSERT INTO Medications VALUES ('MED-003','RX-00002','Paracetamol','500mg','Twice daily','5 days');
INSERT INTO Medications VALUES ('MED-004','RX-00003','Diclofenac','50mg','Twice daily','7 days');
INSERT INTO Medications VALUES ('MED-005','RX-00004','Amlodipine','5mg','Once daily','30 days');

--------------------------------------------------
-- BILLING (Completed appointments)
--------------------------------------------------
INSERT INTO Billing VALUES ('BILL-0001','APT-00001',1500,'Cash','Paid');
INSERT INTO Billing VALUES ('BILL-0002','APT-00002',1000,'UPI','Paid');
INSERT INTO Billing VALUES ('BILL-0003','APT-00003',1800,'Cash','Paid');
INSERT INTO Billing VALUES ('BILL-0004','APT-00004',800,'Cash','Paid');
INSERT INTO Billing VALUES ('BILL-0005','APT-00005',1200,'UPI','Paid');

--------------------------------------------------
COMMIT;
EXIT;
