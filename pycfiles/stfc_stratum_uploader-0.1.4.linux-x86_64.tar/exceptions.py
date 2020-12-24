# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/vwa13376/workspace/uploader/archer/core/exceptions.py
# Compiled at: 2013-08-14 09:28:54


class ApplicationError(Exception):
    """
    Raised by application logic.l
    """
    pass


class ArgumentError(ApplicationError):
    """
    Raised on unexpected actions which should not occur during normal usage,
    e.g. an user sends crafted HTTP header or opens URL which link does not exist anywhere in the application.
    """
    pass


class ValidationError(ApplicationError):
    """
    Raised when data provided by user does not match the requirements,
    e.g. an user sends /root or parent directory as the argument of an action.
    """
    pass