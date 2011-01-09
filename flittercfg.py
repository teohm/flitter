import os

_homedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = False
RESET_DB = False

SECRET_KEY = 'test key'
DATABASE = os.path.join(_homedir, 'flitter.db')

del os