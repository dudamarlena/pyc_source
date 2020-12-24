# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.cygwin-2.6.0-i686/egg/tvdbapi_client/exceptions.py
# Compiled at: 2016-11-05 17:23:32
"""Exceptions for API and decorator to wrap request exceptions."""
from requests import exceptions
import six

def error_map(func):
    """Wrap exceptions raised by requests.

    .. py:decorator:: error_map
    """

    @six.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except exceptions.RequestException as err:
            raise TVDBRequestException((
             getattr(err, 'errno', None),
             getattr(err, 'strerror', None)), response=getattr(err, 'response', None), request=getattr(err, 'request', None))

        return

    return wrapper


class TVDBRequestException(exceptions.RequestException):
    """Provide a base exception for local use."""
    pass