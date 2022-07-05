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


def project_reply_markup_1():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton('Форма: предприятия', callback_data='Form_enterprises'),
               InlineKeyboardButton('Форма: запасы', callback_data='Form_supply'),
               InlineKeyboardButton('Форма: туризм', callback_data='Form_tourism'),
               InlineKeyboardButton('Форма: лагеря отдыха', callback_data='Form_holiday_camps'),
               InlineKeyboardButton('Справочник: лагеря', callback_data='Dict_camps'),
               InlineKeyboardButton('Регионы: стратегии цифровой трансформации',
                                    callback_data='Regions_digital_transform'),
               InlineKeyboardButton('Фронтальная стратегия ЦТ', callback_data='Frontal_strategy_CT'),
               InlineKeyboardButton('База знаний', callback_data='Knowledge_database'),
               InlineKeyboardButton('Союзное государство', callback_data='UnionState'),
               InlineKeyboardButton('ДФО', callback_data='DFO'))
    return markup

def project_reply_markup_2():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton('Инциденты', callback_data='Incidents'))
    return markup


def category_reply_markup():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton('Смена ответственного за проект', callback_data='change_responsibility'),
               InlineKeyboardButton('Создание учётной записи ', callback_data='create_account'),
               InlineKeyboardButton('Ошибка входа: неверное контрольное слово', callback_data='Bad_entry_Wrong_word'),
               InlineKeyboardButton('Смена устройства для двухфакторной авторизации',
                                    callback_data='Change_device_for_two_steps_auth'),
               InlineKeyboardButton('Ошибка входа: неверный логин-пароль',
                                    callback_data='Bad_entry_Wrong_login_or_pass'),
               InlineKeyboardButton('Ошибка входа: двухэтапная авторизация (неверный одноразовый код)',
                                    callback_data='Bad_entry_Wrong_invalig_one_time_code'),
               InlineKeyboardButton('Консультация', callback_data='Consultation'),
               InlineKeyboardButton('Ошибка в модуле форм', callback_data='Error_module_form'),
               InlineKeyboardButton('Иное', callback_data='Other'))
    return markup
