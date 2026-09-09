import sys
import os
import json
import requests

GROQ_API_KEY = "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"
GROQ_MODEL = "qwen/qwen3.8-27b"
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

system_prompt = """You are the AI Intelligent Database Operator for a Customer Management System (CMS).
You have two abilities:
1. Answer questions about the customer database.
2. Execute CRUD operations on the database (create customer, update customer, delete customer).

Current Customers in Database:
[
  {"id": 1, "name": "John Doe", "email": "john@example.com", "company": "Tech Corp", "phone": "+1-234-567-8900", "address": "123 Main St"},
  {"id": 2, "name": "Jane Smith", "email": "jane@example.com", "company": "Digital Solutions", "phone": "+1-234-567-8901", "address": "456 Oak Ave"}
]

Instructions:
You MUST ALWAYS respond with a JSON object with this structure:
{
  "action": "create" | "update" | "delete" | "none",
  "data": {
    "id": integer or null (used for update or delete),
    "target_email": string or null (used to identify customer if id not given),
    "target_name": string or null (used to identify customer if id not given),
    "name": string (customer name for create or update),
    "email": string (customer email for create or update),
    "phone": string (phone number, optional),
    "company": string (company name, optional),
    "address": string (address, optional)
  },
  "reply": "Friendly explanation of what you did or the answer to the user's question."
}

Rules for actions:
- If the user asks to add/create/register a customer: set "action": "create", extract customer fields into "data", and write a confirmation message in "reply".
- If the user asks to update/change/edit a customer: set "action": "update", identify customer by id, email, or name in "data", specify the updated fields in "data", and write a confirmation in "reply".
- If the user asks to delete/remove a customer: set "action": "delete", identify customer in "data", and confirm in "reply".
- If the user asks a general query or greeting (no database modification): set "action": "none", set "data": {}, and answer in "reply".

Do not wrap output in markdown code blocks if possible, return raw valid JSON.
"""

def test_query(prompt):
    print(f"\n--- Testing prompt: '{prompt}' ---")
    payload = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2,
        "response_format": {"type": "json_object"}
    }
    r = requests.post(
        GROQ_API_URL,
        headers={"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"},
        json=payload,
        timeout=15
    )
    res = r.json()
    content = res['choices'][0]['message']['content']
    print("Groq response JSON:")
    parsed = json.loads(content)
    print(json.dumps(parsed, indent=2))
    return parsed

if __name__ == '__main__':
    test_query("Add a customer named Sarah Connor, email sarah@skynet.com, company Cyberdyne Systems, phone 555-1212")
    test_query("Update John Doe's company to Tech Global Enterprises")
    test_query("Delete customer Jane Smith")
    test_query("How many customers are there from Tech Corp?")
