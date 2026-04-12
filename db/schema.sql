-- =========================================
-- CLINIC MANAGEMENT SYSTEM (STRING IDs)
-- =========================================

-- DROP ALL TABLES (for safe re-run)
BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE Billing CASCADE CONSTRAINTS';
    EXECUTE IMMEDIATE 'DROP TABLE Medications CASCADE CONSTRAINTS';
    EXECUTE IMMEDIATE 'DROP TABLE Prescriptions CASCADE CONSTRAINTS';
    EXECUTE IMMEDIATE 'DROP TABLE Medical_Records CASCADE CONSTRAINTS';
    EXECUTE IMMEDIATE 'DROP TABLE Appointments CASCADE CONSTRAINTS';
    EXECUTE IMMEDIATE 'DROP TABLE Patients CASCADE CONSTRAINTS';
    EXECUTE IMMEDIATE 'DROP TABLE Staff CASCADE CONSTRAINTS';
    EXECUTE IMMEDIATE 'DROP TABLE Departments CASCADE CONSTRAINTS';
    EXECUTE IMMEDIATE 'DROP TABLE Doctors CASCADE CONSTRAINTS';
EXCEPTION
    WHEN OTHERS THEN NULL;
END;
/
--------------------------------------------------

-- DEPARTMENTS
CREATE TABLE Departments (
    department_id VARCHAR2(10) PRIMARY KEY,
    name VARCHAR2(100) NOT NULL,
    head_doctor_id VARCHAR2(10)
);

-- DOCTORS
CREATE TABLE Doctors (
    doctor_id VARCHAR2(10) PRIMARY KEY,
    department_id VARCHAR2(10) NOT NULL,
    first_name VARCHAR2(50) NOT NULL,
    last_name VARCHAR2(50) NOT NULL,
    email VARCHAR2(100) UNIQUE,
    phone VARCHAR2(20),
    CONSTRAINT fk_doc_dept FOREIGN KEY (department_id)
    REFERENCES Departments(department_id)
);

-- ADD FK (CIRCULAR)
ALTER TABLE Departments
ADD CONSTRAINT fk_dept_head_doctor
FOREIGN KEY (head_doctor_id)
REFERENCES Doctors(doctor_id);

--------------------------------------------------

-- STAFF
CREATE TABLE Staff (
    staff_id VARCHAR2(10) PRIMARY KEY,
    department_id VARCHAR2(10) NOT NULL,
    first_name VARCHAR2(50) NOT NULL,
    last_name VARCHAR2(50) NOT NULL,
    role VARCHAR2(50) NOT NULL,
    CONSTRAINT fk_staff_dept FOREIGN KEY (department_id)
    REFERENCES Departments(department_id)
);

--------------------------------------------------

-- PATIENTS
CREATE TABLE Patients (
    patient_id VARCHAR2(10) PRIMARY KEY,
    first_name VARCHAR2(50) NOT NULL,
    last_name VARCHAR2(50) NOT NULL,
    dob DATE NOT NULL,
    gender VARCHAR2(10) CHECK (gender IN ('Male','Female','Other')),
    phone VARCHAR2(20) UNIQUE NOT NULL,
    email VARCHAR2(100),
    address VARCHAR2(255)
);

--------------------------------------------------

-- APPOINTMENTS
CREATE TABLE Appointments (
    appointment_id VARCHAR2(10) PRIMARY KEY,
    patient_id VARCHAR2(10) NOT NULL,
    doctor_id VARCHAR2(10) NOT NULL,
    appointment_date DATE NOT NULL,
    start_time VARCHAR2(5) NOT NULL,
    end_time VARCHAR2(5) NOT NULL,
    status VARCHAR2(20) DEFAULT 'Scheduled'
        CHECK (status IN ('Scheduled','Completed','Cancelled')),
    CONSTRAINT fk_app_patient FOREIGN KEY (patient_id)
        REFERENCES Patients(patient_id),
    CONSTRAINT fk_app_doctor FOREIGN KEY (doctor_id)
        REFERENCES Doctors(doctor_id)
);

--------------------------------------------------

-- MEDICAL RECORDS
CREATE TABLE Medical_Records (
    record_id VARCHAR2(10) PRIMARY KEY,
    appointment_id VARCHAR2(10) UNIQUE NOT NULL,
    symptoms VARCHAR2(500) NOT NULL,
    treatment VARCHAR2(500) NOT NULL,
    CONSTRAINT fk_medrec_app FOREIGN KEY (appointment_id)
        REFERENCES Appointments(appointment_id)
);

--------------------------------------------------

-- PRESCRIPTIONS
CREATE TABLE Prescriptions (
    prescription_id VARCHAR2(10) PRIMARY KEY,
    appointment_id VARCHAR2(10) UNIQUE NOT NULL,
    notes VARCHAR2(500),
    CONSTRAINT fk_presc_app FOREIGN KEY (appointment_id)
        REFERENCES Appointments(appointment_id)
);

--------------------------------------------------

-- MEDICATIONS
CREATE TABLE Medications (
    medication_id VARCHAR2(10) PRIMARY KEY,
    prescription_id VARCHAR2(10) NOT NULL,
    name VARCHAR2(100) NOT NULL,
    dosage VARCHAR2(50) NOT NULL,
    frequency VARCHAR2(50) NOT NULL,
    duration VARCHAR2(50) NOT NULL,
    CONSTRAINT fk_med_presc FOREIGN KEY (prescription_id)
        REFERENCES Prescriptions(prescription_id)
        ON DELETE CASCADE
);

--------------------------------------------------

-- BILLING
CREATE TABLE Billing (
    bill_id VARCHAR2(10) PRIMARY KEY,
    appointment_id VARCHAR2(10) NOT NULL,
    amount NUMBER(10,2) NOT NULL,
    payment_mode VARCHAR2(50),
    payment_status VARCHAR2(20) DEFAULT 'Pending'
        CHECK (payment_status IN ('Pending','Paid')),
    CONSTRAINT fk_bill_app FOREIGN KEY (appointment_id)
        REFERENCES Appointments(appointment_id)
);

--------------------------------------------------

-- TRIGGER 1: PREVENT DOUBLE BOOKING
CREATE OR REPLACE TRIGGER trg_prevent_double_booking
BEFORE INSERT OR UPDATE ON Appointments
FOR EACH ROW
DECLARE
    v_overlap_count NUMBER;
BEGIN
    SELECT COUNT(*)
    INTO v_overlap_count
    FROM Appointments
    WHERE doctor_id = :NEW.doctor_id
      AND appointment_date = :NEW.appointment_date
      AND status != 'Cancelled'
      AND appointment_id != :NEW.appointment_id
      AND (
          (TO_DATE(:NEW.start_time,'HH24:MI') >= TO_DATE(start_time,'HH24:MI')
           AND TO_DATE(:NEW.start_time,'HH24:MI') < TO_DATE(end_time,'HH24:MI'))
          OR
          (TO_DATE(:NEW.end_time,'HH24:MI') > TO_DATE(start_time,'HH24:MI')
           AND TO_DATE(:NEW.end_time,'HH24:MI') <= TO_DATE(end_time,'HH24:MI'))
          OR
          (TO_DATE(:NEW.start_time,'HH24:MI') <= TO_DATE(start_time,'HH24:MI')
           AND TO_DATE(:NEW.end_time,'HH24:MI') >= TO_DATE(end_time,'HH24:MI'))
      );

    IF v_overlap_count > 0 THEN
        RAISE_APPLICATION_ERROR(-20001,
        'Double booking error: Doctor is already occupied.');
    END IF;
END;
/

--------------------------------------------------

-- TRIGGER 2: AUTO BILL GENERATION
CREATE OR REPLACE TRIGGER trg_auto_generate_billing
AFTER INSERT ON Appointments
FOR EACH ROW
BEGIN
    IF :NEW.status = 'Scheduled' THEN
        INSERT INTO Billing (bill_id, appointment_id, amount, payment_status)
        VALUES (
            'BILL-' || SUBSTR(:NEW.appointment_id,5),
            :NEW.appointment_id,
            150.00,
            'Pending'
        );
    END IF;
END;
/

--------------------------------------------------

-- TRIGGER 3: AUTO PAYMENT STATUS
CREATE OR REPLACE TRIGGER trg_update_payment_status
BEFORE UPDATE ON Billing
FOR EACH ROW
BEGIN
    IF :NEW.payment_mode IS NOT NULL
       AND :NEW.payment_status = 'Pending' THEN
        :NEW.payment_status := 'Paid';
    END IF;
END;
/

--------------------------------------------------

COMMIT;
