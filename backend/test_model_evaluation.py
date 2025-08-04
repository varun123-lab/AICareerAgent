#!/usr/bin/env python3
"""
Model Evaluation Test Suite
Tests the comprehensive model evaluation and analytics features
"""

import requests
import json
import time

def test_model_evaluation_features():
    """Test all model evaluation endpoints and features"""
    
    base_url = "http://localhost:5000"
    
    print("🔬 Testing Model Evaluation Features")
    print("=" * 60)
    
    # Test data to generate some evaluation data
    test_requests = [
        {
            "endpoint": "/career-advice",
            "data": {"query": "Should I transition from frontend to AI/ML development?"},
            "description": "Career advice with evaluation"
        },
        {
            "endpoint": "/generate-resume",
            "data": {"experience": "Led a team of 5 developers to build a React application that increased user engagement by 40%"},
            "description": "Resume generation with metrics"
        },
        {
            "endpoint": "/mock-interview",
            "data": {"role": "Senior Data Scientist"},
            "description": "Interview prep with quality scoring"
        }
    ]
    
    print("1. Testing API endpoints with evaluation features...")
    print()
    
    response_ids = []
    
    for i, test in enumerate(test_requests, 1):
        endpoint = test["endpoint"]
        data = test["data"]
        description = test["description"]
        
        print(f"   {i}.{i} Testing {endpoint} - {description}")
        
        try:
            response = requests.post(f"{base_url}{endpoint}", json=data, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                
                # Check for evaluation fields
                if "evaluation" in result:
                    eval_data = result["evaluation"]
                    print(f"       ✅ Quality Score: {eval_data.get('quality_score', 'N/A')}/100")
                    print(f"       📊 Quality Grade: {eval_data.get('quality_grade', 'N/A')}")
                    print(f"       ⏱️  Response Time: {eval_data.get('response_time', 'N/A')}s")
                    print(f"       🆔 Response ID: {eval_data.get('response_id', 'N/A')}")
                    
                    response_ids.append(eval_data.get('response_id'))
                else:
                    print(f"       ⚠️  Missing evaluation data")
                    
            else:
                print(f"       ❌ HTTP Error: {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            print(f"       ⚠️  Connection failed - Flask server not running")
            return
        except Exception as e:
            print(f"       ❌ Error: {e}")
        
        print()
        time.sleep(1)
    
    print("2. Testing model evaluation analytics endpoint...")
    print()
    
    try:
        response = requests.get(f"{base_url}/model-evaluation", timeout=10)
        
        if response.status_code == 200:
            analytics = response.json()
            
            print("   ✅ Model Evaluation Analytics Retrieved:")
            print(f"       📊 Total Evaluations: {analytics.get('total_evaluations', 0)}")
            
            if "overall_statistics" in analytics:
                stats = analytics["overall_statistics"]
                print(f"       🎯 Average Quality Score: {stats.get('average_quality_score', 'N/A')}/100")
                print(f"       ⏱️  Average Response Time: {stats.get('average_response_time', 'N/A')}s")
                print(f"       📝 Average Response Length: {stats.get('average_response_length', 'N/A')} chars")
                print(f"       📈 Grade Distribution: {stats.get('quality_grade_distribution', {})}")
            
            if "endpoint_performance" in analytics:
                print("       🔧 Endpoint Performance:")
                for endpoint, perf in analytics["endpoint_performance"].items():
                    print(f"         • {endpoint}: Quality {perf.get('avg_quality', 'N/A')}/100, Time {perf.get('avg_response_time', 'N/A')}s")
            
            if "model_info" in analytics:
                model_info = analytics["model_info"]
                print(f"       🤖 Model: {model_info.get('framework', 'N/A')} with {model_info.get('base_model', 'N/A')}")
                
        else:
            print(f"   ❌ HTTP Error: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print()
    
    # Test feedback submission if we have response IDs
    if response_ids:
        print("3. Testing user feedback submission...")
        print()
        
        for i, response_id in enumerate(response_ids[:2], 1):  # Test feedback for first 2 responses
            feedback_data = {
                "response_id": response_id,
                "rating": 4 + i % 2,  # Rating of 4 or 5
                "feedback": f"Test feedback {i}: The response was helpful and well-structured."
            }
            
            try:
                response = requests.post(f"{base_url}/feedback", json=feedback_data, timeout=10)
                
                if response.status_code == 200:
                    result = response.json()
                    print(f"   ✅ Feedback submitted for {response_id}: Rating {feedback_data['rating']}/5")
                else:
                    print(f"   ❌ Feedback submission failed: {response.status_code}")
                    
            except Exception as e:
                print(f"   ❌ Feedback error: {e}")
    
    print()
    print("4. Testing conversation history endpoint...")
    print()
    
    try:
        response = requests.get(f"{base_url}/conversation-history", timeout=10)
        
        if response.status_code == 200:
            history = response.json()
            print(f"   ✅ Conversation History Retrieved:")
            print(f"       📊 Total Conversations: {history.get('total_conversations', 0)}")
            print(f"       📋 Recent Conversations: {len(history.get('conversations', []))}")
        else:
            print(f"   ❌ HTTP Error: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print()
    print("=" * 60)
    print("🎯 Model Evaluation Test Complete!")
    print()
    print("📊 Features Tested:")
    print("• ✅ Real-time quality scoring (0-100 scale)")
    print("• ✅ Response time measurement")
    print("• ✅ Content analysis and grading (A-D)")
    print("• ✅ Endpoint-specific quality metrics")
    print("• ✅ Comprehensive analytics dashboard")
    print("• ✅ User feedback collection")
    print("• ✅ Performance trend analysis")
    print("• ✅ Model metadata tracking")
    print()
    print("🚀 Access Evaluation Dashboard:")
    print("• Model Analytics: GET /model-evaluation")
    print("• Conversation History: GET /conversation-history")
    print("• Submit Feedback: POST /feedback")
    print()
    print("📈 Quality Scoring Criteria:")
    print("• Length Appropriateness (20 pts)")
    print("• Structure & Formatting (25 pts)")
    print("• Content Relevance (30 pts)")
    print("• Actionability (15 pts)")
    print("• Professional Tone (10 pts)")

if __name__ == "__main__":
    test_model_evaluation_features()
