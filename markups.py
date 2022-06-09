from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


def reply_start_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('Составить обращение', ))
    return markup


def reply_start_keyboard_support():
    markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True).add(KeyboardButton('Составить обращение'),
                                                           KeyboardButton('Получить комментарий по запросу'),
                                                           KeyboardButton('Закрыть запрос'))
    return markup


def system_reply_markup():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(InlineKeyboardButton('PM', callback_data='PM'), InlineKeyboardButton('IMS', callback_data='IMS'))
    return markup


def project_reply_markup():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton('Проект1', callback_data='project1'),
               InlineKeyboardButton('Проект2', callback_data='project2'),
               InlineKeyboardButton('Проект3', callback_data='project3'),
               InlineKeyboardButton('Проект4', callback_data='project4'),
               InlineKeyboardButton('Проект5', callback_data='project5'))
    return markup


def category_reply_markup():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton('Категория1', callback_data='Category1'),
               InlineKeyboardButton('Категория1', callback_data='Category2'))
    return markup
