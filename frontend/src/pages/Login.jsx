import { useState } from 'react';
import { useAuth } from '../AuthContext';
import { useNavigate, Link } from 'react-router-dom';

export default function Login() {
  const [role, setRole] = useState('patient');
  const [emailOrPhone, setEmailOrPhone] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    setError('');
    try {
      // Backend api lives at localhost:8000
      const response = await fetch('http://localhost:8000/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          role,
          email_or_phone: emailOrPhone,
          password
        })
      });
      
      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.detail || 'Login failed');
      }
      
      login(data);
      navigate('/');
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="login-container" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '100vh', background: '#f5f7fa' }}>
      <div style={{ background: 'white', padding: '2rem', borderRadius: '12px', boxShadow: '0 4px 6px rgba(0,0,0,0.1)', width: '100%', maxWidth: '400px' }}>
        <h2 style={{ textAlign: 'center', color: '#2c3e50', marginBottom: '1.5rem' }}>CareSync Login</h2>
        
        {error && <div style={{ background: '#ffebee', color: '#c62828', padding: '10px', borderRadius: '4px', marginBottom: '1rem', textAlign: 'center' }}>{error}</div>}
        
        <div style={{ display: 'flex', gap: '10px', marginBottom: '1.5rem' }}>
          <button 
            type="button"
            onClick={() => setRole('patient')}
            style={{ flex: 1, padding: '10px', borderRadius: '6px', border: '1px solid #3498db', background: role === 'patient' ? '#3498db' : 'white', color: role === 'patient' ? 'white' : '#3498db', cursor: 'pointer', fontWeight: 'bold' }}
          >
            Patient
          </button>
          <button 
            type="button"
            onClick={() => setRole('doctor')}
            style={{ flex: 1, padding: '10px', borderRadius: '6px', border: '1px solid #3498db', background: role === 'doctor' ? '#3498db' : 'white', color: role === 'doctor' ? 'white' : '#3498db', cursor: 'pointer', fontWeight: 'bold' }}
          >
            Doctor
          </button>
        </div>

        <form onSubmit={handleLogin} style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
          <div>
            <label style={{ display: 'block', marginBottom: '5px', color: '#7f8c8d' }}>Email or Phone</label>
            <input 
              type="text" 
              value={emailOrPhone}
              onChange={(e) => setEmailOrPhone(e.target.value)}
              required
              style={{ width: '100%', padding: '10px', borderRadius: '4px', border: '1px solid #ccc', boxSizing: 'border-box' }}
              placeholder={role === 'patient' ? 'Enter your phone/email' : 'Enter doc email/phone'}
            />
          </div>
          <div>
            <label style={{ display: 'block', marginBottom: '5px', color: '#7f8c8d' }}>Password</label>
            <input 
              type="password" 
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              style={{ width: '100%', padding: '10px', borderRadius: '4px', border: '1px solid #ccc', boxSizing: 'border-box' }}
              placeholder="Enter password"
            />
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', marginTop: '10px' }}>
            <button type="submit" style={{ padding: '12px', background: '#2ecc71', color: 'white', border: 'none', borderRadius: '6px', cursor: 'pointer', fontWeight: 'bold', fontSize: '16px' }}>
              Login
            </button>
            {role === 'patient' && (
              <button 
                type="button" 
                onClick={() => navigate('/register')}
                style={{ padding: '12px', background: '#3498db', color: 'white', border: 'none', borderRadius: '6px', cursor: 'pointer', fontWeight: 'bold', fontSize: '16px' }}
              >
                Register
              </button>
            )}
          </div>
        </form>
        <div style={{ marginTop: '15px', textAlign: 'center', fontSize: '12px', color: '#95a5a6' }}>
          Try {role === 'patient' ? '9876543210 / pat_ramesh' : 'rajesh@clinic.com / doc_rajesh'}
        </div>
      </div>
    </div>
  );
}
