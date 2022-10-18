from pydantic import BaseModel


class LoginPost(BaseModel):
    email: str
    password: str
