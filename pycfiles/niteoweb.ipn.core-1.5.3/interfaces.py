# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/matej/workarea/nw1/niteoweb.ipn.core/src/niteoweb/ipn/core/interfaces.py
# Compiled at: 2013-09-25 09:25:26
"""Module where all interfaces, events and exceptions live."""
from zope.interface import Interface
from zope.interface import Attribute
from zope.interface import implements

class IIPN(Interface):
    """Definition of the IPN adapter."""

    def enable_member():
        """Enable an existing or create a new member."""
        pass

    def disable_member():
        """Disable an existing member."""
        pass


class NiteowebIpnCoreError(Exception):
    """Exception class for the niteoweb.ipn.core package."""
    pass


class MissingParamError(NiteowebIpnCoreError):
    """Exception raised when a required parameter is not found."""
    pass


class InvalidParamValueError(NiteowebIpnCoreError):
    """Exception raised when a parameter has an invalid value."""
    pass


class INiteowebIpnCoreEvent(Interface):
    """Base class for niteoweb.ipn.core events."""
    pass


class IMemberEnabledEvent(INiteowebIpnCoreEvent):
    """Interface for MemberEnabledEvent."""
    username = Attribute('Username of enabled member.')


class MemberEnabledEvent(object):
    """Emmited when a member is enabled."""
    implements(IMemberEnabledEvent)

    def __init__(self, username):
        self.username = username


class IMemberDisabledEvent(INiteowebIpnCoreEvent):
    """Interface for MemberDisabledEvent."""
    username = Attribute('Username of disabled member.')


class MemberDisabledEvent(object):
    """Emmited when a member is disabled."""
    implements(IMemberDisabledEvent)

    def __init__(self, username):
        self.username = username