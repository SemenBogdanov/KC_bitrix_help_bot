import logging
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.utils import executor

from BotDB import BotDB
from key import token


API_TOKEN = token

# Подключаем соответствующую конфигурацию логгирования документа
logging.basicConfig(level=logging.INFO)

# Создаем экземпляры классов Bot и Dispatcher, которые мы заранее ипортировали
# из библиотеки aiogram на строке 2
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

try:
    botDatabase = BotDB()
except Exception as e:
    print(e)


class SupportQuery(StatesGroup):
    system = State()
    project = State()
    ticket_category = State()
    fio = State()
    mail = State()
    phone = State()
    short_task_description = State()


class ClarifyTask(StatesGroup):
    taskNum = State()
    getComment = State()


class CloseTask(StatesGroup):
    taskNum = State()
