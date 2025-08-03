
from utils.openai_helper import agentic_completion

def get_learning_resources(topic):
    system_prompt = "You are an expert AI learning advisor."
    user_prompt = f"Suggest the best online resources, courses, and books for learning: {topic}"
    result = agentic_completion(system_prompt, user_prompt)
    return result["content"]
