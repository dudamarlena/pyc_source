# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rstuart/.pyenv/versions/gcloudoem/lib/python2.7/site-packages/gcloudoem/exceptions.py
# Compiled at: 2015-06-10 21:39:40
"""
Custom exceptions.
"""
from collections import defaultdict
import json, six
_HTTP_CODE_TO_EXCEPTION = {}

class GCloudError(Exception):
    """Base error class for gcloud errors (abstract).

    Each subclass represents a single type of HTTP error response.
    """
    code = None

    def __init__(self, message, errors=()):
        super(GCloudError, self).__init__()
        self.message = message
        self._errors = [ error.copy() for error in errors ]

    def __str__(self):
        return '%d %s' % (self.code, self.message)

    @property
    def errors(self):
        """Detailed error information.

        :rtype: list(dict)
        :returns: a list of mappings describing each error.
        """
        return [ error.copy() for error in self._errors ]


class Redirection(GCloudError):
    """Base for 3xx responses

    This class is abstract.
    """
    pass


class MovedPermanently(Redirection):
    """Exception mapping a '301 Moved Permanently' response."""
    code = 301


class NotModified(Redirection):
    """Exception mapping a '304 Not Modified' response."""
    code = 304


class TemporaryRedirect(Redirection):
    """Exception mapping a '307 Temporary Redirect' response."""
    code = 307


class ResumeIncomplete(Redirection):
    """Exception mapping a '308 Resume Incomplete' response."""
    code = 308


class ClientError(GCloudError):
    """Base for 4xx responses

    This class is abstract
    """
    pass


class BadRequest(ClientError):
    """Exception mapping a '400 Bad Request' response."""
    code = 400


class Unauthorized(ClientError):
    """Exception mapping a '401 Unauthorized' response."""
    code = 401


class Forbidden(ClientError):
    """Exception mapping a '403 Forbidden' response."""
    code = 403


class NotFound(ClientError):
    """Exception mapping a '404 Not Found' response."""
    code = 404


class MethodNotAllowed(ClientError):
    """Exception mapping a '405 Method Not Allowed' response."""
    code = 405


class Conflict(ClientError):
    """Exception mapping a '409 Conflict' response."""
    code = 409


class LengthRequired(ClientError):
    """Exception mapping a '411 Length Required' response."""
    code = 411


class PreconditionFailed(ClientError):
    """Exception mapping a '412 Precondition Failed' response."""
    code = 412


class RequestRangeNotSatisfiable(ClientError):
    """Exception mapping a '416 Request Range Not Satisfiable' response."""
    code = 416


class TooManyRequests(ClientError):
    """Exception mapping a '429 Too Many Requests' response."""
    code = 429


class ServerError(GCloudError):
    """Base for 5xx responses:  (abstract)"""
    pass


class InternalServerError(ServerError):
    """Exception mapping a '500 Internal Server Error' response."""
    code = 500


class NotImplemented(ServerError):
    """Exception mapping a '501 Not Implemented' response."""
    code = 501


class ServiceUnavailable(ServerError):
    """Exception mapping a '503 Service Unavailable' response."""
    code = 503


def make_exception(response, content, use_json=True):
    """
    Factory: create exception based on HTTP response code.

    :type response: :class:`httplib2.Response` or other HTTP response object
    :param response: A response object that defines a status code as the status attribute.

    :type content: string or dictionary
    :param content: The body of the HTTP error response.

    :type use_json: boolean
    :param use_json: Flag indicating if ``content`` is expected to be JSON.

    :rtype: instance of :class:`GCloudError`, or a concrete subclass.
    :returns: Exception specific to the error response.
    """
    message = content
    errors = ()
    if isinstance(content, str):
        if use_json:
            payload = json.loads(content)
        else:
            payload = {}
    else:
        payload = content
    message = payload.get('message', message)
    errors = payload.get('error', {}).get('errors', ())
    try:
        klass = _HTTP_CODE_TO_EXCEPTION[response.status]
    except KeyError:
        error = GCloudError(message, errors)
        error.code = response.status
    else:
        error = klass(message, errors)

    return error


def _walk_subclasses(klass):
    """Recursively walk subclass tree."""
    for sub in klass.__subclasses__():
        yield sub
        for subsub in _walk_subclasses(sub):
            yield subsub


for eklass in _walk_subclasses(GCloudError):
    code = getattr(eklass, 'code', None)
    if code is not None:
        _HTTP_CODE_TO_EXCEPTION[code] = eklass

class ValidationError(AssertionError):
    """
    Validation exception.

    May represent an error validating a field or a document containing fields with validation errors.

    :ivar errors: A dictionary of errors for fields within this document or list, or None if the error is for an
        individual field.
    """
    errors = {}
    field_name = None
    _message = None

    def __init__(self, message='', **kwargs):
        self.errors = kwargs.get('errors', {})
        self.field_name = kwargs.get('field_name', None)
        self.message = message
        return

    def __str__(self):
        return six.text_type(self.message)

    def __repr__(self):
        return '%s(%s,)' % (self.__class__.__name__, self.message)

    def __getattribute__(self, name):
        message = super(ValidationError, self).__getattribute__(name)
        if name == 'message':
            if self.field_name:
                message = '%s' % message
            if self.errors:
                message = '%s(%s)' % (message, self._format_errors())
        return message

    def _get_message(self):
        return self._message

    def _set_message(self, message):
        self._message = message

    message = property(_get_message, _set_message)

    def to_dict(self):
        """
        Returns a dictionary of all errors within a entity.

        Keys are field names or list indices and values are the validation error messages, or a nested dictionary of
        errors for an embedded document or list.
        """

        def build_dict(source):
            errors_dict = {}
            if not source:
                return errors_dict
            if isinstance(source, dict):
                for field_name, error in source.items():
                    errors_dict[field_name] = build_dict(error)

            else:
                if isinstance(source, ValidationError) and source.errors:
                    return build_dict(source.errors)
                else:
                    return six.text_type(source)

            return errors_dict

        if not self.errors:
            return {}
        return build_dict(self.errors)

    def _format_errors(self):
        """Returns a string listing all errors within a document"""

        def generate_key(value, prefix=''):
            if isinstance(value, list):
                value = (' ').join([ generate_key(k) for k in value ])
            if isinstance(value, dict):
                value = (' ').join([ generate_key(v, k) for k, v in value.items() ])
            results = '%s.%s' % (prefix, value) if prefix else value
            return results

        error_dict = defaultdict(list)
        for k, v in self.to_dict().items():
            error_dict[generate_key(v)].append(k)

        return (' ').join([ '%s: %s' % (k, v) for k, v in error_dict.items() ])


class InvalidQueryError(Exception):
    """Invalid Datastore query."""
    pass


class EnvironmentError(Exception):
    """Generally means that connect() wasn't called."""
    pass


class DoesNotExist(Exception):
    pass


class MultipleObjectsReturned(Exception):
    pass


class ConnectionError(Exception):
    pass