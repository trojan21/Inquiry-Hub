import smtplib
from email.mime.text import MIMEText
import os

def send_otp_email(to_email, otp):
    subject = "Your OTP for Password Reset"
    body = f"""
Your OTP is: {otp}

This OTP is valid for 5 minutes.
Do not share it with anyone.
"""

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = os.getenv("EMAIL_USER")
    msg["To"] = to_email

    with smtplib.SMTP(os.getenv("EMAIL_HOST"), int(os.getenv("EMAIL_PORT"))) as server:
        server.starttls()
        server.login(os.getenv("EMAIL_USER"), os.getenv("EMAIL_PASS"))
        server.send_message(msg)