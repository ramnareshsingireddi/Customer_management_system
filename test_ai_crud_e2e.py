import sys
import os
import json
import urllib.request

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def run_e2e_ai_crud_test():
    print("=== Testing End-to-End AI CRUD Operations via /api/ai/chat ===")
    
    # 1. Register and Login dynamic user to get token
    uname = f"ai_tester_{os.urandom(3).hex()}"
    reg_data = json.dumps({"username": uname, "email": f"{uname}@example.com", "password": "password123"}).encode('utf-8')
    req = urllib.request.Request(
        "http://localhost:5000/api/register",
        data=reg_data,
        headers={"Content-Type": "application/json"}
    )
    res = json.loads(urllib.request.urlopen(req).read().decode('utf-8'))
    token = res['token']
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    print(f"[PASS] Successfully registered & authenticated test user '{uname}' with JWT")
    
    def send_ai_chat(message):
        payload = json.dumps({"message": message}).encode('utf-8')
        r = urllib.request.Request("http://localhost:5000/api/ai/chat", data=payload, headers=headers)
        return json.loads(urllib.request.urlopen(r).read().decode('utf-8'))
    
    # 2. Test CREATE via AI
    print("\n--- Testing AI CREATE Customer ---")
    uid = os.urandom(3).hex()
    test_name = f"Diana Prince {uid}"
    test_email = f"diana_{uid}@themyscira.io"
    create_prompt = f"Add customer named {test_name}, email {test_email}, company Amazonian Defense, phone +1-555-0188"
    print(f"User Prompt: '{create_prompt}'")
    create_res = send_ai_chat(create_prompt)
    print(f"AI Action: {create_res.get('action_performed')}")
    print(f"AI Reply: {create_res.get('reply')}")
    assert create_res.get('action_performed') == 'create', f"Expected 'create', got {create_res}"
    diana_id = create_res['action_details']['id']
    assert diana_id, "Customer ID missing"
    print(f"[PASS] {test_name} created in database with ID #{diana_id}")

    
    # Verify in Customer List API
    req = urllib.request.Request("http://localhost:5000/api/customers", headers=headers)
    cust_res = json.loads(urllib.request.urlopen(req).read().decode('utf-8'))
    found = any(c['id'] == diana_id for c in cust_res['customers'])
    assert found, "Created customer not found in GET /api/customers"
    print("[PASS] Verified Diana Prince exists in GET /api/customers")
    
    # 3. Test UPDATE via AI
    print("\n--- Testing AI UPDATE Customer ---")
    update_prompt = f"Update customer {test_name}'s company to Justice League International"
    print(f"User Prompt: '{update_prompt}'")
    update_res = send_ai_chat(update_prompt)
    print(f"AI Action: {update_res.get('action_performed')}")
    print(f"AI Reply: {update_res.get('reply')}")
    assert update_res.get('action_performed') == 'update', f"Expected 'update', got {update_res}"
    
    # Verify in Customer API
    req = urllib.request.Request(f"http://localhost:5000/api/customers/{diana_id}", headers=headers)
    single_res = json.loads(urllib.request.urlopen(req).read().decode('utf-8'))
    assert "Justice League" in single_res['company'], f"Company not updated: {single_res}"
    print(f"[PASS] Verified customer #{diana_id} company updated to '{single_res['company']}'")
    
    # 4. Test DELETE via AI
    print("\n--- Testing AI DELETE Customer ---")
    delete_prompt = f"Delete customer {test_name}"
    print(f"User Prompt: '{delete_prompt}'")
    delete_res = send_ai_chat(delete_prompt)
    print(f"AI Action: {delete_res.get('action_performed')}")
    print(f"AI Reply: {delete_res.get('reply')}")
    assert delete_res.get('action_performed') == 'delete', f"Expected 'delete', got {delete_res}"
    
    # Verify in Customer List API that Diana Prince is gone
    req = urllib.request.Request("http://localhost:5000/api/customers", headers=headers)
    cust_res_after = json.loads(urllib.request.urlopen(req).read().decode('utf-8'))
    still_exists = any(c['id'] == diana_id for c in cust_res_after['customers'])
    assert not still_exists, "Customer still exists after deletion"
    print(f"[PASS] Verified customer #{diana_id} is no longer in database")
    
    # 5. Test Query / Analysis via AI
    print("\n--- Testing AI Query / General Question ---")
    query_prompt = "How many customers are currently in the database?"
    query_res = send_ai_chat(query_prompt)
    print(f"AI Action: {query_res.get('action_performed')}")
    print(f"AI Reply: {query_res.get('reply')}")
    assert query_res.get('action_performed') is None
    print("[PASS] AI handled query without triggering database changes")
    
    print("\n==============================================")
    print("ALL AI CRUD OPERATIONS PASSED WITH 100% SUCCESS!")
    print("==============================================")

if __name__ == '__main__':
    run_e2e_ai_crud_test()
