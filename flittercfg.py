import os

_homedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = False
RESET_DB = False

SECRET_KEY = 'test key'
ENTRY_MAX_LENGTH = 200
DATABASE = os.path.join(_homedir, 'flitter.db')

del os