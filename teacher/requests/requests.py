from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from config import dp
from db import db_teacher as db
import const
from db.db_teacher import check_id
from teacher.requests import keyboard as kb

import start.keyboard as kbs


@dp.callback_query(lambda query: query.data == "my_students_teacher")
async def my_students_teacher(callback: CallbackQuery, state: FSMContext):
    requests = await db.get_requests(callback.from_user.id)
    if len(requests) == 0:
        user, i = check_id(callback.from_user.id)
        await callback.message.edit_text("У вас нет заявок\n" +
                                         const.YourForm.format(user.name, user.grade, user.sphere, user.description),
                                         reply_markup=kbs.start_teacher_kb())
        return
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
    for i in range(id - 1, -1, -1):
        if db.check_exist_request(requests[i]["id"]):
            new_requests = requests[:i + 1]
            break
        else:
            new_id -= 1
    if flag:
        new_requests.append(requests[id])
    new_requests += requests[id + 1:]
    if len(new_requests) == 0:
        user, i = check_id(callback.from_user.id)
        await callback.message.edit_text("У вас нет заявок\n" +
                                         const.YourForm.format(user.name, user.grade, user.sphere, user.description),
                                         reply_markup=kbs.start_teacher_kb())
        return
    new_id -= 1
    if new_id == -1:
        new_id = len(new_requests) - 1
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
    new_id = id
    flag = db.check_exist_request(requests[id]["id"])
    new_requests = requests[:id]
    if flag:
        new_requests.append(requests[id])
    else:
        new_id -= 1
    for i in range(id + 1, len(requests)):
        if db.check_exist_request(requests[i]["id"]):
            new_requests += (requests[i:])
            break
    if len(new_requests) == 0:
        user, i = check_id(callback.from_user.id)
        await callback.message.edit_text("У вас нет заявок\n" +
                                         const.YourForm.format(user.name, user.grade, user.sphere, user.description),
                                         reply_markup=kbs.start_teacher_kb())
        return
    new_id += 1
    if new_id == len(new_requests):
        new_id = 0
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


@dp.callback_query(lambda query: query.data == "like_student_teacher")
async def my_students_teacher(callback: CallbackQuery, state: FSMContext):
    info = await state.get_data()
    requests = info["requests"]
    id = info["id"]
    request = requests[id]
    await db.like_requests(request["id"])
    await db.delete_all_window_requests(request["window"]["id"])
    await db.delete_time_student_requests(request["student"]["id"], request["window"]["id"])
    new_id = id
    flag = db.check_exist_request(requests[id]["id"])
    new_requests = requests[:id]
    if flag:
        new_requests.append(requests[id])
    else:
        new_id -= 1
    for i in range(id + 1, len(requests)):
        if db.check_exist_request(requests[i]["id"]):
            new_requests += (requests[i:])
            break

    if len(new_requests) == 0:
        user, i = check_id(callback.from_user.id)
        await callback.message.edit_text("У вас нет заявок\n" +
                                         const.YourForm.format(user.name, user.grade, user.sphere, user.description),
                                         reply_markup=kbs.start_teacher_kb())
        return
    new_id += 1
    if new_id == len(new_requests):
        new_id = 0
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


@dp.callback_query(lambda query: query.data == "dislike_student_teacher")
async def my_students_teacher(callback: CallbackQuery, state: FSMContext):
    info = await state.get_data()
    requests = info["requests"]
    id = info["id"]
    new_id = id
    request = requests[id]
    await db.delete_one_dislike_requests(request["id"])
    flag = db.check_exist_request(requests[id]["id"])
    new_requests = requests[:id]
    if flag:
        new_requests.append(requests[id])
    else:
        new_id -= 1
    for i in range(id + 1, len(requests)):
        if db.check_exist_request(requests[i]["id"]):
            new_requests += (requests[i:])
            break
    if len(new_requests) == 0:
        user, i = check_id(callback.from_user.id)
        await callback.message.edit_text("У вас нет заявок\n" +
                                         const.YourForm.format(user.name, user.grade, user.sphere, user.description),
                                         reply_markup=kbs.start_teacher_kb())
        return
    new_id += 1
    if new_id == len(new_requests):
        new_id = 0
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
