import sqlite3 as sql

def recordUser(ID, time):
    try:
        with sql.connect("messages.db") as con:
            cur = con.cursor()
            query = u"INSERT INTO users (user_id, user_name, last_active) VALUES('" 
            query += str(ID)
            query += u"', '" + time + "');"
            cur.execute(query)
            print("EXE: ", query)
            con.commit()
    except Exception as e:   
        print(e)

def user(ID):
    try:
        with sql.connect("messages.db") as con:
            cur = con.cursor()
            query = "SELECT user_id, last_active FROM users WHERE user_id = " + str(ID) + ";"
            cur.execute(query)
            print("EXE: ", query)
            res = cur.fetchall()
            con.commit()
            return res
    except Exception as e:   
        print(e)

def recordActivity(ID, time):
    try:
        with sql.connect("messages.db") as con:
            cur = con.cursor()
            query = "UPDATE users SET last_active = '" + time + "' WHERE user_id = " + str(ID) + ";"
            cur.execute(query)
            con.commit()
            print("EXE: ", query)
    except Exception as e:   
        print(e)

def recordMessage(ID, date, time, message):
    try:
        with sql.connect("messages.db") as con:
            cur = con.cursor()
            query = "INSERT INTO messages (from_user, date_sent, time_sent, text_sent) VALUES('" 
            query += str(ID) 
            query += "', '" 
            query += date
            query += "', '" 
            query += time
            query += "', '" 
            query += message + "');"
            cur.execute(query)
            print("EXE: ", query)
            con.commit()
    except Exception as e:   
        print(e)

def messageID(ID, text):
    try:
        with sql.connect("messages.db") as con:
            cur = con.cursor()
            query = "SELECT message_id FROM messages WHERE messages.text_sent = '" + text
            query += "' AND messages.from_user = '" + ID + "';"
            cur.execute(query)
            print("EXE: ", query)
            res = cur.fetchone()
            con.commit()
            return res
    except Exception as e:   
        print(e)

def recordHistory(ID, message_id):
    try:
        with sql.connect("messages.db") as con:
            cur = con.cursor()
            query = "INSERT INTO history (user_id, message_id) VALUES('" 
            query += str(ID) + "', " 
            query += str(message_id) + ");"
            cur.execute(query)
            print("EXE: ", query)
            res = cur.fetchall()
            con.commit()
    except Exception as e:   
        print(e)

def activity(ID):
    try:
        with sql.connect("messages.db") as con:
            cur = con.cursor()
            query = "SELECT user_id, last_active FROM users WHERE user_id = " + str(ID) + ";"
            cur.execute(query)
            print("EXE: ", query)
            res = cur.fetchall()
            con.commit()
            return res
    except Exception as e:   
        print(e)

def messages():
    try:
        with sql.connect("messages.db") as con:
            cur = con.cursor()
            query = "SELECT message_id, from_user, text_sent FROM messages"
            cur.execute(query)
            print("EXE: ", query)
            res = cur.fetchall()
            con.commit()
            return res
    except Exception as e:   
        print(e)

def in_history(ID, message_id):
    try:
        with sql.connect("messages.db") as con:
            cur = con.cursor()
            query = "SELECT message_id, user_id FROM history WHERE message_id = " + str(message_id) + " AND user_id = '" + str(ID)  + "';"
            cur.execute(query)
            print("EXE: ", query)
            res = cur.fetchall()
            con.commit()
            if len(res) != 0:
                return True
            else:
                return False
    except Exception as e:   
        print(e)

def username(ID):
    try:
        with sql.connect("messages.db") as con:
            cur = con.cursor()
            query = "SELECT user_name FROM users WHERE users.user_id = '" + str(ID) + "';"
            cur.execute(query)
            print("EXE: ", query)
            res = cur.fetchone()
            con.commit()
            return res
    except Exception as e:   
        print(e)