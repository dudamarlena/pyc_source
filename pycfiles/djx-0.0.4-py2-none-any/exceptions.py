# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-zr3xXj/pytest/_pytest/config/exceptions.py
# Compiled at: 2019-02-14 00:35:47


class UsageError(Exception):
    """ error in pytest usage or invocation"""
    pass


class PrintHelp(Exception):
    """Raised when pytest should print it's help to skip the rest of the
    argument parsing and validation."""
    pass