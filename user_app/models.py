from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean
from datetime import datetime
from user_app.database import Base


class PasswordResetOTP(Base):
    __tablename__ = "password_reset_otp"
    id         = Column(Integer, primary_key=True, index=True)
    email      = Column(String, index=True)
    otp        = Column(String)
    expires_at = Column(DateTime)


class BuyerProfile(Base):
    __tablename__ = "buyer_profiles"
    id         = Column(Integer, primary_key=True, index=True)
    buyer_id   = Column(Integer, unique=True, index=True)
    name       = Column(String)
    mobile     = Column(String)
    email      = Column(String)
    company    = Column(String, nullable=True)
    link       = Column(String, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class SellerProfile(Base):
    """Saved once — shown to buyer when they receive a quote."""
    __tablename__ = "seller_profiles"
    id         = Column(Integer, primary_key=True, index=True)
    seller_id  = Column(Integer, unique=True, index=True)
    name       = Column(String)
    mobile     = Column(String)
    email      = Column(String)
    location   = Column(String, nullable=True)
    company    = Column(String, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Quote(Base):
    __tablename__ = "quotes"
    id         = Column(Integer, primary_key=True, index=True)
    inquiry_id = Column(Integer)
    seller_id  = Column(Integer)
    buyer_id   = Column(Integer)
    status     = Column(String, default="pending")  # pending / accepted / rejected
    price      = Column(Float)
    message    = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)


class User(Base):
    __tablename__ = "users"
    id          = Column(Integer, primary_key=True, index=True)
    email       = Column(String, unique=True)
    password    = Column(String)
    role        = Column(String)
    status      = Column(String, default="approved")
    is_approved = Column(Boolean, default=False)


class Inquiry(Base):
    __tablename__ = "inquiries"
    id                 = Column(Integer, primary_key=True, index=True)
    name               = Column(String)
    mobile             = Column(String)
    email              = Column(String)
    category           = Column(String)
    details            = Column(Text)
    city               = Column(String)
    hotel              = Column(String)
    brand              = Column(String)
    company_name       = Column(String)
    budget             = Column(String)
    profile_link       = Column(String)
    file_path          = Column(String, nullable=True)
    buyer_id           = Column(Integer)
    created_at         = Column(DateTime, default=datetime.utcnow)
    is_closed          = Column(Boolean, default=False)
    accepted_seller_id = Column(Integer, nullable=True)