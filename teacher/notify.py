import asyncio

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pytz import timezone

from config import bot, dp, schedule
from datetime import datetime, timedelta

from db.db_student import interview_marking_for_students, interview_marking_for_teachers


async def dislike(id_student: int, id_teacher: int, window: dict):
    await bot.send_message(
        chat_id=id_student,
        text=f"Ваша заявка {id_teacher} на окно: {datetime.strftime(window["time"], "%d.%m %H:%M")} "
             f"{window['description']} была отвергнута",
        reply_markup=kb_notify())

def before(id_student, nickname_student, id_teacher, nickname_teacher, window):
    loop = asyncio.get_running_loop()
    loop.create_task(notify_before_interview(id_student, nickname_student, id_teacher, nickname_teacher, window))

def after(id_student, nickname_student, id_teacher, nickname_teacher, window):
    loop = asyncio.get_running_loop()
    loop.create_task(notify_after_interview(id_student, nickname_student, id_teacher, nickname_teacher, window))


async def like(id_student: int, id_teacher: int, window: dict, nickname_teacher: str, nickname_student: str):
    time = window["time"]
    delta = timedelta(minutes=60)
    time_before = time - delta
    time_after = time + delta

    schedule.add_job(before(id_student, nickname_student, id_teacher, nickname_teacher, window),
                     run_date=time_before)

    schedule.add_job(after(id_student, nickname_student, id_teacher, nickname_teacher, window),
                     run_date=time_after)
    await bot.send_message(
        chat_id=id_student,
        text=f"Ваша заявка {id_teacher} на окно: {datetime.strftime(window["time"], "%d.%m %H:%M")} "
             f"{window['description']} была принята",
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

def teacher_marks_kb(id_student) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="Собеседник пришел", callback_data=f"{id_student}_came_student_mark")],
        [InlineKeyboardButton(text="Собеседник не пришел =(", callback_data=f"{id_student}_passed_student_mark")],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def student_marks_kb(id_teacher) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="Собеседник пришел", callback_data=f"{id_teacher}_came_teacher_mark")],
        [InlineKeyboardButton(text="Собеседник не пришел =(", callback_data=f"{id_teacher}_passed_teacher_mark")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


async def notify_before_interview(id_teacher, nick_tch, id_student, nick_st, window):
    datetime_obj = window['time']
    date = datetime_obj.strftime("%d.%m")
    time = datetime_obj.strftime("%H:%M")
    description = window['description']
    await bot.send_message(chat_id=id_teacher, text=NOTIFY_TEXT.format(date, time, description, nick_st), reply_markup=kb_notify())
    await bot.send_message(chat_id=id_student, text=NOTIFY_TEXT.format(date, time, description, nick_tch), reply_markup=kb_notify())


async def notify_after_interview(id_teacher, nick_tch, id_student, nick_st, window):
    datetime_obj = window['time']
    date = datetime_obj.strftime("%d.%m")
    time = datetime_obj.strftime("%H:%M")
    await bot.send_message(chat_id=id_teacher, text=NOTIFY_TEXT_after.format(nick_st, date, time), reply_markup=teacher_marks_kb(id_student))
    await bot.send_message(chat_id=id_student, text=NOTIFY_TEXT_after.format(nick_tch, date, time), reply_markup=student_marks_kb(id_teacher))

NOTIFY_TEXT="""
Напоминание.
Вы записаны на собеседование
{} в {}
Описание:
{}

Никнейм для связи - @{}
"""

NOTIFY_TEXT_after="""
Вы были записаны на собеседование
{} в {}
с {}

Нажмите, пожалуйста, на соответствующую\n кнопку
"""

@dp.callback_query(lambda c: c.data.split("_")[-1] == "mark")
async def teacher_marks_came(callback: CallbackQuery):
    who = callback.data.split("_")[-2]
    what = callback.data.split("_")[-3]
    id_ = int(callback.data.split("_")[-4])
    if who == "student":
        await interview_marking_for_students(id_, what)
    else:
        await interview_marking_for_teachers(id_, what)

    await bot.delete_message(callback.message.chat.id, callback.message.message_id)