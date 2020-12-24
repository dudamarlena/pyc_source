# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/ComunioScore/exceptions.py
# Compiled at: 2020-04-22 13:11:22
# Size of source mod 2**32: 387 bytes


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


class SofascoreRequestError(Exception):
    """SofascoreRequestError"""
    pass