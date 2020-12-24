# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ryosukekita/Desktop/PROJECTS/DSVISUALIZER/aefiles/lib/cloudstorage/errors.py
# Compiled at: 2017-10-27 18:08:49
"""Google Cloud Storage specific Files API calls."""
__all__ = [
 'AuthorizationError',
 'check_status',
 'Error',
 'FatalError',
 'FileClosedError',
 'ForbiddenError',
 'InvalidRange',
 'NotFoundError',
 'ServerError',
 'TimeoutError',
 'TransientError']
import httplib

class Error(Exception):
    """Base error for all gcs operations.

  Error can happen on GAE side or GCS server side.
  For details on a particular GCS HTTP response code, see
  https://developers.google.com/storage/docs/reference-status#standardcodes
  """
    pass


class TransientError(Error):
    """TransientError could be retried."""
    pass


class TimeoutError(TransientError):
    """HTTP 408 timeout."""
    pass


class FatalError(Error):
    """FatalError shouldn't be retried."""
    pass


class FileClosedError(FatalError):
    """File is already closed.

  This can happen when the upload has finished but 'write' is called on
  a stale upload handle.
  """
    pass


class NotFoundError(FatalError):
    """HTTP 404 resource not found."""
    pass


class ForbiddenError(FatalError):
    """HTTP 403 Forbidden.

  While GCS replies with a 403 error for many reasons, the most common one
  is due to bucket permission not correctly setup for your app to access.
  """
    pass


class AuthorizationError(FatalError):
    """HTTP 401 authentication required.

  Unauthorized request has been received by GCS.

  This error is mostly handled by GCS client. GCS client will request
  a new access token and retry the request.
  """
    pass


class InvalidRange(FatalError):
    """HTTP 416 RequestRangeNotSatifiable."""
    pass


class ServerError(TransientError):
    """HTTP >= 500 server side error."""
    pass


def check_status(status, expected, path, headers=None, resp_headers=None, body=None, extras=None):
    """Check HTTP response status is expected.

  Args:
    status: HTTP response status. int.
    expected: a list of expected statuses. A list of ints.
    path: filename or a path prefix.
    headers: HTTP request headers.
    resp_headers: HTTP response headers.
    body: HTTP response body.
    extras: extra info to be logged verbatim if error occurs.

  Raises:
    AuthorizationError: if authorization failed.
    NotFoundError: if an object that's expected to exist doesn't.
    TimeoutError: if HTTP request timed out.
    ServerError: if server experienced some errors.
    FatalError: if any other unexpected errors occurred.
  """
    if status in expected:
        return
    msg = 'Expect status %r from Google Storage. But got status %d.\nPath: %r.\nRequest headers: %r.\nResponse headers: %r.\nBody: %r.\nExtra info: %r.\n' % (
     expected, status, path, headers, resp_headers, body, extras)
    if status == httplib.UNAUTHORIZED:
        raise AuthorizationError(msg)
    elif status == httplib.FORBIDDEN:
        raise ForbiddenError(msg)
    elif status == httplib.NOT_FOUND:
        raise NotFoundError(msg)
    elif status == httplib.REQUEST_TIMEOUT:
        raise TimeoutError(msg)
    elif status == httplib.REQUESTED_RANGE_NOT_SATISFIABLE:
        raise InvalidRange(msg)
    elif status == httplib.OK and 308 in expected and httplib.OK not in expected:
        raise FileClosedError(msg)
    elif status >= 500:
        raise ServerError(msg)
    else:
        raise FatalError(msg)