from pydantic import BaseModel
from typing import List, Optional

class UserProfile(BaseModel):
    name: str
    education: str
    current_skills: List[str]
    career_interest: str

class ChatMessage(BaseModel):
    message: str
    history: Optional[List[dict]] = []

class SkillGapRequest(BaseModel):
    current_skills: List[str]
    target_role: str
