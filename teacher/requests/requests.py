from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from datetime import datetime

from config import dp
from db import db_teacher as db
import const
from teacher.requests import keyboard as kb


@dp.callback_query(lambda query: query.data == "my_students_teacher")
async def my_students_teacher(callback: CallbackQuery, state: FSMContext):
    requests = db.get_requests(callback.from_user.id)
    await state.update_data(requests=requests, id=0)
    request = requests[0]
    window = request["window"]
    student = request["student"]
    await callback.message.edit_text(text=const.StudentData.format(window["time"].strftime("%d.%m"),
                                                                   window["time"].strftime("%H:%M"),
                                                                   window["description"],
                                                                   student["name"],
                                                                   student["grade"],
                                                                   student["sphere"],
                                                                   student["description"],
                                                                   student["cnt_came"],
                                                                   student["cnt_pass"],
                                                                   student["cnt_cancel"], ),
                                     reply_markup=kb.my_student())


@dp.callback_query(lambda query: query.data == "pred_student_teacher")
async def my_students_teacher(callback: CallbackQuery, state: FSMContext):
    info = await state.get_data()
    requests = info["requests"]
    id = info["id"]
    new_requests = []
    new_id = id
    flag = db.check_exist_request(requests[id]["id"])
    for i in range(0, id):
        if db.check_exist_request(requests[i]["id"]):
            new_requests.append(requests[i])
        if not db.check_exist_request(requests[i]["id"]):
            new_id -= 1
    if flag:
        new_requests.append(requests[id])
    for i in range(id + 1, len(requests)):
        if db.check_exist_request(requests[i]["id"]):
            new_requests.append(requests[i])
    new_id -= 1
    request = new_requests[new_id]
    await state.update_data(requests=new_requests, id=new_id)
    window = request["window"]
    student = request["student"]
    await callback.message.edit_text(text=const.StudentData.format(window["time"].strftime("%d.%m"),
                                                                   window["time"].strftime("%H:%M"),
                                                                   window["description"],
                                                                   student["name"],
                                                                   student["grade"],
                                                                   student["sphere"],
                                                                   student["description"],
                                                                   student["cnt_came"],
                                                                   student["cnt_pass"],
                                                                   student["cnt_cancel"], ),
                                     reply_markup=kb.my_student())


@dp.callback_query(lambda query: query.data == "next_student_teacher")
async def my_students_teacher(callback: CallbackQuery, state: FSMContext):
    info = await state.get_data()
    requests = info["requests"]
    id = info["id"]
    new_requests = []
    new_id = id
    flag = db.check_exist_request(requests[id]["id"])
    for i in range(0, id):
        if db.check_exist_request(requests[i]["id"]):
            new_requests.append(requests[i])
        if not db.check_exist_request(requests[i]["id"]):
            new_id -= 1
    if flag:
        new_requests.append(requests[id])
    else:
        new_id -= 1
    for i in range(id + 1, len(requests)):
        if db.check_exist_request(requests[i]["id"]):
            new_requests.append(requests[i])
    new_id += 1
    request = new_requests[new_id]
    await state.update_data(requests=new_requests, id=new_id)
    window = request["window"]
    student = request["student"]
    await callback.message.edit_text(text=const.StudentData.format(window["time"].strftime("%d.%m"),
                                                                   window["time"].strftime("%H:%M"),
                                                                   window["description"],
                                                                   student["name"],
                                                                   student["grade"],
                                                                   student["sphere"],
                                                                   student["description"],
                                                                   student["cnt_came"],
                                                                   student["cnt_pass"],
                                                                   student["cnt_cancel"], ),
                                     reply_markup=kb.my_student())
