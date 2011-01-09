import sqlite3

def connect_db(name):
    return sqlite3.connect(name)

def init_db(db, reset=False):
    con = db if isinstance(db, sqlite3.Connection) else connect_db(db)
    with con as db:
        if reset:
            db.cursor().executescript(DROP_ALL)
        db.cursor().executescript(CREATE_ALL)


CREATE_ALL = '''
create table if not exists user (
    username text primary key,
    secret text not null
);
create table if not exists entry (
    id integer primary key autoincrement,
    username text not null,
    content text not null,
    timestamp text not null
);
'''

DROP_ALL = '''
drop table if exists user;
drop table if exists entry;
'''