# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /private/var/folders/pb/598z8h910dvf2wrvwnbyl_2m0000gn/T/pip-install-65c3rg8f/urllib3/urllib3/contrib/appengine.py
# Compiled at: 2019-11-10 08:27:46
# Size of source mod 2**32: 11290 bytes
__doc__ = "\nThis module provides a pool manager that uses Google App Engine's\n`URLFetch Service <https://cloud.google.com/appengine/docs/python/urlfetch>`_.\n\nExample usage::\n\n    from urllib3 import PoolManager\n    from urllib3.contrib.appengine import AppEngineManager, is_appengine_sandbox\n\n    if is_appengine_sandbox():\n        # AppEngineManager uses AppEngine's URLFetch API behind the scenes\n        http = AppEngineManager()\n    else:\n        # PoolManager uses a socket-level API behind the scenes\n        http = PoolManager()\n\n    r = http.request('GET', 'https://google.com/')\n\nThere are `limitations <https://cloud.google.com/appengine/docs/python/urlfetch/#Python_Quotas_and_limits>`_ to the URLFetch service and it may not be\nthe best choice for your application. There are three options for using\nurllib3 on Google App Engine:\n\n1. You can use :class:`AppEngineManager` with URLFetch. URLFetch is\n   cost-effective in many circumstances as long as your usage is within the\n   limitations.\n2. You can use a normal :class:`~urllib3.PoolManager` by enabling sockets.\n   Sockets also have `limitations and restrictions\n   <https://cloud.google.com/appengine/docs/python/sockets/   #limitations-and-restrictions>`_ and have a lower free quota than URLFetch.\n   To use sockets, be sure to specify the following in your ``app.yaml``::\n\n        env_variables:\n            GAE_USE_SOCKETS_HTTPLIB : 'true'\n\n3. If you are using `App Engine Flexible\n<https://cloud.google.com/appengine/docs/flexible/>`_, you can use the standard\n:class:`PoolManager` without any configuration or special environment variables.\n"
from __future__ import absolute_import
import io, logging, warnings
from packages.six.moves.urllib.parse import urljoin
from ..exceptions import HTTPError, HTTPWarning, MaxRetryError, ProtocolError, TimeoutError, SSLError
from ..request import RequestMethods
from ..response import HTTPResponse
from util.timeout import Timeout
from util.retry import Retry
from . import _appengine_environ
try:
    from google.appengine.api import urlfetch
except ImportError:
    urlfetch = None

log = logging.getLogger(__name__)

class AppEnginePlatformWarning(HTTPWarning):
    pass


class AppEnginePlatformError(HTTPError):
    pass


class AppEngineManager(RequestMethods):
    """AppEngineManager"""

    def __init__(self, headers=None, retries=None, validate_certificate=True, urlfetch_retries=True):
        if not urlfetch:
            raise AppEnginePlatformError('URLFetch is not available in this environment.')
        if is_prod_appengine_mvms():
            raise AppEnginePlatformError('Use normal urllib3.PoolManager instead of AppEngineManageron Managed VMs, as using URLFetch is not necessary in this environment.')
        warnings.warn('urllib3 is using URLFetch on Google App Engine sandbox instead of sockets. To use sockets directly instead of URLFetch see https://urllib3.readthedocs.io/en/latest/reference/urllib3.contrib.html.', AppEnginePlatformWarning)
        RequestMethods.__init__(self, headers)
        self.validate_certificate = validate_certificate
        self.urlfetch_retries = urlfetch_retries
        self.retries = retries or 

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False

    def urlopen(self, method, url, body=None, headers=None, retries=None, redirect=True, timeout=Timeout.DEFAULT_TIMEOUT, **response_kw):
        retries = self._get_retries(retries, redirect)
        try:
            follow_redirects = redirect and retries.redirect != 0 and retries.total
            response = urlfetch.fetch(url,
              payload=body,
              method=method,
              headers=(headers or ),
              allow_truncated=False,
              follow_redirects=(self.urlfetch_retries and follow_redirects),
              deadline=(self._get_absolute_timeout(timeout)),
              validate_certificate=(self.validate_certificate))
        except urlfetch.DeadlineExceededError as e:
            try:
                raise TimeoutError(self, e)
            finally:
                e = None
                del e

        except urlfetch.InvalidURLError as e:
            try:
                if 'too large' in str(e):
                    raise AppEnginePlatformError('URLFetch request too large, URLFetch only supports requests up to 10mb in size.', e)
                raise ProtocolError(e)
            finally:
                e = None
                del e

        except urlfetch.DownloadError as e:
            try:
                if 'Too many redirects' in str(e):
                    raise MaxRetryError(self, url, reason=e)
                raise ProtocolError(e)
            finally:
                e = None
                del e

        except urlfetch.ResponseTooLargeError as e:
            try:
                raise AppEnginePlatformError('URLFetch response too large, URLFetch only supportsresponses up to 32mb in size.', e)
            finally:
                e = None
                del e

        except urlfetch.SSLCertificateError as e:
            try:
                raise SSLError(e)
            finally:
                e = None
                del e

        except urlfetch.InvalidMethodError as e:
            try:
                raise AppEnginePlatformError('URLFetch does not support method: %s' % method, e)
            finally:
                e = None
                del e

        http_response = (self._urlfetch_response_to_http_response)(
 response, retries=retries, **response_kw)
        redirect_location = redirect and http_response.get_redirect_location()
        if redirect_location:
            if self.urlfetch_retries and retries.raise_on_redirect:
                raise MaxRetryError(self, url, 'too many redirects')
            else:
                if http_response.status == 303:
                    method = 'GET'
                try:
                    retries = retries.increment(method,
                      url, response=http_response, _pool=self)
                except MaxRetryError:
                    if retries.raise_on_redirect:
                        raise MaxRetryError(self, url, 'too many redirects')
                    return http_response
                else:
                    retries.sleep_for_retry(http_response)
                    log.debug('Redirecting %s -> %s', url, redirect_location)
                    redirect_url = urljoin(url, redirect_location)
                    return (self.urlopen)(
 method,
 redirect_url,
 body,
 headers, retries=retries, 
                     redirect=redirect, 
                     timeout=timeout, **response_kw)
        has_retry_after = bool(http_response.getheader('Retry-After'))
        if retries.is_retry(method, http_response.status, has_retry_after):
            retries = retries.increment(method, url, response=http_response, _pool=self)
            log.debug('Retry: %s', url)
            retries.sleep(http_response)
            return (self.urlopen)(
 method,
 url, body=body, 
             headers=headers, 
             retries=retries, 
             redirect=redirect, 
             timeout=timeout, **response_kw)
        return http_response

    def _urlfetch_response_to_http_response(self, urlfetch_resp, **response_kw):
        if is_prod_appengine():
            content_encoding = urlfetch_resp.headers.get('content-encoding')
            if content_encoding == 'deflate':
                del urlfetch_resp.headers['content-encoding']
        transfer_encoding = urlfetch_resp.headers.get('transfer-encoding')
        if transfer_encoding == 'chunked':
            encodings = transfer_encoding.split(',')
            encodings.remove('chunked')
            urlfetch_resp.headers['transfer-encoding'] = ','.join(encodings)
        original_response = HTTPResponse(body=io.BytesIO(urlfetch_resp.content), 
         msg=urlfetch_resp.header_msg, 
         headers=urlfetch_resp.headers, 
         status=urlfetch_resp.status_code, **response_kw)
        return HTTPResponse(body=io.BytesIO(urlfetch_resp.content), 
         headers=urlfetch_resp.headers, 
         status=urlfetch_resp.status_code, 
         original_response=original_response, **response_kw)

    def _get_absolute_timeout(self, timeout):
        if timeout is Timeout.DEFAULT_TIMEOUT:
            return
        if isinstance(timeout, Timeout):
            if timeout._read is not None or timeout._connect is not None:
                warnings.warn('URLFetch does not support granular timeout settings, reverting to total or default URLFetch timeout.', AppEnginePlatformWarning)
            return timeout.total
        return timeout

    def _get_retries(self, retries, redirect):
        if not isinstance(retries, Retry):
            retries = Retry.from_int(retries, redirect=redirect, default=(self.retries))
        if retries.connect or retries.read or retries.redirect:
            warnings.warn('URLFetch only supports total retries and does not recognize connect, read, or redirect retry parameters.', AppEnginePlatformWarning)
        return retries


is_appengine = _appengine_environ.is_appengine
is_appengine_sandbox = _appengine_environ.is_appengine_sandbox
is_local_appengine = _appengine_environ.is_local_appengine
is_prod_appengine = _appengine_environ.is_prod_appengine
is_prod_appengine_mvms = _appengine_environ.is_prod_appengine_mvms