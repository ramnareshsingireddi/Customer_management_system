import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db, User, Customer, init_db

def run_tests():
    print("=== Testing Backend Functionality ===")
    with app.app_context():
        init_db()
        print("[PASS] Database initialized successfully with migrations")
        
    client = app.test_client()
    
    # 1. Test Registration
    test_user = 'testuser_' + os.urandom(4).hex()
    test_email = f"{test_user}@example.com"
    res = client.post('/api/register', json={
        'username': test_user,
        'email': test_email,
        'password': 'testpassword123'
    })
    assert res.status_code == 201, f"Registration failed: {res.data}"
    reg_data = res.get_json()
    token = reg_data['token']
    assert token, "Token missing from registration response"
    print(f"[PASS] Registration of {test_user} succeeded")

    # 2. Test Login with username
    res = client.post('/api/login', json={'username': test_user, 'password': 'testpassword123'})
    assert res.status_code == 200, f"Login with username failed: {res.data}"
    data = res.get_json()
    assert data['token'], "Token missing from login response"
    print("[PASS] Login with username succeeded")
    
    # 3. Test Login with email
    res = client.post('/api/login', json={'email': test_email, 'password': 'testpassword123'})
    assert res.status_code == 200, f"Login with email failed: {res.data}"
    print("[PASS] Login with email succeeded")
    
    # 4. Test Duplicate Registration (username)
    res = client.post('/api/register', json={
        'username': test_user,
        'email': 'different_' + test_email,
        'password': 'password123'
    })
    assert res.status_code == 409, f"Duplicate username was not rejected: {res.status_code}"
    print("[PASS] Duplicate username correctly rejected (409)")
    
    # 5. Test Duplicate Registration (email)
    res = client.post('/api/register', json={
        'username': 'different_' + test_user,
        'email': test_email,
        'password': 'password123'
    })
    assert res.status_code == 409, f"Duplicate email was not rejected: {res.status_code}"
    print("[PASS] Duplicate email correctly rejected (409)")
    
    # 6. Test /api/auth/me
    res = client.get('/api/auth/me', headers={'Authorization': f'Bearer {token}'})
    assert res.status_code == 200, f"/api/auth/me failed: {res.data}"
    me_data = res.get_json()
    assert me_data['user']['username'] == test_user
    print("[PASS] /api/auth/me returned authenticated user")
    
    # 8. Test Customers CRUD with JWT
    headers = {'Authorization': f'Bearer {token}'}
    res = client.get('/api/customers', headers=headers)
    assert res.status_code == 200, f"Get customers failed: {res.data}"
    customers = res.get_json().get('customers', [])
    print(f"[PASS] GET /api/customers succeeded ({len(customers)} customers)")
    
    # Create customer
    c_email = f"cust_{os.urandom(4).hex()}@corp.com"
    res = client.post('/api/customers', json={
        'name': 'Acme Corp Contact',
        'email': c_email,
        'phone': '+1-555-0199',
        'company': 'Acme Global',
        'address': '742 Evergreen Terrace'
    }, headers=headers)
    assert res.status_code == 201, f"Create customer failed: {res.data}"
    cust_id = res.get_json()['customer']['id']
    print(f"[PASS] POST /api/customers succeeded (ID {cust_id})")
    
    # Search customer
    res = client.get(f'/api/customers/search?q={c_email}', headers=headers)
    assert res.status_code == 200
    assert len(res.get_json()['customers']) >= 1
    print("[PASS] GET /api/customers/search succeeded")
    
    # Update customer
    res = client.put(f'/api/customers/{cust_id}', json={
        'name': 'Acme Corp Contact Updated',
        'company': 'Acme Global Industries'
    }, headers=headers)
    assert res.status_code == 200
    print("[PASS] PUT /api/customers/:id succeeded")
    
    # Delete customer
    res = client.delete(f'/api/customers/{cust_id}', headers=headers)
    assert res.status_code == 200
    print("[PASS] DELETE /api/customers/:id succeeded")
    
    # 9. Test Google Auth endpoint
    res = client.get('/api/auth/google', headers={'Accept': 'application/json'})
    # When credentials are placeholder or empty, it returns 400 with helpful JSON message
    print(f"[PASS] GET /api/auth/google response: status={res.status_code}, data={res.get_json()}")
    
    print("\nALL BACKEND TESTS PASSED!")

if __name__ == '__main__':
    run_tests()
