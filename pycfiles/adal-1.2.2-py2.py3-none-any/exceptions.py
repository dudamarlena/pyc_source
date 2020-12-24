# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /opt/adagios/adagios/../adagios/exceptions.py
# Compiled at: 2018-05-16 10:07:32
__doc__ = ' Exceptions that Adagios uses and raises\n'

class AdagiosError(Exception):
    """ Base Class for all Adagios Exceptions """


class AccessDenied(AdagiosError):
    """ This exception is raised whenever a user tries to access a page he does not have access to. """

    def __init__(self, username, access_required, message, path=None, *args, **kwargs):
        self.username = username
        self.access_required = access_required
        self.message = message
        self.path = path
        super(AccessDenied, self).__init__(message, *args, **kwargs)