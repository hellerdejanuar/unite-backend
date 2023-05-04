from fastapi import FastAPI
from routes.user import userAPI
from routes.event import eventAPI
from routes.group import groupAPI
from routes.channel import channelAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware
from config.db import meta, engine

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8100",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(userAPI)
app.include_router(eventAPI)
app.include_router(groupAPI)
app.include_router(channelAPI)

meta.create_all(engine)
