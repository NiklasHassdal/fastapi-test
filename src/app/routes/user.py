from fastapi import APIRouter, HTTPException, Depends
from app.db import engine, users
from app.security import TokenData, authentication_required, hash_password
from app.models.user import UserGet, UserPost
from sqlalchemy.exc import IntegrityError

router = APIRouter()


@router.get("/user", response_model=UserGet)
async def get_user(token_data: TokenData = Depends(authentication_required)):
    query = users.select(users.c.id == token_data.user_id)
    result = engine.execute(query)
    return result.fetchone()


@router.post("/sign_up", response_model=UserGet)
async def post_users(user: UserPost):
    try:
        values = user.dict()
        values["password"] = hash_password(values["password"])
        query = users.insert(values)
        result = engine.execute(query)
        return {**values, **result.inserted_primary_key}
    except IntegrityError:
        raise HTTPException(409, "User with that email already exists")
