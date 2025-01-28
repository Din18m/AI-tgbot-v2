from config import bot
from datetime import datetime


async def dislike(id_student: int, id_teacher: int, window: dict):
    await bot.send_message(
        chat_id=id_student,
        text=f"Ваша заявка {id_teacher} на окно: {datetime.strftime(window["time"], "%d.%m %H:%M")} {window['description']} была отвергнута")


async def like(id_student: int, id_teacher: int, window: dict):
    await bot.send_message(
        chat_id=id_student,
        text=f"Ваша заявка {id_teacher} на окно: {datetime.strftime(window["time"], "%d.%m %H:%M")} {window['description']} была принята")
