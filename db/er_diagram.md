# Clinic Management System — ER Diagram

## Entity-Relationship Diagram

```mermaid
erDiagram
    DEPARTMENTS ||--o{ DOCTORS : "has"
    DEPARTMENTS ||--o{ STAFF : "employs"
    DEPARTMENTS ||--o| DOCTORS : "headed by"

    DOCTORS ||--o{ APPOINTMENTS : "attends"
    PATIENTS ||--o{ APPOINTMENTS : "books"

    APPOINTMENTS ||--o| MEDICAL_RECORDS : "produces"
    APPOINTMENTS ||--o| PRESCRIPTIONS : "may produce"
    APPOINTMENTS ||--|| BILLING : "generates"

    PRESCRIPTIONS ||--o{ MEDICATIONS : "contains"

    DEPARTMENTS {
        VARCHAR2 department_id PK
        VARCHAR2 name
        VARCHAR2 head_doctor_id FK
    }

    DOCTORS {
        VARCHAR2 doctor_id PK
        VARCHAR2 department_id FK
        VARCHAR2 first_name
        VARCHAR2 last_name
        VARCHAR2 email UK
        VARCHAR2 phone
        VARCHAR2 password
    }

    STAFF {
        VARCHAR2 staff_id PK
        VARCHAR2 department_id FK
        VARCHAR2 first_name
        VARCHAR2 last_name
        VARCHAR2 role
    }

    PATIENTS {
        VARCHAR2 patient_id PK
        VARCHAR2 first_name
        VARCHAR2 last_name
        DATE dob
        VARCHAR2 gender
        VARCHAR2 phone UK
        VARCHAR2 email
        VARCHAR2 address
        VARCHAR2 password
    }

    APPOINTMENTS {
        VARCHAR2 appointment_id PK
        VARCHAR2 patient_id FK
        VARCHAR2 doctor_id FK
        DATE appointment_date
        VARCHAR2 start_time
        VARCHAR2 end_time
        VARCHAR2 status
    }

    MEDICAL_RECORDS {
        VARCHAR2 record_id PK
        VARCHAR2 appointment_id FK_UK
        VARCHAR2 symptoms
        VARCHAR2 treatment
    }

    PRESCRIPTIONS {
        VARCHAR2 prescription_id PK
        VARCHAR2 appointment_id FK_UK
        VARCHAR2 notes
    }

    MEDICATIONS {
        VARCHAR2 medication_id PK
        VARCHAR2 prescription_id FK
        VARCHAR2 name
        VARCHAR2 dosage
        VARCHAR2 frequency
        VARCHAR2 duration
    }

    BILLING {
        VARCHAR2 bill_id PK
        VARCHAR2 appointment_id FK
        NUMBER amount
        VARCHAR2 payment_mode
        VARCHAR2 payment_status
    }
```

---

## Cardinality Summary

| Relationship | Type | Description |
|-------------|------|-------------|
| Departments → Doctors | 1:N | One department has many doctors |
| Departments → Staff | 1:N | One department employs many staff members |
| Departments → Head Doctor | 1:1 (optional) | Each department has at most one head doctor (circular FK) |
| Patients → Appointments | 1:N | One patient books many appointments |
| Doctors → Appointments | 1:N | One doctor attends many appointments |
| Appointments → Medical_Records | 1:1 (optional) | Each appointment has at most one medical record |
| Appointments → Prescriptions | 1:1 (optional) | Each appointment may optionally produce one prescription |
| Appointments → Billing | 1:1 | Each appointment generates exactly one bill (via trigger) |
| Prescriptions → Medications | 1:N | One prescription may contain many medications |

---

## Entity Descriptions

### Strong Entities
- **Departments** — Hospital units (e.g., Cardiology, Pediatrics)
- **Doctors** — Medical practitioners assigned to departments
- **Patients** — Individuals who register and book appointments
- **Staff** — Non-clinical personnel assigned to departments

### Weak / Dependent Entities
- **Appointments** — Scheduled/completed meeting between a patient and a doctor (depends on both)
- **Medical_Records** — Symptoms and treatment recorded per completed appointment (depends on Appointments)
- **Prescriptions** — Optional prescription notes per appointment (depends on Appointments)
- **Medications** — Individual prescribed medicines (depends on Prescriptions)
- **Billing** — Auto-generated bill per appointment (depends on Appointments)

---

## Participation Constraints

| Entity | Participation | Detail |
|--------|--------------|--------|
| Doctors in Departments | **Total** | Every doctor must belong to a department |
| Staff in Departments | **Total** | Every staff must belong to a department |
| Head Doctor in Departments | **Partial** | Not every department must have a head doctor |
| Patient in Appointments | **Partial** | A patient may or may not have appointments |
| Doctor in Appointments | **Partial** | A doctor may or may not have appointments |
| Appointment in Medical_Records | **Partial** | Only completed appointments have records |
| Appointment in Prescriptions | **Partial** | Not every appointment produces a prescription |
| Appointment in Billing | **Total** | Every scheduled appointment auto-generates a bill |
| Prescription in Medications | **Partial** | A prescription may have zero or more medications |
