from flask_cors import CORS
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from agents.career_agent import get_career_advice
from agents.interview_agent import get_interview_questions
from agents.learning_agent import get_learning_resources
from agents.resume_agent import generate_resume_bullets
from utils.openai_helper import setup_openai

from flask import send_from_directory
import os

print("[DEBUG] Starting Flask app...")
load_dotenv()
print("[DEBUG] Loaded environment variables.")
setup_openai()
print("[DEBUG] OpenAI setup complete.")

# Initialize Flask app
app = Flask(__name__)
CORS(app)
print("[DEBUG] Flask app initialized.")

FRONTEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../frontend"))
print(f"[DEBUG] Serving frontend from: {FRONTEND_DIR}")

@app.route("/career-advice", methods=["POST"])
def career_advice():
    print("[DEBUG] /career-advice endpoint hit")
    data = request.get_json()
    print(f"[DEBUG] Request data: {data}")
    query = data.get("query", "")
    print(f"[DEBUG] Query: {query}")
    result = get_career_advice(query)
    print(f"[DEBUG] Result: {result}")
    return jsonify({"advice": result})

@app.route("/generate-resume", methods=["POST"])
def generate_resume():
    print("[DEBUG] /generate-resume endpoint hit")
    data = request.get_json()
    print(f"[DEBUG] Request data: {data}")
    experience = data.get("experience", "")
    print(f"[DEBUG] Experience: {experience}")
    result = generate_resume_bullets(experience)
    print(f"[DEBUG] Result: {result}")
    return jsonify({"resume": result})

@app.route("/mock-interview", methods=["POST"])
def mock_interview():
    print("[DEBUG] /mock-interview endpoint hit")
    data = request.get_json()
    print(f"[DEBUG] Request data: {data}")
    role = data.get("role", "")
    print(f"[DEBUG] Role: {role}")
    result = get_interview_questions(role)
    print(f"[DEBUG] Result: {result}")
    return jsonify({"questions": result})

@app.route("/learning-resources", methods=["POST"])
def learning_resources():
    print("[DEBUG] /learning-resources endpoint hit")
    data = request.get_json()
    print(f"[DEBUG] Request data: {data}")
    topic = data.get("topic", "")
    print(f"[DEBUG] Topic: {topic}")
    result = get_learning_resources(topic)
    print(f"[DEBUG] Result: {result}")
    return jsonify({"resources": result})





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


if __name__ == "__main__":
    print("[DEBUG] Running Flask app...")
    app.run(debug=True)
