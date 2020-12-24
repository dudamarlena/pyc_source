# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nicolas/workspace/spynl-git/venv/src/spynl/spynl/main/exceptions.py
# Compiled at: 2017-01-16 09:58:52
# Size of source mod 2**32: 3309 bytes
"""Generic custom exceptions for all packages to use."""
from pyramid.httpexceptions import HTTPBadRequest, HTTPForbidden
from spynl.main.locale import SpynlTranslationString as _

class SpynlException(Exception):
    __doc__ = '\n    The Superclass for all Spynl-specific Exceptions.\n\n    If your Exception inherits from this, the Spynl Error handling\n    can treat it differently, e.g. show its message.\n    You can also specify with which HTTP exception it should be\n    escalated.\n    '
    http_escalate_as = HTTPBadRequest

    def __init__(self, message='an internal error has occured'):
        self.message = message

    def __str__(self):
        """
        This will return a str version of the message. If the message is a
        SpynlTranslationString, it will return an interpolated version of the
        default (no translation). """
        return str(self.message)


class BadOrigin(SpynlException):
    __doc__ = 'Bad origin exception.'
    http_escalate_as = HTTPForbidden

    def __init__(self, origin):
        """Set the origin attribute."""
        self.origin = origin
        self.message = _('bad-origin', default="Requests to the Spynl API are not permitted from origin '${origin}'.", mapping={'origin': self.origin})


class IllegalAction(SpynlException):
    __doc__ = 'Raise if the desired action is not allowed.'

    def __init__(self, message):
        """Exception message."""
        self.message = message


class MissingParameter(SpynlException):
    __doc__ = 'Exception when parameter is missing.'

    def __init__(self, param):
        """Exception message."""
        self.message = _('missing-parameter', default='Missing required parameter: ${param}', mapping={'param': param})


class IllegalParameter(SpynlException):
    __doc__ = 'Exception when parameter is illegal.'

    def __init__(self, param):
        """Exception message."""
        self.message = _('illegal-parameter', default='Illegal parameter: ${param}', mapping={'param': param})


class BadValidationInstructions(SpynlException):
    __doc__ = 'Exception when the validation documentation cannot be used.'

    def __init__(self, error):
        """Exception message."""
        self.message = _('bad-validation-instructions', default='The description of validations for this endpoint cannot be used: ${error}', mapping={'error': error})


class InvalidResponse(SpynlException):
    __doc__ = 'Exception when the response should be validated, but could not.'

    def __init__(self, error):
        """Exception message."""
        self.message = _('invalid-response', default='Spynl could not generate a valid response: ${error}', mapping={'error': error})


class EmailTemplateNotFound(SpynlException):
    __doc__ = 'Exception when email template file is not found.'

    def __init__(self, template):
        """Exception message."""
        self.message = _('email-tmpl-not-found', default='The email template <${template}> was not found.', mapping={'template': template})