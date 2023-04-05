from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel
from pydantic import EmailStr, Field


class UserRole(str, Enum):
    Admin = 'admin'
    Moderator = 'moderator'
    User = 'user'


class UserBase(BaseModel):
    username: str = Field(min_length=2, max_length=15)
    first_name: str = Field(min_length=2, max_length=15)
    last_name: str = Field(min_length=2, max_length=15)
    email: EmailStr


class UserCreate(UserBase):
    username: str = Field(min_length=2, max_length=25)
    email: EmailStr
    password: str = Field(min_length=6)


class UserModel(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime
    number_of_photos: int
    is_active: bool
    user_role: UserRole

    class Config:
        orm_mode = True


class TagBase(BaseModel):
    tag: str


class TagCreate(TagBase):
    pass


class TagModel(TagBase):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    user_id: Optional[int]

    class Config:
        orm_mode = True


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    

class PostBase(BaseModel):
    photo_url: str
    description: Optional[str]
    tags: Optional[List[TagBase]]


class PostCreate(PostBase):
    pass


class PostModel(PostBase):
    id: int
    created_at: datetime
    updated_at: datetime
    user_id: int
    tags: Optional[List[TagModel]]

    class Config:
        orm_mode = True


class CommentBase(BaseModel):
    comment_url: Optional[str]
    comment_text: Optional[str]


class CommentCreate(CommentBase):
    pass


class CommentModel(CommentBase):
    id: int
    created_at: datetime
    updated_at: datetime
    user_id: int
    post_id: int

    class Config:
        orm_mode = True