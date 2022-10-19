from os import system
from time import sleep
from fastapi import FastAPI
from app.db import engine
from app.routes import token, user

while True:
    try:
        conn = engine.connect()
        conn.close()
        break
    except:
        sleep(1)

system("alembic upgrade head")

app = FastAPI()
app.include_router(user.router, prefix="/api/v1")
app.include_router(token.router, prefix="/api/v1")
