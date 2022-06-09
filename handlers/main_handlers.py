import logging
from asyncio import sleep
import gspread
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from chats import supportChat
from markups import system_reply_markup, reply_start_keyboard, reply_start_keyboard_support
from create_bot import bot, botDatabase
from support_query_chain import support_query_start, clarify_task_start, setDoneStatus


async def get_me(message: types.Message):
    await bot.send_message(message.chat.id, str(message.chat.id))


async def get_task(message: types.Message):
    # print('aim')
    task_id = message.text.lower().replace('найти ', '')
    # print(task_id)
    ans = botDatabase.get_task(task_id)
    await bot.send_message(message.chat.id, ans)


async def long_test(message: types.Message):
    await sleep(10)
    await bot.send_message(message.chat.id, str(message.chat.id))


async def short_test(message: types.Message):
    await bot.send_message(message.chat.id, str(message.chat.id))


async def start(message: types.Message):
    isSupportUser = botDatabase.get_support_user_name_by_chat_id(message.chat.id)
    if str(message.chat.id) == supportChat:
        await message.reply('Запрос формируется вне чата поддержки!')
    elif isSupportUser:
        ans_text = 'Добрый день! \nЭтот бот создан для удобства общения с технической поддержкой по часто возникающим ' \
                   'вопросам.\nРаботая с ботом, будьте уверены, что Ваш вопрос дойдет быстро и точно по адресу. А ' \
                   'дополнительная информация позволит решить вопрос в максимально короткий срок! \nХорошего дня!!'
        await bot.send_message(message.chat.id, ans_text, parse_mode='HTML', reply_markup=reply_start_keyboard_support())
    else:
        ans_text = 'Добрый день! \nЭтот бот создан для удобства общения с технической поддержкой по часто возникающим ' \
                   'вопросам.\nРаботая с ботом, будьте уверены, что Ваш вопрос дойдет быстро и точно по адресу. А ' \
                   'дополнительная информация позволит решить вопрос в максимально короткий срок! \nХорошего дня!'
        await bot.send_message(message.chat.id, ans_text, parse_mode='HTML', reply_markup=reply_start_keyboard())


async def sup_query_start(message: types.Message):
    if botDatabase.check_allow_user_to_create_new_task(message.chat.id):
        await support_query_start(message)
    else:
        await bot.send_message(message.chat.id, "Вы не можете создать новую заявку пока не завершены предыдущие!")


async def clarify_task(message: types.Message):
    await clarify_task_start(message)


# @dp.message_handler(commands=['to_bot'])
# @dp.message_handler(Text(contains='аявка'))
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
        # logging.info(e)
        await message.reply('Не удалось зафиксировать Ваш вопрос, просьба направить на почту '
                            'supportPM@ac.gov.ru, спасибо!')
        await bot.send_message('287994530', "Ошибка в работе бота KC_bitrix_help_bot: "
                                            "не удалось записать данные в гугл-шит. "
                                            f"Подробности: \n {e}")


async def accept_task(message: types.Message):
    if not (str(message.chat.id) == supportChat):
        await bot.send_message(message.chat.id, 'Данная команда применяется только в чате тех поддержки!')
        return False

    if not getattr(message, 'reply_to_message'):
        await bot.send_message(message.chat.id, 'Ошибка! Возможно необходимо сделать reply на сообщение!')
        return False

    if not getattr(message.reply_to_message.from_user, 'is_bot'):
        await bot.send_message(message.chat.id, 'Исходное сообщение пришло не от бота!')
        return False
    else:
        # await bot.send_message(message.chat.id, 'Все нормально!')
        isMsgFromBot = True
        try:
            st = message.reply_to_message.text.find('№ ') + 2
            end = message.reply_to_message.text.find('!')
            task_id = int(message.reply_to_message.text[st:end])
            # print(isinstance(task_id, int))
        except Exception as e:
            await bot.send_message(message.chat.id, 'Не могу извлечь номер запроса!')
            logging.info(e)
            return False

        try:
            await bot.send_message(message.chat.id, 'Проверка статуса задачи...')
            is_in_progress = botDatabase.is_in_progress(task_id)
            if is_in_progress:
                await bot.send_message(message.chat.id, 'Заявка уже в в работе!')
            else:
                await bot.send_message(message.chat.id, 'Заявка не в работе...')
        except Exception as e:
            logging.info(e)
            await bot.send_message(message.chat.id, 'Нет доступа к базе данных. Возможно заявка уже в работе.')
            return False

        if is_in_progress:
            user_name = botDatabase.get_support_user_name_by_task_id(task_id)
            await bot.send_message(message.chat.id, f"Задача ранее была назначена на сотрудника поддержки: "
                                                    f"{str(user_name)}", parse_mode='HTML')
        elif isMsgFromBot and str(message.chat.id) == supportChat and not is_in_progress:
            isUserFromSupport = botDatabase.get_support_user_name_by_chat_id(message.from_user.id)
            if isUserFromSupport:
                user_name = botDatabase.set_task_status_in_progress(task_id, message.from_user.id)
                await bot.send_message(message.chat.id, f"Задача успешно назначена на сотрудника: {str(user_name)}",
                                       parse_mode='HTML')
            else:
                await message.reply('Ошибка! Попробуйте еще раз! Необходимо проверить является ли принимающий '
                                    'на себя задачу сотрудник, сотрудником тех. поддержки...')
                return False
        else:
            await message.reply('Ошибка!')
            return False


async def redirect_all_while_task_in_progress(message: types.Message):
    """Функция пересылки сообщений от юзера исполнителю заявки"""
    userHaveTaskInProgress = not botDatabase.check_allow_user_to_create_new_task(message.from_user.id)
    print('userHaveTaskInProgress:  ' + str(userHaveTaskInProgress))
    print('message_from_user_id:' + str(message.from_user.id))
    empl_from_support = botDatabase.cnd_redirect(message.from_user.id)
    print('empl_from_support:  ' + str(empl_from_support))

    # task_is_in_progress = botDatabase.get_task_user_from_id()
    if empl_from_support and userHaveTaskInProgress:
        await message.forward(empl_from_support)
    else:
        print('Обычное сообщение!')


async def set_done_handler(message:types.Message):
    """Функция для закрытия задачи"""
    await setDoneStatus(message)


def register_main_handlers(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(get_me, commands=['getchatid'])
    dp.register_message_handler(get_task, Text(contains='найти', ignore_case=True))
    dp.register_message_handler(short_test, Text(equals='шорттест', ignore_case=True))
    dp.register_message_handler(long_test, Text(equals='лонгтест', ignore_case=True))
    dp.register_message_handler(accept_task, Text(ignore_case=True, equals='принято'))
    dp.register_message_handler(sup_query_start, Text(equals='Составить обращение', ignore_case=True))
    dp.register_message_handler(clarify_task, Text(equals='Получить комментарий по запросу', ignore_case=True))
    dp.register_message_handler(set_done_handler, Text(equals='Закрыть запрос', ignore_case=True))
    dp.register_message_handler(redirect_all_while_task_in_progress)
