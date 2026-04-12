import React, { useState, useEffect } from 'react';
import { api } from '../api';

export default function Patients() {
  const [patients, setPatients] = useState([]);
  const [formData, setFormData] = useState({
    first_name: '', last_name: '', dob: '', gender: 'Male', phone: '', email: '', address: ''
  });

  const fetchPatients = () => {
    api.get('/patients').then(setPatients).catch(console.error);
  };

  useEffect(() => { fetchPatients(); }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await api.post('/patients', formData);
      alert('Patient registered successfully');
      setFormData({first_name: '', last_name: '', dob: '', gender: 'Male', phone: '', email: '', address: ''});
      fetchPatients();
    } catch (err) {
      alert(`Error: ${err.message}`);
    }
  };

  return (
    <div>
      <h1>Patient Management</h1>
      <div className="glass-card" style={{ marginBottom: '2rem' }}>
        <h3>Register New Patient</h3>
        <form onSubmit={handleSubmit} style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
          <div className="form-group">
            <label>First Name</label>
            <input className="form-control" required value={formData.first_name} onChange={e => setFormData({...formData, first_name: e.target.value})} />
          </div>
          <div className="form-group">
            <label>Last Name</label>
            <input className="form-control" required value={formData.last_name} onChange={e => setFormData({...formData, last_name: e.target.value})} />
          </div>
          <div className="form-group">
            <label>Date of Birth</label>
            <input type="date" className="form-control" required value={formData.dob} onChange={e => setFormData({...formData, dob: e.target.value})} />
          </div>
          <div className="form-group">
            <label>Gender</label>
            <select className="form-control" value={formData.gender} onChange={e => setFormData({...formData, gender: e.target.value})}>
              <option>Male</option>
              <option>Female</option>
              <option>Other</option>
            </select>
          </div>
          <div className="form-group">
            <label>Phone</label>
            <input className="form-control" required value={formData.phone} onChange={e => setFormData({...formData, phone: e.target.value})} />
          </div>
          <div className="form-group">
            <label>Email</label>
            <input type="email" className="form-control" value={formData.email} onChange={e => setFormData({...formData, email: e.target.value})} />
          </div>
          <div className="form-group" style={{ gridColumn: 'span 2' }}>
            <label>Address</label>
            <input className="form-control" value={formData.address} onChange={e => setFormData({...formData, address: e.target.value})} />
          </div>
          <div style={{ gridColumn: 'span 2' }}>
            <button type="submit" className="btn">Register Patient</button>
          </div>
        </form>
      </div>
    </div>
  );
}
