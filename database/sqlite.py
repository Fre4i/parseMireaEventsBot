import sqlite3 as sq


def sql_start():
    global base, cur
    base = sq.connect('mirea_events_bot.db')
    cur = base.cursor()
    if base:
        print('Database connected OK!')
    # user_id and option
    base.execute('CREATE TABLE IF NOT EXISTS users(user_id TEXT PRIMARY KEY, notify_enable INTEGER NOT NULL)')
    # events_info db
    base.execute(
        'CREATE TABLE IF NOT EXISTS events_info(header TEXT NOT NULL, date TEXT NOT NULL, link TEXT NOT NULL, event_desc TEXT NOT NULL,'
        'PRIMARY KEY(header, link, event_desc))')

    base.commit()


async def sql_users_add_command(user_id, notify_enable):
    cur.execute(f'INSERT OR IGNORE INTO users VALUES ("{user_id}", {notify_enable})')
    base.commit()


async def sql_users_query():
    result = cur.execute(f'SELECT * FROM users')
    return result.fetchall()


async def sql_get_user(id):
    result = cur.execute(f'SELECT * FROM users WHERE user_id = {id}')
    return result.fetchall()


async def sql_users_update(id):
    result = cur.execute(f'SELECT * FROM users WHERE user_id = "{id}"')
    global enable
    if result.fetchall()[0][1] == 0:
        enable = 1
    else:
        enable = 0

    # enable = 1 if result.fetchall()[0][1] == 0 else 1
    cur.execute(f'UPDATE users SET notify_enable = {enable} WHERE user_id = "{id}"')
    base.commit()
    return enable


async def sql_add_events_info_record(header, date, link, event_desc):
    header = header.replace('"', "'")
    link = link.replace('"', "'")
    event_desc = event_desc.replace('"', "'")
    cur.execute(f'INSERT OR IGNORE INTO events_info VALUES ("{header}", "{date}", "{link}","{event_desc}")')
    base.commit()


async def sql_get_events_info():
    res = cur.execute(f'SELECT * FROM events_info')
    return res.fetchall()


async def sql_drop_events_info():
    base.execute(f'DROP TABLE events_info')
    base.commit()

    base.execute(
        'CREATE TABLE IF NOT EXISTS events_info(header TEXT NOT NULL, date TEXT NOT NULL, link TEXT NOT NULL, event_desc TEXT NOT NULL,'
        'PRIMARY KEY(header, link, event_desc))')
    base.commit()
