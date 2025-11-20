#!/usr/bin/env python3
"""Test the ?= workaround for Peloton auth."""

import requests
import os
from dotenv import load_dotenv

load_dotenv()

username = os.getenv('PELOTON_USERNAME')
password = os.getenv('PELOTON_PASSWORD')

print("Testing Peloton API workaround with ?= parameter")
print("=" * 60)

# Test with ?= parameter
print("\nTrying with ?= parameter...")
try:
    session = requests.Session()
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'peloton-analysis/0.1.0'
    }
    response = session.post(
        'https://api.onepeloton.com/auth/login?=',
        json={'username_or_email': username, 'password': password},
        headers=headers
    )
    print(f"Status: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        print(f"✓ SUCCESS!")
        print(f"User ID: {data.get('user_id')}")
        print(f"Session ID: {data.get('session_id')[:20]}..." if data.get('session_id') else "No session ID")
    else:
        print(f"Response: {response.text[:500]}")
except Exception as e:
    print(f"Error: {e}")

print("\n" + "=" * 60)
