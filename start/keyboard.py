"""
Клавиатуры для начального блока
"""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def start_teacher_kb() -> InlineKeyboardMarkup:
    kb = [
        [
            InlineKeyboardButton(text="Изменить анкету", callback_data="teacher"),
        ],
        [
            InlineKeyboardButton(text="⚙️ Настройки календаря", callback_data="setting_teacher"),
        ],
        [
            InlineKeyboardButton(text="Полученные приглашения", callback_data="my_students_teacher"),
        ],
        [InlineKeyboardButton(text="Вернуться", callback_data="return_to_start")]
    ]

    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard

def starting_kb() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="Хочу пройти собеседование", callback_data="start_student")],
        [InlineKeyboardButton(text="Хочу провести собеседование", callback_data="start")],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def info_and_continue_kb() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="Изменения информации", callback_data="registration")],
        [InlineKeyboardButton(text="Поиск", callback_data="cmd_go")],
        [InlineKeyboardButton(text="Настройки календаря", callback_data="calendar")],
        [InlineKeyboardButton(text="Вернуться к выбору роли", callback_data="return_to_start")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def student_registration_kb() -> InlineKeyboardMarkup:
    buttons = [
            [
                InlineKeyboardButton(text="Регистрация", callback_data="registration"),
                InlineKeyboardButton(text="Назад", callback_data="return_to_start"),
            ]]

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def teacher_registration_kb() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text="Регистрация", callback_data="teacher"),
            InlineKeyboardButton(text="Вернуться", callback_data="return_to_start"),
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard