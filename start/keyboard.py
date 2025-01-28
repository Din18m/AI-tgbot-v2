"""
Клавиатуры для начального блока
"""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def starting_kb() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="Хочу пройти собеседование", callback_data="start_student")],
        [InlineKeyboardButton(text="Хочу провести собеседование", callback_data="start")],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def info_and_continue_kb() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="Регистрация", callback_data="registration")],
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