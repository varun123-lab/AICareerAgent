
from utils.openai_helper import agentic_completion

def generate_resume_bullets(experience):
    system_prompt = "You are an expert AI resume writer."
    user_prompt = f"Generate strong, achievement-focused resume bullet points for this experience: {experience}"
    result = agentic_completion(system_prompt, user_prompt)
    return result["content"]
