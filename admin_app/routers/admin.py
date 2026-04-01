from fastapi import APIRouter
from user_app.database import SessionLocal
from user_app.models import User

router = APIRouter()

# GET pending sellers
@router.get("/sellers/")
def get_pending_sellers():
    db = SessionLocal()
    sellers = db.query(User).filter(
        User.role == "seller",
        User.status == "pending"
    ).all()
    db.close()
    return sellers


# GET all users (approved sellers + others)
@router.get("/sellers/all")
def get_all_users():
    db = SessionLocal()

    users = db.query(User).filter(
        (User.role != "seller") | (User.status == "approved")
    ).all()

    db.close()
    return users


# APPROVE seller
@router.post("/sellers/approve/{id}")
def approve_seller(id: int):
    db = SessionLocal()
    user = db.query(User).filter(User.id == id).first()

    if not user:
        db.close()
        return {"message": "User not found"}

    user.status = "approved"   # ✅ FIXED
    db.commit()
    db.close()

    return {"message": "Seller approved"}


# REJECT seller
@router.post("/sellers/reject/{id}")
def reject_seller(id: int):
    db = SessionLocal()
    user = db.query(User).filter(User.id == id).first()

    if not user:
        db.close()
        return {"message": "User not found"}

    db.delete(user)
    db.commit()
    db.close()

    return {"message": "Seller rejected"}


# DELETE user
@router.delete("/sellers/delete/{id}")
def delete_user(id: int):
    db = SessionLocal()
    user = db.query(User).filter(User.id == id).first()

    if not user:
        db.close()
        return {"message": "User not found"}

    db.delete(user)
    db.commit()
    db.close()

    return {"message": "User deleted"}