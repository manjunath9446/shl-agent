# app/models.py
from pydantic import BaseModel, validator
from typing import List, Literal, Optional

class Message(BaseModel):
    role: Literal["user", "assistant"]
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]
    
    @validator("messages")
    def messages_not_empty(cls, v):
        if not v:
            raise ValueError("messages cannot be empty")
        if v[-1].role != "user":
            raise ValueError("last message must be from user")
        return v

class Recommendation(BaseModel):
    name: str
    url: str
    test_type: str

class ChatResponse(BaseModel):
    reply: str
    recommendations: List[Recommendation]
    end_of_conversation: bool