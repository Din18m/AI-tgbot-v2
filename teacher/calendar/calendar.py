"""Реализация настроек календаря"""
from datetime import datetime, timedelta

from aiogram.filters import StateFilter, state
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message

import db.db_teacher
import teacher.calendar.keyboard as kb
from config import dp
from const import DayWeekEN
from db.db_teacher import check_id, get_cnt_windows, add_new_window, get_free_window, delete_window, get_all_window


class CalendarTeacher(StatesGroup):
    week = State()
    date = State()
    time = State()
    description = State()
    finish = State()
    wait = State()


@dp.callback_query(lambda query: query.data == "setting_teacher")
async def calendar(callback: CallbackQuery):
    await callback.message.edit_text("Создать окно\nУдалить окно\nПросмотреть Окна\nНазад",
                                     reply_markup=kb.setting_teacher())


@dp.callback_query(lambda query: query.data == "create_setting_teacher")
async def create_setting_teacher(callback: CallbackQuery, state: FSMContext):
    cnt_windows = get_cnt_windows(callback.from_user.id)
    if cnt_windows == 8:
        await callback.message.edit_text("у вас уже 8 окон\nСоздать окно\nУдалить окно\nПросмотреть Окна\nНазад",
                                         reply_markup=kb.setting_teacher())
        return
    await state.update_data(call=callback)
    await state.set_state(CalendarTeacher.wait)
    await callback.message.edit_text("выберите в какой день провести собеседование",
                                     reply_markup=kb.create_setting_teacher())


@dp.callback_query(lambda query: query.data == "delete_setting_teacher")
async def delete_setting_teacher(callback: CallbackQuery, state: FSMContext):
    windows = get_free_window(callback.from_user.id)
    if len(windows) == 0:
        await callback.message.edit_text("у вас нет свободных окон для удаления\nСоздать окно\nУдалить "
                                         "окно\nПросмотреть Окна\nНазад",
                                         reply_markup=kb.setting_teacher())
        return
    text = []
    ids = []
    for i in range(len(windows)):
        ids.append(windows[i]["id"])
        text.append(
            f"{i + 1}) {windows[i]["time"].strftime('%d.%m')} "
            f"{windows[i]["time"].strftime('%H:%M')} {windows[i]['description']}")
    await state.update_data(ids=ids, text=text)
    await callback.message.edit_text("удалите свободные окна \n" + "\n".join(text),
                                     reply_markup=kb.delete_setting_teacher(len(windows)))


@dp.callback_query(lambda query: query.data.endswith("_delete_setting_teacher"))
async def delete_setting_teacher(callback: CallbackQuery, state: FSMContext):
    id = callback.data.split("_")[0]
    info = await state.get_data()
    ids = info["ids"]
    text = info["text"]
    await state.update_data(delete=ids[int(id) - 1])
    await callback.message.edit_text("Вы уверены что хотите удалить окно \n" + text[int(id)-1],
                                     reply_markup=kb.sure())

@dp.callback_query(lambda query: query.data==("delete_now_calendar_teacher"))
async def delete_setting_teacher(callback: CallbackQuery, state: FSMContext):
    info = await state.get_data()
    delete = info["delete"]
    delete_window(delete)
    windows = get_free_window(callback.from_user.id)
    if len(windows) == 0:
        await callback.message.edit_text("у вас нет свободных окон для удаления\nСоздать окно\nУдалить "
                                         "окно\nПросмотреть Окна\nНазад",
                                         reply_markup=kb.setting_teacher())
        return
    text = []
    ids = []
    for i in range(len(windows)):
        ids.append(windows[i]["id"])
        text.append(
            f"{i + 1}) {windows[i]["time"].strftime('%d.%m')} "
            f"{windows[i]["time"].strftime('%H:%M')} {windows[i]['description']}")
    await state.update_data(ids=ids, text=text)
    await callback.message.edit_text("удалите свободные окна \n" + "\n".join(text),
                                     reply_markup=kb.delete_setting_teacher(len(windows)))


@dp.callback_query(lambda query: query.data == "show_setting_teacher")
async def show_setting_teacher(callback: CallbackQuery):
    windows = get_all_window(callback.from_user.id)
    if len(windows) == 0:
        await callback.message.edit_text("у вас нет окон\nСоздать окно\nУдалить "
                                         "окно\nПросмотреть Окна\nНазад",
                                         reply_markup=kb.setting_teacher())
        return
    text = []
    ids = []
    for i in range(len(windows)):
        ids.append(windows[i]["id"])
        if windows[i]["student"] is not None:
            text.append(
                f"{i + 1}) {windows[i]["time"].strftime('%d.%m')} "
                f"{windows[i]["time"].strftime('%H:%M')} {windows[i]['description']}-{windows[i]["student"]}")
        else:
            text.append(
                f"{i + 1}) {windows[i]["time"].strftime('%d.%m')} "
                f"{windows[i]["time"].strftime('%H:%M')} {windows[i]['description']}")
    await callback.message.edit_text("ваши окна \n" + "\n".join(text),
                                     reply_markup=kb.cancel_setting_teacher())


@dp.callback_query(lambda query: query.data.endswith("_create_setting_teacher"))
async def create_setting_teacher(callback: CallbackQuery, state: FSMContext):
    today = datetime.today().weekday()
    ind = DayWeekEN.index(callback.data.split("_")[0])
    different_days = ind - today if today < ind else 7 - today + ind
    d1 = (datetime.today() + timedelta(days=different_days))
    d2 = d1 + timedelta(days=7)
    y1 = d1.strftime('%Y')
    y2 = d2.strftime('%Y')
    d1 = d1.strftime('%d.%m')
    d2 = d2.strftime('%d.%m')
    await state.update_data(d1=d1, d2=d2, y1=y1, y2=y2)
    await callback.message.edit_text("выберите дату", reply_markup=kb.day_week(d1, d2))


@dp.callback_query(lambda query: query.data.endswith("_day_teacher"))
async def day_teacher(callback: CallbackQuery, state: FSMContext):
    d = callback.data.split("_")[0]
    info = await state.get_data()
    data = info[d]
    year = info["y" + d[1]]
    await state.update_data(date=str(data), year=str(year))
    await state.set_state(CalendarTeacher.time)
    await callback.message.edit_text(
        text=f"Введите время, в которое вы проведете собеседование {data} числа в формате hh:mm",
        reply_markup=kb.cancel_setting_teacher())



@dp.callback_query(lambda query: query.data == "time_ret_calendar")
async def time_ret_teacher(callback: CallbackQuery, state: FSMContext):
    info = await state.get_data()
    call = info["call"]
    data = info["date"]
    await state.set_state(CalendarTeacher.time)
    await call.message.edit_text(
        text=f"Введите время, в которое вы проведете собеседование {data} числа в формате hh:mm",
        reply_markup=kb.cancel_setting_teacher())

@dp.message(StateFilter(CalendarTeacher.time))
async def time_teacher(message: Message, state: FSMContext):
    time = message.text
    info = await state.get_data()
    call = info["call"]
    data = info["date"]
    year = info["year"]

    await message.delete()
    try:
        t1, t2 = time.split(':')
        h = int(t1)
        m = int(t2)
        if h > 23 or m > 59:
            int("e")
        await state.update_data(time=datetime.strptime(f'{h}:{m}:{data}:{year}', '%H:%M:%d.%m:%Y'),
                                h=h, m=m)
        await state.set_state(CalendarTeacher.description)
        await call.message.edit_text(
            f"Введите краткое (не более 23 символа) описание собеседования которое будет проведено {data} числа в {str(h).rjust(2, "0")}:{str(m).rjust(2, "0")} ",
            reply_markup=kb.cancel_setting_teacher())
    except Exception:
        await call.message.edit_text(
            text=f"Неправильный формат времени\n"
                 + f"Введите время, в которое вы проведете собеседование {data} числа в формате hh:mm",
            reply_markup=kb.cancel_setting_teacher())


@dp.callback_query(lambda query: query.data == "description_ret_calendar")
async def time_ret_teacher(callback: CallbackQuery, state: FSMContext):
    info = await state.get_data()
    call = info["call"]
    data = info["date"]
    h = info["h"]
    m = info["m"]
    await state.set_state(CalendarTeacher.description)
    await call.message.edit_text(
        f"Введите краткое (не более 23 символа) описание собеседования которое будет проведено {data} числа в {str(h).rjust(2, "0")}:{str(m).rjust(2, "0")} ",
        reply_markup=kb.cancel_setting_teacher())


@dp.message(StateFilter(CalendarTeacher.description))
async def time_tiacher(message: Message, state: FSMContext):
    desc = message.text
    info = await state.get_data()
    call = info["call"]
    data = info["date"]
    h = info['h']
    m = info['m']
    await message.delete()
    try:
        if len(desc) > 23:
            int("e")
        await state.update_data(desc=desc)
        await state.set_state(CalendarTeacher.finish)
        await call.message.edit_text(
            f"Проверьте правильность и сохраните, иначе вернитесь и измените начиная с неправильного пункта\n"
            f"{data} в {str(h).rjust(2, "0")}:{str(m).rjust(2, "0")} {desc}",
            reply_markup=kb.check())
    except Exception:
        await call.message.edit_text(
            text=f"превышение размера текста\n"
                 + f"Введите краткое (не более 23 символа) описание собеседования которое будет проведено {data} числа в {str(h).rjust(2, "0")}:{str(m).rjust(2, "0")}",
            reply_markup=kb.cancel_setting_teacher())


@dp.callback_query(lambda query: query.data == "finish_calendar")
async def calendar(callback: CallbackQuery, state: FSMContext):
    info = await state.get_data()
    time = info["time"]
    desc = info["desc"]
    await state.clear()

    add_new_window(callback.from_user.id, time, desc)
    await callback.message.edit_text("окно успешно сохранено\n\nСоздать окно\nУдалить окно\nПросмотреть Окна\nНазад",
                                     reply_markup=kb.setting_teacher())
