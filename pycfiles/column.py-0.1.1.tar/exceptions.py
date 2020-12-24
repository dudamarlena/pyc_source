# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/column/exceptions.py
# Compiled at: 2017-08-02 01:06:09
import logging
LOG = logging.getLogger(__name__)

class BaseException(Exception):
    """The Base Exception to extend custom exceptions.
    """
    message = 'An unknown exception occurred.'

    def __init__(self, msg=None, **kwargs):
        if msg:
            self.message = msg
        if kwargs:
            try:
                self.msg = self.message % kwargs
            except KeyError as e:
                LOG.warning('Formatting error: %(e)s. Message: %(msg)s. kwargs: %(kwargs)s', {'e': e, 'msg': self.message, 'kwargs': kwargs})
                self.msg = self.message

        else:
            self.msg = self.message
        super(BaseException, self).__init__(self.msg)


class InvalidParameter(BaseException):
    """Invalid parameter given"""
    message = 'Invalid type of %(name)s on parameter %(param)s'


class FileNotFound(BaseException):
    """The given file cannot be found"""
    message = 'File %(name)s cannot be found'