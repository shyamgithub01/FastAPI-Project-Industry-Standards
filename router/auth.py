from fastapi import  APIRouter , HTTPException , status , Depends
from db import database
from sqlalchemy.orm import Session
from models import model
from passlib.context import CryptContext
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from utils import oauth2
from schemas import token

router = APIRouter(
    tags=["Login"]
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



@router.post("/login" , response_model=token.Token)
def user_login(usercredential: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(model.Users).filter(model.Users.email == usercredential.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    if not pwd_context.verify(usercredential.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    access_token = oauth2.create_access_token(data = {"user_id" : user.id})
    return {"access_token": access_token, "token_type": "bearer"}
