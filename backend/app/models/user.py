from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class UserPreferences(BaseModel):
    use_gifs: bool = True
    scheduled_messages: bool = True
    voice_style: str = "default"
    active_hours: List[int] = []

class User(BaseModel):
    user_id: str
    discord_id: str
    preferences: UserPreferences
    created_at: datetime = datetime.utcnow()
    last_active: datetime = datetime.utcnow()