from fastapi import FastAPI

app = FastAPI()

from app import routes
from app.chat import routes
