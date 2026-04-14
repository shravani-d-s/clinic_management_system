import React from 'react';
import { BrowserRouter as Router, Routes, Route, NavLink, Navigate } from 'react-router-dom';
import { useAuth } from './AuthContext';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import Appointments from './pages/Appointments';
import Prescriptions from './pages/Prescriptions';
import Patients from './pages/Patients'; // keeping it just in case
import './index.css';

function AppLayout() {
  const { user, logout } = useAuth();

  if (!user) {
    return (
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="*" element={<Navigate to="/login" replace />} />
      </Routes>
    );
  }

  return (
    <div className="layout-container">
      {/* Sidebar - conditionally render some links based on user.role */}
      <aside className="sidebar" style={{ display: 'flex', flexDirection: 'column' }}>
        <h2>CareSync</h2>
        <div style={{ padding: '0 20px', color: '#7f8c8d', fontSize: '14px', marginBottom: '15px' }}>
          Logged in as: <br/><strong>{user.name}</strong> <br/>Role: {user.role}
        </div>
        
        {user.role === 'doctor' && (
          <>
            <NavLink to="/" className={({isActive}) => `nav-link ${isActive ? 'active' : ''}`}>
              My Dashboard
            </NavLink>
            <NavLink to="/appointments" className={({isActive}) => `nav-link ${isActive ? 'active' : ''}`}>
              My Appointments
            </NavLink>
            <NavLink to="/prescriptions" className={({isActive}) => `nav-link ${isActive ? 'active' : ''}`}>
              Consultations
            </NavLink>
            {/* We could add Billing Report here later */}
          </>
        )}
        
        {user.role === 'patient' && (
          <>
            <NavLink to="/" className={({isActive}) => `nav-link ${isActive ? 'active' : ''}`}>
              My Dashboard
            </NavLink>
            <NavLink to="/appointments" className={({isActive}) => `nav-link ${isActive ? 'active' : ''}`}>
              Appointments
            </NavLink>
            <NavLink to="/prescriptions" className={({isActive}) => `nav-link ${isActive ? 'active' : ''}`}>
              My Consultations
            </NavLink>
          </>
        )}
        
        <button onClick={logout} style={{ marginTop: 'auto', background: '#e74c3c', color: 'white', border: 'none', padding: '15px 20px', cursor: 'pointer', fontWeight: 'bold' }}>
          Logout
        </button>
      </aside>

      <main className="main-content">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/appointments" element={<Appointments />} />
          <Route path="/prescriptions" element={<Prescriptions />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </main>
    </div>
  );
}

function App() {
  return (
    <Router>
      <AppLayout />
    </Router>
  );
}

export default App;
