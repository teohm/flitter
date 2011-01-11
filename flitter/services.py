import hashlib
from datetime import datetime

class SecureHashService:
    """Provides password hashing service"""
    
    def __init__(self, salt, algorithm='sha256'):
        """
        :param salt: salt string to use when hashing
        :param algorithm: hash algorithm supported by `hashlib`, default='sha256'
        """
        self.algo = algorithm
        self.salt = salt
        
    def hash(self, str):
        """Returns hash string (hexadecimal digits) of the input string.
        
        :param str: input string to hash
        """
        m = hashlib.new(self.algo)
        m.update(self.salt)
        m.update(str)
        return m.hexdigest()
        
        
class UserService:
    """Provides user signup and login services"""
    
    def __init__(self, db, hasher):
        self.db = db
        self.hasher = hasher
    
    def _hash(self, str):
        return self.hasher.hash(str)
    
    def signup(self, username, secret):
        """Adds new user to database.
        
        Should call `user_exists()` before signup.
        
        :param username: username
        :param secret: user password
        """
        with self.db as db:
            db.execute(
                'insert into user(username, secret) values (?,?)',
                [username, self._hash(secret)])
    
    def user_exists(self, username):
        """Returns True if username exists in database.
        
        :param username: username to check
        :return: bool. True if username exists, otherwise False.
        """
        cur = self.db.execute(
            'select username from user where username = ?',
            [username])
        rows = cur.fetchall()
        return True if len(rows) == 1  else False
    
    def check_credential(self, username, secret):
        """Returns True if username-password combination exists in database.
        
        :param username: username
        :param secret: password
        :return: bool. True if username-password exists, otherwise False.
        """
        cur = self.db.execute(
            'select username from user where username = ? and secret = ?',
            [username, self._hash(secret)]
        )
        rows = cur.fetchall()
        return True if len(rows) == 1 else False


class TimestampService:
    """Provides timestamp formatting service"""

    def now(self):
        """Returns current UTC time in ISO8601 string"""
        
        return datetime.utcnow().isoformat() + 'Z'
        

class EntryService:
    """Provides add and list entries service"""
    
    def __init__(self, db, clock):
        self.db = db
        self.clock = clock
        
    def _entry_dict(self, content, timestamp):
        return dict(content=content, timestamp=timestamp)
    
    def add_entry(self, username, content, timestamp=None):
        """Adds new entry into database.
        
        :param username: owner of entry
        :param content: entry content
        :param timestamp: optional ISO timestamp string. default: current
                          UTC time formatted in ISO8601.
        """
        _timestamp = timestamp or self.clock.now()
        with self.db as db:
            db.execute(
                '''insert into entry(username, content, timestamp)
                values(?, ?, ?)''',
                [username, content, _timestamp]
            )
        return self._entry_dict(content, _timestamp)
    
    def list_entries(self, username, limit=10, offset=0):
        """Returns entries owned by the specified user.
        
        :param username: owner of entries
        :param limit: total entries to return
        :param offset: starts from which record (0-based)
        :return: a list of dict{content, timestamp}
        """
        cur = self.db.execute(
            '''select content, timestamp from entry
            where username = ?
            order by timestamp desc
            limit ? offset ?''', [username, limit, offset]
        )
        return [self._entry_dict(row[0], row[1])
                for row in cur.fetchall()]
