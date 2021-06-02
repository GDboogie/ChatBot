from uuid import uuid4

import telebot
from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from config import TELEGRAM_TOKEN
from db import orm
from db.database import get_db

bot = telebot.TeleBot(TELEGRAM_TOKEN, parse_mode=None)


def gen_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton('Все верно', callback_data="cb_yes"),
               InlineKeyboardButton('Ошибся', callback_data="cb_no"))
    return markup


@bot.message_handler(commands=['start'])
def command_start(m):
    user_from = m.json['from']
    db = get_db()
    user = db.query(orm.User).filter(orm.User.chat_id == user_from['id']).first()
    if user:
        greet = f'Здравствуйте, {user.user_name}!'
        message = 'Вы можете задать мне свои вопрсосы, по одному за раз'
        bot.send_message(user.chat_id, greet)
        bot.send_message(user.chat_id, message)
        return

    user = orm.User(
        uuid=uuid4(),
        first_name=user_from['first_name'],
        user_name=user_from['username'],
        chat_id=user_from['id'],
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    greet = f'Здравствуйте! Приятно познакомиться, {user.user_name}!'
    message = 'Вы можете задать мне свои вопрсосы, по одному за раз'
    bot.send_message(user.chat_id, greet)
    bot.send_message(user.chat_id, message)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call: CallbackQuery):
    if call.data in ('cb_yes', 'cb_no'):
        bot.answer_callback_query(call.id, 'Ваш ответ учтен')
    if call.data == 'cb_no':
        message = call.message
        bot.reply_to(message, 'Пожалуйста, отправьте правильный ответ на ваш вопрос, '
                              'чтобы я знал, как на него ответить')


@bot.message_handler(func=lambda message: True, content_types=['text'])
def msg_handler(message: Message):
    msg = message.json
    db = get_db()
    user = db.query(orm.User).filter(orm.User.chat_id == msg['from']['id']).first()
    message_obj = orm.Message(
        uuid=uuid4(),
        user_uuid=user.uuid,
        date=msg['date'],
        text=msg['text'],
    )
    db.add(message_obj)
    db.commit()
    db.refresh(message_obj)

    messages = db.query(orm.Message).filter(orm.Message.user == user).count()

    if messages == 1:
        reply = '*Адрес*: г. Краснодар, ул. Ставропольская, 149, ауд. 134\n' \
                '*Контактный телефон*: (8-861) 219-95-30\n' \
                '*E-mail*: abitur@kubsu.ru\n'
    elif messages == 2:
        reply = 'Спасибо, за помощь!'
    else:
        reply = '*График работы приемной комиссии*\n' \
                'Понедельник - Пятница\n' \
                'с 9:00 до 13:00\n' \
                'с 13:30 до 17:30'

    if msg['text'] == 'Какая сегодня погода?':
        reply = 'Извините, но я Вас не понял'
        bot.reply_to(message, reply, parse_mode='markdown')
        return

    if msg['text'] == 'Где найти списки паступления?':
        reply = 'Перефразируйте вопрос или попробуйте найти информацию на ' \
                '<a href="https://kubsu.ru">сайте университета</a>'
        bot.reply_to(message, reply, parse_mode='HTML')
        return

    if messages == 2:
        bot.reply_to(message, reply, parse_mode='markdown')
    else:
        bot.reply_to(message, reply, parse_mode='markdown', reply_markup=gen_markup())


bot.polling()
