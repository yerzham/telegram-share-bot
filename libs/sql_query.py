#!/usr/bin/python -u
# -*- coding: utf-8 -*-

import sqlite3 as sql

def recordUser(ID, name, time, chat_id, browsed):
    try:
        with sql.connect("messages.db") as con:
            cur = con.cursor()
            query = u"INSERT INTO users (user_id, user_name, last_active, chat_id, browsed) VALUES('" 
            query += str(ID)
            query += u"', '" + name
            query += u"', '" + time
            query += u"', '" + str(chat_id)
            query += u"', " + str(browsed) + ");"
            cur.execute(query)
            con.commit()
    except Exception as e:   
        print(e)
    print("EXE: ", "INSERT INTO users (user_id, user_name, last_active, chat_id, browsed) VALUES('")

def user(ID):
    try:
        with sql.connect("messages.db") as con:
            cur = con.cursor()
            query = "SELECT last_active FROM users WHERE user_id = '" + str(ID) + "';"
            cur.execute(query)
            res = cur.fetchall()
            con.commit()
    except Exception as e:   
        print(e)
    print("EXE: ", query)
    return res

def recordActivity(ID, time):
    try:
        with sql.connect("messages.db") as con:
            cur = con.cursor()
            query = "UPDATE users SET last_active = '" + time + "' WHERE user_id = '" + str(ID) + "';"
            cur.execute(query)
            con.commit()
    except Exception as e:   
        print(e)
    print("EXE: ", query)

def recordMessage(ID, date, time, message):
    try:
        with sql.connect("messages.db") as con:
            cur = con.cursor()
            query = "INSERT INTO messages (from_user, date_sent, time_sent, text_sent, views, reputation) VALUES('" 
            query += str(ID) 
            query += "', '" 
            query += date
            query += "', '" 
            query += time
            query += "', '" 
            query += message
            query += "', " 
            query += "0"
            query += ", " 
            query += "0" + ");"
            cur.execute(query)
            con.commit()
    except Exception as e:   
        print(e)
    print("EXE: ", "INSERT INTO messages (from_user, date_sent, time_sent, text_sent, views, reputation) VALUES('" )

def messageID(ID, text):
    try:
        with sql.connect("messages.db") as con:
            cur = con.cursor()
            query = "SELECT message_id FROM messages WHERE messages.text_sent = '" + text
            query += "' AND messages.from_user = '" + str(ID) + "';"
            cur.execute(query)
            res = cur.fetchone()
            con.commit()
    except Exception as e:   
        print(e)
    print("EXE: ", "SELECT message_id FROM messages WHERE messages.text_sent = '")
    return res

def recordHistory(ID, message_id, views):
    try:
        with sql.connect("messages.db") as con:
            cur = con.cursor()
            query = "INSERT INTO history (user_id, message_id) VALUES('" 
            query += str(ID) + "', " 
            query += str(message_id) + ");"
            cur.execute(query)
            con.commit()  
    except Exception as e: 
        print(e)
    print("EXE: ", query)

    try:
        with sql.connect("messages.db") as con:
            cur = con.cursor()
            query = "UPDATE messages SET views = " + str(views) + " WHERE message_id = " + str(message_id) + ";"
            cur.execute(query)
            con.commit()  
    except Exception as e: 
        print(e)
    print("EXE: ", query)

def activity(ID):
    try:
        with sql.connect("messages.db") as con:
            cur = con.cursor()
            query = "SELECT user_id, last_active FROM users WHERE user_id = '" + str(ID) + "';"
            cur.execute(query)
            res = cur.fetchall()
            con.commit()
    except Exception as e:   
        print(e)
    print("EXE: ", query)
    return res

def messages():
    try:
        with sql.connect("messages.db") as con:
            cur = con.cursor()
            query = "SELECT message_id, from_user, text_sent, views FROM messages"
            cur.execute(query)
            res = cur.fetchall()
            con.commit()
    except Exception as e:   
        print(e)
    print("EXE: ", query)
    return res

def in_history(ID, message_id):
    try:
        with sql.connect("messages.db") as con:
            cur = con.cursor()
            query = "SELECT message_id, user_id FROM history WHERE message_id = " + str(message_id) + " AND user_id = '" + str(ID)  + "';"
            cur.execute(query)
            res = cur.fetchall()
            con.commit()
    except Exception as e:   
        print(e)
    print("EXE: ", query)
    if len(res) != 0:
        return True
    else:
        return False

def username(ID):
    try:
        with sql.connect("messages.db") as con:
            cur = con.cursor()
            query = "SELECT user_name FROM users WHERE users.user_id = '" + str(ID) + "';"
            cur.execute(query)
            res = cur.fetchone()
            con.commit()
    except Exception as e:   
        print(e)
    print("EXE: ", query)
    return res

def recordChatID(ID, chat_id):
    try:
        with sql.connect("messages.db") as con:
            cur = con.cursor()
            query = "UPDATE users SET chat_id = '" + str(chat_id) + "' WHERE user_id = '" + str(ID) + "';"
            cur.execute(query)
            con.commit()
    except Exception as e:   
        print(e)
    print("EXE: ", query)

def recordBrowsed(ID):
    try:
        with sql.connect("messages.db") as con:
            cur = con.cursor()
            query = "UPDATE users SET browsed = 1 WHERE user_id = '" + str(ID) + "';"
            cur.execute(query)
            con.commit()
    except Exception as e:   
        print(e)
    print("EXE: ", query)

def browsed():
    try:
        with sql.connect("messages.db") as con:
            cur = con.cursor()
            query = "SELECT chat_id, user_id FROM users WHERE users.browsed = 1;"
            cur.execute(query)
            res = cur.fetchall()
            con.commit()
    except Exception as e:   
        print(e)
    print("EXE: ", query)
    return res

def resetBrowsedExcept(ID):
    try:
        with sql.connect("messages.db") as con:
            cur = con.cursor()
            query = "UPDATE users SET browsed = 0 WHERE user_id != '" + str(ID) + "';"
            cur.execute(query)
            con.commit()
    except Exception as e:   
        print(e)
    print("EXE: ", query)

def stats(ID):
    try:
        with sql.connect("messages.db") as con:
            cur = con.cursor()
            query = "SELECT text_sent, views FROM messages WHERE messages.from_user = '" + str(ID) + "';"
            cur.execute(query)
            res = cur.fetchall()
            con.commit()
    except Exception as e:   
        print(e)
    print("EXE: ", query)
    return res