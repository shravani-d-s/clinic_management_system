import React, { useState, useEffect } from 'react';
import { api } from '../api';

export default function Prescriptions() {
  const [appointments, setAppointments] = useState([]);
  const [formData, setFormData] = useState({
    appointment_id: '',
    notes: '',
    medications: [{ name: '', dosage: '', frequency: '', duration: '' }]
  });

  const fetchData = async () => {
    try {
      const appts = await api.get('/appointments');
      // Only show scheduled appointments allowing prescription to be added
      setAppointments(appts.filter(a => a.status === 'Scheduled'));
    } catch(err) { console.error(err); }
  };

  useEffect(() => { fetchData(); }, []);

  const handleMedChange = (index, field, value) => {
    const newMeds = [...formData.medications];
    newMeds[index][field] = value;
    setFormData({ ...formData, medications: newMeds });
  };

  const addMedication = () => {
    setFormData({
      ...formData,
      medications: [...formData.medications, { name: '', dosage: '', frequency: '', duration: '' }]
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if(!formData.appointment_id) throw new Error("Please select an appointment");
      await api.post('/prescriptions', formData);
      alert('Prescription saved and Appointment marked as Completed!');
      setFormData({
        appointment_id: '', notes: '',
        medications: [{ name: '', dosage: '', frequency: '', duration: '' }]
      });
      fetchData();
    } catch (err) {
      alert(`Error: ${err.message}`);
    }
  };

  return (
    <div>
      <h1>Consultation & Prescriptions</h1>
      <div className="glass-card">
        <h3>Create Prescription</h3>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Select Appointment (Scheduled)</label>
            <select className="form-control" required value={formData.appointment_id} onChange={e => setFormData({...formData, appointment_id: parseInt(e.target.value)})}>
              <option value="">Select Appointment</option>
              {appointments.map(a => (
                <option key={a.appointment_id} value={a.appointment_id}>
                  {a.appointment_date} - {a.patient_name} (Dr. {a.doctor_name})
                </option>
              ))}
            </select>
          </div>
          
          <div className="form-group">
            <label>Consultation Notes</label>
            <textarea className="form-control" rows="3" value={formData.notes} onChange={e => setFormData({...formData, notes: e.target.value})}></textarea>
          </div>

          <h4>Medications</h4>
          {formData.medications.map((med, index) => (
            <div key={index} style={{ display: 'grid', gridTemplateColumns: '2fr 1fr 1fr 1fr', gap: '0.5rem', marginBottom: '1rem' }}>
              <input className="form-control" placeholder="Medication Name" required value={med.name} onChange={e => handleMedChange(index, 'name', e.target.value)} />
              <input className="form-control" placeholder="Dosage" required value={med.dosage} onChange={e => handleMedChange(index, 'dosage', e.target.value)} />
              <input className="form-control" placeholder="Frequency" required value={med.frequency} onChange={e => handleMedChange(index, 'frequency', e.target.value)} />
              <input className="form-control" placeholder="Duration (e.g. 5 days)" required value={med.duration} onChange={e => handleMedChange(index, 'duration', e.target.value)} />
            </div>
          ))}
          
          <button type="button" className="btn" style={{ background: 'var(--bg-card)', border: '1px solid var(--primary)', color: 'var(--primary)', marginBottom: '1.5rem' }} onClick={addMedication}>
            + Add Another Medication
          </button>

          <div style={{ marginTop: '1rem', borderTop: '1px solid var(--border-color)', paddingTop: '1rem' }}>
             <button type="submit" className="btn">Save Prescription & Complete Appointment</button>
          </div>
        </form>
      </div>
    </div>
  );
}
