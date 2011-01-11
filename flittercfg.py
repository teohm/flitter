import os

_homedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = False       # debug mode when run
RESET_DB = False    # drop all tables when run

SECRET_KEY = 'test key'     # encrypt cookie and as password hash salt
ENTRY_MAX_LENGTH = 200      # entry post max length
ENTRIES_PER_PAGE = 10       # entries shown per page

DATABASE = os.path.join(_homedir, 'flitter.db')

del os