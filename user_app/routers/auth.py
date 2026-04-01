from fastapi import APIRouter, Depends, BackgroundTasks
from pydantic import BaseModel
from user_app.database import SessionLocal
from user_app.models import User
import random
from datetime import datetime, timedelta
from user_app.models import PasswordResetOTP, User
from user_app.email_utils import send_otp_email
from sqlalchemy.orm import Session
from user_app.database import get_db

router = APIRouter()

# SCHEMAS
class RegisterData(BaseModel):
    email: str
    password: str
    role: str

class LoginData(BaseModel):
    email: str
    password: str
    role: str


# REGISTER
@router.post("/register")
def register(data: RegisterData):
    db = SessionLocal()

    if data.role == "admin":
        db.close()
        return {"success": False, "message": "Admin cannot register"}

    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        db.close()
        return {"success": False, "message": "User already exists"}

    # ✅ SINGLE SOURCE OF TRUTH
    status = "pending" if data.role == "seller" else "approved"

    user = User(
        email=data.email,
        password=data.password,
        role=data.role,
        status=status
    )

    db.add(user)
    db.commit()
    db.close()

    return {"success": True, "message": "Registered successfully"}


# LOGIN
@router.post("/login")
def login(data: LoginData):
    db = SessionLocal()

    # admin login
    if data.email == "admin" and data.password == "admin@123" and data.role == "admin":
        db.close()
        return {"success": True, "role": "admin", "user_id": 0}

    user = db.query(User).filter(
        User.email == data.email,
        User.password == data.password,
        User.role == data.role
    ).first()

    if not user:
        db.close()
        return {"success": False, "message": "Invalid credentials"}

    # ✅ BLOCK UNAPPROVED SELLERS
    if data.role == "seller" and user.status != "approved":
        db.close()
        return {"success": False, "message": "Waiting for admin approval"}

    db.close()

    return {
        "success": True,
        "role": user.role,
        "user_id": user.id,
        "email": user.email
    }

#FORGOT PASSWORD
@router.post("/forgot-password")
def forgot_password(
    data: dict,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    email = data.get("email")

    user = db.query(User).filter(User.email == email).first()
    if not user:
        return {"success": False, "message": "User not found"}

    otp = str(random.randint(100000, 999999))

    db.query(PasswordResetOTP).filter(
        PasswordResetOTP.email == email
    ).delete()

    otp_entry = PasswordResetOTP(
        email=email,
        otp=otp,
        expires_at=datetime.utcnow() + timedelta(minutes=5)
    )

    db.add(otp_entry)
    db.commit()

    # 🚀 SEND IN BACKGROUND
    background_tasks.add_task(send_otp_email, email, otp)

    return {"success": True}
#VERIFY OTP
@router.post("/verify-otp")
def verify_otp(data: dict, db: Session = Depends(get_db)):
    email = data.get("email")
    otp = data.get("otp")

    record = db.query(PasswordResetOTP).filter(
        PasswordResetOTP.email == email,
        PasswordResetOTP.otp == otp
    ).first()

    if not record:
        return {"success": False, "message": "Invalid OTP"}

    if record.expires_at < datetime.utcnow():
        return {"success": False, "message": "OTP expired"}

    return {"success": True}

#RESET PASSWORD
@router.post("/reset-password")
def reset_password(data: dict, db: Session = Depends(get_db)):
    email = data.get("email")
    new_password = data.get("new_password")

    user = db.query(User).filter(User.email == email).first()
    if not user:
        return {"success": False}

    user.password = new_password  # (hash later if needed)
    db.commit()

    db.query(PasswordResetOTP).filter(PasswordResetOTP.email == email).delete()
    db.commit()

    return {"success": True}