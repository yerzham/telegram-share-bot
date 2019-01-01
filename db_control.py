#!/usr/bin/python -u
# -*- coding: utf-8 -*-

# v 0.0.2

import sqlite3 as sql
import datetime
import time

t = 0
while 1:
    time.sleep(10)
    if abs(int(datetime.datetime.now().strftime("%M")) - t) > 0:
        with sql.connect("messages.db") as con:
            try:
                cur = con.cursor()
                query = "SELECT time_sent, message_id, date_sent FROM messages"
                cur.execute(query)
                res = cur.fetchall()
                for row in res:
                    if str(row[2]) != datetime.datetime.now().strftime("%Y-%m-%d"):
                        print(int(row[0][0:2]) * 60 + int(row[0][3:5]), int(datetime.datetime.now().strftime("%M")) + int(datetime.datetime.now().strftime("%H")) * 60)
                        if int(row[0][0:2]) * 60 + int(row[0][3:5]) < int(datetime.datetime.now().strftime("%M")) + int(datetime.datetime.now().strftime("%H")) * 60:
                            query = "DELETE FROM messages WHERE message_id = " + str(row[1]) + ";"
                            cur.execute(query)
                            print("Deleted message with id " + str(row[1]))

                            query = "DELETE FROM history WHERE message_id = " + str(row[1]) + ";"
                            cur.execute(query)
                    
            except sql.Error as e:   
                print(e)
        t = int(datetime.datetime.now().strftime("%M"))
    