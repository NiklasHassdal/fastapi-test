from pydantic import BaseModel

class UserGet(BaseModel):
    id: int
    name: str
    email: str