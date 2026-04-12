import React, { useEffect, useState } from 'react';
import { api } from '../api';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';

export default function Dashboard() {
  const [data, setData] = useState(null);

  useEffect(() => {
    api.get('/billing/report').then(setData).catch(console.error);
  }, []);

  if (!data) return <div>Loading dashboard...</div>;

  const totalPending = data.status_summary.find(s => s.payment_status === 'Pending')?.total_amount || 0;
  const totalPaid = data.status_summary.find(s => s.payment_status === 'Paid')?.total_amount || 0;

  return (
    <div>
      <h1>Clinic Dashboard</h1>
      
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '2rem', marginBottom: '3rem' }}>
        <div className="glass-card">
          <h3 style={{color: 'var(--text-muted)'}}>Revenue (Paid)</h3>
          <h2 style={{color: '#34d399', fontSize: '2.5rem'}}>${totalPaid}</h2>
        </div>
        <div className="glass-card">
          <h3 style={{color: 'var(--text-muted)'}}>Pending Bills</h3>
          <h2 style={{color: '#fbbf24', fontSize: '2.5rem'}}>${totalPending}</h2>
        </div>
      </div>

      <div className="glass-card" style={{ marginBottom: '3rem', height: '400px' }}>
        <h3>Appointments by Department</h3>
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
