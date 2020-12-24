# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/turbomail/exceptions.py
# Compiled at: 2009-08-26 20:46:08
"""Exceptions used by TurboMail to report common errors."""
__all__ = [
 'MailException',
 'MailNotEnabledException',
 'MailConfigurationException',
 'TransportException',
 'TransportExhaustedException',
 'ManagerException']

class MailException(Exception):
    """The base for all TurboMail exceptions."""
    pass


class MailNotEnabledException(MailException):
    """Attempted to use TurboMail before being enabled."""

    def __str__(self):
        return "An attempt was made to use a facility of the TurboMail framework but outbound mail hasn't been enabled in the config file [via mail.on]."


class MailConfigurationException(MailException):
    """There was an error in the configuration of TurboMail."""
    pass


class TransportException(MailException):
    """The base for all TurboMail Transport exceptions."""
    pass


class TransportExhaustedException(MailException):
    """Attempted to use TurboMail before being enabled."""

    def __str__(self):
        return 'This Transport instance is no longer capable of delivering mail.'


class ManagerException(MailException):
    """The base for all TurboMail Manager exceptions."""
    pass