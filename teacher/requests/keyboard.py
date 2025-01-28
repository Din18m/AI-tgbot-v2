from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def my_student():
    kb = [
        [
            InlineKeyboardButton(text="Предыдущая", callback_data="pred_student_teacher"),
            InlineKeyboardButton(text="Следующая", callback_data="next_student_teacher"),
        ],
        [
            InlineKeyboardButton(text="Назад", callback_data="start"),
        ]
    ]