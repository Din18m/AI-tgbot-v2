"""
Клавиатуры для поиска 'студентом' учителя
"""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def return_go_kb() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="Назад", callback_data="cmd_go")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def search_or_filters_kb() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="Искать", callback_data="search")],
        [InlineKeyboardButton(text="Фильтры", callback_data="filters")],
        [InlineKeyboardButton(text="Назад", callback_data="start_student")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def searching_kb(windows: list[dict]) -> InlineKeyboardMarkup:
    buttons = []
    for window in windows:
        datetime_obj = window["time"]
        date = datetime_obj.strftime("%d.%m")
        time = datetime_obj.strftime("%H:%M")
        buttons.append([InlineKeyboardButton(text=f"{date} {time} {window["description"]}", callback_data=f"{window['id']}_accept")])

    buttons.append([InlineKeyboardButton(text="Вперед", callback_data="next_teacher")])
    buttons.append([InlineKeyboardButton(text="Назад", callback_data="cmd_go")])

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def fsearching_kb() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="Принять", callback_data="agree"),
         InlineKeyboardButton(text="Вперед", callback_data="fnext_teacher")],
        [InlineKeyboardButton(text="Назад", callback_data="filters")]

    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def cmd_filters_kb() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="Выбрать уровень", callback_data="gradef")],
        [InlineKeyboardButton(text="Выбрать сферу", callback_data="spheref")],
        [InlineKeyboardButton(text="Применить и перейти", callback_data="fsearch")],
        [InlineKeyboardButton(text="Назад", callback_data="cmd_go")]

    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def fchoose_sphere_kb() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="NLP", callback_data="NLP_spheref")],
        [InlineKeyboardButton(text="CV", callback_data="CV_spheref")],
        [InlineKeyboardButton(text="RecSys", callback_data="RecSys_spheref")],
        [InlineKeyboardButton(text="Audio", callback_data="Audio_spheref")],
        [InlineKeyboardButton(text="Classic ML", callback_data="Classic_ML_spheref")],
        [InlineKeyboardButton(text="Любой", callback_data="Any_spheref")],
        [InlineKeyboardButton(text="Назад", callback_data="returnf")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


# no_work, intern, junior, middle. senior
def fchoose_grade_kb() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="No work", callback_data="No_work_gradef")],
        [InlineKeyboardButton(text="Intern", callback_data="Intern_gradef")],
        [InlineKeyboardButton(text="Junior", callback_data="Junior_gradef")],
        [InlineKeyboardButton(text="Middle", callback_data="Middle_gradef")],
        [InlineKeyboardButton(text="Senior", callback_data="Senior_gradef")],
        [InlineKeyboardButton(text="Назад", callback_data="returnf")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def making_sure_kb(identifier: int) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="Да", callback_data=f"{identifier}_accepting"),
         InlineKeyboardButton(text=f"Нет", callback_data=f"not_sure")],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard