
from utils.openai_helper import agentic_completion

def get_career_advice(query):
    system_prompt = "You are an expert AI career coach."
    user_prompt = f"Give detailed, personalized career advice for: {query}"
    result = agentic_completion(system_prompt, user_prompt)
    return result["content"]