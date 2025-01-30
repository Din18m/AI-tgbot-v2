from config import bot


async def notify_before_interview(id_teacher, id_student, window):
    datetime_obj = window['time']
    date = datetime_obj.strftime("%d.%m")
    time = datetime_obj.strftime("%H:%M")
    description = window['description']
    await bot.send_message(chat_id=id_teacher, text=)
    await bot.send_message(chat_id=id_student, text="")


NOTIFY_TEXT_for_student="""

"""