# 🛒 Ecommerce Backend API (FastAPI)

Production-ready Ecommerce Backend built using **FastAPI**, **MySQL**, **Redis**, **Celery**, and **JWT Authentication**.

---

## 🚀 Tech Stack

- FastAPI – Web framework
- MySQL – Primary database
- SQLAlchemy – ORM
- Redis – OTP, Cart cache, Rate limiting
- Celery – Background tasks (emails, order processing)
- JWT – Authentication
- SlowAPI – Rate limiting
- Docker – Containerization

---

## 📁 Project Structure

eccomerce/
├── api/
│   ├── auth.py
│   ├── cart.py
│   ├── order.py
│   └── product.py
│
├── config/
│   ├── database.py
│   ├── redis_config.py
│   ├── celery_app.py
│   ├── rate_limit.py
│   └── settings.py
│
├── models/
│   ├── user.py
│   ├── product.py
│   ├── order.py
│
├── schemas/
│   ├── user.py
│   ├── product.py
│   ├── cart.py
│   └── order.py
│
├── utils/
│   ├── security.py
│   ├── email.py
│   ├── generate_otp.py
│   └── token.py
│
├── main.py
├── .env
├── .gitignore
└── README.md

---

## 🔐 Authentication Flow

1. User enters email
2. OTP sent via email
3. OTP verification
4. Verification token generated
5. Signup allowed only with token
6. Password hashed using bcrypt
7. JWT issued on login

✔ Prevents fake signup  
✔ Only verified users stored in DB  

---

## 📦 Features Implemented

### ✅ Authentication
- Signup with OTP verification
- Login with JWT
- Password hashing (bcrypt)
- Rate-limited endpoints

### ✅ Cart (Redis)
- Cart stored per user
- Add / Remove / Update items
- Redis → DB sync during order

### ✅ Order
- Cart → Order conversion
- Stock reduction logic
- Idempotency key (prevents double order)

### ✅ Background Tasks (Celery)
- OTP email sending
- Order confirmation email
- Async execution

### ✅ Rate Limiting
- OTP → 3/min
- Login → 5/min
- Order → 10/min

---

## ⚙️ Environment Variables (.env)

DATABASE_URL=mysql+pymysql://user:password@localhost:3306/ecommerce  
REDIS_URL=redis://localhost:6379/0  

JWT_SECRET_KEY=supersecret  
JWT_ALGORITHM=HS256  
ACCESS_TOKEN_EXPIRE_MINUTES=60  

EMAIL_HOST=smtp.gmail.com  
EMAIL_PORT=587  
EMAIL_USER=yourmail@gmail.com  
EMAIL_PASSWORD=app_password  

CELERY_BROKER_URL=redis://localhost:6379/1  
CELERY_RESULT_BACKEND=redis://localhost:6379/1  

---

## ▶️ Run Project Locally

### 1️⃣ Create Virtual Environment
python -m venv venv  
venv\Scripts\activate  

### 2️⃣ Install Dependencies
pip install -r requirements.txt  

### 3️⃣ Run FastAPI
uvicorn main:app --reload  

### 4️⃣ Run Redis
redis-server  

### 5️⃣ Run Celery Worker
celery -A config.celery_app worker --loglevel=info  

---

## 🧪 API Documentation

Swagger UI  
http://127.0.0.1:8000/docs  

Redoc  
http://127.0.0.1:8000/redoc  

---

## 🛡️ Security Best Practices

- Password hashing (bcrypt)
- OTP verification before signup
- JWT authentication
- Rate limiting
- Redis TTL for OTP & cart
- Idempotency keys for orders

---

## 🐳 Docker (Optional)

docker-compose up --build  

---

## 💡 Production Notes

- Disable `/docs` in production
- Use HTTPS
- Store secrets in ENV
- Use Redis for caching & rate limiting
- Use Nginx as reverse proxy

---

## 📄 License

MIT License

---

🔥 Built for real-world production ecommerce systems
