# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/peng3dnet/errors.py
# Compiled at: 2017-07-23 09:02:51
# Size of source mod 2**32: 2593 bytes
"""
This module contains the various exception classes used by peng3dnet.

Most methods and functions that use these exceptions will have a link to the appropriate exception in their documentation.
"""
__all__ = [
 'InvalidAddressError', 'InvalidPortError', 'InvalidHostError',
 'UnsupportedAddressError',
 'InvalidSmartPacketActionError',
 'TimedOutError', 'FailedPingError',
 'RegistryError', 'AlreadyRegisteredError']

class InvalidAddressError(ValueError):
    __doc__ = '\n    Indicates that a given address is not valid and thus cannot be used.\n    '


class InvalidPortError(InvalidAddressError):
    __doc__ = '\n    Indicates that the port supplied or parsed is not valid.\n    '


class InvalidHostError(InvalidAddressError):
    __doc__ = '\n    Indicates that the host supplied or parsed is not valid or applicable.\n    '


class UnsupportedAddressError(NotImplementedError):
    __doc__ = '\n    Indicates that the address supplied is not supported, but may still be valid.\n    '


class InvalidSmartPacketActionError(ValueError):
    __doc__ = '\n    Raised if the ``invalid_action`` of a :py:class:`~peng3dnet.packet.SmartPacket` is not valid.\n    '


class TimedOutError(RuntimeError):
    __doc__ = '\n    Indicates that some action has timed out, this includes connections, requests and any other applicable action.\n    '


class FailedPingError(TimedOutError):
    __doc__ = '\n    Indicates that a ping request has failed, usually due to a timeout.\n    '


class RegistryError(ValueError):
    __doc__ = '\n    Indicates that a registry has encountered an error.\n    '


class AlreadyRegisteredError(RegistryError):
    __doc__ = '\n    Indicates that the object given has already been registered.\n    '