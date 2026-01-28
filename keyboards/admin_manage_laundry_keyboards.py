from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from database.db import get_machine_names


def get_machines_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text=name, callback_data="empty")] for name in get_machine_names()]
    )

