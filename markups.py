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
    markup.add(InlineKeyboardButton('Форма: предприятия', callback_data='project1'),
               InlineKeyboardButton('Форма: запасы', callback_data='project2'),
               InlineKeyboardButton('Форма: туризм', callback_data='project3'),
               InlineKeyboardButton('Форма: лагеря отдыха', callback_data='project4'),
               InlineKeyboardButton('Справочник: лагеря', callback_data='project5'),
               InlineKeyboardButton('Регионы: стратегии цифровой трансформации', callback_data='project6'),
               InlineKeyboardButton('Фронтальная стратегия ЦТ', callback_data='project7'),
               InlineKeyboardButton('База знаний', callback_data='project8'),
               InlineKeyboardButton('Союзное государство', callback_data='project9'),
               InlineKeyboardButton('ДФО', callback_data='project10'))
    return markup


def category_reply_markup():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton('Смена ответственного за проект', callback_data='Category1'),
               InlineKeyboardButton('Создание учётной записи ', callback_data='Category2'),
               InlineKeyboardButton('Ошибка входа: неверное контрольное слово', callback_data='Category3'),
               InlineKeyboardButton('Смена устройства для двухфакторной авторизации', callback_data='Category4'),
               InlineKeyboardButton('Ошибка входа: неверный логин-пароль', callback_data='Category5'),
               InlineKeyboardButton('Ошибка входа: двухэтапная авторизация (неверный одноразовый код)', callback_data='Category6'),
               InlineKeyboardButton('Консультация', callback_data='Category7'),
               InlineKeyboardButton('Ошибка в модуле форм', callback_data='Category8'),
               InlineKeyboardButton('Иное', callback_data='Category9'))
    return markup
