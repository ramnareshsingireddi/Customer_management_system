# Customer Management API Reference

Complete API documentation for the Customer Management Application.

## Base URL

```
http://localhost:5000/api
```

## Authentication

All endpoints except `/login` and `/register` require JWT authentication.

### Including JWT Token

Add the token to the Authorization header:

```
Authorization: Bearer <your_jwt_token>
```

### Example with cURL

```bash
curl -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..." \
  http://localhost:5000/api/customers
```

### Example with JavaScript/Fetch

```javascript
fetch('http://localhost:5000/api/customers', {
  method: 'GET',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  }
})
```

---

## 🔐 Authentication Endpoints

### POST /login

Authenticate user and receive JWT token.

**Request:**
```json
{
  "username": "demo",
  "password": "demo"
}
```

**Response (200 OK):**
```json
{
  "message": "Login successful",
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user": {
    "id": 1,
    "username": "demo",
    "created_at": "2024-01-15T10:30:00"
  }
}
```

**Error (401 Unauthorized):**
```json
{
  "message": "Invalid username or password"
}
```

**cURL Example:**
```bash
curl -X POST http://localhost:5000/api/login \
  -H "Content-Type: application/json" \
  -d '{"username":"demo","password":"demo"}'
```

---

### POST /register

Register a new user account.

**Request:**
```json
{
  "username": "newuser",
  "password": "securepassword"
}
```

**Response (201 Created):**
```json
{
  "message": "Registration successful",
  "user": {
    "id": 2,
    "username": "newuser",
    "created_at": "2024-01-15T10:35:00"
  }
}
```

**Error (409 Conflict):**
```json
{
  "message": "Username already exists"
}
```

**cURL Example:**
```bash
curl -X POST http://localhost:5000/api/register \
  -H "Content-Type: application/json" \
  -d '{"username":"newuser","password":"securepassword"}'
```

---

## 👥 Customer Endpoints

### GET /customers

Retrieve all customers.

**Request:**
```
GET /customers
Authorization: Bearer <token>
```

**Response (200 OK):**
```json
{
  "customers": [
    {
      "id": 1,
      "name": "John Doe",
      "email": "john@example.com",
      "phone": "+1-234-567-8900",
      "company": "Tech Corp",
      "address": "123 Main St, New York, NY",
      "created_at": "2024-01-15T10:00:00",
      "updated_at": "2024-01-15T10:00:00"
    },
    {
      "id": 2,
      "name": "Jane Smith",
      "email": "jane@example.com",
      "phone": "+1-234-567-8901",
      "company": "Digital Solutions",
      "address": "456 Oak Ave, Los Angeles, CA",
      "created_at": "2024-01-15T10:05:00",
      "updated_at": "2024-01-15T10:05:00"
    }
  ]
}
```

**cURL Example:**
```bash
curl http://localhost:5000/api/customers \
  -H "Authorization: Bearer <token>"
```

---

### GET /customers/:id

Retrieve a specific customer by ID.

**Request:**
```
GET /customers/1
Authorization: Bearer <token>
```

**Response (200 OK):**
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+1-234-567-8900",
  "company": "Tech Corp",
  "address": "123 Main St, New York, NY",
  "created_at": "2024-01-15T10:00:00",
  "updated_at": "2024-01-15T10:00:00"
}
```

**Error (404 Not Found):**
```json
{
  "message": "Customer not found"
}
```

**cURL Example:**
```bash
curl http://localhost:5000/api/customers/1 \
  -H "Authorization: Bearer <token>"
```

---

### POST /customers

Create a new customer.

**Request:**
```json
{
  "name": "Robert Wilson",
  "email": "robert@example.com",
  "phone": "+1-234-567-8903",
  "company": "Innovation Labs",
  "address": "789 Pine Rd, Chicago, IL"
}
```

**Response (201 Created):**
```json
{
  "message": "Customer created successfully",
  "customer": {
    "id": 4,
    "name": "Robert Wilson",
    "email": "robert@example.com",
    "phone": "+1-234-567-8903",
    "company": "Innovation Labs",
    "address": "789 Pine Rd, Chicago, IL",
    "created_at": "2024-01-15T11:00:00",
    "updated_at": "2024-01-15T11:00:00"
  }
}
```

**Error (409 Conflict - Email exists):**
```json
{
  "message": "Email already exists"
}
```

**Error (400 Bad Request):**
```json
{
  "message": "Name and email are required"
}
```

**cURL Example:**
```bash
curl -X POST http://localhost:5000/api/customers \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "name": "Robert Wilson",
    "email": "robert@example.com",
    "phone": "+1-234-567-8903",
    "company": "Innovation Labs",
    "address": "789 Pine Rd, Chicago, IL"
  }'
```

---

### PUT /customers/:id

Update an existing customer.

**Request:**
```json
{
  "name": "John Doe Updated",
  "email": "john.updated@example.com",
  "phone": "+1-234-567-9999",
  "company": "Tech Corp Updated",
  "address": "999 Main St, New York, NY"
}
```

**Note:** All fields are optional. Only include fields you want to update.

**Response (200 OK):**
```json
{
  "message": "Customer updated successfully",
  "customer": {
    "id": 1,
    "name": "John Doe Updated",
    "email": "john.updated@example.com",
    "phone": "+1-234-567-9999",
    "company": "Tech Corp Updated",
    "address": "999 Main St, New York, NY",
    "created_at": "2024-01-15T10:00:00",
    "updated_at": "2024-01-15T11:15:00"
  }
}
```

**Error (404 Not Found):**
```json
{
  "message": "Customer not found"
}
```

**Error (409 Conflict):**
```json
{
  "message": "Email already exists"
}
```

**cURL Example:**
```bash
curl -X PUT http://localhost:5000/api/customers/1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "name": "John Doe Updated",
    "phone": "+1-234-567-9999"
  }'
```

---

### DELETE /customers/:id

Delete a customer.

**Request:**
```
DELETE /customers/1
Authorization: Bearer <token>
```

**Response (200 OK):**
```json
{
  "message": "Customer deleted successfully"
}
```

**Error (404 Not Found):**
```json
{
  "message": "Customer not found"
}
```

**cURL Example:**
```bash
curl -X DELETE http://localhost:5000/api/customers/1 \
  -H "Authorization: Bearer <token>"
```

---

### GET /customers/search

Search customers by name or email.

**Request:**
```
GET /customers/search?q=john
Authorization: Bearer <token>
```

**Query Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `q` | string | Yes | Search query (name or email) |

**Response (200 OK):**
```json
{
  "customers": [
    {
      "id": 1,
      "name": "John Doe",
      "email": "john@example.com",
      "phone": "+1-234-567-8900",
      "company": "Tech Corp",
      "address": "123 Main St, New York, NY",
      "created_at": "2024-01-15T10:00:00",
      "updated_at": "2024-01-15T10:00:00"
    }
  ]
}
```

**cURL Example:**
```bash
# Search by name
curl "http://localhost:5000/api/customers/search?q=john" \
  -H "Authorization: Bearer <token>"

# Search by email
curl "http://localhost:5000/api/customers/search?q=john@example.com" \
  -H "Authorization: Bearer <token>"
```

---

## ✅ Health Check Endpoint

### GET /health

Check if API is running.

**Request:**
```
GET /health
```

**Response (200 OK):**
```json
{
  "status": "API is running"
}
```

**No authentication required**

**cURL Example:**
```bash
curl http://localhost:5000/api/health
```

---

## Response Status Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Request successful |
| 201 | Created | Resource successfully created |
| 400 | Bad Request | Invalid request data |
| 401 | Unauthorized | Invalid or missing authentication |
| 404 | Not Found | Resource not found |
| 409 | Conflict | Resource already exists (email conflict) |
| 500 | Internal Server Error | Server error |

---

## Common Error Messages

| Error | Cause | Solution |
|-------|-------|----------|
| `Missing username or password` | Required field not provided | Include both username and password |
| `Invalid username or password` | Wrong credentials | Check username and password |
| `Username already exists` | Username taken during registration | Use different username |
| `Name and email are required` | Missing required fields | Provide both name and email |
| `Email already exists` | Email already in use | Use different email address |
| `Customer not found` | Invalid customer ID | Check customer ID |
| `Unauthorized` | Missing/invalid token | Login again to get new token |

---

## Request/Response Examples

### Complete Login Flow

```bash
# 1. Login
TOKEN=$(curl -s -X POST http://localhost:5000/api/login \
  -H "Content-Type: application/json" \
  -d '{"username":"demo","password":"demo"}' | jq -r '.token')

# 2. Create Customer
curl -X POST http://localhost:5000/api/customers \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "name": "Alice Johnson",
    "email": "alice@example.com",
    "phone": "+1-555-123-4567",
    "company": "Data Analytics Inc",
    "address": "321 Elm St, Boston, MA"
  }'

# 3. Get All Customers
curl http://localhost:5000/api/customers \
  -H "Authorization: Bearer $TOKEN"

# 4. Search Customers
curl "http://localhost:5000/api/customers/search?q=alice" \
  -H "Authorization: Bearer $TOKEN"

# 5. Update Customer
curl -X PUT http://localhost:5000/api/customers/4 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "phone": "+1-555-999-9999"
  }'

# 6. Delete Customer
curl -X DELETE http://localhost:5000/api/customers/4 \
  -H "Authorization: Bearer $TOKEN"
```

---

## Rate Limiting

Currently, there is no rate limiting implemented. For production, consider implementing:
- Request rate limiting per user
- IP-based throttling
- Daily request quotas

---

## API Versioning

Current API Version: **v1**
Base URL: `http://localhost:5000/api`

Future: `/api/v2`, `/api/v3`, etc.

---

## Pagination (Future Enhancement)

Planned for future versions:
```
GET /customers?page=1&limit=20
```

---

## Webhooks (Future Enhancement)

Planned features:
- Customer created webhook
- Customer updated webhook
- Customer deleted webhook

---

## Support

For API issues or questions:
1. Check this reference documentation
2. Review error messages carefully
3. Ensure authentication token is valid
4. Verify all required fields are provided
5. Check application logs for detailed errors
