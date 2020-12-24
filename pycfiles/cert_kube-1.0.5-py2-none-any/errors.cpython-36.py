# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cert_issuer/errors.py
# Compiled at: 2018-12-05 14:02:34
# Size of source mod 2**32: 1079 bytes


class Error(Exception):
    """Error"""
    pass


class InsufficientFundsError(Error):
    """InsufficientFundsError"""
    pass


class ConnectorError(Error):
    pass


class UnverifiedSignatureError(Error):
    """UnverifiedSignatureError"""
    pass


class UnableToSignTxError(Error):
    """UnableToSignTxError"""
    pass


class UnverifiedTransactionError(Error):
    """UnverifiedTransactionError"""
    pass


class AlreadySignedError(Error):
    """AlreadySignedError"""
    pass


class NoCertificatesFoundError(Error):
    """NoCertificatesFoundError"""
    pass


class NonemptyOutputDirectoryError(Error):
    """NonemptyOutputDirectoryError"""
    pass


class BroadcastError(Error):
    """BroadcastError"""
    pass


class UnrecognizedChainError(Error):
    """UnrecognizedChainError"""
    pass