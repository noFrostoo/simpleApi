import uvicorn

from typing import List, Optional
from datetime import datetime, timedelta
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from jose import JWTError, jwt
from passlib.context import CryptContext

from .api import schemas
from .database import crud, models
from .database.setup import SessionLocal, engine
from .authorizationsUtils import authenticate_user, create_access_token, get_current_user
models.Base.metadata.create_all(bind=engine)

SECRET_KEY = "6466ad884a1a601c5ab6610e1d2ac9b46a42a07258e2b8a370b2b66b5a1d095d"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="authorize")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



#* AUTHORIZATION UTILS
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)

def authenticate_user(db: Session, username: str, password: str):
    user = crud.get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = crud.get_user(get_db(), username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


#* APP UTILS
def check_message_len(content: str):
    if len(content) == 0:
        raise HTTPException(status_code=400, detail='Non zero length message is required')
    if len(content) >= 160:
        raise HTTPException(status_code=413, detail='Content is too large, max length = 160')

def check_message_exists(db:Session ,message_id: int):
    if not crud.check_msg_exists(db, message_id):
        raise HTTPException(status_code=404, detail='Message of this id does not exists')




@app.post('/new', response_model=schemas.Message, responses={400: {"model": schemas.HTTPError}, 413: {"model": schemas.HTTPError}})
def new_message(message: schemas.MessageBase, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    check_message_len(message.content)
    return crud.create_message(db, message)

@app.put('/{message_id}', response_model=schemas.Message, responses={400: {"model": schemas.HTTPError}, 413: {"model": schemas.HTTPError}, 404: {"model": schemas.HTTPError}})
def edit_message(message_id:int, message: schemas.MessageBase, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    check_message_exists(db, message_id)
    check_message_len(message.content)
    return crud.edit_message(db, message, message_id)

@app.delete('/{message_id}', response_model=bool, responses={404: {"model": schemas.HTTPError}})
def delete_message(message_id:int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    check_message_exists(db, message_id)
    return crud.delete_message(db, message_id)

@app.get('/{message_id}', response_model=schemas.Message, responses={404: {"model": schemas.HTTPError}})
def view_message(message_id:int, db: Session = Depends(get_db)):
    check_message_exists(db, message_id)
    return crud.view_message(db, message_id)

@app.post("/authorize", response_model=schemas.Token, responses={401: {"model": schemas.HTTPError}})
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get('/')
def welcome(db: Session = Depends(get_db)):
    return { 'msg' : 'Hello World'}

def main():
    uvicorn.run('simpleapi:app', host='0.0.0.0', port=8080, reload=True)