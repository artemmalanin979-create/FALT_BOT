import os
from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import (
    Message,
    CallbackQuery,
    FSInputFile,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from keyboards.keyboards import get_main_menu_kb

main_router = Router()


@main_router.message(CommandStart())
async def start_message(message: Message):
    photo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "falt.jpg")
    if not os.path.exists(photo_path):
        await message.answer("Добро пожаловать в Сервисы ФАЛТ 2.0!", reply_markup=get_main_menu_kb(message.chat.id))
        return
    await message.answer_photo(
        photo=FSInputFile(photo_path),
        caption="Добро пожаловать в Сервисы ФАЛТ 2.0!",
        reply_markup=get_main_menu_kb(message.chat.id),
    )


@main_router.callback_query(F.data == "start_from_button")
async def start_message_from_button(call: CallbackQuery):
    photo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "falt.jpg")
    if not os.path.exists(photo_path):
        await call.message.delete()
        await call.message.answer("Добро пожаловать в Сервисы ФАЛТ 2.0!", reply_markup=get_main_menu_kb(call.message.chat.id))
        return
    # Удаляем старое сообщение и отправляем новое фото вместо редактирования
    await call.message.delete()
    await call.message.answer_photo(
        photo=FSInputFile(photo_path),
        caption="Добро пожаловать в Сервисы ФАЛТ 2.0!",
        reply_markup=get_main_menu_kb(call.message.chat.id),
    )


@main_router.callback_query(F.data == "cancel")
async def cancel_action(call: CallbackQuery):
    photo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "falt.jpg")
    if not os.path.exists(photo_path):
        await call.message.delete()
        await call.message.answer("Добро пожаловать в Сервисы ФАЛТ 2.0!", reply_markup=get_main_menu_kb(call.message.chat.id))
        return
    # То же самое для кнопки отмены
    await call.message.delete()
    await call.message.answer_photo(
        photo=FSInputFile(photo_path),
        caption="Добро пожаловать в Сервисы ФАЛТ 2.0!",
        reply_markup=get_main_menu_kb(call.message.chat.id),
    )


@main_router.callback_query(F.data == "support")
async def support(call: CallbackQuery):
    await call.message.edit_caption(
        caption="При возникновении проблем с ботом писать сюда: @zgeorgin",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="◀️ Назад", callback_data="start_from_button"
                    )
                ]
            ]
        ),
    )
