
import os
from openai import OpenAI

client = None

def setup_openai():
    global client
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def complete_prompt(prompt, model="gpt-3.5-turbo", max_tokens=512):
    """Legacy function for backward compatibility"""
    messages = [
        {"role": "user", "content": prompt}
    ]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=max_tokens
    )
    return response.choices[0].message.content.strip()

def agentic_completion(system_prompt, user_prompt, model="gpt-3.5-turbo", max_tokens=512):
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=max_tokens
    )
    return {
        "content": response.choices[0].message.content.strip(),
        "usage": response.usage,
        "id": response.id,
        "model": response.model
    }
