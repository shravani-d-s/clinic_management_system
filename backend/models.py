from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import date

# Request Models (Data from Frontend)

class PatientCreate(BaseModel):
    first_name: str
    last_name: str
    dob: str # Send as YYYY-MM-DD
    gender: str
    phone: str
    email: Optional[EmailStr] = None
    address: Optional[str] = None

class AppointmentCreate(BaseModel):
    patient_id: int
    doctor_id: int
    appointment_date: str # YYYY-MM-DD
    start_time: str # HH24:MI
    end_time: str # HH24:MI

class MedicationCreate(BaseModel):
    name: str
    dosage: str
    frequency: str
    duration: str

class PrescriptionCreate(BaseModel):
    appointment_id: int
    notes: Optional[str] = None
    medications: List[MedicationCreate]

class PaymentUpdate(BaseModel):
    payment_mode: str
