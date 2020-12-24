# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cert_issuer/errors.py
# Compiled at: 2018-12-05 14:02:34
# Size of source mod 2**32: 1079 bytes


class Error(Exception):
    __doc__ = 'Base class for exceptions in this module'


class InsufficientFundsError(Error):
    __doc__ = '\n    There are insufficient funds to issue certificates\n    '


class ConnectorError(Error):
    pass


class UnverifiedSignatureError(Error):
    __doc__ = "\n    The signature in the certificate does not match the issuer's address\n    "


class UnableToSignTxError(Error):
    __doc__ = '\n    The transaction could not be signed\n    '


class UnverifiedTransactionError(Error):
    __doc__ = '\n    The transaction could not be verified\n    '


class AlreadySignedError(Error):
    __doc__ = '\n    The certificate has already been signed\n    '


class NoCertificatesFoundError(Error):
    __doc__ = '\n    No certificates found\n    '


class NonemptyOutputDirectoryError(Error):
    __doc__ = '\n    The output directory is not empty\n    '


class BroadcastError(Error):
    __doc__ = '\n    Error broadcasting transaction\n    '


class UnrecognizedChainError(Error):
    __doc__ = "\n    Didn't recognize chain\n    "