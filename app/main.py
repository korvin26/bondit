from fastapi import FastAPI
from app.api.v1.endpoints import flights

app = FastAPI()

app.include_router(flights.router, prefix="/api/v1")
