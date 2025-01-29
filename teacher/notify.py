from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

from config import bot, dp
from datetime import datetime


async def dislike(id_student: int, id_teacher: int, window: dict):
    await bot.send_message(
        chat_id=id_student,
        text=f"Ваша заявка {id_teacher} на окно: {datetime.strftime(window["time"], "%d.%m %H:%M")} {window['description']} была отвергнута",
        reply_markup=kb_notify())


async def like(id_student: int, id_teacher: int, window: dict):
    await bot.send_message(
        chat_id=id_student,
        text=f"Ваша заявка {id_teacher} на окно: {datetime.strftime(window["time"], "%d.%m %H:%M")} {window['description']} была принята",
        reply_markup=kb_notify())


@dp.callback_query(lambda query: query.data == "ok_notify")
async def delete_setting_teacher(callback: CallbackQuery):
    await callback.message.delete()


def kb_notify():
    buttons = [
        [InlineKeyboardButton(text="ок", callback_data="ok_notify")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
