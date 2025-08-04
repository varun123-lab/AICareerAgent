from flask_cors import CORS
from flask import Flask, request, jsonify, session, redirect, url_for
from dotenv import load_dotenv
from agents.career_agent import get_career_advice
from agents.interview_agent import get_interview_questions
from agents.learning_agent import get_learning_resources
from agents.resume_agent import generate_resume_bullets
from utils.openai_helper import setup_openai

from flask import send_from_directory
import os
import json
from datetime import datetime
import time
import hashlib
from functools import wraps

print("[DEBUG] Starting Flask app...")
load_dotenv()
print("[DEBUG] Loaded environment variables.")
setup_openai()
print("[DEBUG] OpenAI setup complete.")

# Initialize Flask app
app = Flask(__name__)
CORS(app)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "your-secret-key-change-this")  # Change this in production
print("[DEBUG] Flask app initialized.")

FRONTEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../frontend"))
print(f"[DEBUG] Serving frontend from: {FRONTEND_DIR}")

# Initialize conversation history storage
CONVERSATION_HISTORY = []
MODEL_EVAL_DATA = []

# Simple user database (in production, use a real database)
USERS_DB = {
    "admin": {
        "password": "admin123",  # In production, use hashed passwords
        "role": "admin",
        "name": "Administrator"
    },
    "demo": {
        "password": "demo123",
        "role": "user", 
        "name": "Demo User"
    },
    "user": {
        "password": "user123",
        "role": "user",
        "name": "Regular User"
    }
}

def require_login(f):
    """Decorator to require login for protected routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({"error": "Authentication required", "redirect": "/login"}), 401
        return f(*args, **kwargs)
    return decorated_function

def get_current_user():
    """Get current logged-in user info - simplified for demo"""
    return {
        "name": "Demo User",
        "username": "demo", 
        "role": "user"
    }

def calculate_response_metrics(user_input, ai_response, processing_time):
    """Calculate comprehensive response quality metrics"""
    metrics = {
        "response_time_seconds": processing_time,
        "input_length": len(user_input),
        "output_length": len(ai_response),
        "input_word_count": len(user_input.split()),
        "output_word_count": len(ai_response.split()),
        "compression_ratio": len(ai_response) / max(len(user_input), 1),
        "words_per_second": len(ai_response.split()) / max(processing_time, 0.1),
        "has_structured_format": bool(any(marker in ai_response for marker in ['###', '**', '1.', '2.', '•', '-'])),
        "has_quantified_data": bool(any(char.isdigit() and '%' in ai_response[i:i+10] for i, char in enumerate(ai_response))),
        "response_completeness_score": min(len(ai_response) / 500, 1.0),  # Normalized completeness
        "response_id": hashlib.md5(f"{user_input}{ai_response}".encode()).hexdigest()[:8]
    }
    return metrics

def evaluate_response_quality(ai_response, endpoint):
    """Evaluate response quality based on content analysis"""
    quality_score = 0
    quality_factors = []
    
    # Length appropriateness (20 points)
    if 200 <= len(ai_response) <= 3000:
        quality_score += 20
        quality_factors.append("appropriate_length")
    elif len(ai_response) > 100:
        quality_score += 10
        quality_factors.append("minimal_length")
    
    # Structure and formatting (25 points)
    structure_indicators = ['###', '**', '1.', '2.', '3.', '•', '-', '\n\n']
    structure_count = sum(1 for indicator in structure_indicators if indicator in ai_response)
    if structure_count >= 5:
        quality_score += 25
        quality_factors.append("well_structured")
    elif structure_count >= 2:
        quality_score += 15
        quality_factors.append("basic_structure")
    
    # Specific content quality by endpoint (30 points)
    if endpoint == "career-advice":
        career_keywords = ['skill', 'experience', 'growth', 'opportunity', 'market', 'salary', 'trend']
        keyword_count = sum(1 for keyword in career_keywords if keyword.lower() in ai_response.lower())
        quality_score += min(keyword_count * 4, 30)
        if keyword_count >= 5:
            quality_factors.append("comprehensive_career_advice")
    
    elif endpoint == "generate-resume":
        resume_keywords = ['achieved', 'led', 'managed', 'improved', 'increased', '%', 'result']
        keyword_count = sum(1 for keyword in resume_keywords if keyword.lower() in ai_response.lower())
        quality_score += min(keyword_count * 5, 30)
        if keyword_count >= 4:
            quality_factors.append("quantified_achievements")
    
    elif endpoint == "mock-interview":
        interview_keywords = ['question', 'behavior', 'technical', 'experience', 'situation', 'challenge']
        keyword_count = sum(1 for keyword in interview_keywords if keyword.lower() in ai_response.lower())
        quality_score += min(keyword_count * 5, 30)
        if keyword_count >= 4:
            quality_factors.append("comprehensive_interview_prep")
    
    elif endpoint == "learning-resources":
        learning_keywords = ['course', 'book', 'tutorial', 'practice', 'project', 'skill', 'learn']
        keyword_count = sum(1 for keyword in learning_keywords if keyword.lower() in ai_response.lower())
        quality_score += min(keyword_count * 4, 30)
        if keyword_count >= 5:
            quality_factors.append("diverse_learning_resources")
    
    # Actionability (15 points)
    actionable_indicators = ['step', 'action', 'recommendation', 'should', 'consider', 'try', 'start']
    actionable_count = sum(1 for indicator in actionable_indicators if indicator.lower() in ai_response.lower())
    if actionable_count >= 5:
        quality_score += 15
        quality_factors.append("highly_actionable")
    elif actionable_count >= 2:
        quality_score += 8
        quality_factors.append("somewhat_actionable")
    
    # Professional tone (10 points)
    professional_indicators = ['professional', 'industry', 'best practice', 'recommend', 'suggest']
    if any(indicator.lower() in ai_response.lower() for indicator in professional_indicators):
        quality_score += 10
        quality_factors.append("professional_tone")
    
    return {
        "quality_score": quality_score,
        "quality_grade": "A" if quality_score >= 80 else "B" if quality_score >= 60 else "C" if quality_score >= 40 else "D",
        "quality_factors": quality_factors,
        "max_possible_score": 100
    }

def save_model_evaluation(endpoint, user_input, ai_response, processing_time, metadata=None):
    """Save comprehensive model evaluation data"""
    
    # Calculate metrics
    response_metrics = calculate_response_metrics(user_input, ai_response, processing_time)
    quality_eval = evaluate_response_quality(ai_response, endpoint)
    
    eval_entry = {
        "timestamp": datetime.now().isoformat(),
        "endpoint": endpoint,
        "user_input": user_input,
        "ai_response": ai_response,
        "processing_time": processing_time,
        "metrics": response_metrics,
        "quality_evaluation": quality_eval,
        "metadata": metadata or {},
        "model_info": {
            "framework": "LangChain",
            "base_model": "gpt-3.5-turbo",
            "agent_type": "OpenAI Functions Agent",
            "tools_used": True,
            "memory_enabled": True
        }
    }
    
    MODEL_EVAL_DATA.append(eval_entry)
    
    # Save to file for persistence
    try:
        with open("model_evaluation_data.json", "w") as f:
            json.dump(MODEL_EVAL_DATA, f, indent=2)
        print(f"[EVAL] {endpoint} - Quality: {quality_eval['quality_grade']} ({quality_eval['quality_score']}/100) - Time: {processing_time:.2f}s")
    except Exception as e:
        print(f"[WARNING] Could not save evaluation data: {e}")

def save_conversation(endpoint, user_input, ai_response, metadata=None):
    """Save conversation history for analytics and debugging"""
    conversation_entry = {
        "timestamp": datetime.now().isoformat(),
        "endpoint": endpoint,
        "user_input": user_input,
        "ai_response": ai_response,
        "response_length": len(ai_response),
        "metadata": metadata or {}
    }
    
    CONVERSATION_HISTORY.append(conversation_entry)
    
    # Optionally save to file for persistence
    try:
        with open("conversation_history.json", "w") as f:
            json.dump(CONVERSATION_HISTORY, f, indent=2)
        print(f"[DEBUG] Conversation saved: {endpoint} - {len(ai_response)} chars")
    except Exception as e:
        print(f"[WARNING] Could not save conversation history: {e}")

@app.route("/conversation-history", methods=["GET"])
def get_conversation_history():
    """Get conversation history for analytics"""
    return jsonify({
        "total_conversations": len(CONVERSATION_HISTORY),
        "conversations": CONVERSATION_HISTORY[-10:]  # Return last 10 conversations
    })

@app.route("/model-evaluation", methods=["GET"])
def get_model_evaluation():
    """Get comprehensive model evaluation analytics"""
    
    if not MODEL_EVAL_DATA:
        return jsonify({
            "message": "No evaluation data available",
            "total_evaluations": 0
        })
    
    # Calculate aggregate statistics
    total_evals = len(MODEL_EVAL_DATA)
    avg_quality_score = sum(eval_data["quality_evaluation"]["quality_score"] for eval_data in MODEL_EVAL_DATA) / total_evals
    avg_response_time = sum(eval_data["processing_time"] for eval_data in MODEL_EVAL_DATA) / total_evals
    avg_response_length = sum(eval_data["metrics"]["output_length"] for eval_data in MODEL_EVAL_DATA) / total_evals
    
    # Quality grade distribution
    grade_distribution = {}
    for eval_data in MODEL_EVAL_DATA:
        grade = eval_data["quality_evaluation"]["quality_grade"]
        grade_distribution[grade] = grade_distribution.get(grade, 0) + 1
    
    # Endpoint performance breakdown
    endpoint_stats = {}
    for eval_data in MODEL_EVAL_DATA:
        endpoint = eval_data["endpoint"]
        if endpoint not in endpoint_stats:
            endpoint_stats[endpoint] = {
                "count": 0,
                "avg_quality": 0,
                "avg_response_time": 0,
                "quality_scores": []
            }
        
        endpoint_stats[endpoint]["count"] += 1
        endpoint_stats[endpoint]["quality_scores"].append(eval_data["quality_evaluation"]["quality_score"])
    
    # Calculate averages for each endpoint
    for endpoint, stats in endpoint_stats.items():
        stats["avg_quality"] = sum(stats["quality_scores"]) / len(stats["quality_scores"])
        stats["avg_response_time"] = sum(eval_data["processing_time"] for eval_data in MODEL_EVAL_DATA if eval_data["endpoint"] == endpoint) / stats["count"]
        del stats["quality_scores"]  # Remove raw scores from response
    
    # Recent performance trend (last 10 evaluations)
    recent_evals = MODEL_EVAL_DATA[-10:]
    recent_trend = {
        "avg_quality": sum(eval_data["quality_evaluation"]["quality_score"] for eval_data in recent_evals) / len(recent_evals),
        "avg_response_time": sum(eval_data["processing_time"] for eval_data in recent_evals) / len(recent_evals)
    }
    
    return jsonify({
        "total_evaluations": total_evals,
        "overall_statistics": {
            "average_quality_score": round(avg_quality_score, 2),
            "average_response_time": round(avg_response_time, 2),
            "average_response_length": round(avg_response_length, 2),
            "quality_grade_distribution": grade_distribution
        },
        "endpoint_performance": endpoint_stats,
        "recent_trend": recent_trend,
        "model_info": {
            "framework": "LangChain with OpenAI Functions Agent",
            "base_model": "gpt-3.5-turbo",
            "features": ["specialized_tools", "memory_management", "agent_reasoning"]
        },
        "evaluation_criteria": {
            "quality_factors": ["length_appropriateness", "structure", "content_relevance", "actionability", "professional_tone"],
            "max_quality_score": 100,
            "grade_ranges": {"A": "80-100", "B": "60-79", "C": "40-59", "D": "0-39"}
        },
        "recent_evaluations": MODEL_EVAL_DATA[-5:]  # Last 5 evaluations
    })

@app.route("/feedback", methods=["POST"])
def submit_feedback():
    """Submit user feedback for model evaluation"""
    data = request.get_json()
    response_id = data.get("response_id", "")
    rating = data.get("rating", 0)  # 1-5 scale
    feedback_text = data.get("feedback", "")
    
    # Find the corresponding evaluation entry
    for eval_entry in MODEL_EVAL_DATA:
        if eval_entry["metrics"]["response_id"] == response_id:
            eval_entry["user_feedback"] = {
                "rating": rating,
                "feedback_text": feedback_text,
                "timestamp": datetime.now().isoformat()
            }
            
            # Save updated data
            try:
                with open("model_evaluation_data.json", "w") as f:
                    json.dump(MODEL_EVAL_DATA, f, indent=2)
                print(f"[FEEDBACK] Response {response_id} rated {rating}/5")
            except Exception as e:
                print(f"[WARNING] Could not save feedback: {e}")
            
            return jsonify({"message": "Feedback saved successfully", "response_id": response_id})
    
    return jsonify({"error": "Response ID not found", "response_id": response_id}), 404

# Authentication Routes - Bypassed for better UX
@app.route("/login", methods=["GET", "POST"])
def login():
    """Handle user login - bypassed for demo purposes"""
    if request.method == "POST":
        # Always return successful authentication for demo
        return jsonify({
            "success": True,
            "message": "Authentication bypassed for demo",
            "user": {
                "username": "demo",
                "name": "Demo User",
                "role": "user"
            },
            "redirect": "/"
        })
    
    # GET request - redirect to home instead of serving login page
    return redirect(url_for('serve_home'))

@app.route("/logout", methods=["POST"])
def logout():
    """Handle user logout - simplified for demo"""
    return jsonify({
        "success": True,
        "message": "Logout not required in demo mode",
        "redirect": "/"
    })

@app.route("/auth-status", methods=["GET"])
def auth_status():
    """Check authentication status - always authenticated in demo"""
    return jsonify({
        "authenticated": True,
        "user": {
            "username": "demo",
            "name": "Demo User", 
            "role": "user"
        }
    })

@app.route("/protected-test", methods=["GET"])
@require_login
def protected_test():
    """Test endpoint to verify authentication"""
    user = get_current_user()
    return jsonify({
        "message": "You are authenticated!",
        "user": {
            "username": session['user_id'],
            "name": user['name'],
            "role": user['role']
        }
    })

@app.route("/career-advice", methods=["POST"])
# @require_login  # Temporarily disabled for better UX
def career_advice():
    print("[DEBUG] /career-advice endpoint hit")
    start_time = time.time()
    
    data = request.get_json()
    print(f"[DEBUG] Request data: {data}")
    query = data.get("query", "")
    print(f"[DEBUG] Query: {query}")
    
    # Get enhanced career advice
    result = get_career_advice(query)
    processing_time = time.time() - start_time
    print(f"[DEBUG] Result: {result}")
    
    # Save conversation history with user info
    user = get_current_user()
    save_conversation(
        endpoint="career-advice",
        user_input=query,
        ai_response=result,
        metadata={
            "user_context": data.get("context", {}),
            "user_id": session.get('user_id'),
            "user_name": user['name'] if user else None
        }
    )
    
    # Save model evaluation data with user info
    save_model_evaluation(
        endpoint="career-advice",
        user_input=query,
        ai_response=result,
        processing_time=processing_time,
        metadata={
            "user_context": data.get("context", {}),
            "user_id": session.get('user_id'),
            "user_name": user['name'] if user else None
        }
    )
    
    # Calculate response metrics for immediate feedback
    metrics = calculate_response_metrics(query, result, processing_time)
    quality_eval = evaluate_response_quality(result, "career-advice")
    
    return jsonify({
        "advice": result,
        "prompt": query,
        "timestamp": datetime.now().isoformat(),
        "response_length": len(result),
        "evaluation": {
            "quality_score": quality_eval["quality_score"],
            "quality_grade": quality_eval["quality_grade"],
            "response_time": round(processing_time, 2),
            "response_id": metrics["response_id"]
        }
    })

@app.route("/generate-resume", methods=["POST"])
# @require_login  # Temporarily disabled for better UX
def generate_resume():
    print("[DEBUG] /generate-resume endpoint hit")
    start_time = time.time()
    
    data = request.get_json()
    print(f"[DEBUG] Request data: {data}")
    experience = data.get("experience", "")
    print(f"[DEBUG] Experience: {experience}")
    
    # Get enhanced resume bullets
    result = generate_resume_bullets(experience)
    processing_time = time.time() - start_time
    print(f"[DEBUG] Result: {result}")
    
    # Save conversation history
    save_conversation(
        endpoint="generate-resume",
        user_input=experience,
        ai_response=result,
        metadata={"user_context": data.get("context", {})}
    )
    
    # Save model evaluation data
    save_model_evaluation(
        endpoint="generate-resume",
        user_input=experience,
        ai_response=result,
        processing_time=processing_time,
        metadata={"user_context": data.get("context", {})}
    )
    
    # Calculate response metrics for immediate feedback
    metrics = calculate_response_metrics(experience, result, processing_time)
    quality_eval = evaluate_response_quality(result, "generate-resume")
    
    return jsonify({
        "resume": result,
        "prompt": experience,
        "timestamp": datetime.now().isoformat(),
        "response_length": len(result),
        "evaluation": {
            "quality_score": quality_eval["quality_score"],
            "quality_grade": quality_eval["quality_grade"],
            "response_time": round(processing_time, 2),
            "response_id": metrics["response_id"]
        }
    })

@app.route("/mock-interview", methods=["POST"])
# @require_login  # Temporarily disabled for better UX
def mock_interview():
    print("[DEBUG] /mock-interview endpoint hit")
    start_time = time.time()
    
    data = request.get_json()
    print(f"[DEBUG] Request data: {data}")
    role = data.get("role", "")
    print(f"[DEBUG] Role: {role}")
    
    # Get enhanced interview questions
    result = get_interview_questions(role)
    processing_time = time.time() - start_time
    print(f"[DEBUG] Result: {result}")
    
    # Save conversation history
    save_conversation(
        endpoint="mock-interview",
        user_input=role,
        ai_response=result,
        metadata={"user_context": data.get("context", {})}
    )
    
    # Save model evaluation data
    save_model_evaluation(
        endpoint="mock-interview",
        user_input=role,
        ai_response=result,
        processing_time=processing_time,
        metadata={"user_context": data.get("context", {})}
    )
    
    # Calculate response metrics for immediate feedback
    metrics = calculate_response_metrics(role, result, processing_time)
    quality_eval = evaluate_response_quality(result, "mock-interview")
    
    return jsonify({
        "questions": result,
        "prompt": role,
        "timestamp": datetime.now().isoformat(),
        "response_length": len(result),
        "evaluation": {
            "quality_score": quality_eval["quality_score"],
            "quality_grade": quality_eval["quality_grade"],
            "response_time": round(processing_time, 2),
            "response_id": metrics["response_id"]
        }
    })

@app.route("/learning-resources", methods=["POST"])
# @require_login  # Temporarily disabled for better UX
def learning_resources():
    print("[DEBUG] /learning-resources endpoint hit")
    start_time = time.time()
    
    data = request.get_json()
    print(f"[DEBUG] Request data: {data}")
    topic = data.get("topic", "")
    print(f"[DEBUG] Topic: {topic}")
    
    # Get enhanced learning resources
    result = get_learning_resources(topic)
    processing_time = time.time() - start_time
    print(f"[DEBUG] Result: {result}")
    
    # Save conversation history
    save_conversation(
        endpoint="learning-resources",
        user_input=topic,
        ai_response=result,
        metadata={"user_context": data.get("context", {})}
    )
    
    # Save model evaluation data
    save_model_evaluation(
        endpoint="learning-resources",
        user_input=topic,
        ai_response=result,
        processing_time=processing_time,
        metadata={"user_context": data.get("context", {})}
    )
    
    # Calculate response metrics for immediate feedback
    metrics = calculate_response_metrics(topic, result, processing_time)
    quality_eval = evaluate_response_quality(result, "learning-resources")
    
    return jsonify({
        "resources": result,
        "prompt": topic,
        "timestamp": datetime.now().isoformat(),
        "response_length": len(result),
        "evaluation": {
            "quality_score": quality_eval["quality_score"],
            "quality_grade": quality_eval["quality_grade"],
            "response_time": round(processing_time, 2),
            "response_id": metrics["response_id"]
        }
    })





@app.route("/")
def serve_home():
    print(f"[DEBUG] FRONTEND_DIR: {FRONTEND_DIR}")
    print("[DEBUG] Serving index.html")
    return send_from_directory(FRONTEND_DIR, "index.html")

@app.route("/career.html")
def serve_career():
    print(f"[DEBUG] FRONTEND_DIR: {FRONTEND_DIR}")
    print("[DEBUG] Serving career.html")
    return send_from_directory(FRONTEND_DIR, "career.html")

@app.route("/resume.html")
def serve_resume():
    print(f"[DEBUG] FRONTEND_DIR: {FRONTEND_DIR}")
    print("[DEBUG] Serving resume.html")
    return send_from_directory(FRONTEND_DIR, "resume.html")

@app.route("/interview.html")
def serve_interview():
    print(f"[DEBUG] FRONTEND_DIR: {FRONTEND_DIR}")
    print("[DEBUG] Serving interview.html")
    return send_from_directory(FRONTEND_DIR, "interview.html")

@app.route("/learning.html")
def serve_learning():
    print(f"[DEBUG] FRONTEND_DIR: {FRONTEND_DIR}")
    print("[DEBUG] Serving learning.html")
    return send_from_directory(FRONTEND_DIR, "learning.html")

@app.route("/index.html")
def serve_ind():
    print(f"[DEBUG] FRONTEND_DIR: {FRONTEND_DIR}")
    print("[DEBUG] Serving index.html")
    return send_from_directory(FRONTEND_DIR, "index.html")

# Serve static files (CSS, JS)
@app.route("/static/<path:filename>")
def serve_static_files(filename):
    static_dir = os.path.join(os.path.dirname(__file__), "static")
    return send_from_directory(static_dir, filename)

@app.route("/css/<path:filename>")
def serve_css(filename):
    css_dir = os.path.join(FRONTEND_DIR, "css")
    return send_from_directory(css_dir, filename)

@app.route("/js/<path:filename>")
def serve_js(filename):
    js_dir = os.path.join(FRONTEND_DIR, "js")
    return send_from_directory(js_dir, filename)


if __name__ == "__main__":
    print("[DEBUG] Running Flask app...")
    app.run(debug=True, port=5002)
