#!/usr/bin/env python3
"""
Debug script to test Peloton authentication with different configurations.
"""

import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

username = os.getenv('PELOTON_USERNAME')
password = os.getenv('PELOTON_PASSWORD')

print("Testing Peloton API Authentication")
print("=" * 60)

# Test 1: Basic authentication
print("\nTest 1: Basic POST with JSON payload")
print("-" * 60)
try:
    session = requests.Session()
    response = session.post(
        'https://api.onepeloton.com/auth/login',
        json={'username_or_email': username, 'password': password}
    )
    print(f"Status: {response.status_code}")
    print(f"Headers: {dict(response.headers)}")
    if response.status_code != 200:
        print(f"Response: {response.text[:500]}")
except Exception as e:
    print(f"Error: {e}")

# Test 2: With User-Agent header
print("\nTest 2: With User-Agent header")
print("-" * 60)
try:
    session = requests.Session()
    headers = {
        'User-Agent': 'peloton-analysis/0.1.0'
    }
    response = session.post(
        'https://api.onepeloton.com/auth/login',
        json={'username_or_email': username, 'password': password},
        headers=headers
    )
    print(f"Status: {response.status_code}")
    if response.status_code != 200:
        print(f"Response: {response.text[:500]}")
except Exception as e:
    print(f"Error: {e}")

# Test 3: With Content-Type and User-Agent
print("\nTest 3: With Content-Type and User-Agent")
print("-" * 60)
try:
    session = requests.Session()
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'peloton-analysis/0.1.0'
    }
    response = session.post(
        'https://api.onepeloton.com/auth/login',
        json={'username_or_email': username, 'password': password},
        headers=headers
    )
    print(f"Status: {response.status_code}")
    if response.status_code != 200:
        print(f"Response: {response.text[:500]}")
    else:
        print(f"Success! User ID: {response.json().get('user_id')}")
except Exception as e:
    print(f"Error: {e}")

# Test 4: Browser-like User-Agent
print("\nTest 4: Browser-like User-Agent")
print("-" * 60)
try:
    session = requests.Session()
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    response = session.post(
        'https://api.onepeloton.com/auth/login',
        json={'username_or_email': username, 'password': password},
        headers=headers
    )
    print(f"Status: {response.status_code}")
    if response.status_code != 200:
        print(f"Response: {response.text[:500]}")
    else:
        print(f"Success! User ID: {response.json().get('user_id')}")
except Exception as e:
    print(f"Error: {e}")

# Test 5: Form data instead of JSON
print("\nTest 5: Form data instead of JSON")
print("-" * 60)
try:
    session = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }
    response = session.post(
        'https://api.onepeloton.com/auth/login',
        data={'username_or_email': username, 'password': password},
        headers=headers
    )
    print(f"Status: {response.status_code}")
    if response.status_code != 200:
        print(f"Response: {response.text[:500]}")
    else:
        print(f"Success! User ID: {response.json().get('user_id')}")
except Exception as e:
    print(f"Error: {e}")

print("\n" + "=" * 60)
print("Debug complete")
