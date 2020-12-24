# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/go_gae_proxy/__init__.py
# Compiled at: 2014-01-12 14:41:28
import base64, json
from urllib2 import BaseHandler, Request
import urlparse

class GoProxyHandler(BaseHandler):
    handler_order = 100

    def __init__(self, proxy_url):
        parsed_url = urlparse.urlparse(proxy_url)
        self.authorization_code = parsed_url.username
        self.proxy_endpoint = urlparse.urlunparse((parsed_url.scheme, parsed_url.hostname if parsed_url.port is None else '%s:%d' % (parsed_url.hostname, parsed_url.port), parsed_url.path, parsed_url.params, parsed_url.query, parsed_url.fragment))
        return

    def http_open(self, req):
        return self.proxy_open(req)

    def https_open(self, req):
        return self.proxy_open(req)

    def proxy_open(self, req):
        if req.get_full_url() == self.proxy_endpoint:
            return None
        else:
            proxy_request = {'Code': self.authorization_code, 
               'Verb': req.get_method(), 
               'URI': req.get_full_url(), 
               'Body': base64.standard_b64encode(req.get_data() or ''), 
               'Headers': req.headers}
            return self.parent.open(Request(self.proxy_endpoint, json.dumps(proxy_request)), timeout=req.timeout)