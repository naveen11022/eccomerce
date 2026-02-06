import smtplib
from email.message import EmailMessage
import os

EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")


def send_otp_email(to_email: str, otp: str):
    msg = EmailMessage()
    msg["Subject"] = "Your Signup OTP Code"
    msg["From"] = EMAIL_USER
    msg["To"] = to_email
    msg.set_content(f"Your OTP is: {otp}")

    with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)


def send_mail(to_email: str, subject: str, body: str):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = EMAIL_USER
    msg["To"] = to_email
    msg.set_content(body)
    with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)