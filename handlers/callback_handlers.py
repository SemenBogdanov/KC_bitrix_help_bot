from aiogram import types
from aiogram import Dispatcher
from create_bot import bot
#
#
# async def answer_to_user_for_call(call: types.CallbackQuery):
#     await bot.answer_callback_query(call.id)
#     await call.message.delete_reply_markup()
#     await bot.send_message(call.from_user.id, 'Выбрана система: ' + call.data)
#
#
# def register_call_handlers(dp: Dispatcher):
#     dp.register_callback_query_handler(answer_to_user_for_call)
