# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/adagios/adagios/../adagios/exceptions.py
# Compiled at: 2018-05-16 10:07:32
""" Exceptions that Adagios uses and raises
"""

class AdagiosError(Exception):
    """ Base Class for all Adagios Exceptions """
    pass


class AccessDenied(AdagiosError):
    """ This exception is raised whenever a user tries to access a page he does not have access to. """

    def __init__(self, username, access_required, message, path=None, *args, **kwargs):
        self.username = username
        self.access_required = access_required
        self.message = message
        self.path = path
        super(AccessDenied, self).__init__(message, *args, **kwargs)