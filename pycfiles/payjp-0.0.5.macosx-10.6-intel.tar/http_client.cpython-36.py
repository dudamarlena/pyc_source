# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages/payjp/http_client.py
# Compiled at: 2018-06-22 02:45:13
# Size of source mod 2**32: 2834 bytes
import textwrap, warnings
from payjp import error
import requests

def new_default_http_client(*args, **kwargs):
    impl = RequestsClient
    return impl(*args, **kwargs)


class HTTPClient(object):

    def request(self, method, url, headers, post_data=None):
        raise NotImplementedError('HTTPClient subclasses must implement `request`')


class RequestsClient(HTTPClient):
    name = 'requests'

    def request(self, method, url, headers, post_data=None):
        kwargs = {}
        try:
            try:
                result = (requests.request)(method,
 url, headers=headers, 
                 data=post_data, 
                 timeout=80, **kwargs)
            except TypeError as e:
                raise TypeError('Warning: It looks like your installed version of the "requests" library is not compatible with Payjp\'s usage thereof. (HINT: The most likely cause is that your "requests" library is out of date. You can fix that by running "pip install -U requests".) The underlying error was: %s' % (
                 e,))

            content = result.content
            status_code = result.status_code
        except Exception as e:
            self._handle_request_error(e)

        return (
         content, status_code)

    def _handle_request_error(self, e):
        if isinstance(e, requests.exceptions.RequestException):
            msg = 'Unexpected error communicating with Payjp.  If this problem persists, let us know at support@payjp.com.'
            err = '%s: %s' % (type(e).__name__, str(e))
        else:
            msg = "Unexpected error communicating with Payjp. It looks like there's probably a configuration issue locally.  If this problem persists, let us know at support@payjp.com."
            err = 'A %s was raised' % (type(e).__name__,)
            if str(e):
                err += ' with error message %s' % (str(e),)
            else:
                err += ' with no error message'
        msg = textwrap.fill(msg) + '\n\n(Network error: %s)' % (err,)
        raise error.APIConnectionError(msg)