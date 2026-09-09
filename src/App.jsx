import React, { useState, useEffect, useMemo } from 'react';
import './App.css';

// Dynamic API base URL configuration:
// In production (Render), VITE_API_URL is baked in during build (e.g., https://your-backend.onrender.com/api)
// In local development, falls back cleanly to http://localhost:5000/api
const rawApiUrl = import.meta.env.VITE_API_URL || 'http://localhost:5000/api';
const API_URL = rawApiUrl.endsWith('/api') ? rawApiUrl : `${rawApiUrl.replace(/\/+$/, '')}/api`;

// ==========================================================================
// SVG Icons
// ==========================================================================

function GoogleIcon() {
  return (
    <svg viewBox="0 0 24 24" width="18" height="18" xmlns="http://www.w3.org/2000/svg">
      <path
        fill="#4285F4"
        d="M23.745 12.27c0-.7-.06-1.4-.19-2.07H12v4.51h6.6c-.29 1.52-1.14 2.82-2.4 3.68v3.05h3.88c2.27-2.09 3.66-5.17 3.66-9.17z"
      />
      <path
        fill="#34A853"
        d="M12 24c3.24 0 5.95-1.08 7.93-2.91l-3.88-3.05c-1.08.72-2.45 1.16-4.05 1.16-3.12 0-5.77-2.1-6.72-4.93H1.25v3.15C3.26 21.36 7.34 24 12 24z"
      />
      <path
        fill="#FBBC05"
        d="M5.28 14.27c-.25-.72-.38-1.49-.38-2.27s.13-1.55.38-2.27V6.58H1.25C.45 8.18 0 9.99 0 12s.45 3.82 1.25 5.42l4.03-3.15z"
      />
      <path
        fill="#EA4335"
        d="M12 4.75c1.77 0 3.35.61 4.6 1.8l3.42-3.42C17.95 1.19 15.24 0 12 0 7.34 0 3.26 2.64 1.25 6.58l4.03 3.15c.95-2.83 3.6-4.98 6.72-4.98z"
      />
    </svg>
  );
}

function BrandLogoIcon({ size = 28 }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2" />
      <circle cx="9" cy="7" r="4" />
      <path d="M22 21v-2a4 4 0 0 0-3-3.87" />
      <path d="M16 3.13a4 4 0 0 1 0 7.75" />
    </svg>
  );
}

function SparklesIcon({ size = 16 }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z" />
      <path d="M5 3v4" />
      <path d="M19 17v4" />
      <path d="M3 5h4" />
      <path d="M17 19h4" />
    </svg>
  );
}


function EyeIcon() {
  return (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z" />
      <circle cx="12" cy="12" r="3" />
    </svg>
  );
}

function EyeOffIcon() {
  return (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M9.88 9.88a3 3 0 1 0 4.24 4.24" />
      <path d="M10.73 5.08A10.43 10.43 0 0 1 12 5c7 0 10 7 10 7a13.16 13.16 0 0 1-1.67 2.68" />
      <path d="M6.61 6.61A13.526 13.526 0 0 0 2 12s3 7 10 7a9.74 9.74 0 0 0 5.39-1.61" />
      <line x1="2" y1="2" x2="22" y2="22" />
    </svg>
  );
}

function SearchIcon() {
  return (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="11" cy="11" r="8" />
      <line x1="21" y1="21" x2="16.65" y2="16.65" />
    </svg>
  );
}

function PlusIcon() {
  return (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
      <line x1="12" y1="5" x2="12" y2="19" />
      <line x1="5" y1="12" x2="19" y2="12" />
    </svg>
  );
}

function EditIcon() {
  return (
    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M17 3a2.85 2.83 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5Z" />
      <path d="m15 5 4 4" />
    </svg>
  );
}

function TrashIcon() {
  return (
    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M3 6h18" />
      <path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6" />
      <path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2" />
    </svg>
  );
}

function LogoutIcon() {
  return (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" />
      <polyline points="16 17 21 12 16 7" />
      <line x1="21" y1="12" x2="9" y2="12" />
    </svg>
  );
}

function CloseIcon() {
  return (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <line x1="18" y1="6" x2="6" y2="18" />
      <line x1="6" y1="6" x2="18" y2="18" />
    </svg>
  );
}

// ==========================================================================
// Toast Notification Component
// ==========================================================================

function ToastContainer({ toasts, removeToast }) {
  return (
    <div className="toast-container" aria-live="polite">
      {toasts.map((toast) => (
        <div key={toast.id} className={`toast toast-${toast.type || 'info'}`}>
          <div className="toast-content">{toast.message}</div>
          <button className="toast-close" onClick={() => removeToast(toast.id)} aria-label="Close alert">
            <CloseIcon />
          </button>
        </div>
      ))}
    </div>
  );
}

// Generate consistent avatar color based on customer name
function getAvatarBg(name = '') {
  const colors = [
    '#4f46e5', '#059669', '#d97706', '#dc2626', 
    '#7c3aed', '#0284c7', '#db2777', '#0d9488'
  ];
  let hash = 0;
  for (let i = 0; i < name.length; i++) {
    hash = name.charCodeAt(i) + ((hash << 5) - hash);
  }
  return colors[Math.abs(hash) % colors.length];
}

function getInitials(name = '') {
  const parts = name.trim().split(/\s+/);
  if (parts.length >= 2) {
    return (parts[0][0] + parts[1][0]).toUpperCase();
  }
  return name.slice(0, 2).toUpperCase() || 'CU';
}

// ==========================================================================
// Authentication Components (Login & Sign-Up)
// ==========================================================================

function AuthView({ onLogin, addToast }) {
  const [isSignUp, setIsSignUp] = useState(false);
  
  // Form fields
  const [identifier, setIdentifier] = useState(''); // username or email
  const [name, setName] = useState('');
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  
  // UI states
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [showForgotPasswordModal, setShowForgotPasswordModal] = useState(false);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleGoogleAuth = () => {
    // Redirects browser to backend Google OAuth initiation route
    window.location.href = `${API_URL}/auth/google`;
  };

  const handleLoginSubmit = async (e) => {
    e.preventDefault();
    setError('');

    if (!identifier.trim() || !password) {
      setError('Please enter your username/email and password.');
      return;
    }

    setLoading(true);

    try {
      const response = await fetch(`${API_URL}/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          username: identifier.trim(),
          password,
        }),
      });

      const data = await response.json();

      if (response.ok && data.token) {
        localStorage.setItem('token', data.token);
        addToast('Welcome back! Login successful.', 'success');
        onLogin(data.token, data.user);
      } else {
        setError(data.message || 'Invalid username/email or password.');
      }
    } catch (err) {
      setError('Cannot reach server. Please check your network connection or ensure the backend service is running.');
    } finally {
      setLoading(false);
    }
  };

  const handleSignUpSubmit = async (e) => {
    e.preventDefault();
    setError('');

    if (!username.trim() || !password) {
      setError('Username and password are required.');
      return;
    }

    if (password.length < 4) {
      setError('Password must be at least 4 characters long.');
      return;
    }

    if (password !== confirmPassword) {
      setError('Passwords do not match.');
      return;
    }

    setLoading(true);

    try {
      const response = await fetch(`${API_URL}/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          username: username.trim(),
          email: email.trim() || undefined,
          password,
        }),
      });

      const data = await response.json();

      if (response.ok && data.token) {
        localStorage.setItem('token', data.token);
        addToast('Account created successfully! Welcome to CMS.', 'success');
        onLogin(data.token, data.user);
      } else {
        setError(data.message || 'Registration failed. Please check your inputs.');
      }
    } catch (err) {
      setError('Connection error. Please verify backend is running.');
    } finally {
      setLoading(false);
    }
  };

  const toggleMode = (signUp) => {
    setIsSignUp(signUp);
    setError('');
    setPassword('');
    setConfirmPassword('');
  };

  return (
    <div className="auth-wrapper">
      <div className="auth-card">
        {/* Brand Header */}
        <div className="auth-brand">
          <div className="auth-logo-badge">
            <BrandLogoIcon size={30} />
          </div>
          <h1>{isSignUp ? 'Create your account' : 'Sign in to CMS'}</h1>
          <p>
            {isSignUp
              ? 'Get started managing your customers with ease'
              : 'Welcome back! Enter your details to continue'}
          </p>
        </div>

        {/* Google OAuth Button */}
        <button
          type="button"
          className="btn-google"
          onClick={handleGoogleAuth}
          id="btn-google-auth"
          title="Sign in with your verified Google Account"
        >
          <GoogleIcon />
          <span>Continue with Google</span>
        </button>

        {/* Divider */}
        <div className="auth-divider">
          <span>or continue with {isSignUp ? 'email' : 'credentials'}</span>
        </div>

        {/* Error Alert */}
        {error && (
          <div className="alert-error" style={{ marginBottom: 16 }}>
            <span>{error}</span>
          </div>
        )}

        {/* Login Form */}
        {!isSignUp ? (
          <form className="auth-form" onSubmit={handleLoginSubmit}>
            <div className="form-group">
              <label htmlFor="login-identifier">Username or Email</label>
              <input
                id="login-identifier"
                type="text"
                value={identifier}
                onChange={(e) => setIdentifier(e.target.value)}
                placeholder="Enter your username or email"
                required
                autoComplete="username"
              />
            </div>

            <div className="form-group">
              <label htmlFor="login-password">
                <span>Password</span>
                <button
                  type="button"
                  className="forgot-password-link"
                  onClick={() => setShowForgotPasswordModal(true)}
                >
                  Forgot Password?
                </button>
              </label>
              <div className="input-with-icon">
                <input
                  id="login-password"
                  type={showPassword ? 'text' : 'password'}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="Enter your password"
                  required
                  autoComplete="current-password"
                />
                <button
                  type="button"
                  className="input-toggle-btn"
                  onClick={() => setShowPassword(!showPassword)}
                  aria-label={showPassword ? 'Hide password' : 'Show password'}
                >
                  {showPassword ? <EyeOffIcon /> : <EyeIcon />}
                </button>
              </div>
            </div>

            <button type="submit" className="btn-submit" disabled={loading} id="btn-login-submit">
              {loading ? <div className="spinner-sm" /> : null}
              <span>{loading ? 'Signing in...' : 'Sign In'}</span>
            </button>

            <div className="auth-footer">
              Don't have an account?{' '}
              <button type="button" className="auth-switch-btn" onClick={() => toggleMode(true)}>
                Sign Up
              </button>
            </div>
          </form>
        ) : (
          /* Sign-Up Form */
          <form className="auth-form" onSubmit={handleSignUpSubmit}>
            <div className="form-group">
              <label htmlFor="signup-name">Full Name (Optional)</label>
              <input
                id="signup-name"
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="Jane Doe"
              />
            </div>

            <div className="form-group">
              <label htmlFor="signup-email">Email Address</label>
              <input
                id="signup-email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="jane@example.com"
              />
            </div>

            <div className="form-group">
              <label htmlFor="signup-username">Username *</label>
              <input
                id="signup-username"
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="janedoe"
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="signup-password">Password *</label>
              <div className="input-with-icon">
                <input
                  id="signup-password"
                  type={showPassword ? 'text' : 'password'}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="At least 4 characters"
                  required
                />
                <button
                  type="button"
                  className="input-toggle-btn"
                  onClick={() => setShowPassword(!showPassword)}
                  aria-label={showPassword ? 'Hide password' : 'Show password'}
                >
                  {showPassword ? <EyeOffIcon /> : <EyeIcon />}
                </button>
              </div>
            </div>

            <div className="form-group">
              <label htmlFor="signup-confirm-password">Confirm Password *</label>
              <div className="input-with-icon">
                <input
                  id="signup-confirm-password"
                  type={showConfirmPassword ? 'text' : 'password'}
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  placeholder="Repeat your password"
                  required
                />
                <button
                  type="button"
                  className="input-toggle-btn"
                  onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                  aria-label={showConfirmPassword ? 'Hide password' : 'Show password'}
                >
                  {showConfirmPassword ? <EyeOffIcon /> : <EyeIcon />}
                </button>
              </div>
              {confirmPassword && password !== confirmPassword && (
                <span style={{ fontSize: 12, color: 'var(--danger)', marginTop: 2 }}>
                  Passwords do not match
                </span>
              )}
            </div>

            <button type="submit" className="btn-submit" disabled={loading} id="btn-signup-submit">
              {loading ? <div className="spinner-sm" /> : null}
              <span>{loading ? 'Creating Account...' : 'Create Account'}</span>
            </button>

            <div className="auth-footer">
              Already have an account?{' '}
              <button type="button" className="auth-switch-btn" onClick={() => toggleMode(false)}>
                Sign In
              </button>
            </div>
          </form>
        )}
      </div>

      {/* Forgot Password Modal */}
      {showForgotPasswordModal && (
        <div className="modal-backdrop" onClick={() => setShowForgotPasswordModal(false)}>
          <div className="modal-dialog modal-dialog-sm" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h3>Reset Password</h3>
              <button className="modal-close-btn" onClick={() => setShowForgotPasswordModal(false)}>
                <CloseIcon />
              </button>
            </div>
            <div className="modal-body">
              <p style={{ color: 'var(--text-muted)', fontSize: 14, lineHeight: 1.6 }}>
                For security reasons, password resets in this CMS are managed by system administrators.
              </p>
              <div style={{ marginTop: 14, padding: 12, background: '#f8fafc', borderRadius: 8, fontSize: 13, color: 'var(--text-muted)' }}>
                Tip: You can instantly sign in using <strong>"Continue with Google"</strong> or create a new personal account via <strong>Sign Up</strong>.
              </div>
            </div>
            <div className="modal-footer">
              <button
                type="button"
                className="btn-secondary-action"
                onClick={() => setShowForgotPasswordModal(false)}
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

// ==========================================================================
// Customer Add / Edit Modal Component
// ==========================================================================

function CustomerModal({ customer, isOpen, onClose, onSaved, addToast }) {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    company: '',
    address: '',
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (customer) {
      setFormData({
        name: customer.name || '',
        email: customer.email || '',
        phone: customer.phone || '',
        company: customer.company || '',
        address: customer.address || '',
      });
    } else {
      setFormData({
        name: '',
        email: '',
        phone: '',
        company: '',
        address: '',
      });
    }
    setError('');
  }, [customer, isOpen]);

  if (!isOpen) return null;

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    if (!formData.name.trim() || !formData.email.trim()) {
      setError('Name and email are required fields.');
      return;
    }

    setLoading(true);

    try {
      const token = localStorage.getItem('token');
      const isEditing = Boolean(customer?.id);
      const url = isEditing
        ? `${API_URL}/customers/${customer.id}`
        : `${API_URL}/customers`;
      const method = isEditing ? 'PUT' : 'POST';

      const response = await fetch(url, {
        method,
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(formData),
      });

      const data = await response.json();

      if (response.ok) {
        addToast(
          isEditing ? 'Customer updated successfully!' : 'Customer added successfully!',
          'success'
        );
        onSaved();
        onClose();
      } else {
        setError(data.message || 'Failed to save customer');
      }
    } catch (err) {
      setError('Network error while saving customer');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div className="modal-dialog" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h3>{customer?.id ? 'Edit Customer' : 'Add New Customer'}</h3>
          <button className="modal-close-btn" onClick={onClose}>
            <CloseIcon />
          </button>
        </div>

        <form onSubmit={handleSubmit}>
          <div className="modal-body">
            {error && (
              <div className="alert-error" style={{ marginBottom: 16 }}>
                {error}
              </div>
            )}

            <div className="form-group" style={{ marginBottom: 14 }}>
              <label htmlFor="cust-name">Full Name *</label>
              <input
                id="cust-name"
                name="name"
                type="text"
                value={formData.name}
                onChange={handleChange}
                placeholder="John Doe"
                required
              />
            </div>

            <div className="form-group" style={{ marginBottom: 14 }}>
              <label htmlFor="cust-email">Email Address *</label>
              <input
                id="cust-email"
                name="email"
                type="email"
                value={formData.email}
                onChange={handleChange}
                placeholder="john@example.com"
                required
              />
            </div>

            <div className="form-group" style={{ marginBottom: 14 }}>
              <label htmlFor="cust-phone">Phone Number</label>
              <input
                id="cust-phone"
                name="phone"
                type="tel"
                value={formData.phone}
                onChange={handleChange}
                placeholder="+1-234-567-8900"
              />
            </div>

            <div className="form-group" style={{ marginBottom: 14 }}>
              <label htmlFor="cust-company">Company</label>
              <input
                id="cust-company"
                name="company"
                type="text"
                value={formData.company}
                onChange={handleChange}
                placeholder="Acme Corporation"
              />
            </div>

            <div className="form-group">
              <label htmlFor="cust-address">Address</label>
              <textarea
                id="cust-address"
                name="address"
                rows="3"
                value={formData.address}
                onChange={handleChange}
                placeholder="123 Main St, City, Country"
              />
            </div>
          </div>

          <div className="modal-footer">
            <button type="button" className="btn-secondary-action" onClick={onClose} disabled={loading}>
              Cancel
            </button>
            <button type="submit" className="btn-primary-action" disabled={loading}>
              {loading ? <div className="spinner-sm" /> : null}
              <span>{customer?.id ? 'Update Customer' : 'Save Customer'}</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

// ==========================================================================
// Delete Confirmation Modal Component
// ==========================================================================

function DeleteConfirmationModal({ customer, isOpen, onClose, onConfirm, loading }) {
  if (!isOpen || !customer) return null;

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div className="modal-dialog modal-dialog-sm" onClick={(e) => e.stopPropagation()}>
        <div className="modal-body">
          <div className="delete-confirm-content">
            <div className="delete-warning-icon">
              <TrashIcon />
            </div>
            <h4>Delete Customer</h4>
            <p>
              Are you sure you want to delete this customer record? This action cannot be undone.
            </p>
            <div className="customer-delete-highlight">
              {customer.name} ({customer.email})
            </div>
          </div>
        </div>

        <div className="modal-footer" style={{ justifyContent: 'center' }}>
          <button type="button" className="btn-secondary-action" onClick={onClose} disabled={loading}>
            Cancel
          </button>
          <button
            type="button"
            className="btn-danger-action"
            onClick={() => onConfirm(customer.id)}
            disabled={loading}
          >
            {loading ? <div className="spinner-sm" /> : null}
            <span>Delete Customer</span>
          </button>
        </div>
      </div>
    </div>
  );
}

// ==========================================================================
// AI Customer Copilot Modal Component
// ==========================================================================

function AICopilotModal({ isOpen, onClose, addToast, onCustomersChanged }) {
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: "Hello! I'm your AI Customer Copilot powered by Groq. I can answer questions about your customer base AND directly perform database actions for you!\n\nTry commands like:\n• \"Add customer Sarah Connor, email sarah@skynet.com, company Cyberdyne Systems\"\n• \"Update company for sarah@skynet.com to Resistance Corp\"\n• \"Summarize my customers by company\"\n• \"Which customers do not have a phone number?\"",
    },
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const chatEndRef = React.useRef(null);

  useEffect(() => {
    if (chatEndRef.current) {
      chatEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages, loading]);

  if (!isOpen) return null;

  const handleSend = async (textToSend) => {
    const query = (textToSend || inputMessage).trim();
    if (!query || loading) return;

    const newMessages = [...messages, { role: 'user', content: query }];
    setMessages(newMessages);
    setInputMessage('');
    setLoading(true);

    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`${API_URL}/ai/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          message: query,
          history: newMessages.slice(-6),
        }),
      });

      const data = await response.json();
      if (response.ok && data.reply) {
        setMessages((prev) => [...prev, { role: 'assistant', content: data.reply }]);
        
        // If an AI action was performed, refresh customer list and notify
        if (data.action_performed) {
          if (onCustomersChanged) onCustomersChanged();
          if (data.action_performed === 'create') {
            addToast(`AI Database: Created customer "${data.action_details?.name || ''}"!`, 'success');
          } else if (data.action_performed === 'update') {
            addToast(`AI Database: Updated customer "${data.action_details?.name || ''}"!`, 'success');
          } else if (data.action_performed === 'delete') {
            addToast(`AI Database: Deleted customer "${data.action_details?.name || ''}"!`, 'info');
          }
        }
      } else {
        addToast(data.message || 'AI request failed.', 'error');
        setMessages((prev) => [
          ...prev,
          { role: 'assistant', content: `Notice: ${data.message || 'Unable to complete request.'}` },
        ]);
      }
    } catch (err) {
      addToast('Cannot reach AI backend service.', 'error');
    } finally {
      setLoading(false);
    }
  };

  const quickPrompts = [
    '➕ Add customer: Sarah Connor, sarah@skynet.com, Cyberdyne',
    '📊 Summarize my customer portfolio',
    '🏢 Breakdown customers by company',
    '🔍 Find customers missing phone numbers',
  ];

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div className="modal-dialog ai-copilot-dialog" onClick={(e) => e.stopPropagation()}>
        <div className="ai-copilot-header">
          <div className="ai-copilot-title">
            <SparklesIcon size={18} />
            <h3 style={{ margin: 0, fontSize: 16 }}>AI Customer Copilot</h3>
            <span className="ai-copilot-badge">Groq &bull; Qwen 3.8</span>
          </div>
          <button className="modal-close-btn" onClick={onClose} aria-label="Close">
            <CloseIcon />
          </button>
        </div>

        <div className="ai-chat-thread">
          {messages.map((m, idx) => (
            <div key={idx} className={`ai-msg ${m.role}`}>
              <div className="ai-msg-avatar">
                {m.role === 'user' ? 'You' : <SparklesIcon size={14} />}
              </div>
              <div className="ai-msg-bubble">{m.content}</div>
            </div>
          ))}
          {loading && (
            <div className="ai-msg assistant">
              <div className="ai-msg-avatar">
                <SparklesIcon size={14} />
              </div>
              <div className="ai-msg-bubble" style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                <div className="spinner-sm" style={{ borderColor: '#c4b5fd', borderTopColor: '#7c3aed' }} />
                <span>Thinking with Groq AI...</span>
              </div>
            </div>
          )}
          <div ref={chatEndRef} />
        </div>

        <div className="ai-chips-bar">
          {quickPrompts.map((prompt, i) => (
            <button
              key={i}
              type="button"
              className="ai-prompt-chip"
              onClick={() => handleSend(prompt.replace(/^[^\w]+/, ''))}
              disabled={loading}
            >
              {prompt}
            </button>
          ))}
        </div>

        <form
          className="ai-input-bar"
          onSubmit={(e) => {
            e.preventDefault();
            handleSend();
          }}
        >
          <input
            type="text"
            placeholder="Ask anything about your customers or request recommendations..."
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            disabled={loading}
          />
          <button type="submit" className="btn-primary-action" disabled={loading || !inputMessage.trim()}>
            <span>Send</span>
          </button>
        </form>
      </div>
    </div>
  );
}

// ==========================================================================
// AI Customer Email Drafter Modal Component
// ==========================================================================

function AIEmailDraftModal({ customer, isOpen, onClose, addToast }) {
  const [goal, setGoal] = useState('check_in');
  const [notes, setNotes] = useState('');
  const [subject, setSubject] = useState('');
  const [body, setBody] = useState('');
  const [loading, setLoading] = useState(false);
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    if (customer && isOpen) {
      setSubject('');
      setBody('');
      setNotes('');
      setCopied(false);
      setGoal('check_in');
      generateDraft('check_in', '');
    }
  }, [customer, isOpen]);

  if (!isOpen || !customer) return null;

  const generateDraft = async (targetGoal, customNotes) => {
    setLoading(true);
    setCopied(false);
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`${API_URL}/ai/draft-email`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          customer_id: customer.id,
          goal: targetGoal || goal,
          notes: customNotes !== undefined ? customNotes : notes,
        }),
      });

      const data = await response.json();
      if (response.ok) {
        setSubject(data.subject || '');
        setBody(data.body || '');
      } else {
        addToast(data.message || 'Failed to draft email.', 'error');
      }
    } catch (err) {
      addToast('Error communicating with AI service.', 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleCopy = () => {
    const fullText = `Subject: ${subject}\n\n${body}`;
    navigator.clipboard.writeText(fullText);
    setCopied(true);
    addToast('Email draft copied to clipboard!', 'success');
    setTimeout(() => setCopied(false), 3000);
  };

  const mailtoHref = `mailto:${customer.email}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div className="modal-dialog" style={{ maxWidth: 620 }} onClick={(e) => e.stopPropagation()}>
        <div className="modal-header" style={{ background: 'linear-gradient(to right, #faf5ff, #ffffff)' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
            <SparklesIcon size={18} />
            <h3 style={{ margin: 0, fontSize: 16 }}>AI Smart Email Drafter</h3>
          </div>
          <button className="modal-close-btn" onClick={onClose}>
            <CloseIcon />
          </button>
        </div>

        <div className="modal-body" style={{ padding: '20px 24px' }}>
          <div style={{ marginBottom: 14, fontSize: 13, color: 'var(--text-muted)' }}>
            Recipient: <strong>{customer.name}</strong> ({customer.email}) &bull; Company: <strong>{customer.company || 'N/A'}</strong>
          </div>

          <label style={{ fontSize: 12, fontWeight: 600, color: 'var(--text-muted)', display: 'block', marginBottom: 6 }}>
            Select Outreach Objective:
          </label>
          <div className="goal-selector">
            {[
              { id: 'check_in', label: '👋 Check-In' },
              { id: 'proposal', label: '💼 Value Proposal' },
              { id: 'meeting', label: '📅 Catch-Up Call' },
              { id: 'custom', label: '✏️ Custom Request' },
            ].map((g) => (
              <button
                key={g.id}
                type="button"
                className={`btn-goal-chip ${goal === g.id ? 'active' : ''}`}
                onClick={() => {
                  setGoal(g.id);
                  generateDraft(g.id, notes);
                }}
              >
                {g.label}
              </button>
            ))}
          </div>

          {goal === 'custom' && (
            <div style={{ marginBottom: 14 }}>
              <input
                type="text"
                className="form-group input"
                style={{ width: '100%', padding: '8px 12px', fontSize: 13, border: '1px solid var(--border-color)', borderRadius: 6 }}
                placeholder="E.g., Announce our upcoming feature release and invite them to an early demo..."
                value={notes}
                onChange={(e) => setNotes(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === 'Enter') {
                    generateDraft(goal, notes);
                  }
                }}
              />
            </div>
          )}

          {loading ? (
            <div className="loading-state" style={{ padding: '40px 10px' }}>
              <div className="spinner" style={{ borderColor: '#ddd6fe', borderTopColor: '#7c3aed' }} />
              <span>Drafting personalized email with Groq AI...</span>
            </div>
          ) : body ? (
            <div className="draft-output-card">
              <div className="draft-subject-row">
                <div>
                  <span style={{ fontSize: 11, fontWeight: 700, color: 'var(--text-muted)', textTransform: 'uppercase' }}>
                    Subject Line
                  </span>
                  <div className="draft-subject-text">{subject}</div>
                </div>
              </div>

              <div className="draft-body-preview">{body}</div>

              <div className="draft-actions-bar">
                <button
                  type="button"
                  className="btn-secondary-action"
                  onClick={() => generateDraft(goal, notes)}
                  title="Regenerate draft"
                  style={{ fontSize: 12, padding: '6px 12px' }}
                >
                  ↻ Regenerate
                </button>

                <div style={{ display: 'flex', gap: 8 }}>
                  <button type="button" className="btn-copy-draft" onClick={handleCopy}>
                    {copied ? '✓ Copied!' : '📋 Copy Draft'}
                  </button>
                  <a href={mailtoHref} className="btn-mailto">
                    ✉️ Open in Mail
                  </a>
                </div>
              </div>
            </div>
          ) : null}
        </div>

        <div className="modal-footer">
          <button type="button" className="btn-secondary-action" onClick={onClose}>
            Close
          </button>
        </div>
      </div>
    </div>
  );
}

// ==========================================================================
// Dashboard Component
// ==========================================================================


function CustomerDashboard({ user, onLogout, addToast }) {
  const [customers, setCustomers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  
  // Modals state
  const [modalCustomer, setModalCustomer] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [deleteTarget, setDeleteTarget] = useState(null);
  const [deleteLoading, setDeleteLoading] = useState(false);

  // AI features state
  const [isAiCopilotOpen, setIsAiCopilotOpen] = useState(false);
  const [aiCustomer, setAiCustomer] = useState(null);

  useEffect(() => {
    fetchCustomers();
  }, []);

  const fetchCustomers = async () => {
    setLoading(true);
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`${API_URL}/customers`, {
        headers: { Authorization: `Bearer ${token}` },
      });

      if (response.ok) {
        const data = await response.json();
        setCustomers(data.customers || []);
      } else if (response.status === 401) {
        addToast('Your session has expired. Please log in again.', 'error');
        onLogout();
      } else {
        addToast('Failed to load customers from server.', 'error');
      }
    } catch (err) {
      addToast('Cannot connect to backend server.', 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteCustomer = async (id) => {
    setDeleteLoading(true);
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`${API_URL}/customers/${id}`, {
        method: 'DELETE',
        headers: { Authorization: `Bearer ${token}` },
      });

      if (response.ok) {
        addToast('Customer record deleted successfully.', 'success');
        setDeleteTarget(null);
        fetchCustomers();
      } else {
        const data = await response.json();
        addToast(data.message || 'Failed to delete customer.', 'error');
      }
    } catch (err) {
      addToast('Network error while deleting customer.', 'error');
    } finally {
      setDeleteLoading(false);
    }
  };

  // Filtered customer list
  const filteredCustomers = useMemo(() => {
    const term = searchTerm.toLowerCase().trim();
    if (!term) return customers;
    return customers.filter(
      (c) =>
        (c.name && c.name.toLowerCase().includes(term)) ||
        (c.email && c.email.toLowerCase().includes(term)) ||
        (c.company && c.company.toLowerCase().includes(term)) ||
        (c.phone && c.phone.toLowerCase().includes(term))
    );
  }, [customers, searchTerm]);

  // Derived metrics
  const uniqueCompanies = useMemo(() => {
    const set = new Set();
    customers.forEach((c) => {
      if (c.company && c.company.trim()) set.add(c.company.trim());
    });
    return set.size;
  }, [customers]);

  return (
    <div className="dashboard-layout">
      {/* Top Navigation Bar */}
      <header className="dashboard-header">
        <div className="header-brand">
          <div className="brand-icon">
            <BrandLogoIcon size={22} />
          </div>
          <h2>Customer Management System</h2>
        </div>

        <div className="header-actions">
          {user && (
            <div className="user-profile-badge">
              <div className="user-avatar">
                {user.username ? user.username.slice(0, 2).toUpperCase() : 'U'}
              </div>
              <div className="user-meta">
                <span className="user-name">{user.username}</span>
                <span className={`auth-badge ${user.auth_provider === 'google' ? 'google' : ''}`}>
                  {user.auth_provider === 'google' ? 'Google Account' : 'Local Account'}
                </span>
              </div>
            </div>
          )}

          <button
            className="btn-ai-copilot"
            onClick={() => setIsAiCopilotOpen(true)}
            title="Open AI Customer Copilot powered by Groq"
            id="btn-open-ai-copilot"
          >
            <SparklesIcon size={16} />
            <span>AI Copilot</span>
          </button>

          <button className="btn-logout" onClick={onLogout} title="Log out of application">
            <LogoutIcon />
            <span>Logout</span>
          </button>
        </div>
      </header>

      {/* Main Container */}
      <main className="dashboard-main">
        {/* Metric Cards */}
        <section className="stats-grid">
          <div className="stat-card">
            <div className="stat-icon-wrap indigo">
              <BrandLogoIcon size={24} />
            </div>
            <div className="stat-info">
              <span className="stat-label">Total Customers</span>
              <span className="stat-value">{customers.length}</span>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon-wrap emerald">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M3 21h18" />
                <path d="M5 21V7l8-4v18" />
                <path d="M19 21V11l-6-4" />
              </svg>
            </div>
            <div className="stat-info">
              <span className="stat-label">Companies</span>
              <span className="stat-value">{uniqueCompanies}</span>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon-wrap amber">
              <SearchIcon />
            </div>
            <div className="stat-info">
              <span className="stat-label">Filtered Results</span>
              <span className="stat-value">{filteredCustomers.length}</span>
            </div>
          </div>
        </section>

        {/* Action Toolbar */}
        <div className="table-toolbar">
          <div className="search-box">
            <span className="search-icon">
              <SearchIcon />
            </span>
            <input
              type="text"
              className="search-input-field"
              placeholder="Search by name, email, company, or phone..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              id="input-customer-search"
            />
            {searchTerm && (
              <button
                className="search-clear-btn"
                onClick={() => setSearchTerm('')}
                title="Clear search"
              >
                <CloseIcon />
              </button>
            )}
          </div>

          <div className="toolbar-actions">
            <button
              className="btn-refresh"
              onClick={fetchCustomers}
              title="Refresh customer list"
              disabled={loading}
            >
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M21.5 2v6h-6M21.34 15.57a10 10 0 1 1-.57-8.38l5.67-5.19" />
              </svg>
            </button>

            <button
              className="btn-primary-action"
              onClick={() => {
                setModalCustomer(null);
                setIsModalOpen(true);
              }}
              id="btn-add-customer"
            >
              <PlusIcon />
              <span>Add Customer</span>
            </button>
          </div>
        </div>

        {/* Customer Table Card */}
        <div className="table-card">
          {loading ? (
            <div className="loading-state">
              <div className="spinner" />
              <span>Loading customer records...</span>
            </div>
          ) : filteredCustomers.length === 0 ? (
            <div className="empty-state">
              <div className="empty-state-icon">
                <BrandLogoIcon size={32} />
              </div>
              <h3>
                {customers.length === 0
                  ? 'No customers added yet'
                  : 'No matching customers found'}
              </h3>
              <p>
                {customers.length === 0
                  ? 'Get started by creating your first customer profile.'
                  : `We couldn't find any customers matching "${searchTerm}". Try a different keyword.`}
              </p>
              {customers.length === 0 ? (
                <button
                  className="btn-primary-action"
                  onClick={() => {
                    setModalCustomer(null);
                    setIsModalOpen(true);
                  }}
                >
                  <PlusIcon />
                  <span>Create First Customer</span>
                </button>
              ) : (
                <button className="btn-secondary-action" onClick={() => setSearchTerm('')}>
                  Clear Search Filter
                </button>
              )}
            </div>
          ) : (
            <div className="table-responsive-wrap">
              <table className="modern-table">
                <thead>
                  <tr>
                    <th>Customer</th>
                    <th>Email</th>
                    <th>Phone</th>
                    <th>Company</th>
                    <th>Address</th>
                    <th style={{ textAlign: 'right' }}>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredCustomers.map((customer) => (
                    <tr key={customer.id}>
                      <td>
                        <div className="customer-profile-cell">
                          <div
                            className="customer-initials-avatar"
                            style={{ backgroundColor: getAvatarBg(customer.name) }}
                          >
                            {getInitials(customer.name)}
                          </div>
                          <div className="customer-name-meta">
                            <span className="customer-name-title">{customer.name}</span>
                            <span className="customer-joined">
                              ID #{customer.id}
                            </span>
                          </div>
                        </div>
                      </td>

                      <td>
                        <a href={`mailto:${customer.email}`} className="customer-email-link">
                          {customer.email}
                        </a>
                      </td>

                      <td>
                        {customer.phone ? (
                          <a href={`tel:${customer.phone}`} style={{ color: 'inherit' }}>
                            {customer.phone}
                          </a>
                        ) : (
                          <span style={{ color: 'var(--text-light)' }}>-</span>
                        )}
                      </td>

                      <td>
                        {customer.company ? (
                          <span className="company-badge">{customer.company}</span>
                        ) : (
                          <span style={{ color: 'var(--text-light)' }}>-</span>
                        )}
                      </td>

                      <td>
                        <div className="address-cell" title={customer.address || ''}>
                          {customer.address || '-'}
                        </div>
                      </td>

                      <td>
                        <div className="action-buttons-group" style={{ justifyContent: 'flex-end' }}>
                          <button
                            className="btn-action-ai"
                            onClick={() => setAiCustomer(customer)}
                            title="Draft email & generate insights with Groq AI"
                          >
                            <SparklesIcon size={14} />
                            <span>AI Draft</span>
                          </button>

                          <button
                            className="btn-action-edit"
                            onClick={() => {
                              setModalCustomer(customer);
                              setIsModalOpen(true);
                            }}
                            title="Edit customer details"
                          >
                            <EditIcon />
                            <span>Edit</span>
                          </button>

                          <button
                            className="btn-action-delete"
                            onClick={() => setDeleteTarget(customer)}
                            title="Delete customer"
                          >
                            <TrashIcon />
                            <span>Delete</span>
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>

              <div className="table-footer">
                <span>Showing {filteredCustomers.length} of {customers.length} customer records</span>
                <span>Sorted by recent additions</span>
              </div>
            </div>
          )}
        </div>
      </main>

      {/* Add / Edit Customer Modal */}
      <CustomerModal
        customer={modalCustomer}
        isOpen={isModalOpen}
        onClose={() => {
          setIsModalOpen(false);
          setModalCustomer(null);
        }}
        onSaved={fetchCustomers}
        addToast={addToast}
      />

      {/* Delete Confirmation Modal */}
      <DeleteConfirmationModal
        customer={deleteTarget}
        isOpen={Boolean(deleteTarget)}
        onClose={() => setDeleteTarget(null)}
        onConfirm={handleDeleteCustomer}
        loading={deleteLoading}
      />

      {/* AI Customer Copilot Modal */}
      <AICopilotModal
        isOpen={isAiCopilotOpen}
        onClose={() => setIsAiCopilotOpen(false)}
        addToast={addToast}
        onCustomersChanged={fetchCustomers}
      />

      {/* AI Smart Email Drafter Modal */}
      <AIEmailDraftModal
        customer={aiCustomer}
        isOpen={Boolean(aiCustomer)}
        onClose={() => setAiCustomer(null)}
        addToast={addToast}
      />
    </div>
  );
}

// ==========================================================================
// Root Application Component
// ==========================================================================

function App() {
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [user, setUser] = useState(null);
  const [toasts, setToasts] = useState([]);

  const addToast = (message, type = 'info') => {
    const id = Date.now() + Math.random();
    setToasts((prev) => [...prev, { id, message, type }]);
    setTimeout(() => {
      setToasts((prev) => prev.filter((t) => t.id !== id));
    }, 4500);
  };

  const removeToast = (id) => {
    setToasts((prev) => prev.filter((t) => t.id !== id));
  };

  // Google OAuth URL callback parsing on initial load
  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const oauthToken = params.get('token');
    const oauthError = params.get('error');

    if (oauthToken) {
      localStorage.setItem('token', oauthToken);
      setToken(oauthToken);
      addToast('Google Sign-In successful! Welcome back.', 'success');
      // Clean query parameters from URL without reloading
      window.history.replaceState({}, document.title, window.location.pathname);
    } else if (oauthError) {
      addToast(`Authentication note: ${decodeURIComponent(oauthError)}`, 'error');
      window.history.replaceState({}, document.title, window.location.pathname);
    }
  }, []);

  // Fetch authenticated user profile when token is active
  useEffect(() => {
    if (token) {
      fetchUserProfile(token);
    } else {
      setUser(null);
    }
  }, [token]);

  const fetchUserProfile = async (authToken) => {
    try {
      const response = await fetch(`${API_URL}/auth/me`, {
        headers: { Authorization: `Bearer ${authToken}` },
      });
      if (response.ok) {
        const data = await response.json();
        setUser(data.user);
      } else if (response.status === 401) {
        handleLogout();
      }
    } catch (err) {
      console.warn('Could not fetch user profile:', err);
    }
  };

  const handleLogin = (newToken, userData) => {
    setToken(newToken);
    if (userData) {
      setUser(userData);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    setToken(null);
    setUser(null);
    addToast('You have been logged out.', 'info');
  };

  return (
    <div className="App">
      <ToastContainer toasts={toasts} removeToast={removeToast} />
      {token ? (
        <CustomerDashboard user={user} onLogout={handleLogout} addToast={addToast} />
      ) : (
        <AuthView onLogin={handleLogin} addToast={addToast} />
      )}
    </div>
  );
}

export default App;
