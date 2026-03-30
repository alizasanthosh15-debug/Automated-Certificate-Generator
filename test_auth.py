#!/usr/bin/env python3
"""
Test script for API authentication and endpoints
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://127.0.0.1:5000/api"

def print_response(title, response):
    """Pretty print API responses"""
    print(f"\n{'='*60}")
    print(f"📋 {title}")
    print(f"{'='*60}")
    print(f"Status: {response.status_code}")
    try:
        print(json.dumps(response.json(), indent=2))
    except:
        print(response.text)

def test_auth_flow():
    """Test signup, login, and protected endpoints"""
    
    # Test data
    test_user = {
        "name": "Test User",
        "email": f"test{datetime.now().timestamp()}@example.com",
        "password": "password123",
        "role": "user"
    }
    
    # 1. SIGNUP
    print("\n🚀 STARTING AUTH FLOW TESTS\n")
    response = requests.post(f"{BASE_URL}/auth/signup", json=test_user)
    print_response("SIGNUP TEST", response)
    
    if response.status_code != 201:
        print("❌ Signup failed! Cannot continue tests.")
        return
    
    # 2. LOGIN
    login_data = {
        "email": test_user["email"],
        "password": test_user["password"],
        "role": "user"
    }
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    print_response("LOGIN TEST", response)
    
    if response.status_code != 200:
        print("❌ Login failed! Cannot continue tests.")
        return
    
    token = response.json().get("token")
    headers = {"Authorization": f"Bearer {token}"}
    
    # 3. TEST CERTIFICATE LIST (Protected)
    response = requests.get(f"{BASE_URL}/certificates", headers=headers)
    print_response("LIST CERTIFICATES TEST", response)
    
    # 4. TEST EMAIL SEND (Protected)
    email_data = {
        "email": test_user["email"],
        "name": test_user["name"],
        "subject": "Test Certificate"
    }
    response = requests.post(f"{BASE_URL}/email/send", json=email_data, headers=headers)
    print_response("SEND EMAIL TEST", response)
    
    # 5. TEST NO TOKEN (Should fail)
    response = requests.get(f"{BASE_URL}/certificates")
    print_response("TEST WITHOUT TOKEN (Should fail)", response)
    
    print("\n✅ All tests completed!\n")

if __name__ == "__main__":
    print("\n⚠️  Make sure the backend is running on http://127.0.0.1:5000")
    print("    Run: python run.py\n")
    
    try:
        test_auth_flow()
    except requests.exceptions.ConnectionError:
        print("❌ ERROR: Cannot connect to backend at http://127.0.0.1:5000")
        print("   Make sure the backend server is running!")
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
