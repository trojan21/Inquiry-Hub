"""
seller_profile.py — Seller profile endpoints

GET  /seller/profile/{seller_id}  → returns saved profile or 404
PUT  /seller/profile/{seller_id}  → upsert (create or update)
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session
from datetime import datetime

from user_app.database import get_db
from user_app.models import SellerProfile

router = APIRouter()


class SellerProfileData(BaseModel):
    name:     str
    mobile:   Optional[str] = None
    email:    Optional[str] = None
    location: Optional[str] = None
    company:  Optional[str] = None


@router.get("/seller/profile/{seller_id}")
def get_profile(seller_id: int, db: Session = Depends(get_db)):
    p = db.query(SellerProfile).filter(SellerProfile.seller_id == seller_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Profile not found")
    return {
        "seller_id": p.seller_id,
        "name":      p.name,
        "mobile":    p.mobile,
        "email":     p.email,
        "location":  p.location,
        "company":   p.company,
    }


@router.put("/seller/profile/{seller_id}")
def upsert_profile(seller_id: int, data: SellerProfileData, db: Session = Depends(get_db)):
    p = db.query(SellerProfile).filter(SellerProfile.seller_id == seller_id).first()
    if p:
        p.name     = data.name
        p.mobile   = data.mobile
        p.email    = data.email
        p.location = data.location
        p.company  = data.company
        p.updated_at = datetime.utcnow()
    else:
        p = SellerProfile(
            seller_id = seller_id,
            name      = data.name,
            mobile    = data.mobile,
            email     = data.email,
            location  = data.location,
            company   = data.company,
        )
        db.add(p)
    db.commit()
    return {"success": True}