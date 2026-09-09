# Customer Management Application - Setup Guide

A complete guide to set up and run the Customer Management Web Application with React frontend and Python Flask backend.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Database Setup](#database-setup)
3. [Backend Setup](#backend-setup)
4. [Frontend Setup](#frontend-setup)
5. [Running the Application](#running-the-application)
6. [API Documentation](#api-documentation)
7. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Software
- **Node.js** (v14+) - Download from [nodejs.org](https://nodejs.org)
- **Python** (v3.8+) - Download from [python.org](https://www.python.org)
- **PostgreSQL** (v12+) - Download from [postgresql.org](https://www.postgresql.org)
- **Git** (optional) - For version control

### Verify Installation
```bash
node --version      # Should be v14 or higher
npm --version       # Should be v6 or higher
python --version    # Should be 3.8 or higher
pip --version       # Python package manager
psql --version      # PostgreSQL client
```

---

## Database Setup

### Step 1: Create PostgreSQL Database

**On Windows (Command Prompt):**
```bash
psql -U postgres
```

**On macOS/Linux (Terminal):**
```bash
sudo -u postgres psql
```

### Step 2: Create Database and User

Run these SQL commands in the PostgreSQL prompt:

```sql
-- Create database
CREATE DATABASE customer_db;

-- Create user (optional - if using custom credentials)
CREATE USER customer_admin WITH PASSWORD 'secure_password';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE customer_db TO customer_admin;

-- Connect to the database
\c customer_db

-- Grant schema privileges
GRANT ALL ON SCHEMA public TO customer_admin;

-- Exit
\q
```

### Step 3: Verify Database Connection

```bash
psql -U customer_admin -d customer_db -h localhost
```

If successful, you'll see the PostgreSQL prompt. Type `\q` to exit.

### Database Schema (Auto-created by Flask)

The Flask application will automatically create these tables:

```sql
-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Customers table
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

## Backend Setup

### Step 1: Create Project Directory

```bash
mkdir customer-management-app
cd customer-management-app
```

### Step 2: Create Python Virtual Environment

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` prefix in your terminal.

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

Copy the `.env.example` file to `.env`:

```bash
cp .env.example .env
```

Edit `.env` with your database credentials:

```
DATABASE_URL=postgresql://customer_admin:secure_password@localhost:5432/customer_db
JWT_SECRET_KEY=your-super-secret-key-change-in-production-12345
FLASK_ENV=development
FLASK_DEBUG=True
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

### Step 5: Initialize Database and Run Backend

```bash
python app.py
```

**Expected Output:**
```
Demo user created: username=demo, password=demo
Sample customers created
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

The backend is now running on `http://localhost:5000`

### Verify Backend is Running

```bash
curl http://localhost:5000/api/health
```

Should return: `{"status":"API is running"}`

---

## Frontend Setup

### Step 1: Create React Application

Open a new terminal (keep backend running) and run:

```bash
npx create-react-app customer-app
cd customer-app
```

### Step 2: Copy Frontend Files

Replace the contents of the following files:

**`src/App.jsx`** - Copy the React component code
**`src/App.css`** - Copy the CSS styling

### Step 3: Install Additional Dependencies (if needed)

```bash
npm install axios
```

### Step 4: Configure API Endpoint

In `src/App.jsx`, verify the API URL is set correctly:

```javascript
const API_URL = 'http://localhost:5000/api';
```

### Step 5: Start Frontend Development Server

```bash
npm start
```

The application will open automatically at `http://localhost:3003`

---

## Running the Application

### Quick Start (Terminal 1 - Backend)

```bash
# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Run Flask server
python app.py
```

### Quick Start (Terminal 2 - Frontend)

```bash
cd customer-app
npm start
```

### Verify Everything is Running

1. Backend: `http://localhost:5000/api/health` - Returns `{"status":"API is running"}`
2. Frontend: `http://localhost:3003` - Shows login page
3. Database: Connected and populated with demo user and sample customers

---

## Login Credentials

**Default Demo Account:**
- Username: `demo`
- Password: `demo`

---

## API Documentation

### Base URL
`http://localhost:5000/api`

### Authentication
All endpoints (except login and register) require JWT token in headers:
```
Authorization: Bearer <token>
```

### Endpoints

#### Authentication

**POST /login**
```bash
curl -X POST http://localhost:5000/api/login \
  -H "Content-Type: application/json" \
  -d '{"username":"demo","password":"demo"}'
```
Response: `{"token":"eyJ...", "user":{...}}`

**POST /register**
```bash
curl -X POST http://localhost:5000/api/register \
  -H "Content-Type: application/json" \
  -d '{"username":"newuser","password":"password"}'
```

#### Customers

**GET /customers** (List all)
```bash
curl -X GET http://localhost:5000/api/customers \
  -H "Authorization: Bearer <token>"
```

**GET /customers/:id** (Get by ID)
```bash
curl -X GET http://localhost:5000/api/customers/1 \
  -H "Authorization: Bearer <token>"
```

**POST /customers** (Create)
```bash
curl -X POST http://localhost:5000/api/customers \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "name":"John Doe",
    "email":"john@example.com",
    "phone":"+1-234-567-8900",
    "company":"Tech Corp",
    "address":"123 Main St"
  }'
```

**PUT /customers/:id** (Update)
```bash
curl -X PUT http://localhost:5000/api/customers/1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "name":"Updated Name",
    "email":"updated@example.com"
  }'
```

**DELETE /customers/:id** (Delete)
```bash
curl -X DELETE http://localhost:5000/api/customers/1 \
  -H "Authorization: Bearer <token>"
```

**GET /customers/search** (Search)
```bash
curl -X GET "http://localhost:5000/api/customers/search?q=john" \
  -H "Authorization: Bearer <token>"
```

---

## Project Structure

```
customer-management-app/
├── app.py                      # Flask backend
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (local)
├── .env.example               # Environment template
├── SETUP_GUIDE.md             # This file
│
└── customer-app/              # React frontend (created by npx)
    ├── src/
    │   ├── App.jsx            # Main React component
    │   ├── App.css            # Styling
    │   ├── index.js           # Entry point
    │   └── ...
    ├── package.json           # Frontend dependencies
    └── ...
```

---

## Troubleshooting

### Backend Issues

**Issue: `ModuleNotFoundError: No module named 'flask'`**
- Solution: Activate virtual environment and run `pip install -r requirements.txt`

**Issue: `psycopg2` installation fails**
- Solution: Install PostgreSQL development libraries
  - Windows: Use psycopg2-binary
  - macOS: `brew install postgresql`
  - Linux: `sudo apt-get install libpq-dev`

**Issue: `Connection refused` when connecting to database**
- Verify PostgreSQL is running
- Check database URL in `.env`
- Ensure database exists: `createdb customer_db`

**Issue: `JWT_SECRET_KEY` not set**
- Update `.env` with a strong secret key
- Restart Flask server

### Frontend Issues

**Issue: CORS errors in browser console**
- Verify backend is running on port 5000
- Check `CORS_ORIGINS` in backend `.env`
- Ensure frontend is on `http://localhost:3000`

**Issue: `Cannot find module 'axios'`**
- Run `npm install axios` in the frontend directory

**Issue: Blank page or "Connection error"**
- Verify backend health: `curl http://localhost:5000/api/health`
- Check browser console for errors
- Ensure `API_URL` in App.jsx points to correct backend

### Database Issues

**Issue: `FATAL: role "postgres" does not exist`**
- On Windows: Use SQL Server Management or pgAdmin
- On macOS/Linux: Use `sudo -u postgres psql`

**Issue: Permission denied for schema public**
- Run: `GRANT ALL ON SCHEMA public TO customer_admin;`

---

## Production Deployment

### Security Checklist
- [ ] Change `JWT_SECRET_KEY` to a strong random value
- [ ] Update `DATABASE_URL` with secure credentials
- [ ] Set `FLASK_ENV=production`
- [ ] Set `FLASK_DEBUG=False`
- [ ] Use HTTPS for all connections
- [ ] Add rate limiting and request validation
- [ ] Implement proper error handling
- [ ] Add logging and monitoring

### Deployment Options
1. **Heroku** - Easy deployment with add-ons for PostgreSQL
2. **AWS** - EC2 for backend, RDS for database
3. **DigitalOcean** - Droplets for backend, Managed Database
4. **Railway** - Simple one-click deployment
5. **Vercel** - For React frontend, paired with any backend

---

## Additional Features to Add

- [ ] Email verification
- [ ] Password reset functionality
- [ ] Customer notes and activity tracking
- [ ] Bulk import/export (CSV)
- [ ] Customer segmentation and tags
- [ ] Call history and interaction log
- [ ] Email integration
- [ ] SMS notifications
- [ ] Analytics and reporting dashboard
- [ ] Mobile app (React Native)

---

## Support

For issues or questions:
1. Check the Troubleshooting section above
2. Review API Documentation
3. Check application logs
4. Verify environment variables
5. Ensure all services are running (PostgreSQL, Backend, Frontend)

---

## License

This project is provided as-is for educational purposes.
