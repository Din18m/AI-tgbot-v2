from config import bot

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

from db import db_teacher as db
from config import schedule, bot, dp


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

async def notify_before_interview(id_teacher, nick_tch, id_student, nick_st, window):
    datetime_obj = window['time']
    date = datetime_obj.strftime("%d.%m")
    time = datetime_obj.strftime("%H:%M")
    description = window['description']
    await bot.send_message(chat_id=id_teacher, text=)
    await bot.send_message(chat_id=id_student, text=)


NOTIFY_TEXT="""
Напоминание.
Вы записаны на собеседование
{} в {}
Описание:
{}

Никнейм для связи - {}
"""