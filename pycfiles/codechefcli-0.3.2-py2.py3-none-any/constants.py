# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: codechefcli/utils/constants.py
# Compiled at: 2018-03-28 05:23:56
from os.path import expanduser
BASE_URL = 'https://www.codechef.com'
COOKIES_FILE_PATH = expanduser('~') + '/.cookies'
SERVER_DOWN_MSG = 'Please try again later. Seems like CodeChef server is down!'
INTERNET_DOWN_MSG = 'Nothing to show. Check your internet connection.'
UNAUTHORIZED_MSG = 'You are not logged in.'
EMPTY_AUTH_DATA_MSG = 'Username/Password field cannot be left blank.'
SESSION_LIMIT_MSG = 'Session limit exceeded!'
INCORRECT_CREDS_MSG = 'Incorrect Credentials!'
LOGIN_SUCCESS_MSG = 'Successfully logged in!'
LOGOUT_SUCCESS_MSG = 'Successfully logged out!'
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like              Gecko) Chrome/62.0.3202.62 Safari/537.36'
RESULT_CODES = {'AC': 15, 
   'WA': 14, 
   'TLE': 13, 
   'RTE': 12, 
   'CTE': 11}
RATINGS_TABLE_HEADINGS = [
 'GLOBAL(COUNTRY)', 'USER NAME', 'RATING', 'GAIN/LOSS']
PROBLEM_LIST_TABLE_HEADINGS = ['CODE', 'NAME', 'SUBMISSION', 'ACCURACY']
DEFAULT_NUM_LINES = 20
BCOLORS = {'HEADER': '\x1b[95m', 
   'BLUE': '\x1b[94m', 
   'GREEN': '\x1b[92m', 
   'WARNING': '\x1b[93m', 
   'FAIL': '\x1b[91m', 
   'ENDC': '\x1b[0m', 
   'BOLD': '\x1b[1m', 
   'UNDERLINE': '\x1b[4m'}
INVALID_USERNAME = '##no_login##'