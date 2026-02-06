from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, status
from sqlalchemy.orm import Session
from utils.security import hash_password, verify_password
from config.redis_config import config
from database.database import get_db_dependency
from models.user import User
from schemas.user import UserVerify, UserSignup, OTPVerify, UserLogin
from utils.email import send_otp_email
from utils.generate_otp import generate_otp
from datetime import timedelta
from utils.token import create_access_token
from config.rate_limiting import limiter

import uuid

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/user_exists", tags=["Auth"])
@limiter.limit("5/minute")
def user_exists(
    client: UserVerify,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db_dependency),
):
    user = db.query(User).filter(User.email == client.email).first()

    if user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Email already exists"
        )

    otp = generate_otp()

    config.setex(client.email, 300, otp)

    background_tasks.add_task(
        send_otp_email,
        client.email,
        otp
    )

    return {"message": "OTP sent successfully"}


@router.post("/verify-otp", tags=["Auth"])
@limiter.limit("5/minute")
def verify_otp(data: OTPVerify):
    key = data.email
    stored_otp = config.get(key)

    if not stored_otp or stored_otp.decode() != data.otp:
        raise HTTPException(400, "Invalid or expired OTP")

    config.delete(key)

    verification_token = str(uuid.uuid4())

    config.setex(
        f"verify:{verification_token}",
        600,
        data.email
    )

    return {
        "verification_token": verification_token
    }


@router.post("/signup", tags=["Auth"])
@limiter.limit("5/minute")
def signup(
    data: UserSignup,
    verification_token: str,
    db: Session = Depends(get_db_dependency)
):
    redis_key = f"verify:{verification_token}"
    email = config.get(redis_key)

    if not email:
        raise HTTPException(403, "OTP verification required")

    if email.decode() != data.email:
        raise HTTPException(403, "Email mismatch")

    user = User(
        name=data.name,
        email=data.email,
        hashed_password=hash_password(data.password)
    )

    db.add(user)
    db.commit()

    config.delete(redis_key)

    return {"message": "User created successfully"}


@router.post("/login", tags=["Auth"])
@limiter.limit("5/minute")
def login(data: UserLogin, db: Session = Depends(get_db_dependency)):
    user = db.query(User).filter(User.email == data.email).first()

    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=timedelta(minutes=30)
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
