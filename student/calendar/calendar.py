"""
Реализация 'расписания' для студента
"""
from aiogram.types import CallbackQuery

from config import dp, bot
from db.db_student import get_student_windows, cancel_student_window
from student.calendar.keyboard import calendar_kb, return_to_calendar_kb, cancel_windows_kb, agreement_kb



@dp.callback_query(lambda c: c.data == "calendar")
async def calendar(callback: CallbackQuery):
    await bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="Здесь ты можешь увидеть настройки календаря =)))))))",
        reply_markup=calendar_kb()
    )

@dp.callback_query(lambda c: c.data == "look_windows")
async def look_windows(callback: CallbackQuery):
    all_student_windows = await get_student_windows(callback.from_user.id)
    if all_student_windows:
        text="Окна на которые ты записан:\n\n"
        for i in range(len(all_student_windows)):
            window=all_student_windows[i]
            datetime_obj=window["time"]
            date=datetime_obj.strftime("%d.%m")
            time=datetime_obj.strftime("%H:%M")
            text+= f"{i+1}) {date} в {time} ({window["description"]}), преподаватель - @{window["t_nickname"]}\n"
    else:
        text="Ты пока никуда не записан =("

    await bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=text,
        reply_markup=return_to_calendar_kb()
    )


@dp.callback_query(lambda c: c.data == "cancel_windows")
async def cancel_windows(callback: CallbackQuery):
    windows = await get_student_windows(callback.from_user.id)
    if windows:
        text=("Выбери окно, которое хочешь отменить\nи "
              "нажми на соответствующий\nпорядковый номер на клавиатуре\n"
              "(учти, тебя за это трахнут)\n\n")
        for i in range(len(windows)):
            window=windows[i]
            datetime_obj=window["time"]
            date=datetime_obj.strftime("%d.%m")
            time=datetime_obj.strftime("%H:%M")
            text+= f"{i+1}) {date} в {time} ({window["description"]}), преподаватель - @{window["t_nickname"]}\n"
    else:
        text="Тебе нечего отменять, абалдуй"

    await bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=text,
        reply_markup=cancel_windows_kb(len(windows))
    )


@dp.callback_query(lambda c: c.data.split("_")[-1] == "cancel")
async def cancel_chosen_window(callback: CallbackQuery):
    window_index = int(callback.data.split("_")[0])
    window_id = (await get_student_windows(callback.from_user.id))[window_index]["window_id"]
    await bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="Вы уверены, что хотите отменить окно?",
        reply_markup=agreement_kb(window_id)
    )


@dp.callback_query(lambda c: c.data.split("_")[-1] == "agree")
async def agree_chosen_window_cancel(callback: CallbackQuery):
    window_id = int(callback.data.split("_")[0])
    await cancel_student_window(callback.from_user.id, window_id)
    await bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="Окно успешно отменено =)",
        reply_markup=return_to_calendar_kb()
    )