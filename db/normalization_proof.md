# Clinic Management System — Normalization Proof

## Overview

This document proves that each relation in the Clinic Management System satisfies **Third Normal Form (3NF)** and discusses **Boyce-Codd Normal Form (BCNF)** compliance.

### Normal Form Definitions (Quick Reference)

| NF | Requirement |
|----|-------------|
| **1NF** | All attributes are atomic (no repeating groups, no multi-valued attributes) |
| **2NF** | 1NF + No partial dependencies (every non-key attribute depends on the *full* PK) |
| **3NF** | 2NF + No transitive dependencies (non-key attributes don't depend on other non-key attributes) |
| **BCNF** | For every functional dependency X → Y, X is a superkey |

---

## Per-Table Analysis

### 1. Departments

**Schema:** `Departments(department_id, name, head_doctor_id)`

**Functional Dependencies:**
- `department_id → name, head_doctor_id`

| NF | Satisfied? | Justification |
|----|-----------|---------------|
| 1NF | Yes | All attributes are atomic, single-valued |
| 2NF | Yes | PK is a single attribute (`department_id`), so no partial dependency is possible |
| 3NF | Yes | No transitive deps — `name` and `head_doctor_id` depend only on PK |
| BCNF | Yes | Only determinant is the PK (`department_id`) |

---

### 2. Doctors

**Schema:** `Doctors(doctor_id, department_id, first_name, last_name, email, phone, password)`

**Functional Dependencies:**
- `doctor_id → department_id, first_name, last_name, email, phone, password`
- `email → doctor_id` (email is UNIQUE — candidate key)

| NF | Satisfied? | Justification |
|----|-----------|---------------|
| 1NF | Yes | All attributes are atomic |
| 2NF | Yes | Single-attribute PK; no partial dependency |
| 3NF | Yes | No non-key attribute depends on another non-key attribute |
| BCNF | Yes | Both determinants (`doctor_id`, `email`) are superkeys |

> **Note:** `department_id` is an FK to Departments, not a transitive dependency. The department's name is not stored in Doctors — it is referenced via the FK join.

---

### 3. Staff

**Schema:** `Staff(staff_id, department_id, first_name, last_name, role)`

**Functional Dependencies:**
- `staff_id → department_id, first_name, last_name, role`

| NF | Satisfied? | Justification |
|----|-----------|---------------|
| 1NF | Yes | All attributes are atomic |
| 2NF | Yes | Single-attribute PK |
| 3NF | Yes | No transitive dependencies |
| BCNF | Yes | Only determinant is PK |

---

### 4. Patients

**Schema:** `Patients(patient_id, first_name, last_name, dob, gender, phone, email, address, password)`

**Functional Dependencies:**
- `patient_id → first_name, last_name, dob, gender, phone, email, address, password`
- `phone → patient_id` (phone is UNIQUE — candidate key)

| NF | Satisfied? | Justification |
|----|-----------|---------------|
| 1NF | Yes | All attributes are atomic, single-valued |
| 2NF | Yes | Single-attribute PK |
| 3NF | Yes | No non-key attribute depends transitively on the PK |
| BCNF | Yes | Both determinants (`patient_id`, `phone`) are superkeys |

---

### 5. Appointments

**Schema:** `Appointments(appointment_id, patient_id, doctor_id, appointment_date, start_time, end_time, status)`

**Functional Dependencies:**
- `appointment_id → patient_id, doctor_id, appointment_date, start_time, end_time, status`

| NF | Satisfied? | Justification |
|----|-----------|---------------|
| 1NF | Yes | All attributes are atomic |
| 2NF | Yes | Single-attribute PK |
| 3NF | Yes | No transitive deps — `patient_id` and `doctor_id` are FKs, not causing transitivity |
| BCNF | Yes | Only determinant is PK |

> **Discussion:** One might argue that `{doctor_id, appointment_date, start_time}` could also uniquely identify a row (due to the trigger preventing overlaps). However, this is enforced at the application/trigger level, not as a schema-level UNIQUE constraint, so it does not create a BCNF violation.

---

### 6. Medical_Records

**Schema:** `Medical_Records(record_id, appointment_id, symptoms, treatment)`

**Functional Dependencies:**
- `record_id → appointment_id, symptoms, treatment`
- `appointment_id → record_id, symptoms, treatment` (appointment_id is UNIQUE — candidate key)

| NF | Satisfied? | Justification |
|----|-----------|---------------|
| 1NF | Yes | All attributes are atomic |
| 2NF | Yes | Single-attribute PK |
| 3NF | Yes | No transitive dependencies |
| BCNF | Yes | Both determinants (`record_id`, `appointment_id`) are superkeys |

---

### 7. Prescriptions

**Schema:** `Prescriptions(prescription_id, appointment_id, notes)`

**Functional Dependencies:**
- `prescription_id → appointment_id, notes`
- `appointment_id → prescription_id, notes` (appointment_id is UNIQUE — candidate key)

| NF | Satisfied? | Justification |
|----|-----------|---------------|
| 1NF | Yes | All attributes are atomic |
| 2NF | Yes | Single-attribute PK |
| 3NF | Yes | No transitive dependencies |
| BCNF | Yes | Both determinants are superkeys |

---

### 8. Medications

**Schema:** `Medications(medication_id, prescription_id, name, dosage, frequency, duration)`

**Functional Dependencies:**
- `medication_id → prescription_id, name, dosage, frequency, duration`

| NF | Satisfied? | Justification |
|----|-----------|---------------|
| 1NF | Yes | All attributes are atomic. Medications are stored in a separate table rather than as a multi-valued attribute in Prescriptions — this is the key 1NF decomposition |
| 2NF | Yes | Single-attribute PK |
| 3NF | Yes | No transitive dependencies |
| BCNF | Yes | Only determinant is PK |

> **1NF Justification:** If medications were stored as a comma-separated string inside Prescriptions (e.g., `"Aspirin 5mg daily, Paracetamol 500mg twice"`), it would violate 1NF. By decomposing into a separate Medications table with atomic attributes (`name`, `dosage`, `frequency`, `duration`), we achieve 1NF.

---

### 9. Billing

**Schema:** `Billing(bill_id, appointment_id, amount, payment_mode, payment_status)`

**Functional Dependencies:**
- `bill_id → appointment_id, amount, payment_mode, payment_status`

| NF | Satisfied? | Justification |
|----|-----------|---------------|
| 1NF | Yes | All attributes are atomic |
| 2NF | Yes | Single-attribute PK |
| 3NF | Yes | `payment_status` might seem dependent on `payment_mode` (if mode is set, status = Paid). However, `payment_status` is set independently via trigger logic, and both are stored as independent attributes of the billing record. There is no structural FD `payment_mode → payment_status` since `payment_mode` can be NULL while `payment_status` is 'Pending'. |
| BCNF | Yes | Only determinant is PK |

> **BCNF Discussion:** The trigger `trg_update_payment_status` automatically sets `payment_status = 'Paid'` when `payment_mode` is provided, but this is *procedural logic*, not a structural FD. The attributes remain independently meaningful (a bill can be Pending with no payment_mode, or Paid with a specific mode).

---

> **Conclusion:** All 9 relations in the Clinic Management System satisfy **BCNF** (and therefore also 3NF). No decomposition is needed. The schema avoids redundancy and anomalies by:
> - Decomposing multi-valued data (medications) into separate relations
> - Using foreign keys instead of duplicating data across tables
> - Ensuring every non-trivial functional dependency has a superkey as its determinant
