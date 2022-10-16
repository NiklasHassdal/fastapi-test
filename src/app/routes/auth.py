from fastapi import APIRouter, HTTPException
from app.db import engine, users
from app.security import create_tokens, decode_jwt, verify_password, TokenPair
from app.models.auth import LoginPost, RefreshToken

router = APIRouter()


@router.post("/auth/login", response_model=TokenPair)
async def post_login(credentials: LoginPost):
    query = users.select(users.c.email == credentials.email)
    result = engine.execute(query)
    user = result.fetchone()
    if user and verify_password(credentials.password, user.password):
        return create_tokens(user)
    else:
        raise HTTPException(403, "Wrong email or password")


@router.post("/auth/refresh", response_model=TokenPair)
async def post_refresh(token: RefreshToken):
    token_data = decode_jwt(token.refresh_token, "refresh_token")
    query = users.select(users.c.id == token_data.user_id)
    result = engine.execute(query)
    user = result.fetchone()
    if user:
        return create_tokens(user)
    else:
        raise HTTPException(403, "User doesn't exist")
