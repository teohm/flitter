import unittest
import tempfile
import os

from database import connect_db, init_db

class DatabaseTests(unittest.TestCase):
    
    def setUp(self):
        self.dbname = 'database_test.db'
        self.db = None
        
    def tearDown(self):
        self.db.close()
        os.unlink(self.dbname)
        
    def test_connect_db(self):
        #when
        self.db = connect_db(self.dbname)
        
        #expect
        self.assertEqual(self.db.execute('select 1').fetchone()[0], 1)
    
    def test_init_db(self):
        #when
        init_db(self.dbname)
        self.db = connect_db(self.dbname)
        
        #expect
        self.assertEqual(self.db.execute('select * from user').fetchall(), [])
        self.assertEqual(self.db.execute('select * from entry').fetchall(), [])
        
        
if __name__ == '__main__':
    unittest.main()