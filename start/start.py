"""
Начальный блок
"""
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message

from config import dp
from const import INFO_TEXT, HELLO, START_MESSAGE
from db.db_student import  check_student_id
from db.db_teacher import check_id
from start.keyboard import info_and_continue_kb, student_registration_kb, starting_kb


@dp.callback_query(lambda c: c.data == "start")
async def process_callback(callback_query: CallbackQuery, state: FSMContext):
    user, i = check_id(callback_query.from_user.id)
    if i == 0:
        kb = [
            [
                InlineKeyboardButton(text="Регистрация", callback_data="registration"),
            ]]

        keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
        await callback_query.message.edit_text("Здравствуйте, сначала пройдите регистрацию", reply_markup=keyboard)
    else:
        kb = [
            [
                InlineKeyboardButton(text="Изменить анкету", callback_data="registration"),
            ],
            [
                InlineKeyboardButton(text="⚙️ Настройки", callback_data="setting_teacher"),
            ],
            [
                InlineKeyboardButton(text="🔍 Поиск собеседника", callback_data="new_students_teacher"),
            ],
            [
                InlineKeyboardButton(text="Люди которых вы хотите собеседовать", callback_data="my_students_teacher"),
            ],
            [InlineKeyboardButton(text="Вернуться", callback_data="return_to_start")]
        ]

        keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
        await callback_query.message.edit_text(
            HELLO.format(user.name, user.grade, user.sphere, user.description),
            reply_markup=keyboard)


@dp.callback_query(lambda c: c.data == "return_to_start")
async def cmd_start(callback_query: CallbackQuery):
    kb = [
        [InlineKeyboardButton(text="Хочу пройти собеседование", callback_data="start_student")],
        [InlineKeyboardButton(text="Хочу провести собеседование", callback_data="start")],
    ]

    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    await callback_query.message.edit_text(START_MESSAGE, reply_markup=keyboard)



@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(START_MESSAGE, reply_markup=starting_kb())



@dp.callback_query(lambda c: c.data == "start_student")
async def student_info(callback_query: CallbackQuery, state: FSMContext):
    user, i = await check_student_id(callback_query.from_user.id)
    if i == 0:
        await callback_query.message.edit_text("Здравствуйте, сначала пройдите регистрацию", reply_markup=student_registration_kb())
    else:
        DATA = HELLO + INFO_TEXT
        await callback_query.message.edit_text(
            DATA.format(user["name"], user["grade"], user["sphere"], user["description"]),
            reply_markup=info_and_continue_kb())


