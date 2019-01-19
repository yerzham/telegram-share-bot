# Telegram Share Bot
#### *Script to run a bot that shares received messages with random people*

### Dependencies
Works only with python 3 <br />
`$ pip3 install python-telegram-bot` <br />
`$ sudo apt-get install sqlite`

### Create suitable database 
- `$ sqlite3 messages.db` <br />
- Then copy-paste query from *saved.sql*. <br />
- Press Enter.
- `sqlite-> .q`

### Run the scripts
- `python3 bot.py {YOUR BOT TOKEN}` - will run the main script for user interaction and data managment
- `python3 db_control.py` - will run the script to delete messages received 24h ago
