import React, { useState, useEffect } from 'react';
import { api } from '../api';
import { useAuth } from '../AuthContext';

export default function Appointments() {
  const { user } = useAuth();
  const [appointments, setAppointments] = useState([]);
  const [doctors, setDoctors] = useState([]);
  const [formData, setFormData] = useState({
    doctor_id: '', appointment_date: '', start_time: '', end_time: ''
  });

  const fetchData = async () => {
    try {
      let url = '/appointments';
      if (user.role === 'patient') url += `?patient_id=${user.id}`;
      else if (user.role === 'doctor') url += `?doctor_id=${user.id}`;
      
      const appts = await api.get(url);
      setAppointments(appts);
      
      if (user.role === 'patient') {
        const docs = await api.get('/doctors');
        setDoctors(docs);
      }
    } catch(err) { console.error(err); }
  };

  useEffect(() => { fetchData(); }, [user]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await api.post('/appointments', {
        ...formData,
        patient_id: user.id
      });
      alert('Appointment booked successfully!');
      fetchData();
    } catch (err) {
      alert(`Error booking appointment: ${err.message}`);
    }
  };

  const handleCancel = async (id) => {
    if (!window.confirm("Are you sure you want to cancel and delete this appointment?")) return;
    try {
      await api.delete(`/appointments/${id}`);
      fetchData();
    } catch (err) {
      alert(`Error cancelling: ${err.message}`);
    }
  };

  return (
    <div>
      <h1>{user.role === 'patient' ? "My Appointments" : "Scheduled Appointments"}</h1>
      
      {user.role === 'patient' && (
        <div className="glass-card" style={{ marginBottom: '2rem' }}>
          <h3>Book Appointment</h3>
          <form onSubmit={handleSubmit} style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
            <div className="form-group">
              <label>Select Doctor</label>
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
      )}

      <div className="glass-card table-container">
        <h3>Appointments List</h3>
        <table>
          <thead>
            <tr>
              <th>Date</th>
              <th>Time</th>
              {user.role === 'doctor' && <th>Patient</th>}
              {user.role === 'patient' && <th>Doctor</th>}
              <th>Status</th>
              {user.role === 'patient' && <th>Actions</th>}
            </tr>
          </thead>
          <tbody>
            {appointments.map(a => (
              <tr key={a.appointment_id}>
                <td>{a.appointment_date}</td>
                <td>{a.start_time} - {a.end_time}</td>
                {user.role === 'doctor' && <td>{a.patient_name}</td>}
                {user.role === 'patient' && <td>Dr. {a.doctor_name}</td>}
                <td>
                  <span className={`badge ${a.status === 'Completed' ? 'paid' : (a.status === 'Scheduled' ? 'pending' : '')}`}>
                    {a.status}
                  </span>
                </td>
                {user.role === 'patient' && (
                  <td>
                    {a.status === 'Scheduled' && (
                       <button onClick={() => handleCancel(a.appointment_id)} style={{background: '#e74c3c', color: '#fff', border: 'none', padding: '5px 10px', borderRadius: '4px', cursor: 'pointer'}}>
                         Cancel
                       </button>
                    )}
                  </td>
                )}
              </tr>
            ))}
            {appointments.length === 0 && <tr><td colSpan="5">No appointments found.</td></tr>}
          </tbody>
        </table>
      </div>
    </div>
  );
}
