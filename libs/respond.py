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
    response = 'Очень рад что вы заинтересованы. Я бот, который на 24 часа сохраняет все отправленные мне сообщения в базе данных'
    bot.send_message(chat_id=update.message.chat_id, text=response)
    response = 'Если мой собеседник присылает мне команду /share, я отвечаю ему случайно выбранным сообщением, которое хранится в той базе данных'
    bot.send_message(chat_id=update.message.chat_id, text=response)
    response = 'Пишите мне то, что хотите донести случайным людям. Я сделаю это за вас. Удачи!'
    bot.send_message(chat_id=update.message.chat_id, text=response, reply_markup=kb_markup)

def register(bot, update, kb_markup):
    bot.send_message(chat_id=update.message.chat_id, text='Я не могу вам ответить :(. Зарегистрируйтесь в моей системе, просто введите /start', reply_markup=kb_markup)

def wait(bot, update, kb_markup):
    bot.send_message(chat_id=update.message.chat_id, text='Я не могу вам ответить :(. Зарегистрируйтесь в моей системе, просто введите /start', reply_markup=kb_markup)

def received(bot, update, kb_markup, text):
    response = update.message.from_user.first_name + u', я получил Ваше сообщение: "' + text + u'". Спасибо за то что поделились этим!'
    bot.send_message(chat_id=update.message.chat_id, text=response)
    bot.send_message(chat_id=update.message.chat_id, text='Помните, ваши данные могут быть видны другим моим собеседникам. Не вводите личную информацию.', reply_markup=kb_markup)