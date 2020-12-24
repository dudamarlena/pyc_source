# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/peterdowns/Desktop/djoauth2/djoauth2/errors.py
# Compiled at: 2013-11-22 18:12:08


class DJOAuthError(Exception):
    """ Base class for all OAuth-related errors. """
    error_name = 'invalid_request'
    status_code = 400


def get_error_details(error):
    """ Return details about an OAuth error.

  Returns a mapping with two keys, ``'error'`` and ``'error_description'``,
  that are used in all error responses described by the OAuth 2.0
  specification. Read more at:

  * http://tools.ietf.org/html/rfc6749
  * http://tools.ietf.org/html/rfc6750
  """
    return {'error': getattr(error, 'error_name', 'invalid_request'), 
       'error_description': str(error) or '(no description available)'}