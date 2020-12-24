# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /marrow/mailer/exc.py
# Compiled at: 2019-09-13 21:23:39
# Size of source mod 2**32: 2294 bytes
"""Exceptions used by marrow.mailer to report common errors."""
__all__ = [
 'MailException',
 'MailConfigurationException',
 'TransportException',
 'TransportFailedException',
 'MessageFailedException',
 'TransportExhaustedException',
 'ManagerException']

class MailException(Exception):
    __doc__ = 'The base for all marrow.mailer exceptions.'


class DeliveryException(MailException):
    __doc__ = 'The base class for all public-facing exceptions.'


class DeliveryFailedException(DeliveryException):
    __doc__ = 'The message stored in args[0] could not be delivered for the reason\n    given in args[1].  (These can be accessed as e.msg and e.reason.)'

    def __init__(self, message, reason):
        self.msg = message
        self.reason = reason
        super(DeliveryFailedException, self).__init__(message, reason)


class MailerNotRunning(MailException):
    __doc__ = 'Raised when attempting to deliver messages using a dead interface.'


class MailConfigurationException(MailException):
    __doc__ = 'There was an error in the configuration of marrow.mailer.'


class TransportException(MailException):
    __doc__ = 'The base for all marrow.mailer Transport exceptions.'


class TransportFailedException(TransportException):
    __doc__ = 'The transport has failed to deliver the message due to an internal\n    error; a new instance of the transport should be used to retry.'


class MessageFailedException(TransportException):
    __doc__ = 'The transport has failed to deliver the message due to a problem with\n    the message itself, and no attempt should be made to retry delivery of\n    this message.  The transport may still be re-used, however.\n    \n    The reason for the failure should be the first argument.\n    '


class TransportExhaustedException(TransportException):
    __doc__ = 'The transport has successfully delivered the message, but can no longer\n    be used for future message delivery; a new instance should be used on the\n    next request.'


class ManagerException(MailException):
    __doc__ = 'The base for all marrow.mailer Manager exceptions.'