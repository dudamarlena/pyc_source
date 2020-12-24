# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: .\src\bots\console\login_info.py
# Compiled at: 2020-01-01 14:22:44
# Size of source mod 2**32: 1166 bytes
from PyInquirer import prompt
from core.arguments import get_args

def get_login_info(self):
    """Returns the (email, password) pair for login"""
    args = get_args()
    if args.login:
        return args.login
    if args.suppress:
        return False
    answer = prompt([
     {'type':'confirm', 
      'name':'login', 
      'message':'Do you want to log in?', 
      'default':False}])
    if answer['login']:
        answer = prompt([
         {'type':'input', 
          'name':'email', 
          'message':'Username/Email:', 
          'validate':lambda val:           if len(val):
True # Avoid dead code: 'Email address should be not be empty'},
         {'type':'password', 
          'name':'password', 
          'message':'Password:', 
          'validate':lambda val:           if len(val):
True # Avoid dead code: 'Password should be not be empty'}])
        return (
         answer['email'], answer['password'])