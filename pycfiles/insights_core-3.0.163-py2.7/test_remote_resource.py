# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/tests/test_remote_resource.py
# Compiled at: 2019-05-16 13:41:33
from insights.core.remote_resource import RemoteResource, CachedRemoteResource
from insights.tests.mock_web_server import TestMockServer
import sys, pytest
GOOD_PAYLOAD = 'Successful return from Mock Service'
NOT_FOUND = '{"error":{"code": "404", "message": "Not Found"}}'

class TestRemoteResource(TestMockServer):

    def test_get_remote_resource(self):
        rr = RemoteResource()
        url = ('http://localhost:{port}/mock/').format(port=self.server_port)
        rtn = rr.get(url)
        assert GOOD_PAYLOAD in rtn.content

    def test_get_remote_resource_not_found(self):
        rr = RemoteResource()
        url = ('http://localhost:{port}/moc/').format(port=self.server_port)
        rtn = rr.get(url)
        assert rtn.content == NOT_FOUND

    def test_get_cached_remote_resource(self):
        crr = CachedRemoteResource()
        url = ('http://localhost:{port}/mock/').format(port=self.server_port)
        rtn = crr.get(url)
        assert GOOD_PAYLOAD in rtn.content

    @pytest.mark.skipif(sys.version_info < (2, 7), reason='CacheControl requires python 2.7 or higher')
    def test_get_cached_remote_resource_cached(self):
        crr = CachedRemoteResource()
        url = ('http://localhost:{port}/mock/').format(port=self.server_port)
        rtn = crr.get(url)
        cont_1 = rtn.content
        rtn = crr.get(url)
        cont_2 = rtn.content
        assert cont_1 == cont_2

    def test_get_cached_remote_resource_not_found(self):
        crr = CachedRemoteResource()
        url = ('http://localhost:{port}/moc/').format(port=self.server_port)
        rtn = crr.get(url)
        assert rtn.content == NOT_FOUND