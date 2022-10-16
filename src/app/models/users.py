from pydantic import BaseModel


class UserGet(BaseModel):
    id: int
    name: str
    email: str


class UserPost(BaseModel):
    name: str
    email: str
    password: str
