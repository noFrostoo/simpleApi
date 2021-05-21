from datetime import datetime, timezone
from typing import List, Optional
import uuid

from sqlalchemy.orm import Session

from simpleapi.api import schemas
from . import models

def create_message(db: Session, message: schemas.MessageBase) -> models.Message:
    new_message = models.Message(**message.dict())
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    return new_message

def edit_message(db: Session, msg: schemas.Message, id: int) -> models.Message:
    message = models.Message()
    message.id = id
    message.views_count = 0
    message.content = msg.content
    rows = db.query(models.Message).filter(models.Message.id == id).update(message.dict())
    db.commit()
    return message

def delete_message(db: Session, id: int) -> bool:
    rows = db.query(models.Message).filter(models.Message.id == id).delete()
    db.commit()
    return rows != 0

def view_message(db: Session, id: int) -> models.Message:
    rows = db.query(models.Message).filter(models.Message.id == id).all()
    if rows != 0:
        pass # raise expecption
    message = rows[0]
    message.views_count += 1
    db.query(models.Message).filter(models.Message.id == id).update(message.dict())
    db.commit()
    return message

def get_message_by_id(db: Session, id: int) -> models.Message:
    rows = db.query(models.Message).filter(models.Message.id == id).all()
    if rows != 0:
        pass # raise expecption
    return rows[0] 

def get_user(db: Session, username: str) -> models.User:
    return db.query(models.User).filter(models.User.username == username).all()[0]

def add_user(db: Session, username: str, password: str) -> models.User:
    new_user = models.User()
    new_user.username = username
    new_user.password = password
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def check_msg_exists(db: Session, id: int) -> bool:
    rows = db.query(models.Message).filter(models.Message.id == id).all()
    return len(rows) != 0