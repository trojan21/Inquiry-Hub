from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean
from datetime import datetime, timedelta
from user_app.database import Base

class PasswordResetOTP(Base):
    __tablename__ = "password_reset_otp"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, index=True)
    otp = Column(String)
    expires_at = Column(DateTime)

class Quote(Base):
    __tablename__ = "quotes"

    id = Column(Integer, primary_key=True, index=True)

    inquiry_id = Column(Integer)
    seller_id = Column(Integer)
    buyer_id = Column(Integer)
    status = Column(String, default="pending")  # pending / rejected
    price = Column(Float)
    message = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    password = Column(String)
    role = Column(String)
    status = Column(String, default="approved")  # pending for sellers
    is_approved = Column(Boolean, default=False)

class Inquiry(Base):
    __tablename__ = "inquiries"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String)
    mobile = Column(String)
    email = Column(String)

    category = Column(String)
    details = Column(Text)

    city = Column(String)
    hotel = Column(String)
    brand = Column(String)
    company_name = Column(String)
    budget = Column(String)
    profile_link = Column(String)
    file_path = Column(String, nullable=True)
    # image_path = Column(String)

    buyer_id = Column(Integer)

    # ✅ FIXED: moved inside model
    created_at = Column(DateTime, default=datetime.utcnow)