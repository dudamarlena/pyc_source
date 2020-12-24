# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/anyex/base/errors.py
# Compiled at: 2018-04-27 06:00:45
__all__ = [
 'BaseError',
 'ExchangeError',
 'NotSupported',
 'AuthenticationError',
 'PermissionDenied',
 'InsufficientFunds',
 'InvalidOrder',
 'OrderNotFound',
 'OrderNotCached',
 'NetworkError',
 'DDoSProtection',
 'RequestTimeout',
 'ExchangeNotAvailable',
 'InvalidNonce',
 'InvalidAddress']

class BaseError(Exception):
    """Base class for all exceptions"""


class ExchangeError(BaseError):
    """"Raised when an exchange server replies with an error in JSON"""


class NotSupported(ExchangeError):
    """Raised if the endpoint is not offered/not yet supported by the exchange API"""


class AuthenticationError(ExchangeError):
    """Raised when API credentials are required but missing or wrong"""


class PermissionDenied(AuthenticationError):
    """Raised when API credentials are required but missing or wrong"""


class InsufficientFunds(ExchangeError):
    """Raised when you don't have enough currency on your account balance to place an order"""


class InvalidOrder(ExchangeError):
    """"Base class for all exceptions related to the unified order API"""


class InvalidAddress(ExchangeError):
    """Raised on invalid funding address"""


class OrderNotFound(InvalidOrder):
    """Raised when you are trying to fetch or cancel a non-existent order"""


class OrderNotCached(InvalidOrder):
    """Raised when the order is not found in local cache (where applicable)"""


class CancelPending(InvalidOrder):
    """Raised when an order that is already pending cancel is being canceled again"""


class NetworkError(BaseError):
    """Base class for all errors related to networking"""


class DDoSProtection(NetworkError):
    """Raised whenever DDoS protection restrictions are enforced per user or region/location"""


class RequestTimeout(NetworkError):
    """Raised when the exchange fails to reply in .timeout time"""


class ExchangeNotAvailable(NetworkError):
    """Raised if a reply from an exchange contains keywords related to maintenance or downtime"""


class InvalidNonce(NetworkError):
    """Raised in case of a wrong or conflicting nonce number in private requests"""


class PositionNotFound(InvalidOrder):
    """Raised when you are trying to fetch or cancel a non-existent position"""