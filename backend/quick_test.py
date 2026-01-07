"""Quick test script for the API."""
import requests

BASE_URL = "http://127.0.0.1:8000"

# Test health
print("Testing health endpoint...")
try:
    resp = requests.get(f"{BASE_URL}/health")
    print(f"Health: {resp.json()}")
except Exception as e:
    print(f"Health failed: {e}")

# Test chat
print("\nTesting chat endpoint...")
try:
    resp = requests.post(
        f"{BASE_URL}/api/chat",
        json={"message": "What services does Tiger Logistics offer?"}
    )
    print(f"Status: {resp.status_code}")
    print(f"Response: {resp.json()}")
except Exception as e:
    print(f"Chat failed: {e}")
