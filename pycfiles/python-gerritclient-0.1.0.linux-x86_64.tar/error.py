# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/machin/.virtualenvs/twine/lib/python2.7/site-packages/gerritclient/error.py
# Compiled at: 2017-04-10 07:35:41
import json

class GerritClientException(Exception):
    """Base Exception for GerritClient

    All child classes must be instantiated before raising.
    """

    def __init__(self, *args, **kwargs):
        super(GerritClientException, self).__init__(*args, **kwargs)
        self.message = args[0]


class BadDataException(GerritClientException):
    """Should be raised when passed incorrect data."""
    pass


class InvalidFileException(GerritClientException):
    """Should be raised when some problems while working with file occurred."""
    pass


class ConfigNotFoundException(GerritClientException):
    """Should be raised if configuration for gerritclient was not specified."""
    pass


class HTTPError(GerritClientException):
    pass


def get_error_body(error):
    try:
        error_body = json.loads(error.response.text)['message']
    except (ValueError, TypeError, KeyError):
        error_body = error.response.text

    return error_body


def get_full_error_message(error):
    return ('{} ({})').format(error, get_error_body(error))