# Clinic Management System — Relational Schema

## Relational Schema Notation

Each relation is shown with its attributes. Keys are annotated as follows:
- **PK** = Primary Key
- **FK** = Foreign Key
- **UK** = Unique Key
- **NN** = NOT NULL
- **CK** = CHECK constraint

---

## Relations

### 1. Departments

```
Departments (
    department_id   VARCHAR2(10)    PK,
    name            VARCHAR2(100)   NN,
    head_doctor_id  VARCHAR2(10)    FK → Doctors(doctor_id)
)
```

### 2. Doctors

```
Doctors (
    doctor_id       VARCHAR2(10)    PK,
    department_id   VARCHAR2(10)    FK → Departments(department_id), NN,
    first_name      VARCHAR2(50)    NN,
    last_name       VARCHAR2(50)    NN,
    email           VARCHAR2(100)   UK,
    phone           VARCHAR2(20),
    password        VARCHAR2(100)   NN, DEFAULT 'doc123'
)
```

### 3. Staff

```
Staff (
    staff_id        VARCHAR2(10)    PK,
    department_id   VARCHAR2(10)    FK → Departments(department_id), NN,
    first_name      VARCHAR2(50)    NN,
    last_name       VARCHAR2(50)    NN,
    role            VARCHAR2(50)    NN
)
```

### 4. Patients

```
Patients (
    patient_id      VARCHAR2(10)    PK,
    first_name      VARCHAR2(50)    NN,
    last_name       VARCHAR2(50)    NN,
    dob             DATE            NN,
    gender          VARCHAR2(10)    CK: IN ('Male', 'Female', 'Other'),
    phone           VARCHAR2(20)    UK, NN,
    email           VARCHAR2(100),
    address         VARCHAR2(255),
    password        VARCHAR2(100)   NN, DEFAULT 'pat123'
)
```

### 5. Appointments

```
Appointments (
    appointment_id  VARCHAR2(10)    PK,
    patient_id      VARCHAR2(10)    FK → Patients(patient_id), NN,
    doctor_id       VARCHAR2(10)    FK → Doctors(doctor_id), NN,
    appointment_date DATE           NN,
    start_time      VARCHAR2(5)     NN,
    end_time        VARCHAR2(5)     NN,
    status          VARCHAR2(20)    CK: IN ('Scheduled', 'Completed', 'Cancelled'),
                                    DEFAULT 'Scheduled'
)
```

### 6. Medical_Records

```
Medical_Records (
    record_id       VARCHAR2(10)    PK,
    appointment_id  VARCHAR2(10)    FK → Appointments(appointment_id), UK, NN,
    symptoms        VARCHAR2(500)   NN,
    treatment       VARCHAR2(500)   NN
)
```

### 7. Prescriptions

```
Prescriptions (
    prescription_id VARCHAR2(10)    PK,
    appointment_id  VARCHAR2(10)    FK → Appointments(appointment_id), UK, NN,
    notes           VARCHAR2(500)
)
```

### 8. Medications

```
Medications (
    medication_id   VARCHAR2(10)    PK,
    prescription_id VARCHAR2(10)    FK → Prescriptions(prescription_id) ON DELETE CASCADE, NN,
    name            VARCHAR2(100)   NN,
    dosage          VARCHAR2(50)    NN,
    frequency       VARCHAR2(50)    NN,
    duration        VARCHAR2(50)    NN
)
```

### 9. Billing

```
Billing (
    bill_id         VARCHAR2(10)    PK,
    appointment_id  VARCHAR2(10)    FK → Appointments(appointment_id), NN,
    amount          NUMBER(10,2)    NN,
    payment_mode    VARCHAR2(50),
    payment_status  VARCHAR2(20)    CK: IN ('Pending', 'Paid'),
                                    DEFAULT 'Pending'
)
```

---

## Foreign Key Reference Diagram

```
Departments.head_doctor_id  ──→  Doctors.doctor_id         (circular)
Doctors.department_id       ──→  Departments.department_id
Staff.department_id         ──→  Departments.department_id
Appointments.patient_id     ──→  Patients.patient_id
Appointments.doctor_id      ──→  Doctors.doctor_id
Medical_Records.appointment_id ──→  Appointments.appointment_id
Prescriptions.appointment_id   ──→  Appointments.appointment_id
Medications.prescription_id    ──→  Prescriptions.prescription_id  (CASCADE)
Billing.appointment_id         ──→  Appointments.appointment_id
```

---

## Constraint Summary

| Table | PK | FK | UK | NN | CK | DEFAULT |
|-------|----|----|----|----|----|----|
| Departments | 1 | 1 | — | 1 | — | — |
| Doctors | 1 | 1 | 1 (email) | 3 | — | 1 (password) |
| Staff | 1 | 1 | — | 4 | — | — |
| Patients | 1 | — | 1 (phone) | 4 | 1 (gender) | 1 (password) |
| Appointments | 1 | 2 | — | 4 | 1 (status) | 1 (status) |
| Medical_Records | 1 | 1 | 1 (appt_id) | 2 | — | — |
| Prescriptions | 1 | 1 | 1 (appt_id) | — | — | — |
| Medications | 1 | 1 | — | 4 | — | — |
| Billing | 1 | 1 | — | 1 | 1 (payment_status) | 1 (payment_status) |
| **Total** | **9** | **10** | **4** | **23** | **3** | **4** |
