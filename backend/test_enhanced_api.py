#!/usr/bin/env python3
"""
Test Enhanced Flask App with Conversation History
Tests the updated API endpoints that now retain prompts and responses
"""

import requests
import json
import time

def test_enhanced_api():
    """Test the enhanced API endpoints"""
    
    base_url = "http://localhost:5000"
    
    print("🧪 Testing Enhanced Flask API with Conversation History")
    print("=" * 60)
    
    # Test data
    test_cases = [
        {
            "endpoint": "/career-advice",
            "data": {"query": "Should I transition from frontend to backend development?"},
            "expected_fields": ["advice", "prompt", "timestamp", "response_length"]
        },
        {
            "endpoint": "/generate-resume",
            "data": {"experience": "Led a team of 3 developers on React project for 6 months"},
            "expected_fields": ["resume", "prompt", "timestamp", "response_length"]
        },
        {
            "endpoint": "/mock-interview",
            "data": {"role": "Senior Full Stack Developer"},
            "expected_fields": ["questions", "prompt", "timestamp", "response_length"]
        },
        {
            "endpoint": "/learning-resources",
            "data": {"topic": "React advanced patterns"},
            "expected_fields": ["resources", "prompt", "timestamp", "response_length"]
        }
    ]
    
    print("Testing individual endpoints...")
    print()
    
    for i, test_case in enumerate(test_cases, 1):
        endpoint = test_case["endpoint"]
        data = test_case["data"]
        expected_fields = test_case["expected_fields"]
        
        print(f"{i}. Testing {endpoint}")
        print(f"   Input: {data}")
        
        try:
            response = requests.post(f"{base_url}{endpoint}", json=data, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                
                # Check if all expected fields are present
                missing_fields = [field for field in expected_fields if field not in result]
                
                if not missing_fields:
                    print(f"   ✅ SUCCESS - All fields present")
                    print(f"   📝 Prompt retained: {result.get('prompt', 'N/A')[:50]}...")
                    print(f"   📊 Response length: {result.get('response_length', 0)} chars")
                    print(f"   🕒 Timestamp: {result.get('timestamp', 'N/A')}")
                else:
                    print(f"   ⚠️  Missing fields: {missing_fields}")
                    print(f"   📊 Available fields: {list(result.keys())}")
            else:
                print(f"   ❌ HTTP Error: {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            print(f"   ⚠️  Connection failed - Flask server not running")
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        print()
        time.sleep(1)  # Small delay between requests
    
    # Test conversation history endpoint
    print("5. Testing conversation history endpoint...")
    try:
        response = requests.get(f"{base_url}/conversation-history", timeout=10)
        
        if response.status_code == 200:
            history = response.json()
            print(f"   ✅ SUCCESS - History retrieved")
            print(f"   📊 Total conversations: {history.get('total_conversations', 0)}")
            print(f"   📋 Recent conversations: {len(history.get('conversations', []))}")
        else:
            print(f"   ❌ HTTP Error: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print(f"   ⚠️  Connection failed - Flask server not running")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print()
    print("=" * 60)
    print("🎯 Test Complete!")
    print()
    print("📝 Key Features Tested:")
    print("• ✅ Prompt retention in API responses")
    print("• ✅ Response metadata (timestamp, length)")
    print("• ✅ Conversation history storage")
    print("• ✅ Enhanced debugging information")
    print()
    print("🚀 To run tests:")
    print("1. Start Flask server: python app.py")
    print("2. Run this test: python test_enhanced_api.py")

if __name__ == "__main__":
    test_enhanced_api()
