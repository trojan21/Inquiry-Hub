"""
buyer_profile.py — Buyer profile endpoints

GET  /buyer/profile/{buyer_id}   → returns saved profile or 404
PUT  /buyer/profile/{buyer_id}   → upsert profile (create or update)
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session
from datetime import datetime

from user_app.database import get_db
from user_app.models import BuyerProfile

router = APIRouter()


class ProfileData(BaseModel):
    name:    str
    mobile:  Optional[str] = None
    email:   Optional[str] = None
    company: Optional[str] = None
    link:    Optional[str] = None


@router.get("/buyer/profile/{buyer_id}")
def get_profile(buyer_id: int, db: Session = Depends(get_db)):
    profile = db.query(BuyerProfile).filter(BuyerProfile.buyer_id == buyer_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return {
        "buyer_id": profile.buyer_id,
        "name":     profile.name,
        "mobile":   profile.mobile,
        "email":    profile.email,
        "company":  profile.company,
        "link":     profile.link,
    }


@router.put("/buyer/profile/{buyer_id}")
def upsert_profile(buyer_id: int, data: ProfileData, db: Session = Depends(get_db)):
    profile = db.query(BuyerProfile).filter(BuyerProfile.buyer_id == buyer_id).first()

    if profile:
        # Update existing
        profile.name       = data.name
        profile.mobile     = data.mobile
        profile.email      = data.email
        profile.company    = data.company
        profile.link       = data.link
        profile.updated_at = datetime.utcnow()
    else:
        # Create new
        profile = BuyerProfile(
            buyer_id = buyer_id,
            name     = data.name,
            mobile   = data.mobile,
            email    = data.email,
            company  = data.company,
            link     = data.link,
        )
        db.add(profile)

    db.commit()
    return {"success": True, "message": "Profile saved"}