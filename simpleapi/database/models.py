from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, ForeignKey, Integer, PickleType, String
from sqlalchemy.orm import relationship

from .setup import Base


class Message(Base):
    __tablename__ = 'messages'
    
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    views_count = Column(Integer, nullable=False, default=0)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship('User', back_populates='messages')

    def dict(self):
        return {
            "id": self.id,
            "content": self.content,
            "views_count": self.views_count
        }


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    password = Column(String)

    messages = relationship('Message', back_populates='user')
