from simple_app import app
import json

client = app.test_client()

# Test with wrong Content-Type (simulating Todook)
response = client.post('/traffic', 
                       data='{"query": "parking rates"}',
                       content_type='text/plain')

print("Test: POST /traffic without application/json Content-Type")
print(f"Status: {response.status_code}")
print(f"\nResponse:")
print(json.dumps(response.get_json(), indent=2))
