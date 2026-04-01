from fastapi import APIRouter
from user_app.database import SessionLocal
from user_app.models import Quote, Inquiry, User

router = APIRouter()

# ---------------- SEND QUOTE ----------------
@router.post("/quotes/send")
def send_quote(data: dict):
    db = SessionLocal()

    new_quote = Quote(
        inquiry_id=data.get("inquiry_id"),
        seller_id=data.get("seller_id"),
        buyer_id=data.get("buyer_id"),
        price=data.get("price"),
        message=data.get("message")
    )

    db.add(new_quote)
    db.commit()
    db.refresh(new_quote)

    db.close()

    return {"success": True, "message": "Quote sent"}


# ---------------- GET BUYER QUOTES ----------------
@router.get("/quotes/buyer/{buyer_id}")
def get_quotes(buyer_id: int):
    db = SessionLocal()

    quotes = db.query(Quote).filter(Quote.buyer_id == buyer_id).all()

    result = []
    for q in quotes:
        inquiry = db.query(Inquiry).filter(Inquiry.id == q.inquiry_id).first()
        seller = db.query(User).filter(User.id == q.seller_id).first()

        result.append({
            "id": q.id,
            "price": q.price,
            "message": q.message,

            "seller_email": seller.email if seller else "Unknown",  # 🔥 FIX
            "category": inquiry.category if inquiry else "",
            "details": inquiry.details if inquiry else ""
        })

    db.close()
    return result


# ---------------- REJECT QUOTE ----------------
@router.post("/quotes/reject/{id}")
def reject_quote(id: int):
    db = SessionLocal()

    quote = db.query(Quote).filter(Quote.id == id).first()

    if not quote:
        db.close()
        return {"message": "Quote not found"}

    db.delete(quote)
    db.commit()
    db.close()

    return {"message": "Quote rejected"}

# ---------------- ALL QUOTES (FOR DASHBOARD STATS) ----------------
@router.get("/quotes/all")
def get_all_quotes():
    db = SessionLocal()

    quotes = db.query(Quote).all()

    result = []
    for q in quotes:
        result.append({
            "id": q.id,
            "price": q.price,
            "seller_id": q.seller_id,
            "buyer_id": q.buyer_id,
            "inquiry_id": q.inquiry_id
        })

    db.close()
    return result

# ---------------- SELLER STATS ----------------
@router.get("/seller/stats/{seller_id}")
def seller_stats(seller_id: int):
    db = SessionLocal()

    quotes_count = db.query(Quote).filter(Quote.seller_id == seller_id).count()

    db.close()

    return {
        "quotes_sent": quotes_count,
        "products_count": 0
    }


# ---------------- SELLER QUOTES ----------------
@router.get("/quotes/seller/{seller_id}")
def get_seller_quotes(seller_id: int):
    db = SessionLocal()

    quotes = db.query(Quote).filter(Quote.seller_id == seller_id).all()

    result = []
    for q in quotes:
        inquiry = db.query(Inquiry).filter(Inquiry.id == q.inquiry_id).first()

        result.append({
            "id": q.id,
            "category": inquiry.category if inquiry else "",
            "price": q.price,
            "message": q.message,
            "company_name": inquiry.company_name if inquiry else "",
            "city": inquiry.city if inquiry else ""
        })

    db.close()
    return result