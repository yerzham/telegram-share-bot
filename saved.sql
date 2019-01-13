CREATE TABLE users(
    user_id VARCHAR PRIMARY KEY,
    user_name VARCHAR,
    last_active TIME,
    chat_id VARCHAR,
    browsed INTEGER
);

CREATE TABLE messages(
    message_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    from_user VARCHAR,
    date_sent DATE,
    time_sent TIME,
    text_sent VARCHAR,
    views INTEGER,
    reputation INTEGER
);

CREATE TABLE history(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    user_id VARCHAR,
    message_id VARCHAR
);