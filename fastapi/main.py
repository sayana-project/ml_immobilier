from fastapi import FastAPI
from .routes.routes import router


#python -m uvicorn fastapi.main:app --reload --port 8003

app = FastAPI(
    title="real estate Prediction price",
    description="The purpose of the API is a real state prediction price",
)

app.include_router(router)