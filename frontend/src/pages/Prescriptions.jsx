import React, { useState, useEffect } from 'react';
import { api } from '../api';
import { useAuth } from '../AuthContext';

export default function Prescriptions() {
  const { user } = useAuth();
  const [appointments, setAppointments] = useState([]);
  const [patientPresc, setPatientPresc] = useState([]);
  const [formData, setFormData] = useState({
    appointment_id: '',
    symptoms: '',
    treatment: '',
    notes: '',
    medications: []
  });

  const fetchData = async () => {
    try {
      if (user.role === 'doctor') {
        const appts = await api.get(`/appointments?doctor_id=${user.id}`);
        setAppointments(appts.filter(a => a.status === 'Scheduled'));
      } else if (user.role === 'patient') {
        const prescs = await api.get(`/patients/${user.id}/consultations`);
        setPatientPresc(prescs);
      }
    } catch(err) { console.error(err); }
  };

  useEffect(() => { fetchData(); }, [user]);

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
      await api.post('/consultations', formData);
      alert('Consultation recorded securely!');
      setFormData({
        appointment_id: '', symptoms: '', treatment: '', notes: '',
        medications: []
      });
      fetchData();
    } catch (err) {
      alert(`Error: ${err.message}`);
    }
  };

  if (user.role === 'patient') {
    return (
      <div>
        <h1>My Consultations & Medical Records</h1>
        {patientPresc.length === 0 && <p>No records found.</p>}
        {patientPresc.map((p, idx) => (
          <div key={p.record_id || idx} className="glass-card" style={{ marginBottom: '1.5rem' }}>
            <h3>Date: {p.appointment_date}</h3>
            <p><strong>Doctor:</strong> Dr. {p.doctor_name}</p>
            
            <div style={{ padding: '15px', background: 'var(--bg-dark)', borderRadius: '8px', margin: '15px 0' }}>
              <p><strong>Symptoms:</strong> {p.symptoms}</p>
              <p><strong>Treatment:</strong> {p.treatment}</p>
            </div>
            
            {p.notes && <p><strong>Prescription Notes:</strong> {p.notes}</p>}
            {p.medications && p.medications.length > 0 && (
              <table style={{ marginTop: '1rem' }}>
                 <thead><tr><th>Name</th><th>Dosage</th><th>Frequency</th><th>Duration</th></tr></thead>
                 <tbody>
                    {p.medications.map((m, i) => (
                      <tr key={i}>
                        <td>{m.name}</td><td>{m.dosage}</td><td>{m.frequency}</td><td>{m.duration}</td>
                      </tr>
                    ))}
                 </tbody>
              </table>
            )}
          </div>
        ))}
      </div>
    );
  }

  return (
    <div>
      <h1>Provide Consultation & Medical Record</h1>
      <div className="glass-card">
        <h3>Record Details</h3>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Select Appointment (Scheduled)</label>
            <select className="form-control" required value={formData.appointment_id} onChange={e => setFormData({...formData, appointment_id: e.target.value})}>
              <option value="">Select Appointment</option>
              {appointments.map(a => (
                <option key={a.appointment_id} value={a.appointment_id}>
                  {a.appointment_date} - {a.patient_name}
                </option>
              ))}
            </select>
          </div>
          
          <div className="form-group">
            <label>Observed Symptoms (Mandatory)</label>
            <textarea className="form-control" rows="2" required value={formData.symptoms} onChange={e => setFormData({...formData, symptoms: e.target.value})}></textarea>
          </div>
          
          <div className="form-group">
            <label>Provided Treatment (Mandatory)</label>
            <textarea className="form-control" rows="2" required value={formData.treatment} onChange={e => setFormData({...formData, treatment: e.target.value})}></textarea>
          </div>

          <div className="form-group">
            <label>Prescription Notes (Optional)</label>
            <textarea className="form-control" rows="2" value={formData.notes} onChange={e => setFormData({...formData, notes: e.target.value})}></textarea>
          </div>

          <h4>Medications (Optional)</h4>
          {formData.medications.map((med, index) => (
            <div key={index} style={{ display: 'grid', gridTemplateColumns: '2fr 1fr 1fr 1fr', gap: '0.5rem', marginBottom: '1rem' }}>
              <input className="form-control" placeholder="Medication Name" required value={med.name} onChange={e => handleMedChange(index, 'name', e.target.value)} />
              <input className="form-control" placeholder="Dosage" required value={med.dosage} onChange={e => handleMedChange(index, 'dosage', e.target.value)} />
              <input className="form-control" placeholder="Frequency" required value={med.frequency} onChange={e => handleMedChange(index, 'frequency', e.target.value)} />
              <input className="form-control" placeholder="Duration" required value={med.duration} onChange={e => handleMedChange(index, 'duration', e.target.value)} />
            </div>
          ))}
          
          <button type="button" className="btn" style={{ background: 'var(--bg-card)', border: '1px solid var(--primary)', color: 'var(--primary)', marginBottom: '1.5rem' }} onClick={addMedication}>
            + Add Medication
          </button>

          <div style={{ marginTop: '1rem', borderTop: '1px solid var(--border-color)', paddingTop: '1rem' }}>
             <button type="submit" className="btn">Save Medical Record & Complete Appointment</button>
          </div>
        </form>
      </div>
    </div>
  );
}
