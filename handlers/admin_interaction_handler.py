from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message, FSInputFile
from aiogram.enums.content_type import ContentType
from keyboards.keyboards import get_start_kb
from database.db import User, add_user
import os
from database.db import set_registration_click_status
from sources.generate_file import generate_file

admin_router = Router()


@admin_router.callback_query(F.data.contains("registration_admin_accept"))
async def accepting_registration(call : CallbackQuery):
    data = call.data.split()
    user_id = data[0]
    name = " ".join(data[1:-2])
    surname = data[-2]
    user = User(user_id, name, surname)
    add_user(user)
    await call.bot.edit_message_caption(message_id=call.message.message_id, chat_id=call.message.chat.id, caption="Заявка одобрена", reply_markup=None)
    await call.bot.send_photo(user_id, photo=FSInputFile("falt.jpg"), caption="Вы были успешно зарегистрированы!", reply_markup=get_start_kb())


@admin_router.callback_query(F.data.contains("registration_admin_decline"))
async def declining_registration(call : CallbackQuery):
    data = call.data.split()
    try:
        user_id, name, surname = data[:-1]
        user_id = int(user_id)
        await call.bot.edit_message_caption(message_id=call.message.message_id, chat_id=call.message.chat.id, caption="Заявка отклонена", reply_markup=None)
        await call.bot.send_message(user_id, "Ваша заявка на регистрацию отклонена!", reply_markup=get_start_kb())
    except:
        user_id = int(data[0])
        await call.bot.edit_message_caption(message_id=call.message.message_id, chat_id=call.message.chat.id, caption="Заявка отклонена", reply_markup=None)
        await call.bot.send_message(user_id, "Неправильный формат!!!", reply_markup=get_start_kb())
    set_registration_click_status(user_id)


@admin_router.callback_query(F.data.contains("studyroom_record_admin_decline"))
async def declining_registration(call : CallbackQuery):
    user_id = int(call.data.split()[0])
    await call.bot.edit_message_text(message_id=call.message.message_id, chat_id=call.message.chat.id, text=f"{call.message.text}\n\nЗаявка отклонена", reply_markup=None)
    await call.bot.send_photo(user_id, photo=FSInputFile("falt.jpg"), caption="Ваша заявка на бронирование боталки отклонена!", reply_markup=get_start_kb())


@admin_router.callback_query(F.data.contains("studyroom_record_admin_accept"))
async def declining_registration(call : CallbackQuery):
    user_id = int(call.data.split()[0])
    await call.bot.edit_message_text(message_id=call.message.message_id, chat_id=call.message.chat.id, text=f"{call.message.html_text}\n\nЗаявка одобрена", reply_markup=None, parse_mode="html")
    await call.bot.send_photo(user_id, photo=FSInputFile("falt.jpg"), caption="Ваша заявка на бронирование боталки принята!", reply_markup=get_start_kb())

    try:
        path = await generate_file(call.message.text)
        await call.bot.send_document(user_id, document=FSInputFile(path), caption="Распечатайте данный файл и повесьте на дверь боталки, чтобы остальные знали, что она забронирована. Лучше сделать это заранее")
        try:
            os.remove(path)
        except OSError:
            pass
    except Exception:
        pass
