"""
Начальный блок
"""
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message

import start.keyboard as kbs
from config import dp
from const import HELLO, START_MESSAGE, INFO_TEXT_st
from const import YourForm
from db.db_student import check_student_id
from db.db_teacher import check_id
from start.keyboard import student_registration_kb, starting_kb


@dp.callback_query(lambda c: c.data == "start")
async def process_callback(callback_query: CallbackQuery, state: FSMContext):
    user, i = check_id(callback_query.from_user.id)
    if i == 0:
        await callback_query.message.edit_text("Здравствуйте, сначала пройдите регистрацию", reply_markup=kbs.teacher_registration_kb())
    else:
        await callback_query.message.edit_text(
            YourForm.format(user.name, user.grade, user.sphere, user.description),
            reply_markup=kbs.start_teacher_kb())



@dp.callback_query(lambda c: c.data == "return_to_start")
async def cmd_start(callback_query: CallbackQuery):
    await callback_query.message.edit_text(START_MESSAGE, reply_markup=starting_kb())



@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(START_MESSAGE, reply_markup=starting_kb())


@dp.callback_query(lambda c: c.data == "start_student")
async def student_info(callback_query: CallbackQuery, state: FSMContext):
    user, i = await check_student_id(callback_query.from_user.id)
    if i == 0:
        await callback_query.message.edit_text("Здравствуйте, сначала пройдите регистрацию", reply_markup=student_registration_kb())
    else:
        DATA = HELLO + INFO_TEXT_st
        await callback_query.message.edit_text(
            DATA.format(user["name"], user["grade"], user["sphere"], user["description"]),
            reply_markup=kbs.info_and_continue_kb())


