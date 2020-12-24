# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/core/util/user.py
# Compiled at: 2019-08-19 15:09:29
"""
Finds out user inf (currently just the logged user name) for Windows and
Posix machines. sets a USER_NAME variable containing the logged user name
defines a UNKNOWN_USER variable to which username falls back.
It also provides the getSystemUserName() function"""
__all__ = [
 'getSystemUserName', 'USER_NAME', 'UNKNOWN_USER']
__docformat__ = 'restructuredtext'
import getpass
UNKNOWN_USER = 'UnknownUser'

def getSystemUserName():
    """Finds out user inf (currently just the logged user name) for Windows and
    Posix machines. sets a USER_NAME variable containing the logged user name
    defines a UNKNOWN_USER variable to which username falls back.

    :return: (str) current user name
    """
    try:
        return getpass.getuser()
    except:
        return UNKNOWN_USER


USER_NAME = getSystemUserName()