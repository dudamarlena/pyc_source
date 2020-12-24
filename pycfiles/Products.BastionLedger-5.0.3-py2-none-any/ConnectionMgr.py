# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/Products/BastionBanking/ConnectionMgr.py
# Compiled at: 2015-07-18 19:38:10
import os
from httplib2 import Http, ProxyInfo, BasicAuthentication
from httplib2.socks import PROXY_TYPE_HTTP
from urlparse import urlparse
from urllib import urlencode
from threading import Lock
HEADERS = {'Content-type': 'application/x-www-form-urlencoded', 
   'Accept-Encoding': 'identity', 
   'Connection': 'close', 
   'keep-alive': '0', 
   'User-Agent': 'BastionBanking'}

class Transport:
    """
    Python's httplib SSL layer is generally fucked, so we're providing a wrapper
    for it here.
    """
    _lock = Lock()

    def __init__(self, url, user='', password='', timeout=30):
        """
        setup a request to a URL.  If user/password supplied, then set up
        basic http authentication headers
        """
        self.url = url
        self.headers = dict(HEADERS)
        proto = urlparse(url)[0]
        proxyinfo = None
        proxy = '%s_proxy' % proto
        if os.environ.has_key(proxy):
            pproto, phost, directory, params, query, frag = urlparse(os.environ[proxy])
            if phost.find('@') != -1:
                pcreds, phost = phost.split('@')
                puser, ppwd = pcreds.split(':')
            else:
                puser = ppwd = None
            if phost.find(':') != -1:
                phost, pport = phost.split(':')
            elif pproto == 'https':
                pport = '443'
            else:
                pport = '80'
            if puser and ppwd:
                proxyinfo = ProxyInfo(PROXY_TYPE_HTTP, phost, int(pport), proxy_user=puser, proxy_pass=ppwd)
            else:
                proxyinfo = ProxyInfo(PROXY_TYPE_HTTP, phost, int(pport))
        assert proto in ('http', 'https'), 'Unsupported Protocol: %s' % proto
        self.auth = BasicAuthentication((user, password), None, url, None, None, None, None)
        self._v_conn = conn = Http(timeout=timeout, proxy_info=proxyinfo, disable_ssl_certificate_validation=True)
        return

    def __call__(self, body='', headers={}, action='POST'):
        """
        make the request, returns the response packet contents, and response code as
        a tuple
        """
        req_hdrs = self.headers
        req_hdrs.update(headers)
        try:
            self._lock.acquire()
            self.auth and self.auth.request(None, None, req_hdrs, None)
            response, data = self._v_conn.request(self.url, method=action, body=body, headers=req_hdrs)
            return (
             response, data)
        finally:
            self._lock.release()

        return

    def __del__(self):
        try:
            self._v_conn.close()
        except:
            pass