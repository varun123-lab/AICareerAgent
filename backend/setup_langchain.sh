#!/bin/bash

# 🚀 LangChain Migration Setup Script
# This script helps you set up and test the LangChain migration

echo "🚀 Setting up LangChain for AI Career Agent..."

# Check if we're in the backend directory
if [ ! -f "requirements.txt" ]; then
    echo "❌ Please run this script from the backend directory"
    exit 1
fi

echo "📦 Installing LangChain dependencies..."
pip install langchain==0.1.0 langchain-openai==0.0.5 langchain-community==0.0.10 langchain-core==0.1.0 faiss-cpu==1.7.4

echo "✅ Dependencies installed!"

echo "🧪 Testing LangChain integration..."

# Create a simple test script
cat > test_langchain.py << 'EOF'
import os
import sys

# Test basic imports
try:
    from langchain_openai import ChatOpenAI
    from langchain.tools import Tool
    print("✅ LangChain imports successful!")
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

# Test OpenAI connection
if not os.getenv("OPENAI_API_KEY"):
    print("⚠️  Warning: OPENAI_API_KEY not set in environment")
    print("Please add it to your .env file")
else:
    print("✅ OpenAI API key found!")

# Test basic LangChain functionality
try:
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)
    print("✅ LangChain ChatOpenAI initialized successfully!")
except Exception as e:
    print(f"❌ LangChain initialization error: {e}")

print("\n🎉 LangChain setup complete!")
print("\nNext steps:")
print("1. Review the migration guide: LANGCHAIN_MIGRATION_GUIDE.md")
print("2. Test the enhanced career agent: python -c 'from agents.career_agent_langchain import CareerAgentLangChain; print(\"Agent imported successfully!\")'")
print("3. Run the Flask integration example: python flask_langchain_integration.py")
print("4. Update your frontend to use enhanced features")
EOF

python test_langchain.py

# Clean up test file
rm test_langchain.py

echo ""
echo "🎯 Migration Summary:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📁 Files Created:"
echo "   • langchain_agents_example.py - Full LangChain examples"
echo "   • career_agent_langchain.py - Enhanced career agent"
echo "   • flask_langchain_integration.py - Integration examples"
echo "   • LANGCHAIN_MIGRATION_GUIDE.md - Complete migration guide"
echo ""
echo "🔧 Key Improvements:"
echo "   • Tool-based reasoning (industry analysis, skill planning)"
echo "   • Conversation memory across interactions"
echo "   • Structured, comprehensive responses"
echo "   • Better error handling and fallbacks"
echo "   • Extensible architecture for new features"
echo ""
echo "🚀 Ready to migrate! Follow the guide in LANGCHAIN_MIGRATION_GUIDE.md"
