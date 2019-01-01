#!/usr/bin/python -u
# -*- coding: utf-8 -*-

# v 0.0.1

import random
import sqlite3 as sql
import datetime
import sys
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

token = str(sys.argv[1])

updater = Updater(token=token) 
dispatcher = updater.dispatcher

messages = []

def startCommand(bot, update):
    try:
        response = 'Привет, ' + update.message.from_user.first_name + '. Я бот, который будет пересылать все ваши отправленные мне сообщения случайным людям, которые напишут мне команду /share.'
        bot.send_message(chat_id=update.message.chat_id, text=response)
        bot.send_message(chat_id=update.message.chat_id, text='Вы можете поделиться новостями или интересными идеями. Я и мои собеседники будут рады от вас это услышать!')
        bot.send_message(chat_id=update.message.chat_id, text='Но не вводите личную информацию...')
        bot.send_message(chat_id=update.message.chat_id, text='Для помощи, введите /help')

        if not update.message.from_user.is_bot:
            query = "SELECT user_id FROM users WHERE user_id = '" + str(update.message.from_user.id) + "';"
            
            with sql.connect("messages.db") as con:
                cur = con.cursor()
                cur.execute(query)
                res = cur.fetchall()
                if len(res) == 0:
                    query = "INSERT INTO users (user_id, user_name, last_active) VALUES('" 
                    query += str(update.message.from_user.id) 
                    query += "', '" 
                    query += update.message.from_user.first_name 
                    query += "', '" + datetime.datetime.now().strftime("%H:%M:%S") + "');"

                    cur.execute(query)
                con.commit()
    except Exception as e:   
        print(e)

def textMessage(bot, update):
    try:
        allow = False

        with sql.connect("messages.db") as con:
            query = "SELECT user_id, last_active FROM users WHERE user_id = " + str(update.message.from_user.id) + ";"

            cur = con.cursor()
            cur.execute(query)
            res = cur.fetchall()

            if len(res) == 0:
                bot.send_message(chat_id=update.message.chat_id, text='Я не могу вам ответить :(. Зарегистрируйтесь в моей системе, просто введите /start')
            elif abs(int(res[0][1][3:5]) - int(datetime.datetime.now().strftime("%M"))) > 0:
                query = "UPDATE users SET last_active = '" + datetime.datetime.now().strftime("%H:%M:%S") + "' WHERE user_id = " + str(update.message.from_user.id) + ";"
                cur.execute(query)

                allow = True
            else:
                bot.send_message(chat_id=update.message.chat_id, text='Простите, я не успеваю обработать.. Подождите минуту')
            con.commit()

        if allow:
            response = update.message.from_user.first_name + ', я получил Ваше сообщение: "' + update.message.text + '". Спасибо за то что поделились этим!'
            bot.send_message(chat_id=update.message.chat_id, text=response)
            bot.send_message(chat_id=update.message.chat_id, text='Помните, ваши данные могут быть видны другим моим собеседникам. Не вводите личную информацию.')
            
            query = "INSERT INTO messages (from_user, date_sent, time_sent, text_sent) VALUES('" 
            query += str(update.message.from_user.id) 
            query += "', '" 
            query += datetime.datetime.now().strftime("%Y-%m-%d")
            query += "', '" 
            query += datetime.datetime.now().strftime("%H:%M:%S") 
            query += "', '" 
            query += update.message.text + "');"

                
            with sql.connect("messages.db") as con:
                cur = con.cursor()
                cur.execute(query)

                query = "SELECT message_id FROM messages WHERE messages.text_sent = '" + update.message.text 
                query += "' AND messages.from_user = '" + str(update.message.from_user.id) + "';"

                cur.execute(query)
                res = cur.fetchone()

                query = "INSERT INTO history (user_id, message_id) VALUES('" + str(update.message.from_user.id) + "', " 
                query += str(res[0]) + ");"

                cur.execute(query)

                con.commit()
    except Exception as e:   
        print(e)

def individualreq(bot, update, args):
    try:
        id = update.message.text

        id = id[1:]
        if id == 'share':
            with sql.connect("messages.db") as con:
                query = "SELECT user_id, last_active FROM users WHERE user_id = " + str(update.message.from_user.id) + ";"

                cur = con.cursor()
                cur.execute(query)
                res = cur.fetchall()
                

                if len(res) == 0:
                    bot.send_message(chat_id=update.message.chat_id, text='Я не могу вам ответить :(. Зарегистрируйтесь в моей системе, просто введите /start')
                else:
                    query = "SELECT message_id, from_user, text_sent FROM messages"

                    cur = con.cursor()
                    cur.execute(query)
                    res = cur.fetchall()

                    found = False

                    while (not found) and (len(res)!=0):
                        i = random.randint(0,len(res)-1)

                        query = "SELECT message_id, user_id FROM history WHERE message_id = " + str(res[i][0]) + " AND user_id = '" + str(res[i][1]) + "';"

                        cur.execute(query)
                        res2 = cur.fetchall()

                        if (len(res2) == 0):
                            found = True
                        else:
                            res.pop(i)
                    if len(res)!=0:
                        query = "SELECT user_name FROM users WHERE users.user_id = '" + str(res[i][1]) + "';"

                        cur.execute(query)
                        res2 = cur.fetchone()

                        query = "INSERT INTO history (user_id, message_id) VALUES('" + str(update.message.from_user.id) + "', " 
                        query += str(res[i][0]) + ");"

                        cur.execute(query)

                        response = str(res2[0]) + ": " + res[i][2]
                    else:
                        response = "Простите, вы уже все посмотрели. Можете теперь сами мне написать, мы прочитаем!"
                        
                    bot.send_message(chat_id=update.message.chat_id, text=response)
                con.commit()
                
        elif id == 'help':
            response = 'Очень рад что вы заинтересованы. Я бот, который на 24 часа сохраняет все отправленные мне сообщения в базе данных'
            bot.send_message(chat_id=update.message.chat_id, text=response)
            response = 'Если мой собеседник присылает мне команду /share, я отвечаю ему случайно выбранным сообщением, которое хранится в той базе данных'
            bot.send_message(chat_id=update.message.chat_id, text=response)
            response = 'Пишите мне то, что хотите донести случайным людям. Я сделаю это за вас. Удачи!'
            bot.send_message(chat_id=update.message.chat_id, text=response)
    except Exception as e:   
        print(e)


start_command_handler = CommandHandler('start', startCommand)
text_message_handler = MessageHandler(Filters.text, textMessage)

dispatcher.add_handler(start_command_handler)
dispatcher.add_handler(text_message_handler)
dispatcher.add_handler(CommandHandler(['share', 'help'], individualreq, pass_args=True))

updater.start_polling(clean=True)

updater.idle()