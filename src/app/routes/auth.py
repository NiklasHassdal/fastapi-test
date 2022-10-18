from fastapi import APIRouter, HTTPException, Body
from app.db import engine, users
from app.security import create_tokens, decode_jwt, revoke_token, verify_password, TokenPair
from app.models.auth import LoginPost

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


@router.post("/token/refresh", response_model=TokenPair)
async def post_refresh(token: TokenPair):
    token_data = decode_jwt(token.refresh_token, "refresh_token")
    query = users.select(users.c.id == token_data.user_id)
    result = engine.execute(query)
    user = result.fetchone()
    if user:
        revoke_token(token.refresh_token)
        revoke_token(token.access_token)
        return create_tokens(user)
    else:
        raise HTTPException(403, "User doesn't exist")


@router.post("/token/revoke")
async def post_revoke(token: str = Body()):
    revoke_token(token)
