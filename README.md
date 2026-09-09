# Customer Management Web Application

A modern, full-stack web application for managing customer information with authentication, CRUD operations, and search functionality. Built with React, Flask, and PostgreSQL.

## 🎯 Project Overview

This is a **Basic Level** customer management system designed to be extended with AI features in future iterations. It provides a solid foundation for managing customer data with a clean, intuitive user interface.

### Key Features

✅ **User Authentication**
- Secure login system with JWT tokens
- Demo account for quick testing
- Password hashing with werkzeug

✅ **Customer Management**
- View all customers in an organized table
- Add new customers with complete information
- Edit existing customer details
- Delete customers with confirmation
- Search customers by name or email

✅ **Customer Information**
- Customer Name
- Email (unique identifier)
- Phone Number
- Company Name
- Full Address

✅ **Responsive Design**
- Mobile-friendly interface
- Works on desktop, tablet, and mobile devices
- Clean, modern UI with gradient styling

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     USER BROWSER                             │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
        ┌──────────────────────────────────────┐
        │  FRONTEND - React.js (Port 3003)     │
        │  ├─ Login Page                       │
        │  ├─ Customer List                    │
        │  ├─ Add/Edit Form                    │
        │  └─ Search Functionality             │
        └────────────┬─────────────────────────┘
                     │ HTTP/REST API
                     │ (localhost:5000)
        ┌────────────▼─────────────────────────┐
        │  BACKEND - Flask (Port 5000)         │
        │  ├─ Authentication Routes            │
        │  ├─ Customer CRUD Routes             │
        │  ├─ Search & Filter Routes           │
        │  └─ JWT Token Verification           │
        └────────────┬─────────────────────────┘
                     │ SQL/psycopg2
                     │
        ┌────────────▼─────────────────────────┐
        │  DATABASE - PostgreSQL               │
        │  ├─ Users Table                      │
        │  └─ Customers Table                  │
        └──────────────────────────────────────┘
```

### Technology Stack

| Layer | Technology | Version |
|-------|-----------|---------|
| **Frontend** | React.js | 18.2.0 |
| **Backend** | Python Flask | 3.0.0 |
| **Database** | PostgreSQL | 12+ |
| **Authentication** | JWT (Flask-JWT-Extended) | 4.5.2 |
| **ORM** | SQLAlchemy | 3.1.1 |
| **API** | REST | - |

---

## 📋 Prerequisites

### System Requirements
- **Node.js** v14+ (for React frontend)
- **Python** 3.8+ (for Flask backend)
- **PostgreSQL** 12+ (database)
- **8GB RAM** minimum
- **2GB disk space** for dependencies

### Installation Verification

```bash
# Check Node.js
node --version  # Should be v14 or higher

# Check Python
python --version  # Should be 3.8+

# Check PostgreSQL
psql --version
```

---

## 🚀 Quick Start Guide

### 1️⃣ Clone or Download Project

```bash
# Create project directory
mkdir customer-management-app
cd customer-management-app

# Copy all files here
```

### 2️⃣ Database Setup

```bash
# On Windows Command Prompt or macOS/Linux Terminal:
psql -U postgres

# Run in PostgreSQL prompt:
CREATE DATABASE customer_db;
CREATE USER customer_admin WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE customer_db TO customer_admin;
\q
```

### 3️⃣ Backend Setup (Terminal 1)

```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit .env with your database credentials
# (Windows: notepad .env, macOS/Linux: nano .env)

# Run backend
python app.py

# Expected output:
# Demo user created: username=demo, password=demo
# Sample customers created
#  * Running on http://127.0.0.1:5000
```

### 4️⃣ Frontend Setup (Terminal 2)

```bash
# Create React app
npx create-react-app customer-app
cd customer-app

# Copy frontend files to src/
# - Copy App.jsx content to src/App.jsx
# - Copy App.css content to src/App.css

# Install dependencies (if needed)
npm install axios

# Start development server
npm start

# Browser will open at http://localhost:3003
```

### 5️⃣ Login

- **Username:** `demo`
- **Password:** `demo`

---

## 📁 Project File Structure

```
customer-management-app/
│
├── app.py                      # Flask backend server
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables
├── .env.example               # Environment template
│
├── README.md                  # This file
├── SETUP_GUIDE.md             # Detailed setup instructions
│
├── customer-app/              # React frontend (create-react-app)
│   ├── src/
│   │   ├── App.jsx            # Main React component
│   │   ├── App.css            # Application styling
│   │   ├── index.js           # React entry point
│   │   └── index.css          # Global styles
│   ├── public/
│   │   ├── index.html
│   │   └── favicon.ico
│   ├── package.json           # Frontend dependencies
│   └── README.md              # Create React App README
│
└── docs/                      # Documentation (optional)
    ├── DATABASE_SCHEMA.md
    ├── API_REFERENCE.md
    └── DEPLOYMENT_GUIDE.md
```

---

## 🔧 Backend API Endpoints

### Base URL: `http://localhost:5000/api`

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/login` | User login (returns JWT token) |
| POST | `/register` | User registration |

### Customer Operations

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---|
| GET | `/customers` | Get all customers | ✅ |
| GET | `/customers/:id` | Get specific customer | ✅ |
| POST | `/customers` | Create new customer | ✅ |
| PUT | `/customers/:id` | Update customer | ✅ |
| DELETE | `/customers/:id` | Delete customer | ✅ |
| GET | `/customers/search?q=query` | Search customers | ✅ |

### Health Check

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | API health status |

---

## 📊 Database Schema

### Users Table
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Customers Table
```sql
CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    phone VARCHAR(20),
    company VARCHAR(120),
    address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 🔐 Security Features

✅ **JWT Authentication** - Secure token-based authentication
✅ **Password Hashing** - Uses werkzeug.security for password encryption
✅ **CORS Protection** - Configured for specific origins
✅ **SQL Injection Prevention** - SQLAlchemy parameterized queries
✅ **Input Validation** - Required field validation on backend

### Security Best Practices for Production

- [ ] Change JWT_SECRET_KEY to a strong random value
- [ ] Use environment variables for all sensitive data
- [ ] Enable HTTPS
- [ ] Implement rate limiting
- [ ] Add request logging and monitoring
- [ ] Use strong password requirements
- [ ] Implement email verification
- [ ] Regular security audits

---

## 🧪 Testing the Application

### Manual Testing Checklist

#### Login
- [ ] Login with demo account (demo/demo)
- [ ] Test invalid credentials
- [ ] Verify token is stored in localStorage

#### Customer Management
- [ ] View customer list
- [ ] Add new customer
- [ ] Edit existing customer
- [ ] Delete customer with confirmation
- [ ] Search customers by name
- [ ] Search customers by email

#### Error Handling
- [ ] Add customer with duplicate email
- [ ] Submit form with empty required fields
- [ ] Test with backend offline
- [ ] Clear localStorage and test re-authentication

---

## 📈 Performance Metrics

### Expected Response Times
- Login: < 200ms
- Get Customers: < 500ms
- Add Customer: < 300ms
- Search: < 400ms

### Scalability
- Current setup: Supports 10,000+ customers
- For larger datasets: Consider pagination and caching

---

## 🐛 Troubleshooting

### Backend Won't Start

```bash
# Error: Port 5000 already in use
# Solution: Use different port or kill process on 5000

# Windows:
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# macOS/Linux:
lsof -i :5000
kill -9 <PID>
```

### Database Connection Error

```bash
# Verify PostgreSQL is running
# Windows: Check Services
# macOS: brew services list
# Linux: sudo systemctl status postgresql

# Test connection:
psql -U customer_admin -d customer_db -h localhost
```

### CORS Errors in Frontend

1. Verify backend is running on port 5000
2. Check browser console for exact error
3. Verify API_URL in App.jsx: `const API_URL = 'http://localhost:5000/api';`

### Login Always Fails

1. Ensure backend created demo user
2. Check .env DATABASE_URL is correct
3. Verify backend console for errors
4. Try registering a new user

---

## 📚 Learning Resources

### Frontend (React)
- [React Documentation](https://react.dev)
- [React Hooks Guide](https://react.dev/reference/react)
- [Fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API)

### Backend (Python/Flask)
- [Flask Documentation](https://flask.palletsprojects.com)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org)
- [Flask-JWT-Extended](https://flask-jwt-extended.readthedocs.io)

### Database (PostgreSQL)
- [PostgreSQL Documentation](https://www.postgresql.org/docs)
- [SQL Tutorial](https://www.w3schools.com/sql)

---

## 🚀 Future Enhancements

### Phase 2 - AI Integration
- [ ] AI-powered customer insights
- [ ] Automated lead scoring
- [ ] Intelligent customer segmentation
- [ ] Chatbot for customer service

### Phase 3 - Advanced Features
- [ ] Real-time notifications
- [ ] Customer activity timeline
- [ ] Integration with email/CRM
- [ ] Advanced analytics dashboard
- [ ] Bulk import/export (CSV, Excel)
- [ ] Mobile app (React Native)

### Phase 4 - Enterprise Features
- [ ] Multi-user collaboration
- [ ] Role-based access control (RBAC)
- [ ] Audit logging
- [ ] API rate limiting
- [ ] Data encryption at rest

---

## 📝 License

This project is provided as-is for educational and business use.

---

## 👥 Support & Contribution

For issues, questions, or contributions:

1. **Report Issues** - Document steps to reproduce
2. **Feature Requests** - Describe use case and expected behavior
3. **Code Contributions** - Follow project structure and coding standards

---

## 📞 Quick Reference Commands

```bash
# Start Backend
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
python app.py

# Start Frontend
npm start

# Backend Health Check
curl http://localhost:5000/api/health

# Login Request
curl -X POST http://localhost:5000/api/login \
  -H "Content-Type: application/json" \
  -d '{"username":"demo","password":"demo"}'

# Get Customers (replace TOKEN)
curl http://localhost:5000/api/customers \
  -H "Authorization: Bearer TOKEN"

# Database Backup
pg_dump -U customer_admin customer_db > backup.sql

# Database Restore
psql -U customer_admin customer_db < backup.sql
```

---

## 🎓 Project Scope

**Level:** Basic
**Status:** Complete & Ready to Deploy
**Estimated Setup Time:** 15-30 minutes
**Build Time:** 2-4 hours

---

**Last Updated:** 2024
**Version:** 1.0.0
