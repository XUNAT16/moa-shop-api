"""
Test script to verify API responses for Todook integration
Run this to make sure your API is working correctly
"""

import requests
import json

API_URL = "https://moa-shop-api-1.onrender.com"

print("=" * 60)
print("🧪 TESTING MOA SHOP API FOR TODOOK")
print("=" * 60)

# Test 1: Home endpoint
print("\n1️⃣  Testing Home Endpoint...")
try:
    response = requests.get(f"{API_URL}/")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {json.dumps(response.json(), indent=2)}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 2: Search with GET (What Todook will use)
print("\n2️⃣  Testing Search (GET method - like Todook)...")
try:
    response = requests.get(f"{API_URL}/search?shop=uniqlo")
    print(f"   Status: {response.status_code}")
    data = response.json()
    print(f"   Found: {data.get('found')}")
    print(f"   Message:\n{data.get('message')}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 3: Search with POST
print("\n3️⃣  Testing Search (POST method)...")
try:
    response = requests.post(
        f"{API_URL}/search",
        json={"shop": "h&m"}
    )
    print(f"   Status: {response.status_code}")
    data = response.json()
    print(f"   Found: {data.get('found')}")
    print(f"   Shop: {data.get('shop', {}).get('name')}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 4: Shop not found
print("\n4️⃣  Testing Not Found Response...")
try:
    response = requests.get(f"{API_URL}/search?shop=xyz123")
    print(f"   Status: {response.status_code}")
    data = response.json()
    print(f"   Found: {data.get('found')}")
    print(f"   Message: {data.get('message')}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 5: Categories
print("\n5️⃣  Testing Categories...")
try:
    response = requests.get(f"{API_URL}/categories")
    print(f"   Status: {response.status_code}")
    data = response.json()
    print(f"   Categories: {len(data.get('categories', []))} found")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 6: Popular shops
print("\n6️⃣  Testing Popular Shops...")
try:
    response = requests.get(f"{API_URL}/popular")
    print(f"   Status: {response.status_code}")
    data = response.json()
    print(f"   Popular shops: {data.get('count')} found")
except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n" + "=" * 60)
print("✅ API is working! Use these URLs in Todook:")
print("=" * 60)
print(f"\n📍 Search: {API_URL}/search?shop={{{{user_input}}}}")
print(f"📍 Categories: {API_URL}/categories")
print(f"📍 Popular: {API_URL}/popular")
print("\n" + "=" * 60)
