from dotenv import load_dotenv
from celery import Celery
from utils.email import send_mail
import os
load_dotenv()

celery_app = Celery(
    "tasks",
    broker=os.getenv("CELERY_BROKER_URL"),
    backend=os.getenv("CELERY_RESULT_BACKEND"),
)


@celery_app.task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=5,
    retry_kwargs={"max_retries": 3}
)
def send_order_email(self, email: str, order_id: int):
    send_mail(
        to=email,
        subject="Order Confirmation",
        body=f"Your order #{order_id} has been placed successfully"
    )

