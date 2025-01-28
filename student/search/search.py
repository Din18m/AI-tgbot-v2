"""
Реализация рандомного поиска
"""
import random
from itertools import product

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from db.db_student import get_all_teachers, get_teacher_by_id, get_all_info, get_all_teacher_windows, sign_up_student
from config import bot, dp
from student.search import keyboard as kb
from student.search.keyboard import making_sure_kb


@dp.callback_query(lambda c: c.data == "cmd_go")
async def cmd_go(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="""
            Ты можешь выставить определенные фильтры \nили искать по всем подряд
            """,
        reply_markup=kb.search_or_filters_kb()
    )


async def get_random_teachers(id_student) -> list[dict]:
    list_, ids = await get_all_teachers(id_student)
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


TEACHER_DATA = """
Имя: {}
Уровень: {}
Сфера: {}

{}

провел занятий - {}
пропустил занятий - {}
{}
"""

TEACHER_DATA_sign_up = """
*уже в календаре =)*

Имя: {}
Уровень: {}
Сфера: {}

{}

провел занятий - {}
пропустил занятий - {}
{}
"""


async def display_teachers(callback: CallbackQuery, state: FSMContext):
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
            reply_markup=kb.searching_kb(teachers_windows)
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
            reply_markup=kb.searching_kb(teachers_windows)
        )


@dp.callback_query(lambda c: c.data == "search")
async def searching(callback: CallbackQuery, state: FSMContext):
    random_list = await get_random_teachers(callback.from_user.id)
    await state.update_data(list=random_list, index=0)
    await display_teachers(callback, state)


@dp.callback_query(lambda c: c.data == "next_teacher")
async def searching_next(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    index = data.get("index", 0) + 1

    await state.update_data(index=index)
    await display_teachers(callback, state)


@dp.callback_query(lambda c: c.data.split('_')[-1] == "accept")
async def make_sure_with_accepting(callback: CallbackQuery, state: FSMContext):
    window_id = int(callback.data.split('_')[0])
    await bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text='Вы уверены, что хотите записаться?',
        reply_markup=making_sure_kb(window_id)
    )


@dp.callback_query(lambda c: c.data.split('_')[-1] == "accepting")
async def sure_with_accepting(callback: CallbackQuery, state: FSMContext):
    window_id = int(callback.data.split('_')[0])
    data = await state.get_data()
    teacher_id = data["list"][data["index"]]["id"]
    await sign_up_student(callback.from_user.id, teacher_id, window_id)
    await display_teachers(callback, state)


@dp.callback_query(lambda c: c.data == "not_sure")
async def not_sure_with_accepting(callback: CallbackQuery, state: FSMContext):
    await display_teachers(callback, state)


# STUDENT_DATA = """
# Новая заявка! Этот человек хочет пройти с тобой собеседование:
#
# Имя:    {}
# Уровень:    {}
# Сфера:    {}
#
# {}
# """

# @dp.callback_query(lambda c: c.data == "agree")
# async def agree_request(callback: CallbackQuery, state: FSMContext):
#     data = await state.get_data()
#
#     list_ = data["list"]
#     index_ = data["index"]
#
#     user_id = list_[index_]["id"]
#     user_info = (await get_all_info(callback.from_user.id))[0]
#
#     buttons = [
#         [InlineKeyboardButton(text="Принять", callback_data=f"{callback.from_user.id}_accept")],
#         [InlineKeyboardButton(text="Отказать", callback_data=f"{callback.from_user.id}_deny")]
#     ]
#     keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
#     await bot.send_message(user_id, STUDENT_DATA.format(user_info["name"], user_info["grade"],
#                                                         user_info["sphere"], user_info["bio"]), reply_markup=keyboard)
#     data = await state.get_data()
#     index = data.get("index", 0) + 1
#     await callback.answer(text="Заявка отправлена")
#
#     await state.update_data(index=index)
#     await display_teachers(callback, state)
#
#
# RESPONSE_TEACHER_DATA_ACCEPT = """
# Ваша заявка на интервью от
#
# Имя: {}
# Уровень: {}
# Сфера: {}
#
# {}
#
# была ПРИНЯТА
# Никнейм для связи: @{}
# """
#
# RESPONSE_TEACHER_DATA_DENY = """
# Ваша заявка на интервью от
#
# Имя:       {}
# Уровень:   {}
# Сфера:     {}
#
# {}
# была ОТКЛОНЕНА
# """
#
# @dp.callback_query(lambda c: c.data.split("_")[-1] == "accept")
# async def accept_request(callback: CallbackQuery):
#     buttons = [
#         [InlineKeyboardButton(text="Ок", callback_data="ok")],
#     ]
#     keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
#
#     teacher_id = callback.from_user.id
#     student_id = int(callback.data.split("_")[0])
#
#     teacher_info = (await get_teacher_by_id(teacher_id))[0]
#     student_info = (await get_all_info(student_id))[0]
#
#     await insert_into_ts(teacher_id, student_id, callback.from_user.username,
#                          student_info["nickname"]) # тут происходит какая-то магия почему запрос ломается никто не знает
#
#     await bot.send_message(student_id,
#                            RESPONSE_TEACHER_DATA_ACCEPT.format(teacher_info["name"], teacher_info["grade"],
#                                                                teacher_info["sphere"], teacher_info["bio"],
#                                                                teacher_info["nickname"]),
#                            reply_markup=keyboard)
#
#     await callback.answer(text="Вы приняли заявку")
#     await callback.message.delete()
#
# @dp.callback_query(lambda c: c.data.split("_")[-1] == "deny")
# async def deny_request(callback: CallbackQuery):
#     buttons = [
#         [InlineKeyboardButton(text="Ок", callback_data="ok")],
#     ]
#     keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
#     teacher_id = callback.from_user.id
#     teacher_info = (await get_teacher_by_id(teacher_id))[0]
#     await bot.send_message(int(callback.data.split("_")[0]),
#                            RESPONSE_TEACHER_DATA_DENY.format(teacher_info["name"], teacher_info["grade"],
#                                                              teacher_info["sphere"], teacher_info["bio"]),
#                            reply_markup=keyboard)
#
#     await callback.answer(text="Вы отклонили заявку")
#     await callback.message.delete()
#
# @dp.callback_query(lambda c: c.data == "ok")
# async def deny_request(callback: CallbackQuery):
#     await callback.message.delete()
