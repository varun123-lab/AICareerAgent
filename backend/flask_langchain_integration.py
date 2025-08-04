"""
Flask Integration Example for LangChain Career Agent

This shows how to integrate the LangChain-powered career agent with your existing Flask app.
You can gradually migrate one endpoint at a time.
"""

from flask import Flask, request, jsonify
from agents.career_agent_langchain import CareerAgentLangChain, get_career_advice_langchain

# Initialize Flask app
app = Flask(__name__)

# Initialize LangChain agent (singleton pattern for better performance)
career_agent = None

def get_career_agent():
    """Get or create career agent instance"""
    global career_agent
    if career_agent is None:
        career_agent = CareerAgentLangChain()
    return career_agent

# Enhanced career advice endpoint with LangChain
@app.route("/career-advice-enhanced", methods=["POST"])
def career_advice_enhanced():
    """Enhanced career advice endpoint using LangChain agents"""
    try:
        data = request.get_json()
        query = data.get("query", "")
        
        if not query.strip():
            return jsonify({"error": "Please provide a career question"}), 400
        
        # Extract user context if provided
        user_context = {
            "current_role": data.get("current_role", ""),
            "experience_years": data.get("experience_years", ""),
            "industry": data.get("industry", ""),
            "location": data.get("location", ""),
            "education": data.get("education", ""),
            "skills": data.get("skills", ""),
            "career_goals": data.get("career_goals", "")
        }
        
        # Remove empty values
        user_context = {k: v for k, v in user_context.items() if v}
        
        # Get enhanced career advice
        agent = get_career_agent()
        advice = agent.get_career_advice(query, user_context if user_context else None)
        
        return jsonify({
            "advice": advice,
            "enhanced": True,
            "tools_used": True
        })
        
    except Exception as e:
        return jsonify({"error": f"Failed to generate career advice: {str(e)}"}), 500

# Backward compatible endpoint (uses simple function)
@app.route("/career-advice", methods=["POST"])
def career_advice():
    """Original career advice endpoint with optional LangChain enhancement"""
    try:
        data = request.get_json()
        query = data.get("query", "")
        
        if not query.strip():
            return jsonify({"error": "Please provide a career question"}), 400
        
        # Check if client wants enhanced features
        use_enhanced = data.get("enhanced", False)
        
        if use_enhanced:
            # Use LangChain agent
            user_context = {
                "current_role": data.get("current_role", ""),
                "experience_years": data.get("experience_years", ""),
                "industry": data.get("industry", "")
            }
            user_context = {k: v for k, v in user_context.items() if v}
            
            advice = get_career_advice_langchain(query, user_context if user_context else None)
        else:
            # Use original implementation
            from agents.career_agent import get_career_advice
            advice = get_career_advice(query)
        
        return jsonify({"advice": advice})
        
    except Exception as e:
        return jsonify({"error": f"Failed to generate career advice: {str(e)}"}), 500

# A/B Testing endpoint to compare responses
@app.route("/career-advice-compare", methods=["POST"])
def career_advice_compare():
    """Compare original vs LangChain responses for testing"""
    try:
        data = request.get_json()
        query = data.get("query", "")
        
        if not query.strip():
            return jsonify({"error": "Please provide a career question"}), 400
        
        # Get original response
        from agents.career_agent import get_career_advice
        original_advice = get_career_advice(query)
        
        # Get LangChain response
        user_context = {
            "current_role": data.get("current_role", ""),
            "experience_years": data.get("experience_years", ""),
            "industry": data.get("industry", "")
        }
        user_context = {k: v for k, v in user_context.items() if v}
        
        enhanced_advice = get_career_advice_langchain(query, user_context if user_context else None)
        
        return jsonify({
            "original": original_advice,
            "enhanced": enhanced_advice,
            "query": query,
            "context": user_context
        })
        
    except Exception as e:
        return jsonify({"error": f"Failed to compare responses: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
