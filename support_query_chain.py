import logging
import re
from datetime import datetime
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

# from connection import add_task_to_db
from chats import supportChat
from create_bot import SupportQuery, ClarifyTask, bot, dp, botDatabase, CloseTask
from markups import system_reply_markup, project_reply_markup_1, project_reply_markup_2, category_reply_markup


# Цепь опроса через ClarifyTask
async def clarify_task_start(message: types.Message):
    await ClarifyTask.taskNum.set()
    await bot.send_message(message.chat.id, 'Укажите номер заявки, по которой необходимо получить дополнительный '
                                            'комментарий', parse_mode='HTML')


async def get_task_id_and_ask_user_comment(message: types.Message, state: FSMContext):
    # print('попал')

    check1 = re.findall(r"\d+", message.text)
    # task_id = ''
    isInProgress = ''
    userFromId = 0
    if check1 and len(message.text)<5:
        # print("Номер заявки после парсинга сообщения: " + str(check1))
        task_id = int(message.text)
        try:
            isInProgress = botDatabase.is_in_progress(task_id)
            # print(str(isInProgress))
            userFromId = botDatabase.get_task_user_from_id(task_id)
            # userOfSupport = botDatabase.get_support_user_name_by_task_id(task_id)

            # print(str(userFromId))
        except Exception as e:
            logging.info(e)
            await cancel_handler(message, state)
            await bot.send_message(message.chat.id, 'Ошибка в номере заявки или запросе к базе данных!')
    if isInProgress and userFromId > 1:
        await bot.send_message(message.chat.id, 'Заявка найдена', parse_mode='HTML')
        await ClarifyTask.next()
        await bot.send_message(message.chat.id, 'Напишите комментарий для пользователя', parse_mode='HTML')
    else:
        await bot.send_message(message.chat.id, 'Ошибка с заявкой. Заявка не в работе, либо не получен userFromId, '
                                                'либо заявка назначена на другого сотрудника!')
        await cancel_handler(message, state)

    async with state.proxy() as data:
        data['task_id'] = message.text
        data['userFromId'] = userFromId


async def get_user_comment(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        print(data)
        print('Получен таксИД' + str(data['task_id']))
        data['comment'] = message.text
        await bot.send_message(chat_id=data['userFromId'], text=data['comment'])
    await state.finish()


# Цепь опроса через SupportQueryClass
async def support_query_start(message: types.Message):
    await SupportQuery.system.set()
    await bot.send_message(message.chat.id, 'Выберите систему по которой будет обращение:', parse_mode='HTML',
                           reply_markup=system_reply_markup())


async def project(call: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(call.id)
    await call.message.delete_reply_markup()
    await bot.send_message(call.from_user.id, 'Выбрана система: ' + call.data)

    async with state.proxy() as data:
        data['system'] = call.data

    await SupportQuery.next()
    if data['system'] == 'IMS':
        await bot.send_message(call.from_user.id, 'Выберите проект в рамках которого будет обращение:',
                               parse_mode='HTML', reply_markup=project_reply_markup_2())
    else:
        await bot.send_message(call.from_user.id, 'Выберите проект в рамках которого будет обращение:',
                               parse_mode='HTML', reply_markup=project_reply_markup_1())


async def ticket_category(call: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(call.id)
    await call.message.delete_reply_markup()
    await bot.send_message(call.from_user.id, 'Выбранный проект: ' + call.data)

    async with state.proxy() as data:
        data['project'] = call.data
    await SupportQuery.next()
    await bot.send_message(call.from_user.id, 'Выберите категорию вопроса:', parse_mode='HTML',
                           reply_markup=category_reply_markup())


async def additional_info(call: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(call.id)
    await call.message.delete_reply_markup()
    await bot.send_message(call.from_user.id, 'Выбранная категория: ' + call.data)

    async with state.proxy() as data:
        data['ticket_category'] = call.data
    await SupportQuery.next()
    await bot.send_message(call.from_user.id, 'Пожалуйста, укажите своё ФИО (полностью)')


async def additional_info_1(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['fio'] = message.text
    await SupportQuery.next()
    await bot.send_message(message.from_user.id, 'Пожалуйста, напишите свой e-mail, указанный при регистрации в '
                                                 'системе Битрикс. Например, IvanovGM@mail.ru')


async def phone(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['email'] = str(message.text)
    await SupportQuery.next()
    await bot.send_message(message.from_user.id, 'Укажите, пожалуйста, контактный номер телефона '
                                                 'для обратной связи по запросу')


async def additional_info_2(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['phone'] = message.text
    await SupportQuery.next()
    await bot.send_message(message.from_user.id, 'Расскажите подробно что случилось, в чем проблема и что '
                                                 'должна сделать служба поддержки по Вашему мнению')


async def additional_info_3(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['short_task_description'] = message.text
        data['user_from_id'] = message.from_user.id
        data['timestamp'] = str(datetime.now())
        data['task_status'] = 'New!'
    await state.finish()
    id = botDatabase.add_task_to_db(data)
    final_message = f"Новый запрос № {str(id)}!\n" \
                    + "Система: <b>" + str(data['system']) + "</b>\n" \
                    + "Проект: <b>" + data['project'] + "</b>\n" \
                    + "Категория обращения: <b>" + data['ticket_category'] + "</b>\n" \
                    + "ФИО: <b>" + data['fio'] + "</b>\n" \
                    + "Эл. почта: <b>" + str(data['email']) + "</b>\n" \
                    + "Описание: <b>" + data['short_task_description'] + "</b>\n" \
                    + "Дата регистрации: <b>" + str(data['timestamp']) + "</b>"
    await bot.send_message(supportChat, final_message, parse_mode='HTML')
    await bot.send_message(message.from_user.id, f'Отлично! Ваш запрос зарегистрирован под номером: <b>{id}</b> и уже '
                                                 f'направлен ответственному сотруднику, '
                                                 'который будет рад Вам помочь!', parse_mode='HTML')

# Цепь опроса через ClarifyTask
async def setDoneStatus(message: types.Message):
    await CloseTask.taskNum.set()
    await bot.send_message(message.chat.id, 'Укажите номер заявки, которую необходимо закрыть', parse_mode='HTML')


async def setDoneStatus2(message: types.Message, state: FSMContext):
    check1 = re.findall(r"\d+", message.text)
    isInProgress = ''
    task_id = 0
    userFromId = 0
    if check1 and len(message.text) < 5:
        print("Номер заявки после парсинга сообщения: " + str(check1))
        task_id = int(message.text)
        try:
            isInProgress = botDatabase.is_in_progress(task_id)
            # print(str(isInProgress))
            userFromId = botDatabase.get_task_user_from_id(task_id)
            # userOfSupport = botDatabase.get_support_user_name_by_task_id(task_id)

            # print(str(userFromId))
        except Exception as e:
            logging.info(e)
            await cancel_handler(message, state)
            await bot.send_message(message.chat.id, 'Ошибка в номере заявки или запросе к базе данных!')

    if isInProgress and userFromId > 1:
        await bot.send_message(message.chat.id, 'Заявка найдена, попытка перевести запрос в статус "Done"...',
                               parse_mode='HTML')
        r = botDatabase.set_task_status_is_done(task_id)
        if r:
            await bot.send_message(message.chat.id, f'Запрос {task_id} успешно завершен!',
                                   parse_mode='HTML')
            await bot.send_message(supportChat, f'Запрос {task_id} успешно завершен!',
                                   parse_mode='HTML')
            await bot.send_message(userFromId, f'Запрос {task_id} успешно завершен!',
                                   parse_mode='HTML')

    else:
        await bot.send_message(message.chat.id, 'Ошибка с заявкой. Заявка не в работе, либо не получен userFromId, '
                                                'либо заявка назначена на другого сотрудника!')
        await cancel_handler(message, state)

    async with state.proxy() as data:
        data['CloseTaskNum'] = message.text
        data['userFromId'] = userFromId

    await state.finish()


async def cancel_handler(message: types.Message, state: FSMContext):
    """
     Allow user to cancel any action
     """
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info('Cancelling state %r', current_state)
    # Cancel state and inform user about it
    await state.finish()
    # And remove keyboard (just in case)
    await bot.send_message(message.chat.id, 'Опрос отменен. Нужно выполнить команду /start заново!',
                           reply_markup=types.ReplyKeyboardRemove())


def register_supportchains_handler(dp: Dispatcher):
    dp.register_callback_query_handler(project, state=SupportQuery.system)
    dp.register_callback_query_handler(ticket_category, state=SupportQuery.project)
    dp.register_callback_query_handler(additional_info, state=SupportQuery.ticket_category)
    dp.register_message_handler(additional_info_1, state=SupportQuery.fio)
    dp.register_message_handler(additional_info_2, state=SupportQuery.mail)
    dp.register_message_handler(phone, state=SupportQuery.phone)
    dp.register_message_handler(additional_info_3, state=SupportQuery.short_task_description)
    dp.register_message_handler(cancel_handler, Text(equals='cancel', ignore_case=True), state='*')
    dp.register_message_handler(get_task_id_and_ask_user_comment, state=ClarifyTask.taskNum)
    dp.register_message_handler(get_user_comment, state=ClarifyTask.getComment)
    dp.register_message_handler(setDoneStatus2, state=CloseTask.taskNum)
