"""
Реализация рандомного поиска с фильтрами
"""
import random
from itertools import product

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from const import TEACHER_DATA_sign_up, TEACHER_DATA, FILTER_DATA
from db.db_student import get_filter_teachers, get_all_teacher_windows, sign_up_student
from student.search import keyboard as kb

from config import dp, NoneData, bot
from student.search.keyboard import fmaking_sure_kb


class Filters(StatesGroup):
    grade = State()
    sphere = State()
    wait = State()



async def display_filters(state: FSMContext):
    filter_data = await state.get_data()

    g = filter_data['grade']
    s = filter_data['sphere']

    call = filter_data['call']
    await call.message.edit_text(text=FILTER_DATA.format(g, s),
                                 reply_markup=kb.cmd_filters_kb())


@dp.callback_query(lambda c: c.data == "filters")
async def cmd_filters(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await state.update_data(grade=NoneData, sphere=NoneData, call=callback)
    await display_filters(state)


@dp.callback_query(lambda c: c.data == "returnf")
async def filter_return(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Filters.wait)
    await display_filters(state)


@dp.callback_query(lambda c: c.data == "gradef")
async def choose_grade(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Выберите уровень подготовки", reply_markup=kb.fchoose_grade_kb())
    await state.set_state(Filters.grade)


@dp.callback_query(lambda c: c.data.split("_")[-1] == "gradef")
async def choose_grade(callback: CallbackQuery, state: FSMContext):
    filter_data = await state.get_data()
    g = filter_data['grade']
    tt = " ".join(callback.data.split("_")[:-1])
    if g == NoneData:
        await state.update_data(grade=tt)
    elif tt in g:
        tt = ", ".join([i for i in "".join(g.split(tt)).split(", ") if i != ""])
        await state.update_data(grade=tt)
    else:
        tt = g + ", " + tt
        await state.update_data(grade=tt)
    await callback.message.edit_text(text="Выбрано " + tt + "\n\nВыберите дополнительно или\n "
                                                            "нажмите повторно чтобы убрать",
                                     reply_markup=kb.fchoose_grade_kb())
    await state.set_state(Filters.wait)


@dp.callback_query(lambda c: c.data == "spheref")
async def choose_sphere(callback: CallbackQuery, state: FSMContext):
    filter_data = await state.get_data()
    s = filter_data['sphere']
    if s == NoneData:
        await callback.message.edit_text("Выберите ваши сферы деятельности", reply_markup=kb.fchoose_sphere_kb())
    else:
        await callback.message.edit_text("Выбрано " + s + "\n\nВыберите дополнительно или "
                                                          "нажмите повторно чтобы убрать",
                                         reply_markup=kb.fchoose_sphere_kb())
    await state.set_state(Filters.sphere)


@dp.callback_query(lambda c: c.data.split("_")[-1] == "spheref")
async def choose_sphere(callback: CallbackQuery, state: FSMContext):
    filter_data = await state.get_data()
    s = filter_data['sphere']
    tt = " ".join(callback.data.split("_")[:-1])
    if s == NoneData:
        await state.update_data(sphere=tt)
    elif tt in s:
        tt = ", ".join([i for i in "".join(s.split(tt)).split(", ") if i != ""])
        await state.update_data(sphere=tt)
    else:
        tt = s + ", " + tt
        await state.update_data(sphere=tt)
    await callback.message.edit_text(text="Выбрано " + tt + "\n\nВыберите дополнительно или\n "
                                                            "нажмите повторно чтобы убрать",
                                     reply_markup=kb.fchoose_sphere_kb())
    await state.set_state(Filters.wait)


# ================================================================================================


async def display_filter_teachers(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    teacher_list = data.get("list", [])
    index = data.get("index", 0)

    if index < len(teacher_list):
        teacher = teacher_list[index]
        id_teacher = teacher["id"]
        teachers_windows = await get_all_teacher_windows(id_teacher)

        if teacher["flag"]:
            text = TEACHER_DATA_sign_up.format(teacher["name"], teacher["grade"], teacher["sphere"],
                                               teacher["bio"], teacher["cnt_came"], teacher["cnt_pass"], teacher["symbol"])
        else:
            text=TEACHER_DATA.format(teacher["name"], teacher["grade"], teacher["sphere"],
                                       teacher["bio"], teacher["cnt_came"], teacher["cnt_pass"], teacher["symbol"])

        await callback.message.edit_text(
            text=text,
            reply_markup=kb.fsearching_kb(teachers_windows)
        )

    else: #вроде так, пока хз (для бесконечного поиска)
        await state.update_data(index=0)
        teacher = teacher_list[0]
        id_teacher = teacher["id"]
        teachers_windows = await get_all_teacher_windows(id_teacher)

        if teacher["flag"]:
            text = TEACHER_DATA_sign_up.format(teacher["name"], teacher["grade"], teacher["sphere"],
                                               teacher["bio"], teacher["cnt_came"], teacher["cnt_pass"], teacher["symbol"])
        else:
            text=TEACHER_DATA.format(teacher["name"], teacher["grade"], teacher["sphere"],
                                       teacher["bio"], teacher["cnt_came"], teacher["cnt_pass"], teacher["symbol"])

        await callback.message.edit_text(
            text=text,
            reply_markup=kb.fsearching_kb(teachers_windows)
        )


async def get_random_teachersf(grade:str, sphere:str, id_student:int) -> list[dict]:
    list_, ids = await get_filter_teachers(grade, sphere, id_student)
    for teacher in list_:
        if teacher["id"] in ids: #показывать ли текст (*уже в календаре*)
            teacher["flag"] = True
        else:
            teacher["flag"] = False
    random.shuffle(list_)
    unrepeatable_symbols = [''.join(i) for i in product('-_*', repeat=7)]
    random.shuffle(unrepeatable_symbols)
    for i in range(len(list_)):
        list_[i]["symbol"] = unrepeatable_symbols[i]
    return list_

@dp.callback_query(lambda c: c.data == "searchf")
async def searching(callback: CallbackQuery, state: FSMContext):
    teacher_data = await state.get_data()
    gr = teacher_data["grade"]
    sp = teacher_data["sphere"]

    random_list = await get_random_teachersf(gr, sp, callback.from_user.id)
    await state.update_data(list=random_list, index=0)
    await display_filter_teachers(callback, state)


@dp.callback_query(lambda c: c.data == "next_teacherf")
async def searching_next(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    index = data.get("index", 0) + 1

    await state.update_data(index=index)
    await display_filter_teachers(callback, state)


@dp.callback_query(lambda c: c.data.split('_')[-1] == "acceptf")
async def make_sure_with_accepting(callback: CallbackQuery, state: FSMContext):
    window_id = int(callback.data.split('_')[0])
    await bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text='Вы уверены, что хотите записаться?',
        reply_markup=fmaking_sure_kb(window_id)
    )


@dp.callback_query(lambda c: c.data.split('_')[-1] == "acceptingf")
async def sure_with_accepting(callback: CallbackQuery, state: FSMContext):
    window_id = int(callback.data.split('_')[0])
    data = await state.get_data()
    teacher_id = data["list"][data["index"]]["id"]
    await sign_up_student(callback.from_user.id, teacher_id, window_id)
    await display_filter_teachers(callback, state)


@dp.callback_query(lambda c: c.data == "not_suref")
async def not_sure_with_accepting(callback: CallbackQuery, state: FSMContext):
    await display_filter_teachers(callback, state)
