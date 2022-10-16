from time import sleep
from fastapi import FastAPI
from app.db import metadata, engine
from app.routes import user, auth

while True:
    try:
        metadata.create_all(engine)
        break
    except:
        sleep(1)

app = FastAPI()
app.include_router(user.router, prefix="/api/v1")
app.include_router(auth.router, prefix="/api/v1")
