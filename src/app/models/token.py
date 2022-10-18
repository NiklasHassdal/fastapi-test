from datetime import datetime
from pydantic import BaseModel


class TokenData(BaseModel):
    type: str
    exp: datetime
    user_id: int


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
