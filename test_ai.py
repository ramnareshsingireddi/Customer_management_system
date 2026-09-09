import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db, User, Customer, init_db

def run_ai_tests():
    print("=== Testing Groq AI Features ===")
    with app.app_context():
        init_db()
        
    client = app.test_client()
    
    # 1. Register dynamic user and create an isolated customer
    u_name = f"ai_user_{os.urandom(3).hex()}"
    res = client.post('/api/register', json={
        'username': u_name,
        'email': f"{u_name}@example.com",
        'password': 'password123'
    })
    assert res.status_code == 201
    token = res.get_json()['token']
    headers = {'Authorization': f'Bearer {token}'}
    print(f"[PASS] Authenticated dynamic user '{u_name}', obtained JWT")
    
    # Create customer for this user
    res = client.post('/api/customers', json={
        'name': 'Clark Kent',
        'email': f'clark_{os.urandom(3).hex()}@dailyplanet.com',
        'phone': '+1-555-0144',
        'company': 'Daily Planet Inc',
        'address': 'Metropolis'
    }, headers=headers)
    assert res.status_code == 201
    cust_id = res.get_json()['customer']['id']
    print(f"[PASS] Created test customer #{cust_id} (Clark Kent, Daily Planet Inc)")
    
    # 2. Test AI Chat Copilot
    print("[INFO] Sending query to /api/ai/chat...")
    res = client.post('/api/ai/chat', json={
        'message': 'Which customers do we have from Daily Planet Inc, and what is their email?'
    }, headers=headers)
    assert res.status_code == 200, f"AI chat failed: {res.data}"
    chat_data = res.get_json()
    assert 'reply' in chat_data
    assert len(chat_data['reply']) > 10
    print("[PASS] /api/ai/chat succeeded!")
    print(f"       AI Reply Preview: {chat_data['reply'][:120]}...\n")
    
    # 3. Test AI Email Drafter
    print("[INFO] Requesting email draft from /api/ai/draft-email...")
    res = client.post('/api/ai/draft-email', json={
        'customer_id': cust_id,
        'goal': 'check_in',
        'notes': 'Mention that our team recently upgraded our platform.'
    }, headers=headers)
    assert res.status_code == 200, f"AI draft email failed: {res.data}"
    draft_data = res.get_json()
    assert 'subject' in draft_data
    assert 'body' in draft_data
    print("[PASS] /api/ai/draft-email succeeded!")
    print(f"       Subject: {draft_data['subject']}")
    print(f"       Body Preview: {draft_data['body'][:120]}...\n")
    
    print("ALL AI TESTS PASSED SUCCESSFULLY!")

if __name__ == '__main__':
    run_ai_tests()
