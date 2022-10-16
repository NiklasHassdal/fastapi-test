from time import sleep
from fastapi import FastAPI
from app.db import metadata, engine
from app.routes import users

while True:
    try:
        metadata.create_all(engine)
        break
    except:
        sleep(1)

app = FastAPI()
app.include_router(users.router, prefix="/api/v1")
