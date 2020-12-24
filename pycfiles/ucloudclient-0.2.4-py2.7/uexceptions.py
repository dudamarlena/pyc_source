# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/ucloudclient/uexceptions.py
# Compiled at: 2015-11-11 06:54:58


class CommandError(Exception):
    pass


class UCLOUDException(Exception):

    def __str__(self):
        return 'Error'


class ConnectionRefused(Exception):
    """
    Connection refused: the server refused the connection.
    """

    def __init__(self, response=None):
        self.response = response

    def __str__(self):
        return 'ConnectionRefused: %s' % repr(self.response)


class NoJsonFound(Exception):
    """
    no json object was found
    """

    def __init__(self, response=None):
        self.response = response

    def __str__(self):
        return 'NoJsonFound: %s' % repr(self.response)


class BadParameters(Exception):
    """
    no value return since bad parameters
    """

    def __init__(self, response=None):
        self.response = response

    def __str__(self):
        return 'BadParameters: %s' % repr(self.response)


class CommandError(Exception):
    pass