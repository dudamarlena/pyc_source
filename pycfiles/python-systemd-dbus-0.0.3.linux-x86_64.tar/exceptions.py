# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/systemd_dbus/exceptions.py
# Compiled at: 2016-05-04 23:07:49
from functools import wraps
import dbus

class SystemdError(Exception):

    def __init__(self, error):
        self.name = error.get_dbus_name().split('.')[3]
        self.message = error.get_dbus_message()

    def __str__(self):
        return '%s(%s)' % (self.name, self.message)

    def __repr__(self):
        return '%s(%s)' % (self.name, self.message)


def raise_systemd_error(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except dbus.exceptions.DBusException as error:
            raise SystemdError(error)

    return wrapper