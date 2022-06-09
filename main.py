import logging
from create_bot import dp
from aiogram.utils import executor
import handlers
from support_query_chain import register_supportchains_handler


# handlers.callback_handlers.register_call_handlers(dp)
handlers.main_handlers.register_main_handlers(dp)
register_supportchains_handler(dp)


async def on_startup(_):
    logging.info("Bot was started")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
