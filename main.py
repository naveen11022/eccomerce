from api.auth import router as user_router
from api.order import router as order_router
from api.product import router as product_router
from api.cart import router as cart_router
from database.database import Base, Engine
from fastapi import FastAPI
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler
from config.rate_limiting import limiter

app = FastAPI()

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

app = FastAPI(title="Ecommerce API")

app.include_router(user_router)
app.include_router(order_router)
app.include_router(product_router)
app.include_router(cart_router)


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=Engine)


@app.get("/")
async def root():
    return {"api": "ecommerce API"}
