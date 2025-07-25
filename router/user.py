from fastapi import APIRouter, HTTPException, status, Depends
from schemas import user
from db import database
from sqlalchemy.orm import Session
from models import users
from passlib.context import CryptContext
from utils import oauth2

router = APIRouter(
    tags=["User"]
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post('/users', response_model=user.UserOut)
def create_user(
    user_data: user.CreateUser,
    db: Session = Depends(database.get_db),
    current_user: int = Depends(oauth2.get_current_user)
):
    if len(user_data.password) <= 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be more than 8 characters"
        )

    existing_user = db.query(users.Users).filter(users.Users.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    hashed_password = pwd_context.hash(user_data.password)
    user_data.password = hashed_password

    new_user = users.Users(**user_data.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user



@router.get('/users/{id}', response_model=user.UserOut)
def get_one_user(id: int, db: Session = Depends(database.get_db)
                 ,current_user: int = Depends(oauth2.get_current_user)):
    user = db.query(users.Users).filter(users.Users.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user



@router.put("/users/{id}", response_model=user.UserOut)
def update_user(id: int, updated_data: user.CreateUser, db: Session = Depends(database.get_db)
                ,current_user: int = Depends(oauth2.get_current_user)):
    user_query = db.query(users.Users).filter(users.Users.id == id)
    user = user_query.first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    
    email_owner = db.query(users.Users).filter(users.Users.email == updated_data.email).first()
    if email_owner and email_owner.id != id:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already in use")

    updated_data.password = pwd_context.hash(updated_data.password)
    user_query.update(updated_data.model_dump(), synchronize_session=False)
    db.commit()

    return user_query.first()



@router.delete("/users/{id}")
def delete_user(id: int, db: Session = Depends(database.get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    user = db.query(users.Users).filter(users.Users.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    db.delete(user)
    db.commit()

    return {"message": f"User with id {id} deleted successfully"}
