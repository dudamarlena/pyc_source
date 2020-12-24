# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/credstuffer/exceptions.py
# Compiled at: 2020-03-10 15:36:11
# Size of source mod 2**32: 792 bytes


class DBConnectorError(ConnectionError):
    __doc__ = 'DBConnectorException'


class DBCreatorError(Exception):
    __doc__ = 'DBCreatorException'


class DBInserterError(Exception):
    __doc__ = 'DBInserterException'


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