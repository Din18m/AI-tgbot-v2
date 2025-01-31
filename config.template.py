from aiogram import Bot, Dispatcher, Router
from apscheduler.schedulers.asyncio import AsyncIOScheduler

TOKEN_TG = "token"

NoneData = ""

# Инициализация бота
bot = Bot(token=TOKEN_TG)
dp = Dispatcher()
router = Router()

# Инициализация Напоминаний
schedule = AsyncIOScheduler()

DB_NAME = "postgres"
DB_PORT = 5440
DB_PASSWORD = "postgres"
DB_USER = "postgres"
DB_HOST = "postgres"

