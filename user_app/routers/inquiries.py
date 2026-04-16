from fastapi import APIRouter, Form, HTTPException, Body, UploadFile, File
from user_app.database import SessionLocal
from user_app.models import Inquiry, Quote
from datetime import datetime
import os
import uuid

router = APIRouter()

# ---------------- FILE STORAGE SETUP ----------------

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ---------------- CREATE INQUIRY ----------------

@router.post("/inquiries")
async def create_inquiry(
    name: str = Form(...),
    mobile: str = Form(...),
    email: str = Form(...),
    category: str = Form(...),
    details: str = Form(...),
    city: str = Form(None),        # optional — buyer may not select
    company_name: str = Form(None),
    budget: str = Form(None),
    brand: str = Form(None),
    buyer_id: int = Form(...),
    file: UploadFile = File(None)
):
    db = SessionLocal()

    try:
        file_path = None

        # SAFE FILE UPLOAD — guard empty filename
        if file and file.filename:
            ext = file.filename.rsplit(".", 1)[-1] if "." in file.filename else "dat"
            unique_name = f"{uuid.uuid4()}.{ext}"
            file_location = os.path.join(UPLOAD_DIR, unique_name)

            with open(file_location, "wb") as f:
                content = await file.read()
                f.write(content)

            file_path = file_location

        inquiry = Inquiry(
            name=name,
            mobile=mobile,
            email=email,
            category=category,
            details=details,
            city=city,
            company_name=company_name,
            budget=budget,
            brand=brand,
            buyer_id=buyer_id,
            file_path=file_path
        )

        db.add(inquiry)
        db.commit()

        return {"message": "Created"}

    finally:
        db.close()


# ---------------- RESPOND TO INQUIRY ----------------

@router.post("/inquiries/{inquiry_id}/respond")
def respond_to_inquiry(inquiry_id: int, data: dict = Body(...)):
    db = SessionLocal()

    try:
        inquiry = db.query(Inquiry).filter(Inquiry.id == inquiry_id).first()

        if not inquiry:
            raise HTTPException(status_code=404, detail="Inquiry not found")

        quote = Quote(
            inquiry_id=inquiry_id,
            seller_id=data.get("seller_id"),
            buyer_id=inquiry.buyer_id,
            price=data.get("price"),
            message=data.get("message")
        )

        db.add(quote)
        db.commit()

        return {"success": True}

    finally:
        db.close()

# ---------------- GET ALL UNIQUE CITIES ----------------
@router.get("/inquiries/cities")
def get_cities():
    db = SessionLocal()

    cities = db.query(Inquiry.city).distinct().all()

    db.close()

    # flatten list of tuples
    return [c[0] for c in cities if c[0]]

# ---------------- MY INQUIRIES ----------------

@router.get("/inquiries/my/{buyer_id}")
def my_inquiries(buyer_id: int):
    db = SessionLocal()

    try:
        inquiries = db.query(Inquiry).filter(Inquiry.buyer_id == buyer_id).all()

        result = []

        for i in inquiries:
            days_passed = (datetime.utcnow() - i.created_at).days
            days_left = max(0, 7 - days_passed)

            result.append({
                "id": i.id,
                "category": i.category,
                "details": i.details,
                "company_name": i.company_name,
                "budget": i.budget,
                "days_left": days_left
            })

        return result

    finally:
        db.close()


# ---------------- ALL INQUIRIES ----------------

@router.get("/inquiries/all")
def all_inquiries():
    db = SessionLocal()

    try:
        inquiries = db.query(Inquiry).filter(Inquiry.is_closed == False).all()

        result = []

        for i in inquiries:
            days_passed = (datetime.utcnow() - i.created_at).days
            days_left = max(0, 7 - days_passed)

            quotes = db.query(Quote).filter(Quote.inquiry_id == i.id).all()

            result.append({
                "id": i.id,
                "category": i.category,
                "company_name": i.company_name,
                "city": i.city,
                "budget": i.budget,
                "details": i.details,
                "file_path": i.file_path,
                "days_left": days_left,

                "quotes": [
                    {
                        "price": q.price,
                        "message": q.message,
                        "seller_id": q.seller_id
                    }
                    for q in quotes
                ],

                "response_count": len(quotes)
            })

        return result

    finally:
        db.close()


# ---------------- FILTER INQUIRIES ----------------

@router.get("/inquiries/filter")
def filter_inquiries(category: str = None, company_name: str = None):
    db = SessionLocal()

    try:
        query = db.query(Inquiry)

        if category:
            query = query.filter(Inquiry.category == category)

        if company_name:
            query = query.filter(Inquiry.company_name == company_name)

        inquiries = query.all()

        result = []

        for i in inquiries:
            days_passed = (datetime.utcnow() - i.created_at).days
            days_left = max(0, 7 - days_passed)

            result.append({
                "id": i.id,
                "category": i.category,
                "company_name": i.company_name,
                "budget": i.budget,
                "days_left": days_left
            })

        return result

    finally:
        db.close()


# ---------------- FILTER META ----------------

@router.get("/inquiries/meta")
def get_filter_meta():
    db = SessionLocal()

    try:
        categories = db.query(Inquiry.category).distinct().all()
        companies = db.query(Inquiry.company_name).distinct().all()

        return {
            "categories": [c[0] for c in categories if c[0]],
            "companies": [c[0] for c in companies if c[0]]
        }

    finally:
        db.close()


# ---------------- GET SINGLE INQUIRY ----------------

@router.get("/inquiries/{id}")
def get_inquiry(id: int):
    db = SessionLocal()

    try:
        inquiry = db.query(Inquiry).filter(Inquiry.id == id).first()

        if not inquiry:
            raise HTTPException(status_code=404, detail="Inquiry not found")

        return inquiry

    finally:
        db.close()


# ---------------- DELETE INQUIRY ----------------

@router.delete("/inquiries/{inquiry_id}")
def delete_inquiry(inquiry_id: int, buyer_id: int):
    db = SessionLocal()

    try:
        inquiry = db.query(Inquiry).filter(
            Inquiry.id == inquiry_id,
            Inquiry.buyer_id == buyer_id
        ).first()

        if not inquiry:
            raise HTTPException(status_code=404, detail="Inquiry not found")

        db.delete(inquiry)
        db.commit()

        return {"message": "Deleted successfully"}

    finally:
        db.close()