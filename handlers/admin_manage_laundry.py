from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from keyboards.admin_manage_laundry_keyboards import get_machines_kb
from config import ADMIN_CHAT_ID

manage_laundry_router = Router()


@manage_laundry_router.message(Command("manage_laundry"))
async def manage_laundry(message: Message):
    if str(message.chat.id) == ADMIN_CHAT_ID:
        await message.answer("Выберите машину:", reply_markup=get_machines_kb())
