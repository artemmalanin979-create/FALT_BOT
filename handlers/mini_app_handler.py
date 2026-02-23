from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo, MenuButtonWebApp
from database.db import is_registered
from config import MINI_APP_URL

mini_app_router = Router()

def _mini_app_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🧺 Открыть Mini App", web_app=WebAppInfo(url=MINI_APP_URL))],
        [InlineKeyboardButton(text="📋 Мои записи", callback_data="laundry_my")],
        [InlineKeyboardButton(text="💰 Кошелёк", callback_data="wallet")],
    ])

@mini_app_router.message(Command("miniapp"))
async def cmd_miniapp(message: Message):
    if not MINI_APP_URL:
        await message.answer("Mini App пока недоступен.")
        return
    user = is_registered(message.from_user.id)
    if not user:
        await message.answer("Сначала зарегистрируйтесь через /start")
        return
    if not user.email:
        await message.answer("Для Mini App нужен email. Используйте /setemail")
        return
    await message.answer(f"Привет, {user.name}! Откройте Mini App:", reply_markup=_mini_app_kb())

@mini_app_router.message(Command("bookings"))
async def cmd_bookings(message: Message):
    await message.answer("Ваши записи:", reply_markup=InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📋 Посмотреть записи", callback_data="laundry_my")]
    ]))
