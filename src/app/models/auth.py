from datetime import datetime
from pydantic import BaseModel


class LoginPost(BaseModel):
    email: str
    password: str


class RefreshToken(BaseModel):
    refresh_token: str
