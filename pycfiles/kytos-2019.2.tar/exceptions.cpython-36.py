# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/humberto/src/kytos/kytos-asyncio/kytos/core/exceptions.py
# Compiled at: 2018-01-04 11:55:40
# Size of source mod 2**32: 2601 bytes
"""Kytos Core-Defined Exceptions."""

class KytosCoreException(Exception):
    __doc__ = 'Exception thrown when KytosCore is broken.'

    def __str__(self):
        return 'KytosCore exception: ' + super().__str__()


class KytosSwitchOfflineException(Exception):
    __doc__ = 'Exception thrown when a switch is offline.'

    def __init__(self, switch):
        super().__init__()
        self.switch = switch

    def __str__(self):
        """Return message of KytosSwitchOfflineException."""
        msg = 'The switch {} is not reachable. Please check the connection '
        msg += 'between the switch and the controller.'
        return msg.format(self.switch.dpid)


class KytosEventException(Exception):
    __doc__ = 'Exception thrown when a KytosEvent have an illegal use.'

    def __init__(self, message='KytosEvent exception', event=None):
        """Assign parameters to instance variables.

        Args:
            message (string): message from KytosEventException.
            event (:class:`~kytos.core.events.KytosEvent`): Event malformed.
        """
        super().__init__()
        self.message = message
        self.event = event

    def __str__(self):
        """Return the full message from KytosEventException."""
        message = self.message
        if self.event:
            message += '. EventType: ' + type(self.event)
        return message


class KytosWrongEventType(KytosEventException):
    __doc__ = 'Exception related to EventType.\n\n    When related to buffers, it means that the EventType is not allowed on\n    that buffer.\n    '


class KytosNAppException(Exception):
    __doc__ = 'Exception raised on a KytosNApp.'

    def __init__(self, message='KytosNApp exception'):
        """Assign the parameters to instance variables.

        Args:
            message (string): message from KytosNAppException.
        """
        super().__init__()
        self.message = message

    def __str__(self):
        """Return the message from KytosNAppException."""
        return self.message


class KytosNAppMissingInitArgument(KytosNAppException):
    __doc__ = 'Exception thrown when NApp have a missing init argument.'

    def __init__(self, message='KytosNAppMissingInitArgument'):
        """Assing parameters to instance variables.

        Args:
            message (str): Name of the missed argument.
        """
        super().__init__(message=message)