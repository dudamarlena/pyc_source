# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsmclient/tests/unit/v1/fakes.py
# Compiled at: 2016-06-13 14:11:03
from datetime import datetime
try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse

from vsmclient import client as base_client
from vsmclient.tests.unit import fakes
from vsmclient.tests.unit import utils
from vsmclient.v1 import client

def _stub_appnode(**kwargs):
    appnode = {'id': '1234', 
       'os_username': 'admin', 
       'os_password': 'admin', 
       'os_tenant_name': 'admin', 
       'os_auth_url': 'http://192.168.100.100:5000/v2.0', 
       'os_region_name': 'RegionOne', 
       'ssh_user': 'root', 
       'uuid': '00000000-0000-0000-0000-000000000000', 
       'ssh_status': 'reachable', 
       'log_info': None}
    appnode.update(kwargs)
    return appnode


class FakeClient(fakes.FakeClient, client.Client):

    def __init__(self, *args, **kwargs):
        client.Client.__init__(self, 'username', 'password', 'project_id', 'auth_url', extensions=kwargs.get('extensions'))
        self.client = FakeHTTPClient(**kwargs)


class FakeHTTPClient(base_client.HTTPClient):

    def __init__(self, **kwargs):
        self.username = 'username'
        self.password = 'password'
        self.auth_url = 'auth_url'
        self.callstack = []
        self.management_url = 'http://10.0.2.15:8776/v1/fake'

    def _cs_request(self, url, method, **kwargs):
        if method in ('GET', 'DELETE'):
            assert 'body' not in kwargs
        elif not (method == 'PUT' and 'body' in kwargs):
            raise AssertionError
        args = urlparse.parse_qsl(urlparse.urlparse(url)[4])
        kwargs.update(args)
        munged_url = url.rsplit('?', 1)[0]
        munged_url = munged_url.strip('/').replace('/', '_').replace('.', '_')
        munged_url = munged_url.replace('-', '_')
        callback = '%s_%s' % (method.lower(), munged_url)
        assert hasattr(self, callback), 'Called unknown API method: %s %s, expected fakes method name: %s' % (
         method, url, callback)
        self.callstack.append((method, url, kwargs.get('body', None)))
        status, headers, body = getattr(self, callback)(**kwargs)
        r = utils.TestResponse({'status_code': status, 
           'text': body, 
           'headers': headers})
        return (
         r, body)
        if hasattr(status, 'items'):
            return (utils.TestResponse(status), body)
        else:
            return (
             utils.TestResponse({'status': status}), body)
            return

    def get_appnodes(self, **kw):
        return (
         200, {},
         {'appnodes': [
                       _stub_appnode()]})

    def post_appnodes(self, body, **kw):
        return (
         201, {}, {})