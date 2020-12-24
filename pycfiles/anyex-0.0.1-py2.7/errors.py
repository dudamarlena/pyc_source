# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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
    pass


class ExchangeError(BaseError):
    """"Raised when an exchange server replies with an error in JSON"""
    pass


class NotSupported(ExchangeError):
    """Raised if the endpoint is not offered/not yet supported by the exchange API"""
    pass


class AuthenticationError(ExchangeError):
    """Raised when API credentials are required but missing or wrong"""
    pass


class PermissionDenied(AuthenticationError):
    """Raised when API credentials are required but missing or wrong"""
    pass


class InsufficientFunds(ExchangeError):
    """Raised when you don't have enough currency on your account balance to place an order"""
    pass


class InvalidOrder(ExchangeError):
    """"Base class for all exceptions related to the unified order API"""
    pass


class InvalidAddress(ExchangeError):
    """Raised on invalid funding address"""
    pass


class OrderNotFound(InvalidOrder):
    """Raised when you are trying to fetch or cancel a non-existent order"""
    pass


class OrderNotCached(InvalidOrder):
    """Raised when the order is not found in local cache (where applicable)"""
    pass


class CancelPending(InvalidOrder):
    """Raised when an order that is already pending cancel is being canceled again"""
    pass


class NetworkError(BaseError):
    """Base class for all errors related to networking"""
    pass


class DDoSProtection(NetworkError):
    """Raised whenever DDoS protection restrictions are enforced per user or region/location"""
    pass


class RequestTimeout(NetworkError):
    """Raised when the exchange fails to reply in .timeout time"""
    pass


class ExchangeNotAvailable(NetworkError):
    """Raised if a reply from an exchange contains keywords related to maintenance or downtime"""
    pass


class InvalidNonce(NetworkError):
    """Raised in case of a wrong or conflicting nonce number in private requests"""
    pass


class PositionNotFound(InvalidOrder):
    """Raised when you are trying to fetch or cancel a non-existent position"""
    pass