from fastapi import APIRouter, HTTPException, Depends
from app.db import engine, users
from app.security import TokenData, TokenPair, authentication_required, create_tokens, hash_password, verify_password
from app.models.user import UserGet, UserPost, LoginPost
from sqlalchemy.exc import IntegrityError

router = APIRouter()


@router.get("/user", response_model=UserGet)
async def get_user(token_data: TokenData = Depends(authentication_required)):
    query = users.select(users.c.id == token_data.user_id)
    result = engine.execute(query)
    return result.fetchone()


@router.post("/user/sign_up", response_model=UserGet)
async def post_users(user: UserPost):
    try:
        values = user.dict()
        values["password"] = hash_password(values["password"])
        query = users.insert(values)
        result = engine.execute(query)
        return {**values, **result.inserted_primary_key}
    except IntegrityError:
        raise HTTPException(409, "User with that email already exists")


@router.post("/user/login", response_model=TokenPair)
async def post_login(credentials: LoginPost):
    query = users.select(users.c.email == credentials.email)
    result = engine.execute(query)
    user = result.fetchone()
    if user and verify_password(credentials.password, user.password):
        return create_tokens(user)
    else:
        raise HTTPException(403, "Wrong email or password")
