import hashlib
from datetime import datetime

class SecureHashService:
    
    def __init__(self, salt, algorithm):
        self.algo = algorithm
        self.salt = salt
        
    def hash(self, str):
        m = hashlib.new(self.algo)
        m.update(self.salt)
        m.update(str)
        return m.hexdigest()
        
        
class UserService:
    """handle user signup and login"""
    
    def __init__(self, db, hasher):
        self.db = db
        self.hasher = hasher
    
    def _hash(self, str):
        return self.hasher.hash(str)
    
    def signup(self, username, secret):
        with self.db as db:
            db.execute(
                'insert into user(username, secret) values (?,?)',
                [username, self._hash(secret)])
    
    def user_exists(self, username):
        cur = self.db.execute(
            'select username from user where username = ?',
            [username])
        rows = cur.fetchall()
        return True if len(rows) == 1  else False
    
    def check_credential(self, username, secret):
        cur = self.db.execute(
            'select username from user where username = ? and secret = ?',
            [username, self._hash(secret)]
        )
        rows = cur.fetchall()
        return True if len(rows) == 1 else False


class TimestampService:
    
    def now(self):
        return datetime.utcnow().isoformat() + 'Z'
        

class EntryService:
    """Handles user entries"""
    
    def __init__(self, db, clock):
        self.db = db
        self.clock = clock
    
    def add_entry(self, username, content, timestamp=None):
        with self.db as db:
            db.execute(
                '''insert into entry(username, content, timestamp)
                values(?, ?, ?)''',
                [username, content, timestamp or self.clock.now()]
            )
    
    def list_entries(self, username):
        cur = self.db.execute(
            '''select content, timestamp from entry
            where username = ?
            order by timestamp desc''', [username]
        )
        return [dict(content=row[0], timestamp=row[1])
                for row in cur.fetchall()]
        