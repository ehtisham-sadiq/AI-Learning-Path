from pydantic import BaseModel, EmailStr, conint
from datetime import datetime


# all the important entities in our system
# 1. UserCreate
# 2. User
# 3. UserLogin
# 4. Post
# 5. PostBase(title, content, published)
# 6. CreatePost
# 7. Vote(Post_id, user_id)
# 8. PostoUT
 

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    
    
class User(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        orm_mode = True # here orm_mode is set to True to allow pydantic to use the model as a base for the schema
    
class UserLogin(BaseModel):
    username: str
    password: str
    
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    
class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: User
    class Config:
        orm_mode = True # here orm_mode is set to True to allow pydantic to use the model as a base for the schema
    
    
class PostOut(BaseModel): # used for returning details along with the number of votes
    Post: Post
    votes: int
    
    class Config:
        orm_mode = True # here orm_mode is set to True to allow pydantic to use the model as a base for the schema
    
class Token(BaseModel):
    access_token: str
    token_type: str 
    
class TokenData(BaseModel):
    id: str
    username: str
    
class Vote(BaseModel): # represents the vote on a post
    post_id: int
    direction: conint(le=1) # here conint is a constraint that ensures the direction is an integer, and le is less than or equal to 1