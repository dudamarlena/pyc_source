# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/golismero/api/net/http.py
# Compiled at: 2014-01-04 20:30:30
"""
HTTP protocol API for GoLismero.
"""
__license__ = '\nGoLismero 2.0 - The web knife - Copyright (C) 2011-2013\n\nAuthors:\n  Daniel Garcia Garcia a.k.a cr0hn | cr0hn<@>cr0hn.com\n  Mario Vilas | mvilas<@>gmail.com\n\nGolismero project site: https://github.com/golismero\nGolismero project mail: golismero.project<@>gmail.com\n\nThis program is free software; you can redistribute it and/or\nmodify it under the terms of the GNU General Public License\nas published by the Free Software Foundation; either version 2\nof the License, or (at your option) any later version.\n\nThis program is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License\nalong with this program; if not, write to the Free Software\nFoundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.\n'
__all__ = [
 'HTTP']
from . import ConnectionSlot, NetworkException, NetworkOutOfScope
from .cache import NetworkCache
from .web_utils import detect_auth_method, get_auth_obj
from ..config import Config
from ..data import LocalDataCache, discard_data
from ..data.information.http import HTTP_Request, HTTP_Response, HTTP_Raw_Request
from ..data.resource.url import Url
from ...common import Singleton, get_data_folder
from hashlib import md5
from os import environ
from os.path import join
from requests import Session
from requests.cookies import cookiejar_from_dict
from requests.exceptions import RequestException
from socket import socket, error, getaddrinfo, SOCK_STREAM
from ssl import wrap_socket
from StringIO import StringIO
from time import time

class _HTTP(Singleton):
    """
    HTTP protocol API for GoLismero.
    """

    def __init__(self):
        self.__session = None
        return

    def _initialize(self):
        """
        .. warning: Called automatically by GoLismero. Do not call!
        """
        if not environ.get('CURL_CA_BUNDLE'):
            environ['CURL_CA_BUNDLE'] = join(get_data_folder(), 'cacert.pem')
        self.__session = Session()
        proxy_addr = Config.audit_config.proxy_addr
        if proxy_addr:
            proxy_port = Config.audit_config.proxy_port
            if proxy_port:
                proxy_addr = '%s:%s' % (proxy_addr, proxy_port)
            auth_user = Config.audit_config.proxy_user
            auth_pass = Config.audit_config.proxy_pass
            auth, _ = detect_auth_method(proxy_addr)
            self.__session.auth = get_auth_obj(auth, auth_user, auth_pass)
            self.__session.proxies = {'http': proxy_addr, 
               'https': proxy_addr, 
               'ftp': proxy_addr}
        cookie = Config.audit_config.cookie
        if cookie:
            self.__session.cookies = cookiejar_from_dict(cookie)
        self.__user_agent = Config.audit_config.user_agent

    def _finalize(self):
        """
        .. warning: Called automatically by GoLismero. Do not call!
        """
        self.__session = None
        return

    def get_url(self, url, method='GET', callback=None, timeout=10.0, use_cache=None, allow_redirects=True, allow_out_of_scope=False):
        """
        Send a simple HTTP request to the server and get the response back.

        :param url: URL to request.
        :type url: str

        :param method: HTTP method.
        :type method: str

        :param callback: Callback function.
        :type callback: callable

        :param timeout: Timeout in seconds.
            The minimum value is 0.5 and the maximum is 100.0. Any other values
            will be silently converted to either one of them.
        :type timeout: int | float

        :param use_cache: Control the use of the cache.
                          Use True to force the use of the cache,
                          False to force not to use it,
                          or None for automatic.
        :type use_cache: bool | None

        :param allow_redirects: True to follow redirections, False otherwise.
        :type allow_redirects: bool

        :param allow_out_of_scope: True to allow requests out of scope, False otherwise.
        :type allow_out_of_scope: bool

        :returns: HTTP response, or None if the request was cancelled.
        :rtype: HTTP_Response | None

        :raises NetworkOutOfScope: The resource is out of the audit scope.
            Note that this can happen even if the URL has been checked against
            Config.audit_scope -- if the server responds with a
            redirection against another URL that's out of scope.
        :raises NetworkException: A network error occurred.
        """
        request = HTTP_Request(url, method=method, user_agent=self.__user_agent)
        LocalDataCache.on_autogeneration(request)
        return self.make_request(request, callback=callback, timeout=timeout, use_cache=use_cache, allow_redirects=allow_redirects, allow_out_of_scope=allow_out_of_scope)

    def make_request(self, request, callback=None, timeout=10.0, use_cache=None, allow_redirects=True, allow_out_of_scope=False):
        """
        Send an HTTP request to the server and get the response back.

        :param request: HTTP request to send.
        :type request: HTTP_Request

        :param callback: Callback function.
        :type callback: callable

        :param timeout: Timeout in seconds.
            The minimum value is 0.5 and the maximum is 100.0. Any other values
            will be silently converted to either one of them.
        :type timeout: int | float

        :param use_cache: Control the use of the cache.
                          Use True to force the use of the cache,
                          False to force not to use it,
                          or None for automatic.
        :type use_cache: bool | None

        :param allow_redirects: True to follow redirections, False otherwise.
        :type allow_redirects: bool

        :param allow_out_of_scope: True to allow requests out of scope, False otherwise.
        :type allow_out_of_scope: bool

        :returns: HTTP response, or None if the request was cancelled.
        :rtype: HTTP_Response | None

        :raises NetworkOutOfScope: The resource is out of the audit scope.
        :raises NetworkException: A network error occurred.
        """
        if self.__session is None:
            self._initialize()
        if not isinstance(request, HTTP_Request):
            raise TypeError('Expected HTTP_Request, got %r instead' % type(request))
        if callback is not None and not callable(callback):
            raise TypeError('Expected callable (function, class, instance with __call__), got %r instead' % type(callback))
        if use_cache not in (True, False, None):
            raise TypeError('Expected bool or None, got %r instead' % type(use_cache))
        if not request.is_in_scope() and allow_out_of_scope is False:
            raise NetworkOutOfScope('URL out of scope: %s' % request.url)
        if timeout:
            timeout = float(timeout)
            if timeout > 100.0:
                timeout = 100.0
            elif timeout < 0.5:
                timeout = 0.5
        else:
            timeout = 0.5
        cache_key = None
        if use_cache is not False:
            cache_key = '%s|%s|%s' % (request.method, request.url, request.post_data)
            cache_key = md5(cache_key).hexdigest()
            cached_resp = NetworkCache.get(cache_key, request.parsed_url.scheme)
            if cached_resp is not None:
                raw_response, elapsed = cached_resp
                response = HTTP_Response(request=request, raw_response=raw_response, elapsed=elapsed)
                if callback is not None:
                    cont = callback(request, request.url, response.status, response.content_length, response.content_type)
                    if not cont:
                        discard_data(response)
                        return
                return response
        with ConnectionSlot(request.hostname):
            headers = request.headers.to_dict()
            try:
                del headers['host']
            except KeyError:
                pass

            try:
                t1 = time()
                resp = self.__session.request(method=request.method, url=request.url, headers=headers, data=request.post_data, verify=False, stream=True, timeout=timeout, allow_redirects=allow_redirects)
                t2 = time()
            except RequestException as e:
                raise NetworkException(str(e))

            try:
                url = resp.url
                status_code = str(resp.status_code)
                content_type = resp.headers.get('Content-Type')
                try:
                    content_length = int(resp.headers['Content-Length'])
                except Exception:
                    content_length = None

                if url != request.url and url not in Config.audit_scope:
                    raise NetworkOutOfScope('URL out of scope: %s' % url)
                if callback is not None:
                    cont = callback(request, url, status_code, content_length, content_type)
                    if not cont:
                        return
                url_obj = None
                if url != request.url:
                    url_obj = Url(url=url, method=request.method, post_params=request.post_data, referer=request.referer)
                    LocalDataCache.on_autogeneration(url_obj)
                try:
                    t3 = time()
                    data = resp.content
                    t4 = time()
                except RequestException as e:
                    raise NetworkException(str(e))

                elapsed = t2 - t1 + (t4 - t3)
                response = HTTP_Response(request=request, status=status_code, headers=resp.headers, data=data, elapsed=elapsed)
                if url_obj is not None:
                    response.add_resource(url_obj)
                if use_cache is True or use_cache is None and response.is_cacheable():
                    if cache_key is None:
                        cache_key = '%s|%s|%s' % (request.method, url, request.post_data)
                        cache_key = md5(cache_key).hexdigest()
                    cached_resp = (
                     response.raw_response, elapsed)
                    NetworkCache.set(cache_key, cached_resp, request.parsed_url.scheme)
                return response
            finally:
                resp.close()

        return

    def make_raw_request(self, raw_request, host, port=80, proto='http', callback=None, timeout=10.0):
        """
        Send a raw HTTP request to the server and get the response back.

        .. note: This method does not support the use of the cache or a proxy.

        .. warning::
           This method only returns the HTTP response headers, **NOT THE CONTENT**.

        :param raw_request: Raw HTTP request to send.
        :type raw_request: HTTP_Raw_Request

        :param host: Hostname or IP address to connect to.
        :type host: str

        :param port: TCP port to connect to.
        :type port: int

        :param proto: Network protocol (that is, the URL scheme).
        :type proto: str

        :param callback: Callback function.
        :type callback: callable

        :param timeout: Timeout in seconds.
            The minimum value is 0.5 and the maximum is 100.0. Any other values
            will be silently converted to either one of them.
        :type timeout: int | float

        :param use_cache: Control the use of the cache.
                          Use True to force the use of the cache,
                          False to force not to use it,
                          or None for automatic.
        :type use_cache: bool | None

        :returns: HTTP response, or None if the request was cancelled.
        :rtype: HTTP_Response | None

        :raises NetworkOutOfScope: The resource is out of the audit scope.
        :raises NetworkException: A network error occurred.
        """
        if Config.audit_config.proxy_addr:
            raise NotImplementedError('Proxy not yet supported')
        if type(raw_request) is str:
            raw_request = HTTP_Raw_Request(raw_request)
            LocalDataCache.on_autogeneration(raw_request)
        elif not isinstance(raw_request, HTTP_Raw_Request):
            raise TypeError('Expected HTTP_Raw_Request, got %r instead' % type(raw_request))
        if type(host) == unicode:
            raise NotImplementedError('Unicode hostnames not yet supported')
        if type(host) != str:
            raise TypeError('Expected str, got %r instead' % type(host))
        if proto not in ('http', 'https'):
            raise ValueError("Protocol must be 'http' or 'https', not %r" % proto)
        if port is None:
            if proto == 'http':
                port = 80
            elif proto == 'https':
                port = 443
            else:
                assert False, 'internal error!'
        elif type(port) not in (int, long):
            raise TypeError('Expected int, got %r instead' % type(port))
        if port < 1 or port > 32767:
            raise ValueError('Invalid port number: %d' % port)
        if callback is not None and not callable(callback):
            raise TypeError('Expected callable (function, class, instance with __call__), got %r instead' % type(callback))
        if host not in Config.audit_scope:
            raise NetworkOutOfScope('Host out of scope: %s' % host)
        if timeout:
            timeout = float(timeout)
            if timeout > 100.0:
                timeout = 100.0
            elif timeout < 0.5:
                timeout = 0.5
        else:
            timeout = 0.5
        family, socktype, proto, canonname, sockaddr = getaddrinfo(host, port, 0, SOCK_STREAM)[0]
        with ConnectionSlot(host):
            t1 = time()
            try:
                s = socket(family, socktype, proto)
                try:
                    s.settimeout(timeout)
                    s.connect(sockaddr)
                    try:
                        if proto == 'https':
                            s = wrap_socket(s)
                        s.sendall(raw_request.raw_request)
                        raw_response = StringIO()
                        while True:
                            data = s.recv(1)
                            if not data:
                                raise NetworkException('Server has closed the connection')
                            raw_response.write(data)
                            if raw_response.getvalue().endswith('\r\n\r\n'):
                                break
                            if len(raw_response.getvalue()) > 65536:
                                raise NetworkException('Response headers too long')

                        t2 = time()
                        if callback is not None:
                            temp_request = HTTP_Raw_Request(raw_request.raw_request)
                            temp_response = HTTP_Response(temp_request, raw_response=raw_response.getvalue())
                            discard_data(temp_request)
                            discard_data(temp_response)
                            cont = callback(temp_request, temp_response)
                            if not cont:
                                return
                            del temp_request
                            del temp_response
                        t3 = time()
                        t4 = time()
                        return HTTP_Response(request=raw_request, raw_response=raw_response.getvalue(), elapsed=t2 - t1 + (t4 - t3))
                    finally:
                        try:
                            s.shutdown(2)
                        except Exception:
                            pass

                finally:
                    try:
                        s.close()
                    except Exception:
                        pass

            except error as e:
                raise NetworkException(str(e))

        return


HTTP = _HTTP()