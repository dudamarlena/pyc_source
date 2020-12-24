# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/chris/workspace/slothauth/slothauth/exceptions.py
# Compiled at: 2016-01-27 03:44:32


class SlothAuthException(Exception):
    pass


class SlothAuthInvalidSetting(SlothAuthException):
    pass