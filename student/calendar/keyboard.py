"""
Клавиатуры для 'расписания' для студента
"""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def calendar_kb() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="Посмотреть окна", callback_data="look_windows")],
        [InlineKeyboardButton(text="Отменить окна", callback_data="cancel_windows")],
        [InlineKeyboardButton(text="Назад", callback_data="start_student")],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def return_to_calendar_kb() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="Назад", callback_data="calendar")],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def cancel_windows_kb(count: int) -> InlineKeyboardMarkup:
    buttons = []
    for i in range(count):
        buttons.append([InlineKeyboardButton(text=f"{i+1}", callback_data=f"{i}_cancel")])
    buttons.append([InlineKeyboardButton(text="Назад", callback_data="calendar")])
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def agreement_kb(identifier: int) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="Да", callback_data=f"{identifier}_agree"),
         InlineKeyboardButton(text=f"Нет", callback_data=f"cancel_windows")],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

