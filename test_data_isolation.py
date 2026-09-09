import sys
import os
import secrets
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db, User, Customer, init_db

def run_data_isolation_tests():
    print("==========================================================")
    print("      RUNNING USER DATA ISOLATION & CLEAN DATA TESTS      ")
    print("==========================================================")
    
    with app.app_context():
        init_db()
    
    client = app.test_client()
    
    # Generate unique test users
    user_a_name = f"alice_{secrets.token_hex(4)}"
    user_a_email = f"{user_a_name}@corp.com"
    user_b_name = f"bob_{secrets.token_hex(4)}"
    user_b_email = f"{user_b_name}@corp.com"
    
    # ------------------------------------------------------------
    # STEP 1: Register User A and Login
    # ------------------------------------------------------------
    print(f"\n[1] Registering User A ({user_a_name})...")
    res = client.post('/api/register', json={
        'username': user_a_name,
        'email': user_a_email,
        'password': 'password_alice_123'
    })
    assert res.status_code == 201, f"Registration of User A failed: {res.data}"
    token_a = res.get_json()['token']
    headers_a = {'Authorization': f'Bearer {token_a}'}
    print("    [PASS] User A registered and authenticated.")

    # Verify User A starts with 0 customers
    res = client.get('/api/customers', headers=headers_a)
    assert res.status_code == 200
    custs_a_initial = res.get_json()['customers']
    assert len(custs_a_initial) == 0, f"Expected 0 initial customers for User A, got {len(custs_a_initial)}"
    print("    [PASS] User A starts with a completely clean customer list (0 records).")

    # ------------------------------------------------------------
    # STEP 2: User A creates records
    # ------------------------------------------------------------
    print("\n[2] User A creates 2 customer records...")
    res = client.post('/api/customers', json={
        'name': 'Alpha Corp Contact',
        'email': f'alpha_{secrets.token_hex(3)}@alpha.com',
        'phone': '+1-555-0100',
        'company': 'Alpha Corp',
        'address': '100 Alpha Way'
    }, headers=headers_a)
    assert res.status_code == 201
    cust_a1 = res.get_json()['customer']
    cust_a1_id = cust_a1['id']
    
    res = client.post('/api/customers', json={
        'name': 'Beta Systems Contact',
        'email': f'beta_{secrets.token_hex(3)}@beta.com',
        'phone': '+1-555-0200',
        'company': 'Beta Systems',
        'address': '200 Beta Blvd'
    }, headers=headers_a)
    assert res.status_code == 201
    cust_a2 = res.get_json()['customer']
    cust_a2_id = cust_a2['id']
    
    res = client.get('/api/customers', headers=headers_a)
    assert res.status_code == 200
    custs_a = res.get_json()['customers']
    assert len(custs_a) == 2, f"User A should have 2 customers, found {len(custs_a)}"
    print(f"    [PASS] User A created Customer A1 (ID {cust_a1_id}) and Customer A2 (ID {cust_a2_id}).")

    # ------------------------------------------------------------
    # STEP 3: Register User B and verify clean dataset
    # ------------------------------------------------------------
    print(f"\n[3] Registering User B ({user_b_name})...")
    res = client.post('/api/register', json={
        'username': user_b_name,
        'email': user_b_email,
        'password': 'password_bob_123'
    })
    assert res.status_code == 201
    token_b = res.get_json()['token']
    headers_b = {'Authorization': f'Bearer {token_b}'}
    print("    [PASS] User B registered and authenticated.")

    # Critical check: User B customer list MUST be empty (User A's 2 customers must NOT be visible)
    res = client.get('/api/customers', headers=headers_b)
    assert res.status_code == 200
    custs_b = res.get_json()['customers']
    assert len(custs_b) == 0, f"Data leakage! User B sees {len(custs_b)} records from other users!"
    print("    [PASS] User B starts with 0 customers! No data leaked from User A.")

    # ------------------------------------------------------------
    # STEP 4: User B creates their own record
    # ------------------------------------------------------------
    print("\n[4] User B creates Customer B1...")
    res = client.post('/api/customers', json={
        'name': 'Gamma Enterprises Contact',
        'email': f'gamma_{secrets.token_hex(3)}@gamma.com',
        'phone': '+1-555-0300',
        'company': 'Gamma Enterprises',
        'address': '300 Gamma St'
    }, headers=headers_b)
    assert res.status_code == 201
    cust_b1 = res.get_json()['customer']
    cust_b1_id = cust_b1['id']
    
    res = client.get('/api/customers', headers=headers_b)
    assert res.status_code == 200
    custs_b = res.get_json()['customers']
    assert len(custs_b) == 1
    assert custs_b[0]['id'] == cust_b1_id
    print(f"    [PASS] User B only sees their own 1 customer (ID {cust_b1_id}).")

    # ------------------------------------------------------------
    # STEP 5: Cross-User Security & Attack Vector Validation
    # ------------------------------------------------------------
    print("\n[5] Testing Cross-User Security Blockades...")
    
    # 5.1 Direct ID Access: User B attempts GET /api/customers/<User A1 ID>
    res = client.get(f'/api/customers/{cust_a1_id}', headers=headers_b)
    assert res.status_code == 404, f"Security vulnerability! User B was able to view User A's customer: {res.status_code}"
    print("    [PASS] Direct GET by ID cross-user attempt blocked (404 Not Found).")

    # 5.2 Direct ID Mutation: User B attempts PUT /api/customers/<User A1 ID>
    res = client.put(f'/api/customers/{cust_a1_id}', json={
        'name': 'HACKED BY BOB',
        'company': 'Malicious Inc'
    }, headers=headers_b)
    assert res.status_code == 404, f"Security vulnerability! User B was able to modify User A's customer: {res.status_code}"
    print("    [PASS] Direct PUT update cross-user attempt blocked (404 Not Found).")

    # 5.3 Direct ID Deletion: User B attempts DELETE /api/customers/<User A1 ID>
    res = client.delete(f'/api/customers/{cust_a1_id}', headers=headers_b)
    assert res.status_code == 404, f"Security vulnerability! User B was able to delete User A's customer: {res.status_code}"
    print("    [PASS] Direct DELETE cross-user attempt blocked (404 Not Found).")

    # 5.4 Search Isolation: User B searches for User A's customer name
    res = client.get(f'/api/customers/search?q=Alpha', headers=headers_b)
    assert res.status_code == 200
    assert len(res.get_json()['customers']) == 0, "Search query leaked User A's record to User B!"
    print("    [PASS] Customer search is strictly scoped to authenticated user.")

    # 5.5 AI Email Drafter: User B tries to draft email for User A customer ID
    res = client.post('/api/ai/draft-email', json={
        'customer_id': cust_a1_id,
        'goal': 'check_in'
    }, headers=headers_b)
    assert res.status_code == 404, f"AI email drafter cross-user leak! Status: {res.status_code}"
    print("    [PASS] AI Email Drafter blocks cross-user customer access (404 Not Found).")

    # ------------------------------------------------------------
    # STEP 6: Verify User A data integrity
    # ------------------------------------------------------------
    print("\n[6] Verifying User A records remained untouched...")
    res = client.get(f'/api/customers/{cust_a1_id}', headers=headers_a)
    assert res.status_code == 200
    a1_data = res.get_json()
    assert a1_data['name'] == 'Alpha Corp Contact'
    assert a1_data['company'] == 'Alpha Corp'
    
    res = client.get('/api/customers', headers=headers_a)
    assert res.status_code == 200
    assert len(res.get_json()['customers']) == 2
    print("    [PASS] User A's dataset is 100% intact and unaffected by unauthorized attempts.")

    print("\n==========================================================")
    print("     ALL USER DATA ISOLATION TESTS PASSED SUCCESSFULLY!    ")
    print("==========================================================")

if __name__ == '__main__':
    run_data_isolation_tests()
