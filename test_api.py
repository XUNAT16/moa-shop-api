import requests
import json

url = "http://localhost:5000/api/search"
data = {"name": "uniqlo"}

print(f"Testing: POST {url}")
print(f"Body: {json.dumps(data)}\n")

try:
    response = requests.post(url, json=data, timeout=5)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
except requests.exceptions.ConnectionError:
    print("ERROR: Cannot connect to server. Is it running?")
except Exception as e:
    print(f"ERROR: {e}")
