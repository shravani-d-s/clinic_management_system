import React, { useEffect, useState } from 'react';
import { api } from '../api';
import { useAuth } from '../AuthContext';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';

export default function Dashboard() {
  const { user } = useAuth();
  const [data, setData] = useState(null);

  useEffect(() => {
    if (user.role === 'doctor') {
      api.get(`/billing/report?doctor_id=${user.id}`).then(setData).catch(console.error);
    }
  }, [user]);

  if (user.role === 'patient') {
    return (
      <div>
        <h1>Welcome, {user.name}!</h1>
        <p style={{ color: 'var(--text-muted)' }}>Use the sidebar to book your upcoming appointments, or check your active prescriptions.</p>
        <div style={{ marginTop: '2rem', padding: '2rem', background: 'var(--bg-card)', borderRadius: '12px' }}>
           <h3>Health Overview</h3>
           <p>Don't forget to stay hydrated, maintain a proper diet, and follow up closely with your consultation schedules!</p>
        </div>
      </div>
    );
  }

  if (!data) return <div>Loading dashboard...</div>;

  const totalPending = data.status_summary.find(s => s.payment_status === 'Pending')?.total_amount || 0;
  const totalPaid = data.status_summary.find(s => s.payment_status === 'Paid')?.total_amount || 0;

  return (
    <div>
      <h1>Doctor Dashboard</h1>
      
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '2rem', marginBottom: '3rem' }}>
        <div className="glass-card">
          <h3 style={{color: 'var(--text-muted)'}}>Your Revenue Generated</h3>
          <h2 style={{color: '#34d399', fontSize: '2.5rem'}}>${totalPaid}</h2>
        </div>
        <div className="glass-card">
          <h3 style={{color: 'var(--text-muted)'}}>Pending Amounts</h3>
          <h2 style={{color: '#fbbf24', fontSize: '2.5rem'}}>${totalPending}</h2>
        </div>
      </div>

      <div className="glass-card" style={{ marginBottom: '3rem', height: '400px' }}>
        <h3>Overall Appointments by Department</h3>
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data.department_summary}>
            <XAxis dataKey="department_name" stroke="var(--text-muted)" />
            <YAxis stroke="var(--text-muted)" />
            <Tooltip contentStyle={{ backgroundColor: 'var(--bg-dark)', borderColor: 'var(--border-color)' }} />
            <Bar dataKey="appointment_count" fill="var(--primary)" radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
