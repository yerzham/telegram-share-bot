# -*- coding: utf-8 -*-

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
    message =  update.message.from_user.first_name + ': ' + update.message.text
    print(message)

    response = 'Привет, ' + update.message.from_user.first_name + '. Я бот, который будет пересылать все ваши отправленные мне сообщения случайным людям, которые напишут мне команду /share.'
    bot.send_message(chat_id=update.message.chat_id, text=response)
    bot.send_message(chat_id=update.message.chat_id, text='Вы можете поделиться новостями или интересными идеями. Я и мои собеседники будут рады от вас это услышать!')
    bot.send_message(chat_id=update.message.chat_id, text='Но не вводите личную информацию...')
    bot.send_message(chat_id=update.message.chat_id, text='Для помощи, введите /help')

    if not update.message.from_user.is_bot:
        query = "SELECT user_id FROM users WHERE user_id = '" + str(update.message.from_user.id) + "';"
        print("EXECUTED QUERY:")
        print(query)
        
        with sql.connect("messages.db") as con:
            try:
                cur = con.cursor()
                cur.execute(query)
                res = cur.fetchall()
                if len(res) == 0:
                    query = "INSERT INTO users (user_id, user_name, last_active) VALUES('" 
                    query += str(update.message.from_user.id) 
                    query += "', '" 
                    query += update.message.from_user.first_name 
                    query += "', '" + datetime.datetime.now().strftime("%H:%M:%S") + "');"
                    print("EXECUTED QUERY:")
                    print(query)

                    cur.execute(query)
                con.commit()
            except sql.Error as e:   
                print("Error %s:" % e.args[0])

def textMessage(bot, update):
    message =  update.message.from_user.first_name + ': ' + update.message.text
    print(message)

    allow = False

    with sql.connect("messages.db") as con:
        try:
            query = "SELECT user_id, last_active FROM users WHERE user_id = " + str(update.message.from_user.id) + ";"
            print("EXECUTED QUERY:")
            print(query)

            cur = con.cursor()
            cur.execute(query)
            res = cur.fetchall()
            

            if len(res) == 0:
                bot.send_message(chat_id=update.message.chat_id, text='Я не могу вам ответить :(. Зарегистрируйтесь в моей системе, просто введите /start')
            elif abs(int(res[0][1][3:5]) - int(datetime.datetime.now().strftime("%M"))) > 0:
                print(res[0][1][3:5], ":", datetime.datetime.now().strftime("%M"))

                query = "UPDATE users SET last_active = '" + datetime.datetime.now().strftime("%H:%M:%S") + "' WHERE user_id = " + str(update.message.from_user.id) + ";"
                print("EXECUTED QUERY:")
                print(query)
                cur.execute(query)

                allow = True
            else:
                bot.send_message(chat_id=update.message.chat_id, text='Простите, я не успеваю обработать..')


            con.commit()
        except sql.Error as e:   
            print("Error %s:" % e.args[0])

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
        print("EXECUTED QUERY:")
        print(query)

            
        with sql.connect("messages.db") as con:
            try:
                cur = con.cursor()
                cur.execute(query)

                query = "SELECT message_id FROM messages WHERE messages.text_sent = '" + update.message.text 
                query += "' AND messages.from_user = '" + str(update.message.from_user.id) + "';"
                print("EXECUTED QUERY:")
                print(query)

                cur.execute(query)
                res = cur.fetchone()

                query = "INSERT INTO history (user_id, message_id) VALUES('" + str(update.message.from_user.id) + "', " 
                query += str(res[0]) + ");"
                print("EXECUTED QUERY:")  
                print(query)

                cur.execute(query)

                con.commit()
            except sql.Error as e:   
                print("Error %s:" % e.args[0])

def individualreq(bot, update, args):
    id = update.message.text
    message =  update.message.from_user.first_name + ': ' + update.message.text
    print(message)

    id = id[1:]
    if id == 'share':
        with sql.connect("messages.db") as con:
            try:
                query = "SELECT message_id, from_user, text_sent FROM messages"
                print("EXECUTED QUERY:")
                print(query)

                cur = con.cursor()
                cur.execute(query)
                res = cur.fetchall()

                found = False

                while (not found) and (len(res)!=0):
                    i = random.randint(0,len(res)-1)

                    query = "SELECT message_id, user_id FROM history WHERE message_id = " + str(res[i][0]) + " AND user_id = '" + str(res[i][1]) + "';"
                    print("EXECUTED QUERY:")  
                    print(query)

                    cur.execute(query)
                    res2 = cur.fetchall()

                    if (len(res2) == 0):
                        found = True
                    else:
                        res.pop(i)
                if len(res)!=0:
                    query = "SELECT user_name FROM users WHERE users.user_id = '" + str(res[i][1]) + "';"
                    print("EXECUTED QUERY:")  
                    print(query)

                    cur.execute(query)
                    res2 = cur.fetchone()

                    query = "INSERT INTO history (user_id, message_id) VALUES('" + str(update.message.from_user.id) + "', " 
                    query += str(res[i][0]) + ");"
                    print("EXECUTED QUERY:")  
                    print(query)

                    cur.execute(query)

                    response = str(res2[0]) + ": " + res[i][2]
                else:
                    response = "Простите, вы уже все посмотрели. Можете теперь сами мне написать, мы прочитаем!"
                    
                bot.send_message(chat_id=update.message.chat_id, text=response)
                con.commit()
            except sql.Error as e:   
                print("Error %s:" % e.args[0])
    elif id == 'help':
        response = 'Очень рад что вы заинтересованы. Я бот, который сахраняет все отправленные мне сообщения в базу данных и храню их там один день'
        bot.send_message(chat_id=update.message.chat_id, text=response)
        response = 'Если мой собеседник присылает мне команду /share, я отвечаю ему случайно выбранным сообщением, которое хранится в той базе данных'
        bot.send_message(chat_id=update.message.chat_id, text=response)
        response = 'Пишите мне то, что хотите донести случайным людям. Я сделаю это за вас. Удачи!'
        bot.send_message(chat_id=update.message.chat_id, text=response)


start_command_handler = CommandHandler('start', startCommand)
text_message_handler = MessageHandler(Filters.text, textMessage)

dispatcher.add_handler(start_command_handler)
dispatcher.add_handler(text_message_handler)
dispatcher.add_handler(CommandHandler(['share', 'help'], individualreq, pass_args=True))

updater.start_polling(clean=True)

updater.idle()