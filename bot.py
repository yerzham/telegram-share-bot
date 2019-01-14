#!/usr/bin/python -u
# -*- coding: utf-8 -*-

# v 0.0.4 Tlek

import random
import datetime
import sys
from libs import respond
from libs import sql_query as sql
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import KeyboardButton, ReplyKeyboardMarkup

token = str(sys.argv[1])
respond.token = token

updater = Updater(token=token) 
dispatcher = updater.dispatcher

kb_def = [[KeyboardButton('/share')], [KeyboardButton('/stats')]]
kb_reg = [[KeyboardButton('/start')]]
kb_markup = ReplyKeyboardMarkup(kb_def, resize_keyboard=True)
kb_markup_reg = ReplyKeyboardMarkup(kb_reg, resize_keyboard=True)

def startCommand(bot, update):
    try:
        respond.welcome(bot, update, kb_markup)

        if not update.message.from_user.is_bot:
            res = sql.user(update.message.from_user.id)
            if len(res) == 0:
                sql.recordUser(update.message.from_user.id, 
                               update.message.from_user.first_name, 
                               datetime.datetime.now().strftime("%H:%M:%S"), 
                               update.message.chat_id, 0)
    except Exception as e:   
        print(e)

def textMessage(bot, update):
    try:
        allow = False
        res = sql.user(str(update.message.from_user.id))

        if len(res) == 0:
            respond.register(bot, update, kb_markup_reg)
        elif abs(int(res[0][0][3:5]) - int(datetime.datetime.now().strftime("%M"))) > 0:
            sql.recordActivity(update.message.from_user.id, datetime.datetime.now().strftime("%H:%M:%S"))
            sql.recordChatID(update.message.from_user.id, update.message.chat_id)
            allow = True
        else:
            respond.wait(bot, update, kb_markup)

        if allow:
            respond.received(bot, update, kb_markup, update.message.text)
            sql.recordMessage(update.message.from_user.id,
                              datetime.datetime.now().strftime("%Y-%m-%d"),
                              datetime.datetime.now().strftime("%H:%M:%S"),
                              update.message.text)
            res = sql.messageID(update.message.from_user.id, update.message.text)
            sql.recordHistory(update.message.from_user.id, res[0], 0)
            res = sql.browsed()
            reset = True
            for data in res:
                if data[1] != str(update.message.from_user.id): #data[1] - user_id
                    respond.notify(bot, data[0], kb_markup)     #data[0] - chat_id
            sql.resetBrowsed()
    except Exception as e:   
        print(e)

def individualreq(bot, update, args):
    try:
        id = update.message.text

        id = id[1:]
        if id == 'share':
            res = sql.user(update.message.from_user.id)
                
            if len(res) == 0:
                respond.register(bot, update, kb_markup_reg)
            else:
                sql.recordChatID(update.message.from_user.id, update.message.chat_id)
                res = sql.messages()
                found = False

                while (not found) and (len(res)!=0):
                    i = random.randint(0,len(res)-1)
                    if not sql.in_history(update.message.from_user.id, res[i][0]):
                        found = True
                    else:
                        res.pop(i)
                if len(res)!=0:
                    sql.recordHistory(update.message.from_user.id, res[i][0], res[i][3]+1)
                    response = u"[O]: " + res[i][2]
                    if len(res) == 1:
                        sql.recordBrowsed(update.message.from_user.id)
                else:    
                    sql.recordBrowsed(update.message.from_user.id)
                    response = u"Простите, вы уже все посмотрели. Можете теперь сами мне написать, мы прочитаем!"
                bot.send_message(chat_id=update.message.chat_id, text=response, reply_markup=kb_markup)    
        
        elif id == 'help':
            respond.help(bot, update, kb_markup)
            sql.recordChatID(update.message.from_user.id, update.message.chat_id)

        elif id == 'stats':
            res = sql.user(update.message.from_user.id)
            
            if len(res) == 0:
                respond.register(bot, update, kb_markup_reg)
            else:
                res = sql.stats(update.message.from_user.id)
                if len(res) == 0:
                    respond.empty(bot, update, kb_markup)
                else:
                    for stat in res:
                        respond.stats(bot, update, kb_markup, stat[0], stat[1]) # stat[0] - text_sent | stat[1] - views
    except Exception as e:   
        print(e)


start_command_handler = CommandHandler('start', startCommand)
text_message_handler = MessageHandler(Filters.text, textMessage)

dispatcher.add_handler(start_command_handler)
dispatcher.add_handler(text_message_handler)
dispatcher.add_handler(CommandHandler(['share', 'help', 'stats'], individualreq, pass_args=True))

updater.start_polling(clean=True)

updater.idle()