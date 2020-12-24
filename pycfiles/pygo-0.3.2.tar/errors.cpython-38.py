# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/PyGnuTLS/errors.py
# Compiled at: 2020-04-23 12:34:05
# Size of source mod 2**32: 829 bytes
__doc__ = 'GNUTLS errors'
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