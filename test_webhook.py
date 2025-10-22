import requests
import json

# Test the webhook endpoint
url = "https://moa-shop-api-1.onrender.com/webhook"

# Test 1: With "shop" field
print("Test 1: Sending 'shop' field")
response = requests.post(url, json={"shop": "uniqlo"})
print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")
print("-" * 50)

# Test 2: With "name" field
print("Test 2: Sending 'name' field")
response = requests.post(url, json={"name": "h&m"})
print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")
print("-" * 50)

# Test 3: With "user_input" field
print("Test 3: Sending 'user_input' field")
response = requests.post(url, json={"user_input": "starbucks"})
print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")
print("-" * 50)

# Test 4: Invalid shop
print("Test 4: Invalid shop name")
response = requests.post(url, json={"shop": "invalid_shop"})
print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")
