erDiagram

    DEPARTMENTS ||--o{ DOCTORS : has
    DEPARTMENTS ||--o{ STAFF : employs

    DOCTORS ||--o{ APPOINTMENTS : attends
    PATIENTS ||--o{ APPOINTMENTS : books

    APPOINTMENTS ||--|| MEDICAL_RECORDS : produces
    APPOINTMENTS ||--o{ PRESCRIPTIONS : generates
    APPOINTMENTS ||--|| BILLING : generates

    PRESCRIPTIONS ||--o{ MEDICATIONS : contains

    STAFF ||--o{ APPOINTMENTS : manages
    STAFF ||--o{ BILLING : processes

    PATIENTS {
        STRING patient_id
        STRING name
        STRING gender
        STRING phone
    }

    DOCTORS {
        STRING doctor_id
        STRING name
        STRING specialization
    }

    DEPARTMENTS {
        STRING department_id
        STRING name
    }

    STAFF {
        STRING staff_id
        STRING name
        STRING role
    }

    APPOINTMENTS {
        STRING appointment_id
        STRING date
        STRING time
        STRING status
    }

    MEDICAL_RECORDS {
        STRING record_id
        STRING diagnosis
        STRING symptoms
        STRING treatment
    }

    PRESCRIPTIONS {
        STRING prescription_id
    }

    MEDICATIONS {
        STRING medication_id
        STRING medicine_name
    }

    BILLING {
        STRING bill_id
        STRING amount
        STRING payment_status
    }
