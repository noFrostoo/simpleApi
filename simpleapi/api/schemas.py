
from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel

class MessageBase(BaseModel):
    # id: Optional[int]
    content: str


class Message(MessageBase):
    id: int
    views_count : int

    class Config:
        orm_mode = True

class User(BaseModel):
    id: int
    username: str
    password: str
    notes: List[Message]

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None