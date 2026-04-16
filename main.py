import os
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from user_app.database import Base, engine
from user_app.routers import auth, inquiries, quotes
from user_app.routers import buyer_profile
from user_app.routers import seller_profile
from admin_app.routers import admin

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

Base.metadata.create_all(bind=engine)

os.makedirs(os.path.join(BASE_DIR, "uploads"), exist_ok=True)

app.mount(
    "/frontend",
    StaticFiles(directory=os.path.join(BASE_DIR, "frontend")),
    name="frontend"
)

app.mount(
    "/uploads",
    StaticFiles(directory=os.path.join(BASE_DIR, "uploads")),
    name="uploads"
)

templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

app.include_router(auth.router,           prefix="/auth")
app.include_router(inquiries.router)
app.include_router(quotes.router)
app.include_router(admin.router,          prefix="/admin")
app.include_router(buyer_profile.router)
app.include_router(seller_profile.router)

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/buyer")
def buyer_page(request: Request):
    return templates.TemplateResponse("buyer.html", {"request": request})

@app.get("/seller")
def seller_page(request: Request):
    return templates.TemplateResponse("seller.html", {"request": request})

@app.get("/admin")
def admin_page(request: Request):
    return templates.TemplateResponse("admin.html", {"request": request})

@app.get("/inquiry/{id}")
def inquiry_page(request: Request, id: int):
    return templates.TemplateResponse(
        "inquiry.html",
        {"request": request, "id": id}
    )