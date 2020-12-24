# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/PyGnuTLS/errors.py
# Compiled at: 2020-04-23 12:34:05
# Size of source mod 2**32: 829 bytes
"""GNUTLS errors"""
__all__ = [
 'Error',
 'GNUTLSError',
 'OperationWouldBlock',
 'OperationInterrupted',
 'CertificateError',
 'CertificateAuthorityError',
 'CertificateSecurityError',
 'CertificateExpiredError',
 'CertificateRevokedError',
 'RequestedDataNotAvailable']

class Error(Exception):
    pass


class GNUTLSError(Error):
    pass


class OperationWouldBlock(GNUTLSError):
    pass


class OperationInterrupted(GNUTLSError):
    pass


class CertificateError(GNUTLSError):
    pass


class CertificateAuthorityError(CertificateError):
    pass


class CertificateSecurityError(CertificateError):
    pass


class CertificateExpiredError(CertificateError):
    pass


class CertificateRevokedError(CertificateError):
    pass


class RequestedDataNotAvailable(GNUTLSError):
    pass