#!/usr/bin/env python3
"""
Test script for LangChain migration
Validates that all enhanced agents work correctly with both LangChain and fallback modes
"""

import os
import sys
import traceback
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_career_agent():
    """Test the enhanced career agent"""
    print("🔧 Testing Career Agent...")
    try:
        from agents.career_agent import get_career_advice
        
        # Test with simple query
        simple_query = "I'm a software engineer with 3 years experience. Should I specialize in AI/ML or become a full-stack developer?"
        result = get_career_advice(simple_query)
        
        print("✅ Career Agent - Simple Query:")
        print(f"Query: {simple_query}")
        print(f"Response Length: {len(result)} characters")
        print(f"Response Preview: {result[:200]}...")
        print()
        
        # Test with context
        context = {
            "current_role": "Software Engineer",
            "experience_years": "3",
            "industry": "FinTech",
            "skills": "Python, JavaScript, React"
        }
        
        contextual_query = "What career progression should I consider?"
        result_with_context = get_career_advice(contextual_query, context)
        
        print("✅ Career Agent - With Context:")
        print(f"Query: {contextual_query}")
        print(f"Context: {context}")
        print(f"Response Length: {len(result_with_context)} characters")
        print(f"Response Preview: {result_with_context[:200]}...")
        print()
        
        return True
        
    except Exception as e:
        print(f"❌ Career Agent failed: {e}")
        traceback.print_exc()
        return False

def test_resume_agent():
    """Test the enhanced resume agent"""
    print("📄 Testing Resume Agent...")
    try:
        from agents.resume_agent import generate_resume_bullets
        
        experience = """
        Software Engineer at TechCorp (2021-2024)
        - Developed web applications using React and Node.js
        - Worked on a team of 5 developers
        - Improved application performance
        - Collaborated with product managers
        """
        
        result = generate_resume_bullets(experience)
        
        print("✅ Resume Agent:")
        print(f"Input Experience: {experience[:100]}...")
        print(f"Response Length: {len(result)} characters")
        print(f"Response Preview: {result[:300]}...")
        print()
        
        return True
        
    except Exception as e:
        print(f"❌ Resume Agent failed: {e}")
        traceback.print_exc()
        return False

def test_learning_agent():
    """Test the enhanced learning agent"""
    print("📚 Testing Learning Agent...")
    try:
        from agents.learning_agent import get_learning_resources
        
        topic = "Machine Learning for beginners"
        result = get_learning_resources(topic)
        
        print("✅ Learning Agent:")
        print(f"Topic: {topic}")
        print(f"Response Length: {len(result)} characters")
        print(f"Response Preview: {result[:300]}...")
        print()
        
        return True
        
    except Exception as e:
        print(f"❌ Learning Agent failed: {e}")
        traceback.print_exc()
        return False

def test_interview_agent():
    """Test the enhanced interview agent"""
    print("🎤 Testing Interview Agent...")
    try:
        from agents.interview_agent import get_interview_questions
        
        role = "Senior Python Developer"
        result = get_interview_questions(role)
        
        print("✅ Interview Agent:")
        print(f"Role: {role}")
        print(f"Response Length: {len(result)} characters")
        print(f"Response Preview: {result[:300]}...")
        print()
        
        return True
        
    except Exception as e:
        print(f"❌ Interview Agent failed: {e}")
        traceback.print_exc()
        return False

def test_langchain_availability():
    """Test if LangChain is properly installed and configured"""
    print("🔗 Testing LangChain Installation...")
    
    try:
        from langchain_openai import ChatOpenAI
        from langchain.agents import AgentExecutor, create_openai_functions_agent
        from langchain.tools import Tool
        from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
        from langchain.schema import HumanMessage
        from langchain.memory import ConversationBufferWindowMemory
        
        print("✅ All LangChain imports successful")
        
        # Test OpenAI API key
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            print("✅ OpenAI API key found")
            
            # Test simple LLM call
            llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)
            response = llm.invoke([HumanMessage(content="Say 'LangChain integration successful!'")])
            print(f"✅ LLM Test: {response.content}")
            
        else:
            print("⚠️ OpenAI API key not found - agents will use fallback mode")
            
        return True
        
    except ImportError as e:
        print(f"❌ LangChain import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ LangChain test failed: {e}")
        return False

def main():
    """Run comprehensive tests"""
    print("🚀 Starting LangChain Migration Tests\n")
    print("=" * 60)
    
    results = []
    
    # Test LangChain availability first
    results.append(("LangChain Installation", test_langchain_availability()))
    print("=" * 60)
    
    # Test all agents
    results.append(("Career Agent", test_career_agent()))
    print("=" * 60)
    
    results.append(("Resume Agent", test_resume_agent()))
    print("=" * 60)
    
    results.append(("Learning Agent", test_learning_agent()))
    print("=" * 60)
    
    results.append(("Interview Agent", test_interview_agent()))
    print("=" * 60)
    
    # Summary
    print("\n📊 TEST SUMMARY:")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{test_name:<25} {status}")
        if success:
            passed += 1
    
    print("=" * 60)
    print(f"Total: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! LangChain migration successful!")
        return 0
    else:
        print("⚠️ Some tests failed. Check the output above for details.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
