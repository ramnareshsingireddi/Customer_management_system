# Quick Reference - Customer Management Application

Fast lookup guide for common tasks and commands.

## 🚀 Quick Start (5 minutes)

```bash
# Terminal 1 - Backend
python -m venv venv
source venv/bin/activate  # or: venv\Scripts\activate
pip install -r requirements.txt
python app.py

# Terminal 2 - Frontend
npx create-react-app customer-app
cd customer-app
npm install axios
npm start

# Default login: demo / demo
```

---

## 📂 Project Files

| File | Purpose |
|------|---------|
| `app.py` | Flask backend server |
| `requirements.txt` | Python dependencies |
| `.env` | Environment variables |
| `customer-app/` | React frontend |
| `README.md` | Project overview |
| `SETUP_GUIDE.md` | Detailed setup |
| `API_REFERENCE.md` | API documentation |
| `DEPLOYMENT_GUIDE.md` | Production deployment |

---

## 🔌 API Endpoints Quick List

```
POST   /api/login              # Login
POST   /api/register           # Register
GET    /api/customers          # List all
GET    /api/customers/:id      # Get one
POST   /api/customers          # Create
PUT    /api/customers/:id      # Update
DELETE /api/customers/:id      # Delete
GET    /api/customers/search   # Search
GET    /api/health             # Health check
```

---

## 💻 Common Commands

### Backend

```bash
# Install dependencies
pip install -r requirements.txt

# Activate virtual environment
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows

# Run server
python app.py

# Run with specific port
python -c "from app import app; app.run(port=5001)"

# Database reset
python -c "from app import db, app; app.app_context().push(); db.drop_all(); db.create_all()"
```

### Frontend

```bash
# Create new React app
npx create-react-app customer-app

# Install package
npm install package-name

# Start development server
npm start

# Build for production
npm run build

# Run tests
npm test
```

### Database

```bash
# Connect to database
psql -U customer_admin -d customer_db

# Backup database
pg_dump -U customer_admin customer_db > backup.sql

# Restore database
psql -U customer_admin customer_db < backup.sql

# Common SQL queries
SELECT * FROM customers;
SELECT * FROM users;
DELETE FROM customers WHERE id = 1;
UPDATE customers SET name='New Name' WHERE id=1;
```

---

## 🔐 Authentication

### Login Flow

```javascript
// 1. Get token
const response = await fetch('http://localhost:5000/api/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ username: 'demo', password: 'demo' })
});
const { token } = await response.json();
localStorage.setItem('token', token);

// 2. Use token in requests
fetch('http://localhost:5000/api/customers', {
  headers: { 'Authorization': `Bearer ${token}` }
});
```

---

## 📝 HTTP Methods

```
GET     - Retrieve data
POST    - Create new resource
PUT     - Update existing resource
DELETE  - Remove resource
PATCH   - Partial update
```

---

## 📊 Response Status Codes

```
200 - OK (successful request)
201 - Created (resource created)
400 - Bad Request (invalid data)
401 - Unauthorized (no auth)
404 - Not Found (resource doesn't exist)
409 - Conflict (duplicate)
500 - Server Error
```

---

## 🗄️ Database Tables

### Users Table
```sql
id          INTEGER PRIMARY KEY
username    VARCHAR(80) UNIQUE
password    VARCHAR(255)
created_at  TIMESTAMP
```

### Customers Table
```sql
id          INTEGER PRIMARY KEY
name        VARCHAR(120)
email       VARCHAR(120) UNIQUE
phone       VARCHAR(20)
company     VARCHAR(120)
address     TEXT
created_at  TIMESTAMP
updated_at  TIMESTAMP
```

---

## 🌐 Environment Variables

```env
DATABASE_URL=postgresql://user:pass@host:5432/db
JWT_SECRET_KEY=your-secret-key
FLASK_ENV=development
FLASK_DEBUG=True
CORS_ORIGINS=http://localhost:3000
```

---

## 📋 Customer Data Structure

```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+1-234-567-8900",
  "company": "Tech Corp",
  "address": "123 Main St",
  "created_at": "2024-01-15T10:00:00",
  "updated_at": "2024-01-15T10:00:00"
}
```

---

## 🧪 Testing with cURL

```bash
# Login
curl -X POST http://localhost:5000/api/login \
  -H "Content-Type: application/json" \
  -d '{"username":"demo","password":"demo"}'

# Get customers (replace TOKEN)
curl http://localhost:5000/api/customers \
  -H "Authorization: Bearer TOKEN"

# Create customer
curl -X POST http://localhost:5000/api/customers \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer TOKEN" \
  -d '{"name":"John","email":"john@ex.com"}'

# Update customer
curl -X PUT http://localhost:5000/api/customers/1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer TOKEN" \
  -d '{"name":"Updated Name"}'

# Delete customer
curl -X DELETE http://localhost:5000/api/customers/1 \
  -H "Authorization: Bearer TOKEN"

# Search
curl "http://localhost:5000/api/customers/search?q=john" \
  -H "Authorization: Bearer TOKEN"
```

---

## 🔍 Debugging Tips

### Backend Debug

```python
# Add debug print
print(f"Debug: {variable}")

# Check Flask logs
# Should appear in terminal running 'python app.py'

# Database query debug
app.logger.info("Query executed")
```

### Frontend Debug

```javascript
// Console logging
console.log('Debug:', variable);

// React hooks debug
import React from 'react';
React.useLayoutEffect(() => {
  console.log('Component mounted');
}, []);

// Network tab in DevTools (F12)
```

### Database Debug

```sql
-- Check customer count
SELECT COUNT(*) FROM customers;

-- List all customers
SELECT * FROM customers;

-- Check recent entries
SELECT * FROM customers ORDER BY created_at DESC LIMIT 5;

-- Find duplicate emails
SELECT email, COUNT(*) FROM customers GROUP BY email HAVING COUNT(*) > 1;
```

---

## 🚨 Common Issues & Quick Fixes

| Issue | Quick Fix |
|-------|-----------|
| Port already in use | Kill process: `lsof -i :5000` → `kill -9 PID` |
| Module not found | Install: `pip install module_name` |
| CORS error | Check backend CORS_ORIGINS env var |
| Database error | Verify connection: `psql -U customer_admin customer_db` |
| Frontend blank | Check browser console (F12) for errors |
| Token expired | Login again to get new token |

---

## 📱 Frontend Component Structure

```javascript
// App.jsx
App (main)
├── LoginPage (login form)
└── CustomerList (logged in)
    ├── Search bar
    ├── Add button → CustomerForm
    ├── Table
    │   ├── Edit button → CustomerForm
    │   └── Delete button
    └── No customers message
```

---

## 🎨 Styling Classes

```css
.login-container      /* Login page wrapper */
.login-box           /* Login form box */
.app-container       /* Main app wrapper */
.app-header          /* Top header */
.customer-list-container  /* List wrapper */
.customers-table     /* Data table */
.btn-primary         /* Main button */
.btn-secondary       /* Secondary button */
.error-message       /* Error alert */
.loading             /* Loading state */
```

---

## 🔧 Configuration Quick Guide

### Flask Configuration

```python
# app.py
app.config['DATABASE_URL'] = '...'
app.config['JWT_SECRET_KEY'] = '...'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)
```

### React Configuration

```javascript
// App.jsx
const API_URL = 'http://localhost:5000/api';
```

---

## 📦 Dependency Versions

### Backend
```
Flask==3.0.0
PostgreSQL==12+
Python==3.8+
```

### Frontend
```
React==18.2.0
Node.js==14+
npm==6+
```

---

## 🌍 Ports Reference

| Service | Port | URL |
|---------|------|-----|
| React Frontend | 3000 | http://localhost:3000 |
| Flask Backend | 5000 | http://localhost:5000 |
| PostgreSQL | 5432 | localhost:5432 |
| pgAdmin (optional) | 5050 | http://localhost:5050 |

---

## 💾 Database Maintenance

```sql
-- Optimize database
VACUUM ANALYZE;

-- Check table sizes
SELECT schemaname, tablename, pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- Reset sequences
ALTER SEQUENCE customers_id_seq RESTART WITH 1;

-- Drop and recreate tables
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS users;
-- Then run: python -c "from app import db; db.create_all()"
```

---

## 🚀 Deploy Commands

```bash
# Heroku
heroku create app-name
heroku config:set JWT_SECRET_KEY="key"
git push heroku main

# DigitalOcean
doctl apps create --spec app.yaml

# Docker
docker-compose up -d
docker-compose down

# Stop all
docker stop $(docker ps -aq)
```

---

## 📞 Support Resources

- **Backend Issues** → Check `app.py` logs
- **Database Issues** → Run SQL queries in pgAdmin
- **Frontend Issues** → Check browser console (F12)
- **API Issues** → Check `API_REFERENCE.md`
- **Deployment** → See `DEPLOYMENT_GUIDE.md`

---

## 📋 Checklist Templates

### Pre-Launch
- [ ] Backend running on 5000
- [ ] Frontend running on 3000
- [ ] Database connected
- [ ] Demo user created
- [ ] Sample data loaded
- [ ] Login working
- [ ] CRUD operations working

### Pre-Production
- [ ] Security audit passed
- [ ] All tests passing
- [ ] Documentation updated
- [ ] Backups configured
- [ ] Monitoring enabled
- [ ] Error tracking set up
- [ ] Performance optimized

---

**Quick Tip:** Bookmark this page for fast reference during development! 🚀
