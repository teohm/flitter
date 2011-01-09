import unittest
import flitter
from database import connect_db, init_db

class SignUpStory(unittest.TestCase):
    
    def setUp(self):
        flitter.app.config['DATABASE'] = 'app_test.db'
        init_db(connect_db(flitter.app.config['DATABASE']))
        self.app = flitter.app.test_client()
        
    def tearDown(self):
        pass
    
    def signup(self, username, password):
        return self.app.post('/welcome', data=dict(
                username=username,
                password=password
        ), follow_redirects=True)
    
    def test_successful_signup(self):
        username, password = 'teohm', 'welcome'
        rv = self.signup(username, password)
        
        assert username in rv.data
        assert 'Sign up successful' in rv.data
        assert 'add-entry' in rv.data
    
    def test_username_not_available(self):
        self.signup('teohm', 'welcome')
        rv = self.signup('teohm', 'welcome')
        
        assert 'Username already in used' in rv.data


if __name__ == '__main__':
    unittest.main()