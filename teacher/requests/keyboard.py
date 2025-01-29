from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def my_student():
    kb = [
        [
            InlineKeyboardButton(text="Принять", callback_data="like_student_teacher"),
            InlineKeyboardButton(text="Отказать", callback_data="dislike_student_teacher"),
        ],

        [
            InlineKeyboardButton(text="Предыдущая", callback_data="pred_student_teacher"),
            InlineKeyboardButton(text="Следующая", callback_data="next_student_teacher"),
        ],
        [
            InlineKeyboardButton(text="Назад", callback_data="start"),
        ]
    ]

    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard

