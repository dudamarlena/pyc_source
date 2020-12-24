# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/credstuffer/exceptions.py
# Compiled at: 2020-03-10 15:36:11
# Size of source mod 2**32: 792 bytes


class DBConnectorError(ConnectionError):
    """DBConnectorError"""
    pass


class DBCreatorError(Exception):
    """DBCreatorError"""
    pass


class DBInserterError(Exception):
    """DBInserterError"""
    pass


class DBIntegrityError(Exception):
    """DBIntegrityError"""
    pass


class ProxyNotSetError(Exception):
    """ProxyNotSetError"""
    pass


class ProxyMaxRequestError(Exception):
    """ProxyMaxRequestError"""
    pass


class ProxyBadConnectionError(Exception):
    """ProxyBadConnectionError"""
    pass


class InternetConnectionError(ConnectionError):
    """InternetConnectionError"""
    pass


class MailMessageError(Exception):
    """MailMessageError"""
    pass


class AccountInstanceError(Exception):
    """AccountInstanceError"""
    pass