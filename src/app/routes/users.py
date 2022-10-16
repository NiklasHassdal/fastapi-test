from fastapi import APIRouter
from typing import List
from app.models.users import UserGet

router = APIRouter()


@router.get("/users", response_model=List[UserGet])
async def get_users():
    users = [
        UserGet(id=1, name="Test User", email="example@example.com"),
    ]
    return users
