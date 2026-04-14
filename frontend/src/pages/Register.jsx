import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';

export default function Register() {
  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    dob: '',
    gender: 'Male',
    phone: '',
    email: '',
    address: '',
    password: ''
  });
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    try {
      const payload = { ...formData };
      if (!payload.email) delete payload.email;
      if (!payload.address) delete payload.address;

      const response = await fetch('http://localhost:8000/api/patients', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      
      const data = await response.json();
      if (!response.ok) {
        let errorMessage = data.detail || 'Registration failed';
        if (Array.isArray(data.detail)) {
          errorMessage = data.detail.map(err => `${err.loc[err.loc.length-1]}: ${err.msg}`).join(', ');
        } else if (typeof data.detail === 'object') {
          errorMessage = JSON.stringify(data.detail);
        }
        throw new Error(errorMessage);
      }
      
      setSuccess('Registration successful! Redirecting to login...');
      setTimeout(() => navigate('/login'), 2000);
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="login-container" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', minHeight: '100vh', background: '#f5f7fa', padding: '20px' }}>
      <div style={{ background: 'white', padding: '2rem', borderRadius: '12px', boxShadow: '0 4px 6px rgba(0,0,0,0.1)', width: '100%', maxWidth: '400px', maxHeight: '90vh', overflowY: 'auto' }}>
        <h2 style={{ textAlign: 'center', color: '#2c3e50', marginBottom: '1.5rem' }}>Patient Registration</h2>
        
        {error && <div style={{ background: '#ffebee', color: '#c62828', padding: '10px', borderRadius: '4px', marginBottom: '1rem', textAlign: 'center' }}>{error}</div>}
        {success && <div style={{ background: '#e8f5e9', color: '#2e7d32', padding: '10px', borderRadius: '4px', marginBottom: '1rem', textAlign: 'center' }}>{success}</div>}

        <form onSubmit={handleRegister} style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
          <div style={{ display: 'flex', gap: '10px' }}>
            <div style={{ flex: 1 }}>
              <label style={{ display: 'block', marginBottom: '5px', color: '#7f8c8d' }}>First Name</label>
              <input type="text" name="first_name" value={formData.first_name} onChange={handleChange} required style={{ width: '100%', padding: '10px', borderRadius: '4px', border: '1px solid #ccc', boxSizing: 'border-box' }} />
            </div>
            <div style={{ flex: 1 }}>
              <label style={{ display: 'block', marginBottom: '5px', color: '#7f8c8d' }}>Last Name</label>
              <input type="text" name="last_name" value={formData.last_name} onChange={handleChange} required style={{ width: '100%', padding: '10px', borderRadius: '4px', border: '1px solid #ccc', boxSizing: 'border-box' }} />
            </div>
          </div>
          
          <div>
            <label style={{ display: 'block', marginBottom: '5px', color: '#7f8c8d' }}>Date of Birth</label>
            <input type="date" name="dob" value={formData.dob} onChange={handleChange} required style={{ width: '100%', padding: '10px', borderRadius: '4px', border: '1px solid #ccc', boxSizing: 'border-box' }} />
          </div>

          <div>
            <label style={{ display: 'block', marginBottom: '5px', color: '#7f8c8d' }}>Gender</label>
            <select name="gender" value={formData.gender} onChange={handleChange} style={{ width: '100%', padding: '10px', borderRadius: '4px', border: '1px solid #ccc', boxSizing: 'border-box' }}>
              <option value="Male">Male</option>
              <option value="Female">Female</option>
              <option value="Other">Other</option>
            </select>
          </div>

          <div>
            <label style={{ display: 'block', marginBottom: '5px', color: '#7f8c8d' }}>Phone</label>
            <input type="text" name="phone" value={formData.phone} onChange={handleChange} required style={{ width: '100%', padding: '10px', borderRadius: '4px', border: '1px solid #ccc', boxSizing: 'border-box' }} />
          </div>

          <div>
            <label style={{ display: 'block', marginBottom: '5px', color: '#7f8c8d' }}>Email</label>
            <input type="email" name="email" value={formData.email} onChange={handleChange} style={{ width: '100%', padding: '10px', borderRadius: '4px', border: '1px solid #ccc', boxSizing: 'border-box' }} />
          </div>

          <div>
            <label style={{ display: 'block', marginBottom: '5px', color: '#7f8c8d' }}>Address</label>
            <input type="text" name="address" value={formData.address} onChange={handleChange} style={{ width: '100%', padding: '10px', borderRadius: '4px', border: '1px solid #ccc', boxSizing: 'border-box' }} />
          </div>

          <div>
            <label style={{ display: 'block', marginBottom: '5px', color: '#7f8c8d' }}>Password</label>
            <input type="password" name="password" value={formData.password} onChange={handleChange} required style={{ width: '100%', padding: '10px', borderRadius: '4px', border: '1px solid #ccc', boxSizing: 'border-box' }} />
          </div>

          <button type="submit" style={{ padding: '12px', background: '#3498db', color: 'white', border: 'none', borderRadius: '6px', cursor: 'pointer', fontWeight: 'bold', fontSize: '16px', marginTop: '10px' }}>
            Register
          </button>
        </form>
        <div style={{ marginTop: '15px', textAlign: 'center', fontSize: '14px' }}>
          Already have an account? <Link to="/login" style={{ color: '#3498db', textDecoration: 'none', fontWeight: 'bold' }}>Login</Link>
        </div>
      </div>
    </div>
  );
}
