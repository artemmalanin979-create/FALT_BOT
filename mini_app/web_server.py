import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
import re
from database.db import get_user_by_email, create_mini_app_session, validate_session, get_wallet_balance, debit_wallet, get_machine_names, get_machine_status
from config import CORS_ORIGINS, LAUNDRY_PRICE_PER_HOUR_WASH_RUB, LAUNDRY_PRICE_PER_HOUR_DRY_RUB

app = FastAPI(title="FALT Laundry Mini App", version="2.0")
app.add_middleware(CORSMiddleware, allow_origins=CORS_ORIGINS, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

_static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(_static_dir):
    app.mount("/static", StaticFiles(directory=_static_dir), name="static")

class LoginRequest(BaseModel):
    email: EmailStr

class BookingSlot(BaseModel):
    date: str
    machine_id: str
    start_time: str
    end_time: str

class MultiBookingRequest(BaseModel):
    bookings: List[BookingSlot]

async def get_current_user(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")
    user_id = validate_session(authorization.split(" ", 1)[1])
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid session")
    return user_id

@app.get("/", response_class=HTMLResponse)
async def serve_index():
    template = os.path.join(os.path.dirname(__file__), "templates", "index.html")
    if os.path.exists(template):
        with open(template, encoding="utf-8") as f:
            return f.read()
    return "<h1>FALT Mini App</h1>"

@app.post("/api/auth/login")
async def login(req: LoginRequest):
    user = get_user_by_email(req.email)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    token = create_mini_app_session(user.user_id)
    return {"success": True, "token": token, "user": {"id": user.user_id, "name": user.name, "surname": user.surname, "email": user.email, "wallet": get_wallet_balance(user.user_id)}}

@app.get("/api/machines")
async def get_machines():
    machines = []
    for name in get_machine_names():
        m = re.search(r"(\d+)", name)
        mid = m.group(1) if m else name
        is_dryer = "сушилка" in name.lower()
        price = int(LAUNDRY_PRICE_PER_HOUR_DRY_RUB or 75) if is_dryer else int(LAUNDRY_PRICE_PER_HOUR_WASH_RUB or 75)
        machines.append({"id": mid, "name": name, "is_working": get_machine_status(name), "is_dryer": is_dryer, "price_per_hour": price})
    return machines

@app.get("/api/wallet/balance")
async def balance(user_id: int = Depends(get_current_user)):
    return {"balance": get_wallet_balance(user_id)}

@app.post("/api/bookings/pay")
async def pay(req: MultiBookingRequest, user_id: int = Depends(get_current_user)):
    machines = {m["id"]: m for m in await get_machines()}
    total = sum(int(((datetime.strptime(b.end_time, "%H:%M") - datetime.strptime(b.start_time, "%H:%M")).total_seconds() / 3600) * machines[b.machine_id]["price_per_hour"]) for b in req.bookings if b.machine_id in machines)
    if get_wallet_balance(user_id) < total:
        raise HTTPException(status_code=400, detail="Недостаточно средств")
    if not debit_wallet(user_id, total, "laundry_booking"):
        raise HTTPException(status_code=400, detail="Ошибка списания")
    return {"success": True, "charged": total, "new_balance": get_wallet_balance(user_id)}

@app.get("/api/health")
async def health():
    return {"status": "ok"}
