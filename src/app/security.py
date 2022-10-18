from os import getenv
from datetime import datetime, timedelta, timezone
from typing import Any
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext
from jose import jwt
from redis import Redis

from app.models.token import TokenData, TokenPair


secret = getenv("JWT_SECRET")
algorithm = getenv("JWT_ALGORITHM") or "HS256"
access_token_expiry = getenv("JWT_ACCESS_TOKEN_EXPIRY") or 900
refresh_token_expiry = getenv("JWT_REFRESH_TOKEN_EXPIRY") or 604800
redis_host = getenv("REDIS_HOST")
redis_port = getenv("REDIS_PORT") or 6379

pwd_context = CryptContext(schemes=["bcrypt"])
oauth2_scheme = HTTPBearer(auto_error=False)
redis = Redis(host=redis_host, port=redis_port)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hash: str) -> bool:
    return pwd_context.verify(password, hash)


def encode_jwt(payload: TokenData) -> str:
    return jwt.encode(payload.dict(), secret, algorithm=algorithm)


def decode_jwt(token: str, expected_type: str = None) -> TokenData:
    try:
        payload = jwt.decode(token, secret, algorithms=[algorithm])
        token_data = TokenData(**payload)
    except:
        raise HTTPException(403, "Invalid token")
    if expected_type and token_data.type != expected_type:
        raise HTTPException(403, "Expected '%s' but got '%s'" % (expected_type, token_data.type))
    if datetime.now(timezone.utc) > token_data.exp:
        raise HTTPException(403, "Token has expired")
    if redis.get(token):
        raise HTTPException(403, "Token has been revoked")
    return token_data


def revoke_token(token: str) -> bool:
    token_data: TokenData = decode_jwt(token)
    duration = token_data.exp - datetime.now(timezone.utc)
    if duration >= timedelta(0):
        redis.setex(token, duration, "revoked")


def create_access_token(user: Any) -> str:
    token_data = TokenData(
        type="access_token",
        exp=datetime.now(timezone.utc) + timedelta(0, access_token_expiry),
        user_id=user.id,
    )
    return encode_jwt(token_data)


def create_refresh_token(user: Any) -> str:
    token_data = TokenData(
        type="refresh_token",
        exp=datetime.now(timezone.utc) + timedelta(0, refresh_token_expiry),
        user_id=user.id,
    )
    return encode_jwt(token_data)


def create_tokens(user: Any) -> TokenPair:
    return {
        "access_token": create_access_token(user),
        "refresh_token": create_refresh_token(user),
    }


def authentication_required(auth: HTTPAuthorizationCredentials | None = Depends(oauth2_scheme)) -> TokenData:
    if not auth:
        raise HTTPException(403, "Missing authorization header")
    return decode_jwt(auth.credentials, "access_token")


def authentication_optional(auth: HTTPAuthorizationCredentials | None = Depends(oauth2_scheme)) -> TokenData | None:
    try:
        return authentication_required(auth)
    except:
        return None
