# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/treadmill/userutil.py
# Compiled at: 2017-04-03 02:32:49
# Size of source mod 2**32: 479 bytes
"""Treadmill user util module."""
import os
if os.name != 'nt':
    import pwd
else:
    from .syscall import winapi

def is_root():
    """Gets whether the current user is root"""
    if os.name == 'nt':
        return winapi.is_user_admin()
    else:
        return os.geteuid() == 0


def get_current_username():
    """Returns the current user name"""
    if os.name == 'nt':
        return winapi.GetUserName()
    else:
        return pwd.getpwuid(os.getuid()).pw_name