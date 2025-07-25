from pydantic import BaseModel , EmailStr ,ConfigDict


class CreateUser(BaseModel):
    
    name : str
    email : EmailStr
    password : str
    
    model_config = ConfigDict(from_attributes=True)

class UserOut(BaseModel):
    id : int
    name : str
    email : EmailStr

    model_config = ConfigDict(from_attributes=True) 

class UserLogin(BaseModel):
    email :EmailStr
    password : str

