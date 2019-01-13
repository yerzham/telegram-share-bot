#!/usr/bin/python -u
# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import KeyboardButton, ReplyKeyboardMarkup

token = ""

def welcome(bot, update, kb_markup):
    response = u'Привет, ' + update.message.from_user.first_name + u'. Я бот, который будет пересылать все ваши отправленные мне сообщения случайным людям, которые напишут мне команду /share.'
    bot.send_message(chat_id=update.message.chat_id, text=response)
    bot.send_message(chat_id=update.message.chat_id, text='Вы можете поделиться новостями или интересными идеями. Я и мои собеседники будут рады от вас это услышать!')
    bot.send_message(chat_id=update.message.chat_id, text='Но не вводите личную информацию...')
    bot.send_message(chat_id=update.message.chat_id, text='Для помощи, введите /help', reply_markup=kb_markup)

def help(bot, update, kb_markup):
    response = u'Очень рад что вы заинтересованы. Я бот, который на 24 часа сохраняет все отправленные мне сообщения в базе данных'
    bot.send_message(chat_id=update.message.chat_id, text=response)
    response = u'Если мой собеседник присылает мне команду /share, я отвечаю ему случайно выбранным сообщением, которое хранится в той базе данных'
    bot.send_message(chat_id=update.message.chat_id, text=response)
    response = u'Пишите мне то, что хотите донести случайным людям. Я сделаю это за вас. Удачи!'
    bot.send_message(chat_id=update.message.chat_id, text=response, reply_markup=kb_markup)

def register(bot, update, kb_markup):
    bot.send_message(chat_id=update.message.chat_id, text='Я не могу вам ответить :(. Зарегистрируйтесь в моей системе, просто введите /start', reply_markup=kb_markup)

def wait(bot, update, kb_markup):
    bot.send_message(chat_id=update.message.chat_id, text='Я могу не успеть все обработать. Пожалуйста, подождите минуту перед отправлением нового сообщения. Спасибо', reply_markup=kb_markup)

def received(bot, update, kb_markup, text):
    response = update.message.from_user.first_name + u', я получил Ваше сообщение: "' + text + u'". Спасибо за то что поделились этим!'
    bot.send_message(chat_id=update.message.chat_id, text=response)
    bot.send_message(chat_id=update.message.chat_id, text='Помните, ваши данные могут быть видны другим моим собеседникам. Не вводите личную информацию.', reply_markup=kb_markup)

def notify(bot, chat_id, kb_markup):
    response = u"С тех пор как вы все посмотрели, появились новые сообщения! Найдите время заглянуть, а то через день все исчезнет.."
    bot.send_message(chat_id=chat_id, text=response, reply_markup=kb_markup)


def stats(bot, update, kb_markup, text, views):
    response = u"" + str(views) + u' просмотров на "' + text + u'"'
    bot.send_message(chat_id=update.message.chat_id, text=response, reply_markup=kb_markup)

def empty(bot, update, kb_markup):
    response = u"У вас нет ваших сообщений на сегодня"
    bot.send_message(chat_id=update.message.chat_id, text=response, reply_markup=kb_markup)