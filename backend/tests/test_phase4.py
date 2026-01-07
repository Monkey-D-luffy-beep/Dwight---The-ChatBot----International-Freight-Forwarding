"""
Project Dwight - Phase 4 Test Suite
Comprehensive testing of all system components
Run with: pytest tests/test_phase4.py -v
Or as script: python tests/test_phase4.py
"""

import requests
import time
import pytest

BASE_URL = "http://127.0.0.1:8000"


class TestDwightAPI:
    """Pytest test class for Dwight API endpoints"""
    
    def test_health(self):
        """Test health endpoint"""
        r = requests.get(f"{BASE_URL}/health", timeout=5)
        assert r.status_code == 200
        data = r.json()
        assert data['status'] == 'healthy'
        assert 'version' in data
    
    def test_chat_services(self):
        """Test chat endpoint with services query"""
        r = requests.post(
            f"{BASE_URL}/api/chat",
            json={"message": "What services does Tiger Logistics offer?"},
            timeout=180
        )
        assert r.status_code == 200
        data = r.json()
        assert 'response' in data
        assert len(data['response']) > 50  # Should have substantial response
    
    def test_chat_fcl_shipping(self):
        """Test chat endpoint with FCL shipping query"""
        r = requests.post(
            f"{BASE_URL}/api/chat",
            json={"message": "What is FCL shipping?"},
            timeout=180
        )
        assert r.status_code == 200
        data = r.json()
        assert 'response' in data
        # Should mention FCL or container in response
        response_lower = data['response'].lower()
        assert 'fcl' in response_lower or 'container' in response_lower
    
    def test_chat_quote_request(self):
        """Test chat endpoint with quote request (sales intent)"""
        r = requests.post(
            f"{BASE_URL}/api/chat",
            json={"message": "I need a quote for shipping from Mumbai to London"},
            timeout=180
        )
        assert r.status_code == 200
        data = r.json()
        assert 'response' in data
        assert 'intent' in data
    
    def test_chat_tracking(self):
        """Test chat endpoint with tracking query"""
        r = requests.post(
            f"{BASE_URL}/api/chat",
            json={"message": "How do I track my shipment?"},
            timeout=180
        )
        assert r.status_code == 200
        data = r.json()
        assert 'response' in data
    
    def test_lead_capture(self):
        """Test lead capture endpoint"""
        lead_data = {
            "name": "Pytest User",
            "email": "pytest@example.com",
            "phone": "+91 9876543210",
            "company": "Pytest Corp",
            "message": "Testing from pytest"
        }
        r = requests.post(
            f"{BASE_URL}/api/lead",
            json=lead_data,
            timeout=10
        )
        assert r.status_code == 200
        data = r.json()
        assert data['success'] == True


# ============================================================
# Script runner for detailed output
# ============================================================

def _test_chat(message, test_name):
    """Helper function for script mode chat testing"""
    print(f"\n[{test_name}]")
    print("-" * 40)
    print(f"Query: {message}")
    try:
        start = time.time()
        r = requests.post(
            f"{BASE_URL}/api/chat",
            json={"message": message},
            timeout=180
        )
        elapsed = time.time() - start
        data = r.json()
        
        print(f"✅ Response Time: {elapsed:.1f}s")
        print(f"   Intent: {data.get('intent', 'N/A')}")
        print(f"   Lead Prompt: {data.get('lead_prompt', False)}")
        print(f"   Response Preview:")
        response = data.get('response', '')[:300]
        print(f"   {response}...")
        return True
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False


def main():
    """Run tests with detailed output (script mode)"""
    print("=" * 50)
    print("PROJECT DWIGHT - PHASE 4 TEST SUITE")
    print("=" * 50)
    
    results = []
    
    # Test 1: Health
    print("\n[1] HEALTH CHECK")
    print("-" * 40)
    try:
        r = requests.get(f"{BASE_URL}/health", timeout=5)
        data = r.json()
        print(f"✅ Status: {data['status']}")
        print(f"   Version: {data['version']}")
        print(f"   Environment: {data['environment']}")
        results.append(("Health Check", True))
    except Exception as e:
        print(f"❌ FAILED: {e}")
        results.append(("Health Check", False))
    
    # Test 2: Services Query
    results.append(("Services Query", _test_chat(
        "What services does Tiger Logistics offer?",
        "2 - SERVICES QUERY"
    )))
    
    # Test 3: FCL Shipping
    results.append(("FCL Shipping", _test_chat(
        "What is FCL shipping and when should I use it?",
        "3 - FCL SHIPPING"
    )))
    
    # Test 4: Get Quote (Sales Intent)
    results.append(("Quote Request", _test_chat(
        "I need a quote for shipping containers from Mumbai to London",
        "4 - QUOTE REQUEST"
    )))
    
    # Test 5: Tracking
    results.append(("Tracking Query", _test_chat(
        "How do I track my shipment?",
        "5 - TRACKING"
    )))
    
    # Test 6: Custom Clearance
    results.append(("Customs Query", _test_chat(
        "What documents do I need for customs clearance?",
        "6 - CUSTOMS DOCS"
    )))
    
    # Test 7: Lead Capture
    print("\n[7] LEAD CAPTURE")
    print("-" * 40)
    try:
        lead_data = {
            "name": "Test User",
            "email": "test@example.com",
            "phone": "+91 9876543210",
            "company": "Test Company",
            "message": "Testing lead capture"
        }
        r = requests.post(
            f"{BASE_URL}/api/lead",
            json=lead_data,
            timeout=10
        )
        if r.status_code == 200 and r.json().get('success'):
            print(f"✅ Lead submitted successfully")
            print(f"   Response: {r.json()}")
            results.append(("Lead Capture", True))
        else:
            print(f"⚠️  Status: {r.status_code}")
            print(f"   Response: {r.text}")
            results.append(("Lead Capture", False))
    except Exception as e:
        print(f"❌ FAILED: {e}")
        results.append(("Lead Capture", False))
    
    # Summary
    print("\n" + "=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status} - {name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    print("=" * 50)


if __name__ == "__main__":
    main()
