import unittest
from database import connect_db, init_db

from services import UserService, SecureHashService
from services import EntryService, TimestampService

class SecureHashServiceTest(unittest.TestCase):
    
    def test_hash(self):
        #given
        s = SecureHashService('salt', 'sha256')
        secret = 'secret'
        first = s.hash(secret)
        second = s.hash(secret)
        
        #expect
        self.assertEqual(first, second)


class UserServiceTests(unittest.TestCase):
    
    def setUp(self):
        self.db = connect_db(':memory:')
        init_db(self.db)
        self.s = UserService(self.db,
                             SecureHashService('salt', 'sha256'))
        
    def tearDown(self):
        self.db.close()
    
    
    def test_signup_success(self):
        #given
        user = 'teohm'
        self.assertEqual(self.s.user_exists(user), False)
        
        #when
        self.s.signup(user, 'any')
        
        #then
        self.assertEqual(self.s.user_exists(user), True)
        
    def test_signup_failed(self):
        #given
        user = 'teohm'
        self.s.signup(user, 'any')
        
        #expect
        with self.assertRaises(Exception):
            self.s.signup(user, 'any')
        
    def test_check_credential_matched(self):
        #given
        user, password = ('teohm', 'password')
        self.s.signup(user, password)
        
        #expect
        self.assertEqual(self.s.check_credential(user, password), True)
        
    def test_check_credential_not_matched(self):
        #given
        user, password = ('teohm', 'password')
        wrong_password = 'wrongpassword'
        self.s.signup(user, password)
        
        #expect
        self.assertEqual(self.s.check_credential(user, wrong_password), False)
    
            
class EntryServiceTests(unittest.TestCase):
            
    def setUp(self):
        self.db = connect_db(':memory:')
        init_db(self.db)
        self.s = EntryService(self.db, TimestampService())
    
    def tearDown(self):
        self.db.close()
        
    def test_add_entry(self):
        #when
        self.s.add_entry('teohm', 'content')
        
        #then
        list = self.s.list_entries('teohm')
        self.assertEqual(len(list), 1)
        entry = list[0]
        self.assertEqual(entry['content'], 'content')
    
    def test_list_no_entry(self):
        #when
        list = self.s.list_entries('teohm')
        
        #then
        self.assertEqual(len(list), 0)
    
    def test_list_entries(self):
        #when
        self.s.add_entry('teohm', 'content', '2010-01-01T00:00:00Z')
        self.s.add_entry('teohm', 'content', '2010-01-01T00:00:01Z')
        self.s.add_entry('teohm', 'content', '2010-01-01T00:00:02Z')
        self.s.add_entry('foo', 'content', '2010-01-01T00:00:03Z')
        
        #then
        list = self.s.list_entries('teohm')
        self.assertEqual(len(list), 3)
        self.assertTrue(list[0]['timestamp'] > list[1]['timestamp'])
        self.assertTrue(list[1]['timestamp'] > list[2]['timestamp'])
        
    
    
if __name__ == '__main__':
    unittest.main()