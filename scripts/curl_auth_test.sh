#!/bin/bash
# Test Peloton authentication with curl

source .env

echo "Testing Peloton auth with curl..."
echo "=================================="

curl -X POST "https://api.onepeloton.com/auth/login" \
  -H "Content-Type: application/json" \
  -H "User-Agent: curl/8.0" \
  -d "{\"username_or_email\":\"$PELOTON_USERNAME\",\"password\":\"$PELOTON_PASSWORD\"}" \
  -v
