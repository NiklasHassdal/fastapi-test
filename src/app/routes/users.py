from fastapi import APIRouter, HTTPException
from typing import List
from app.db import engine, users
from app.security import hash_password
from app.models.users import UserGet, UserPost
from sqlalchemy.exc import IntegrityError

router = APIRouter()


@router.get("/users", response_model=List[UserGet])
async def get_users():
    query = users.select()
    result = engine.execute(query)
    return result.fetchall()


@router.post("/users", response_model=UserGet)
async def post_users(user: UserPost):
    try:
        values = user.dict()
        values["password"] = hash_password(values["password"])
        query = users.insert(values)
        result = engine.execute(query)
        return {**values, **result.inserted_primary_key}
    except IntegrityError:
        raise HTTPException(409, "User with that email already exists")
