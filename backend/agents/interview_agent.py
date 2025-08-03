
from utils.openai_helper import agentic_completion

def get_interview_questions(role):
    system_prompt = "You are an expert AI interviewer."
    user_prompt = f"Generate challenging and relevant mock interview questions for the role: {role}"
    result = agentic_completion(system_prompt, user_prompt)
    return result["content"]
