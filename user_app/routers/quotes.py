from fastapi import APIRouter
from user_app.database import SessionLocal
from user_app.models import Quote, Inquiry, User, SellerProfile

router = APIRouter()


# ── SEND QUOTE ────────────────────────────────────────────
@router.post("/quotes/send")
def send_quote(data: dict):
    db = SessionLocal()
    new_quote = Quote(
        inquiry_id = data.get("inquiry_id"),
        seller_id  = data.get("seller_id"),
        buyer_id   = data.get("buyer_id"),
        price      = data.get("price"),
        message    = data.get("message"),
    )
    db.add(new_quote)
    db.commit()
    db.refresh(new_quote)
    db.close()
    return {"success": True, "message": "Quote sent"}


# ── GET BUYER QUOTES (with full seller contact info) ──────
@router.get("/quotes/buyer/{buyer_id}")
def get_quotes(buyer_id: int):
    db = SessionLocal()
    quotes = db.query(Quote).filter(Quote.buyer_id == buyer_id).all()

    result = []
    for q in quotes:
        inquiry       = db.query(Inquiry).filter(Inquiry.id == q.inquiry_id).first()
        seller_user   = db.query(User).filter(User.id == q.seller_id).first()
        seller_profile= db.query(SellerProfile).filter(SellerProfile.seller_id == q.seller_id).first()

        result.append({
            "id":       q.id,
            "price":    q.price,
            "message":  q.message,
            "status":   q.status,

            # inquiry info
            "inquiry_id":  q.inquiry_id,
            "category":    inquiry.category if inquiry else "",
            "details":     inquiry.details  if inquiry else "",

            # seller contact — profile first, fallback to user email
            "seller_name":     seller_profile.name     if seller_profile else "",
            "seller_email":    seller_profile.email    if seller_profile else (seller_user.email if seller_user else "Unknown"),
            "seller_mobile":   seller_profile.mobile   if seller_profile else "",
            "seller_company":  seller_profile.company  if seller_profile else "",
            "seller_location": seller_profile.location if seller_profile else "",
        })

    db.close()
    return result


# ── REJECT QUOTE ──────────────────────────────────────────
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


# ── ACCEPT QUOTE ──────────────────────────────────────────
# Buyer accepts one quote →
#   • That quote status → "accepted"
#   • Inquiry marked is_closed = True, accepted_seller_id set
#   • All OTHER quotes on that inquiry are deleted
#   • Inquiry disappears from sellers' open lists
@router.post("/quotes/accept/{id}")
def accept_quote(id: int):
    db = SessionLocal()
    quote = db.query(Quote).filter(Quote.id == id).first()
    if not quote:
        db.close()
        return {"success": False, "message": "Quote not found"}

    # mark this quote accepted
    quote.status = "accepted"

    # close the inquiry
    inquiry = db.query(Inquiry).filter(Inquiry.id == quote.inquiry_id).first()
    if inquiry:
        inquiry.is_closed          = True
        inquiry.accepted_seller_id = quote.seller_id

    # delete all other quotes for this inquiry
    db.query(Quote).filter(
        Quote.inquiry_id == quote.inquiry_id,
        Quote.id != id
    ).delete()

    db.commit()
    db.close()
    return {"success": True, "message": "Quote accepted"}


# ── ALL QUOTES (dashboard stats) ─────────────────────────
@router.get("/quotes/all")
def get_all_quotes():
    db     = SessionLocal()
    quotes = db.query(Quote).all()
    result = [{"id": q.id, "price": q.price, "seller_id": q.seller_id,
               "buyer_id": q.buyer_id, "inquiry_id": q.inquiry_id} for q in quotes]
    db.close()
    return result


# ── SELLER STATS ──────────────────────────────────────────
@router.get("/seller/stats/{seller_id}")
def seller_stats(seller_id: int):
    db          = SessionLocal()
    quotes_count = db.query(Quote).filter(Quote.seller_id == seller_id).count()
    db.close()
    return {"quotes_sent": quotes_count, "products_count": 0}


# ── SELLER QUOTES ─────────────────────────────────────────
@router.get("/quotes/seller/{seller_id}")
def get_seller_quotes(seller_id: int):
    db     = SessionLocal()
    quotes = db.query(Quote).filter(Quote.seller_id == seller_id).all()

    result = []
    for q in quotes:
        inquiry = db.query(Inquiry).filter(Inquiry.id == q.inquiry_id).first()
        result.append({
            "id":           q.id,
            "inquiry_id":   q.inquiry_id,
            "category":     inquiry.category     if inquiry else "",
            "price":        q.price,
            "message":      q.message,
            "status":       q.status,
            "company_name": inquiry.company_name if inquiry else "",
            "city":         inquiry.city         if inquiry else "",
        })

    db.close()
    return result