import logging
import gspread
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters import Text
from datetime import datetime as dt
from key import token
from aiogram.utils import executor

API_TOKEN = token

# Подключаем соответствующую конфигурацию логгирования документа
logging.basicConfig(level=logging.INFO)

# Создаем экземпляры классов Bot и Dispatcher, которые мы заранее ипортировали
# из библиотеки aiogram на строке 2
bot = Bot(token=API_TOKEN)

dp = Dispatcher(bot)


# import os
# print(os.listdir("."))

async def on_startup(_):
    logging.info("Bot was started")


# @dp.message_handler(Text(contains='ривет'))
# async def reply_hello(message: types.Message):
#     await message.reply("Привет! Желаю хорошего дня!")


@dp.message_handler(commands=['to_bot'])
@dp.message_handler(Text(contains='аявка'))
async def get_question(message: types.Message):
    # fsa = "KC_bitrix_help_bot\\service_account.json"
    fsa = "service_account.json"
    sa = gspread.service_account(fsa)
    sh = sa.open("Bitrix_bot_table")

    wsh = sh.worksheet('Data')

    try:
        wsh.append_row(
            [str(message.date.now().strftime('%Y-%m-%d %H:%M')), message.chat.id, " ", message.from_user.id,
             message.from_user.username, message.from_user.full_name, message.text])
        await message.reply('Спасибо, заявка зарегистрирована, с Вами свяжутся!')
    except Exception as e:
        logging.info(e)
        await message.reply('Не удалось зафиксировать Ваш вопрос, просьба направить на почту '
                            'supportPM@ac.gov.ru, спасибо!')
        await bot.send_message('287994530', "Ошибка в работе бота KC_bitrix_help_bot: "
                                            "не удалось записать данные в гугл-шит. "
                                            f"Подробности: \n {e}")


# def register_bot_handlers(pp: Dispatcher):

# pp.register_message_handler(get_question, text=['вопрос боту'], ignore_case=True)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
