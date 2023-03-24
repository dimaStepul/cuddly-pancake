import sqlite3 as sq
from sqlite3 import OperationalError
import logging
from history import History

db = sq.connect('tg.db')
cur = db.cursor()

async def db_start():
    db = sq.connect('tg.db')
    cur = db.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS user_history("
                "i_id INTEGER PRIMARY KEY AUTOINCREMENT,"
                "tg TEXT,"
                "name TEXT,"
                "original_url TEXT, "
                "result TEXT)")
    logging.info(db)
    db.commit()

def get_history(user_id):
    try:
        user = cur.execute("SELECT * FROM user_history WHERE tg = ?",(str(user_id),))
    except OperationalError:
        return "you have sent zero links"
    cur_user_history = user.fetchone()
    db.commit()
    return cur_user_history


def save_to_db(data: History) -> None:
    cur.execute('INSERT OR IGNORE INTO user_history VALUES (?,?,?,?)',[data.tg_id,data.name, data.original_link,data.result_link])
    db.commit()
