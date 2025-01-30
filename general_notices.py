from config import bot


async def notify_before_interview(id_teacher, nick_tch, id_student, nick_st, window):
    datetime_obj = window['time']
    date = datetime_obj.strftime("%d.%m")
    time = datetime_obj.strftime("%H:%M")
    description = window['description']
    await bot.send_message(chat_id=id_teacher, text=)
    await bot.send_message(chat_id=id_student, text=)


TEXT_for_student="""
Напоминание.
Вы записаны на собеседование
{}
"""

TEXT_for_teacher="""

"""