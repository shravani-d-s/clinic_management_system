import React from 'react';
import { BrowserRouter as Router, Routes, Route, NavLink } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import Patients from './pages/Patients';
import Appointments from './pages/Appointments';
import Prescriptions from './pages/Prescriptions';
import './index.css';

function App() {
  return (
    <Router>
      <div className="layout-container">
        {/* Sidebar */}
        <aside className="sidebar">
          <h2>ClinicVantage</h2>
          <NavLink to="/" className={({isActive}) => `nav-link ${isActive ? 'active' : ''}`}>
            Dashboard
          </NavLink>
          <NavLink to="/patients" className={({isActive}) => `nav-link ${isActive ? 'active' : ''}`}>
             Patients
          </NavLink>
          <NavLink to="/appointments" className={({isActive}) => `nav-link ${isActive ? 'active' : ''}`}>
             Appointments
          </NavLink>
          <NavLink to="/prescriptions" className={({isActive}) => `nav-link ${isActive ? 'active' : ''}`}>
             Prescriptions
          </NavLink>
        </aside>

        {/* Main Content */}
        <main className="main-content">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/patients" element={<Patients />} />
            <Route path="/appointments" element={<Appointments />} />
            <Route path="/prescriptions" element={<Prescriptions />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
