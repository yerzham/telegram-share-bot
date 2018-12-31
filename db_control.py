import sqlite3 as sql
import datetime

t = 0
if (abs(int(datetime.datetime.now().strftime("%M")) - t) > 1):
    t = int(datetime.datetime.now().strftime("%M");
    with sql.connect("messages.db") as con:
        try:
            cur = con.cursor()
            query = "SELECT time_sent, message_id FROM messages WHERE messages.date_sent > " + datetime.datetime.now().strftime("%Y-%m-%d") + ";"
            cur.execute(query)
            res = cur.fetchall()
            for row in res:
                if int(row[0][0:2]) * 60 + int(row[0][3:5]) < int(datetime.datetime.now().strftime("%M")) + int(datetime.datetime.now().strftime("%H")) * 60:
                    query = "DELE FROM messages WHERE messages_id = " + row[1] 
                    cur.execute(query)
        except sql.Error as e:   
                    print("Error %s:" % e.args[0])