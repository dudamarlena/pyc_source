# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gbaconnier/dev/locustodoorpc/.env/lib/python2.7/site-packages/locustodoorpc/client.py
# Compiled at: 2017-11-03 10:55:39
import json, os, sys, time, odoorpc
from locust import Locust, events
PY3 = sys.version[0] == 3
if PY3:
    import urllib
    from urllib import parse as urlparse
else:
    import urllib2 as urllib
    from urlparse import urlparse

class ODOOLocustClient(odoorpc.ODOO):

    def capture_request(request_type):

        def _wrapped_func(func):

            def _wrapper(self, *args, **kwargs):
                if args[0] == '/jsonrpc' and args[1].get('method').startswith('execute'):
                    name = '%s | %s: %s' % tuple([
                     args[0]] + args[1]['args'][3:5])
                else:
                    name = args[0]
                start_time = time.time()
                try:
                    response = func(self, *args, **kwargs)
                except (urllib.HTTPError, urllib.URLError) as err:
                    total_time = int((time.time() - start_time) * 1000)
                    events.request_failure.fire(request_type=request_type, name=name, response_time=total_time, exception=err)
                    raise
                else:
                    total_time = int((time.time() - start_time) * 1000)
                    if isinstance(response, dict):
                        size = len(json.dumps(response))
                    else:
                        response = response.read()
                        size = len(response)
                    events.request_success.fire(request_type=request_type, name=name, response_time=total_time, response_length=size)
                    return response

            return _wrapper

        return _wrapped_func

    @capture_request('jsonrpc')
    def json(self, url, params):
        return super(ODOOLocustClient, self).json(url, params)

    @capture_request('http')
    def http(self, url, data=None, headers=None):
        return super(ODOOLocustClient, self).http(url, data=data, headers=headers)


class OdooRPCLocust(Locust):
    """ Locust class providing the odoorpc client

    This is the abstract Locust class which should be subclassed. It provides
    an Odoo client using odoorpc library, that can be used to make requests
    that will be tracked in Locust's statistics.

    The host, port and protocol (jsonrpc or jsonrpc+ssl) comes from the
    ``--host`` option.

    """
    db_name = os.getenv('ODOO_DB_NAME', 'odoo')
    login = os.getenv('ODOO_LOGIN', 'admin')
    password = os.getenv('ODOO_PASSWORD', 'admin')
    version = os.getenv('ODOO_VERSION')

    def __init__(self, *args, **kwargs):
        super(OdooRPCLocust, self).__init__(*args, **kwargs)
        url = urlparse(self.host)
        port = url.port
        if url.scheme == 'https':
            protocol = 'jsonrpc+ssl'
            if not port:
                port = 443
        else:
            protocol = 'jsonrpc'
            if not port:
                port = 80
        protocol = 'jsonrpc+ssl' if url.scheme == 'https' else 'jsonrpc'
        params = {'host': url.hostname, 
           'port': port, 
           'protocol': protocol}
        if self.version:
            params['version'] = self.version
        self.client = ODOOLocustClient(**params)