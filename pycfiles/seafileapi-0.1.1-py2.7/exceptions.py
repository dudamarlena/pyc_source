# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/seafileapi/exceptions.py
# Compiled at: 2014-11-09 11:12:37


class ClientHttpError(Exception):
    """This exception is raised if the returned http response is not as
    expected"""

    def __init__(self, code, message):
        super(ClientHttpError, self).__init__()
        self.code = code
        self.message = message

    def __str__(self):
        return 'ClientHttpError[%s: %s]' % (self.code, self.message)


class OperationError(Exception):
    """Expcetion to raise when an opeartion is failed"""
    pass


class DoesNotExist(Exception):
    """Raised when not matching resource can be found."""

    def __init__(self, msg):
        super(DoesNotExist, self).__init__()
        self.msg = msg

    def __str__(self):
        return 'DoesNotExist: %s' % self.msg