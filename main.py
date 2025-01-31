"""
Точка входа в программу
"""
import asyncio
import logging
from datetime import datetime

import db.migration
from config import dp, bot, schedule

# Импорты ниже НЕОБХОДИМЫ для работы бота,
# здесь указываются все файлы, связанные с исполнением бота

import student.registration.registration
import student.search.search
import student.search.filters
import student.calendar.calendar

import teacher.registration.registration
import teacher.calendar.calendar
import teacher.requests.requests

import start.start
from general_notices import delete_windows_expired, say_about_requests

logging.basicConfig(level=logging.DEBUG)


async def main():
    schedule.add_job(
        delete_windows_expired,
        'cron',
        hour=18, minute=00
    )

    schedule.add_job(
        say_about_requests,
        'cron',
        hour=18, minute=00
    )

    schedule.start()
    await dp.start_polling(bot)


if __name__ == "__main__":
    # db.migration.migration_down()
    # db.migration.migration_up()
    asyncio.run(main())






# todo реализовать список учителей

# @ dp.message(ContentType.PHOTO)
# async def handle_photo(message: Message, state: FSMContext):
#     print("Получена фотография")
#     photo_file_id = message.photo[-1].file_id
#     # Здесь можно добавить дополнительную логику для обработки фотографии
#
#     await message.answer(f"Спасибо за фотографию! Файл ID: {photo_file_id}")
#
#
# @ dp.message(ContentType.VIDEO)
# async def handle_video(message: Message, state: FSMContext):
#     print("Получено видео")
#     video_file_id = message.video.file_id
#     # Здесь можно добавить дополнительную логику для обработки видео
#
#     await message.answer(f"Спасибо за видео! Файл ID: {video_file_id}")
#
#
# @ dp.message(ContentType.DOCUMENT)
# async def handle_document(message: Message, state: FSMContext):
#     print("Получен документ")
#     document_file_id = message.document.file_id
#     # Здесь можно добавить дополнительную логику для обработки документа
#
#     await message.answer(f"Спасибо за документ! Файл ID: {document_file_id}")
#
#
# @ dp.message(ContentType.AUDIO)
# async def handle_audio(message: Message, state: FSMContext):
#     print("Получено аудио")
#     audio_file_id = message.audio.file_id
#     # Здесь можно добавить дополнительную логику для обработки аудио
#
#     await message.answer(f"Спасибо за аудио! Файл ID: {audio_file_id}")
#
#
# @ dp.message(ContentType.STICKER)
# async def handle_sticker(message: Message, state: FSMContext):
#     print("Получен стикер")
#     sticker_file_id = message.sticker.file_id
#     # Здесь можно добавить дополнительную логику для обработки стикера
#
#     await message.answer(f"Спасибо за стикер! Файл ID: {sticker_file_id}")
#
#
# @ dp.message(ContentType.VOICE)
# async def handle_voice(message: Message, state: FSMContext):
#     print("Получено голосовое сообщение")
#     voice_file_id = message.voice.file_id
#     # Здесь можно добавить дополнительную логику для обработки голосового сообщения
#
#     await message.answer(f"Спасибо за голосовое сообщение! Файл ID: {voice_file_id}")
#
#
# @ dp.message(ContentType.VIDEO_NOTE)
# async def handle_video_note(message: Message, state: FSMContext):
#     print("Получено видео-сообщение")
#     video_note_file_id = message.video_note.file_id
#     # Здесь можно добавить дополнительную логику для обработки видео-сообщения
#
#     await message.answer(f"Спасибо за видео-сообщение! Файл ID: {video_note_file_id}")
