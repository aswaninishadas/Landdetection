from typing import Optional

from pydantic.main import BaseModel


class User(BaseModel):
    firstName: str
    lastName: str
    email: str
    userName: str
    phoneNumber: int
    password: str

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class UserLogin(BaseModel):
    userName: str
    password: str


class Member(BaseModel):
    memberId: int = None
    firstName: str = None
    lastName: str = None
    age: int = None
    cardNumber: int = None
    maritalStatus: bool = None
    spouse: int = None
    landOwnedInCent: float = None

    class Config:
        orm_mode = True


class TokenData(BaseModel):
    userName: Optional[str]