from pydantic import BaseModel, EmailStr
from typing import Optional


# USER
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        from_attributes = True


# JOB
class JobBase(BaseModel):
    title: str
    company: str
    location: str
    description: str


class JobCreate(JobBase):
    pass


class JobUpdate(JobBase):
    pass


class JobResponse(JobBase):
    id: int

    class Config:
        from_attributes = True


# TOKEN
class Token(BaseModel):
    access_token: str
    token_type: str