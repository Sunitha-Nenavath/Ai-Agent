import os
import json
from dotenv import load_dotenv
from mistralai import Mistral

load_dotenv()

api_key = os.getenv("MISTRAL_API_KEY")
client = Mistral(api_key=api_key)
model_name = "mistral-large-latest"

def analyze_resume(text):
    prompt = f"""
    Analyze the following resume and return the analysis STRICTLY in JSON format.
    Do not include markdown blocks like ```json ... ```, just the raw JSON object.

    The JSON must contain the following keys:
    {{
        "skills_identified": ["skill1", "skill2"],
        "missing_skills": ["missing1", "missing2"],
        "career_recommendations": ["role1", "role2"],
        "improvement_suggestions": ["suggestion1", "suggestion2"]
    }}

    Resume:
    {text}
    """
    try:
        response = client.chat.complete(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        result = response.choices[0].message.content.strip()
        if result.startswith("```json"):
            result = result[7:-3].strip()
        elif result.startswith("```"):
            result = result[3:-3].strip()
        return json.loads(result)
    except Exception as e:
        error_msg = str(e).lower()
        if "429" in error_msg or "rate limit" in error_msg:
            return {"error": "You have exceeded the Mistral API rate limit. Please wait a moment before trying again."}
        return {"error": "Failed to parse AI response into JSON", "raw": str(e)}

def get_skill_gaps(current_skills, target_role):
    prompt = f"""
    Analyze the skill gaps for a user aiming for the role of '{target_role}'.
    Current Skills: {', '.join(current_skills)}

    Return the analysis STRICTLY in JSON format without markdown blocks.
    The JSON must contain:
    {{
        "missing_skills": ["skill1", "skill2"],
        "learning_resources": ["resource1", "resource2"],
        "certifications": ["cert1", "cert2"]
    }}
    """
    try:
        response = client.chat.complete(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        result = response.choices[0].message.content.strip()
        if result.startswith("```json"):
            result = result[7:-3].strip()
        elif result.startswith("```"):
            result = result[3:-3].strip()
        return json.loads(result)
    except Exception as e:
        error_msg = str(e).lower()
        if "429" in error_msg or "rate limit" in error_msg:
            return {"error": "You have exceeded the Mistral API rate limit. Please wait a moment before trying again."}
        return {"error": "Failed to parse AI response into JSON"}

def generate_roadmap(profile_data):
    prompt = f"""
    Generate a learning roadmap based on the user's profile.
    Profile: {json.dumps(profile_data)}
    
    Return the analysis STRICTLY in JSON format without markdown blocks.
    The JSON must contain:
    {{
        "roadmap": [
            {{
                "step": 1,
                "title": "Phase Title",
                "description": "What to learn",
                "technologies": ["tech1", "tech2"]
            }}
        ]
    }}
    """
    try:
        response = client.chat.complete(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        result = response.choices[0].message.content.strip()
        if result.startswith("```json"):
            result = result[7:-3].strip()
        elif result.startswith("```"):
            result = result[3:-3].strip()
        return json.loads(result)
    except Exception as e:
        error_msg = str(e).lower()
        if "429" in error_msg or "rate limit" in error_msg:
            return {"error": "You have exceeded the Mistral API rate limit. Please wait a moment before trying again."}
        return {"error": "Failed to parse AI response into JSON"}

def chat_with_mentor(message, history):
    # Prepare history format for Mistral
    messages = []
    messages.append({"role": "system", "content": "You are an AI Career Mentor for the VidyaGuide platform. Help the user with their career, resume, and skills."})
    
    for h in history:
        # Assuming history is list of dicts with role and parts (from old gemini code)
        # Gemini roles: 'user' and 'model'. Mistral roles: 'user' and 'assistant'
        role = "assistant" if h.get("role") == "model" else h.get("role", "user")
        messages.append({"role": role, "content": h.get("parts", "")})
        
    messages.append({"role": "user", "content": message})
    
    try:
        response = client.chat.complete(
            model=model_name,
            messages=messages
        )
        return response.choices[0].message.content
    except Exception as e:
        error_msg = str(e).lower()
        if "429" in error_msg or "rate limit" in error_msg:
            return "I'm currently receiving too many questions and hit my rate limit! Please wait a moment before asking me another question."
        print(f"Mistral chat error: {e}")
        return "I encountered an error trying to respond. Please try again."
