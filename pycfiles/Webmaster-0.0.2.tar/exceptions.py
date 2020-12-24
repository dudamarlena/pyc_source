# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Mardix/Dropbox/Projects/Python/web-portfolio/webmaster/packages/user/exceptions.py
# Compiled at: 2016-01-03 03:30:36
from webmaster.exceptions import HTTPException

class UserLoginDisabledError(HTTPException):
    code = 501
    description = 'LOGIN is disabled. Contact admin if this is an error'


class UserSignupDisabledError(HTTPException):
    code = 501
    description = 'SIGNUP is disabled. Contact admin if this is an error'


class UserOAuthDisabledError(HTTPException):
    code = 501
    description = 'OAuth LOGIN is disabled. Contact admin if this is an error'