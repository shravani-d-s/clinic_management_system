import React, { useState, useEffect } from 'react';
import { api } from '../api';

export default function Appointments() {
  const [appointments, setAppointments] = useState([]);
  const [patients, setPatients] = useState([]);
  const [doctors, setDoctors] = useState([]);
  const [formData, setFormData] = useState({
    patient_id: '', doctor_id: '', appointment_date: '', start_time: '', end_time: ''
  });

  const fetchData = async () => {
    try {
      const appts = await api.get('/appointments');
      const pts = await api.get('/patients');
      const docs = await api.get('/doctors');
      setAppointments(appts);
      setPatients(pts);
      setDoctors(docs);
    } catch(err) { console.error(err); }
  };

  useEffect(() => { fetchData(); }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await api.post('/appointments', formData);
      alert('Appointment booked successfully!');
      fetchData();
    } catch (err) {
      alert(`Error booking appointment: ${err.message}`);
    }
  };

  return (
    <div>
      <h1>Appointments</h1>
      
      <div className="glass-card" style={{ marginBottom: '2rem' }}>
        <h3>Book Appointment</h3>
        <form onSubmit={handleSubmit} style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
          <div className="form-group">
            <label>Patient</label>
            <select className="form-control" required value={formData.patient_id} onChange={e => setFormData({...formData, patient_id: e.target.value})}>
              <option value="">Select Patient</option>
              {patients.map(p => <option key={p.patient_id} value={p.patient_id}>{p.first_name} {p.last_name}</option>)}
            </select>
          </div>
          <div className="form-group">
            <label>Doctor</label>
            <select className="form-control" required value={formData.doctor_id} onChange={e => setFormData({...formData, doctor_id: e.target.value})}>
              <option value="">Select Doctor</option>
              {doctors.map(d => <option key={d.doctor_id} value={d.doctor_id}>Dr. {d.first_name} {d.last_name} ({d.department_name})</option>)}
            </select>
          </div>
          <div className="form-group">
            <label>Date</label>
            <input type="date" className="form-control" required value={formData.appointment_date} onChange={e => setFormData({...formData, appointment_date: e.target.value})} />
          </div>
          <div className="form-group">
            <label>Start Time (HH:MM)</label>
            <input type="time" className="form-control" required value={formData.start_time} onChange={e => setFormData({...formData, start_time: e.target.value})} />
          </div>
          <div className="form-group">
            <label>End Time (HH:MM)</label>
            <input type="time" className="form-control" required value={formData.end_time} onChange={e => setFormData({...formData, end_time: e.target.value})} />
          </div>
          <div style={{ gridColumn: 'span 2' }}>
            <button type="submit" className="btn">Book Appointment</button>
          </div>
        </form>
      </div>

      <div className="glass-card table-container">
        <h3>Scheduled Appointments</h3>
        <table>
          <thead>
            <tr>
              <th>Date</th>
              <th>Time</th>
              <th>Patient</th>
              <th>Doctor</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {appointments.map(a => (
              <tr key={a.appointment_id}>
                <td>{a.appointment_date}</td>
                <td>{a.start_time} - {a.end_time}</td>
                <td>{a.patient_name}</td>
                <td>Dr. {a.doctor_name}</td>
                <td><span className={`badge ${a.status === 'Completed' ? 'paid' : (a.status === 'Scheduled' ? 'pending' : '')}`}>{a.status}</span></td>
              </tr>
            ))}
            {appointments.length === 0 && <tr><td colSpan="5">No appointments found.</td></tr>}
          </tbody>
        </table>
      </div>
    </div>
  );
}
