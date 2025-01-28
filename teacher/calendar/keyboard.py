"""
Этот файл отвечает за создание клавиатур настроек
"""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from const import DayWeekRU, DayWeekEN
from datetime import datetime, timedelta


def setting_teacher() -> InlineKeyboardMarkup:
    """
    Клавиатура выбора настроек
    :return: InlineKeyboardMarkup
    """
    kb = [
        [
            InlineKeyboardButton(text="create", callback_data="create_setting_teacher"),
        ],
        [
            InlineKeyboardButton(text="delete", callback_data="delete_setting_teacher"),
        ],
        [
            InlineKeyboardButton(text="show", callback_data="show_setting_teacher"),
        ],
        [
            InlineKeyboardButton(text="Вернуться", callback_data="start"),
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard


def create_setting_teacher() -> InlineKeyboardMarkup:
    # todo """"""
    kb = []
    for i in range(7):
        kb.append([InlineKeyboardButton(text=DayWeekRU[i], callback_data=DayWeekEN[i] + "_create_setting_teacher")])
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard


def day_week(d1, d2: str) -> InlineKeyboardMarkup:
    kb = [
        [
            InlineKeyboardButton(text=d1, callback_data="d1_day_teacher"),
            InlineKeyboardButton(text=d2, callback_data="d2_day_teacher"),
        ],
        [
            InlineKeyboardButton(text="вернуться", callback_data="setting_teacher"),
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard


def cancel_setting_teacher() -> InlineKeyboardMarkup:
    kb = [[InlineKeyboardButton(text="вернуться", callback_data="setting_teacher")]]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard


def delete_setting_teacher(cnt: int) -> InlineKeyboardMarkup:
    kb = []
    for i in range(cnt):
        kb.append(InlineKeyboardButton(text=str(i + 1), callback_data=str(i + 1) + "_delete_setting_teacher"))
    cancel = [InlineKeyboardButton(text="вернуться", callback_data="setting_teacher")]
    keyboard = InlineKeyboardMarkup(inline_keyboard=[kb, cancel])
    return keyboard


def check() -> InlineKeyboardMarkup:
    kb = [
        [InlineKeyboardButton(text="день", callback_data="create_setting_teacher")],
        [InlineKeyboardButton(text="время", callback_data="time_ret_calendar")],
        [InlineKeyboardButton(text="описание", callback_data="description_ret_calendar")],
        [InlineKeyboardButton(text="все ок", callback_data="finish_calendar")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard
def sure() -> InlineKeyboardMarkup:
    kb = [
        [InlineKeyboardButton(text="удалить", callback_data="delete_now_calendar_teacher" )],
        [InlineKeyboardButton(text="нет", callback_data="delete_setting_teacher")],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard