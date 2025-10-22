import requests
import json

# Test the /search endpoint with different field names
url = "https://moa-shop-api-1.onrender.com/search"

tests = [
    {"shop": "uniqlo"},
    {"name": "h&m"},
    {"query": "starbucks"},
    {"text": "muji"},
    {"message": "shake shack"},
    {"user_input": "jollibee"}
]

for i, test_data in enumerate(tests, 1):
    print(f"\nTest {i}: {test_data}")
    response = requests.post(url, json=test_data)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print(f"✅ SUCCESS!")
        print(f"Message: {response.json().get('message', 'N/A')}")
    else:
        print(f"❌ FAILED")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    print("-" * 60)
