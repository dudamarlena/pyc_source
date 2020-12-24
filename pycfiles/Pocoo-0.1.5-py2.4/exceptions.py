# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pocoo/exceptions.py
# Compiled at: 2006-12-26 17:18:07
"""
    pocoo.exceptions
    ~~~~~~~~~~~~~~~~

    Pocoo base exceptions.

    :copyright: 2006 by Georg Brandl, Armin Ronacher.
    :license: GNU GPL, see LICENSE for more details.
"""

class PocooException(Exception):
    """
    Base class for exceptions caused by
     - wrong set-up
     - misconfiguration
     - bad user actions (such as wrong login credentials)
    """
    __module__ = __name__


class ConfigurationError(PocooException):
    """
    Base for errors with the configuration file.
    """
    __module__ = __name__


class InvalidConfigFile(ConfigurationError):
    """
    If the config file cannot be parsed.
    """
    __module__ = __name__

    def __init__(self, fname, lno, msg):
        ConfigurationError.__init__(self)
        self.args = (fname, lno, msg)

    def __str__(self):
        return '%s in file %s, line %s' % (self.args[2], self.args[0], self.args[1])


class MissingConfigValue(ConfigurationError):
    """
    If a mandatory config value is missing.
    """
    __module__ = __name__


class PocooRuntimeError(Exception):
    """
    Base class for exceptions caused by bugs in Pocoo
    and plugins code.
    """
    __module__ = __name__


class PackageImportError(PocooException):
    """
    If a package mentioned in the config cannot be imported.
    """
    __module__ = __name__


class PackageNotFound(PackageImportError):
    """
    If a package cannot be found.
    """
    __module__ = __name__


class MissingResource(PocooException):
    """
    If a resource (template, cobalt file, etc.) cannot be found.
    """
    __module__ = __name__


class MissingLanguagePack(MissingResource):
    """
    If a language pack is missing.
    """
    __module__ = __name__


class EmailSMTPError(PocooException):
    """
    If the Email SMTP server fails working.
    """
    __module__ = __name__


class PasswordIncorrect(PocooException):
    """
    If the user provides a wrong password.
    """
    __module__ = __name__