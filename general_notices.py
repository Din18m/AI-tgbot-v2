from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

from db import db_teacher as db
from config import bot, dp


async def say_about_requests():
    requests = db.get_all_requests()

    for request in requests:
        await bot.send_message(
            chat_id=request['id_teacher'],
            text=f"У вас {request['cnt']} непрочитанных заявок",
            reply_markup=kb_notify())


async def delete_windows_expired():
    db.delete_windows_expired()


def kb_notify():
    buttons = [
        [InlineKeyboardButton(text="ок", callback_data="ok_notify")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard



