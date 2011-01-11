import sqlite3

def connect_db(name):
    """Creates new sqlite3.Connection.
    
    :param name: database file path
    :return: sqlite3.Connection.
    """
    return sqlite3.connect(name)

def init_db(db, reset=False):
    """Creates all tables in the specified db, if not exist yet.
    
    :param db: database file path or a sqlite3.Connection object.
    :param reset: drops all tables if reset is True.
    """
    con = db if isinstance(db, sqlite3.Connection) else connect_db(db)
    with con as db:
        if reset:
            db.cursor().executescript(DROP_ALL)
        db.cursor().executescript(CREATE_ALL)

#sql: create all tables 
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

#sql: drop all tables 
DROP_ALL = '''
drop table if exists user;
drop table if exists entry;
'''