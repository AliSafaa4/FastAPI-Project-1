
from pydantic import BaseModel, EmailStr  # type: ignore # Schema/pydantic Models define the structure of a request & response.
from datetime import datetime
from typing import Optional

from pydantic.types import conint

class UserCreate(BaseModel):
    name:str
    email:EmailStr
    password:str

class UserResponse(BaseModel):
    name:str
    email:str
    created_at:datetime

    class Config:
        from_attributes=True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class PostBase(BaseModel):
    title: str   #This model here is to validation the data That the user has send.
    content: str # So here we defined the two string variable if we try to send diffrent type that will cause an error. 
    published: bool = True

class PostCreate(PostBase):
    pass

class Post(PostBase): #response model
    id: int
    user_id : int
    created_at: datetime
    user: UserResponse

    class Config:
        from_attributes=True

class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None

class Vote(BaseModel):
    post_id: int
    dir: bool = 0