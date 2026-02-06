from fastapi import FastAPI
from api.auth import router as user_router
from database.database import Base, Engine

app = FastAPI(title="Ecommerce API")

app.include_router(user_router)


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=Engine)


@app.get("/")
async def root():
    return {"api": "ecommerce API"}
