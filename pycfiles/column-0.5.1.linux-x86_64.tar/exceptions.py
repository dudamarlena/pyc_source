# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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