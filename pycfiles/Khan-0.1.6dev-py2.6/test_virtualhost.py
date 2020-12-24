# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/khan/tests/test_virtualhost.py
# Compiled at: 2010-05-12 10:25:54
from khan.utils.testing import *
from khan.virtualhost import *

class TestVirtualHost(TestCase):

    def setUp(self):
        vhost = VirtualHost()
        vhost['domain.com'] = PrintValue('domain.com:80')
        vhost['*:*'] = PrintValue('*:*')
        vhost['*:80'] = PrintValue('*:80')
        vhost['www.domain.com:*'] = PrintValue('www.domain.com:*')
        vhost['a.www.domain.com:*'] = PrintValue('a.www.domain.com:*')
        vhost['*.domain.com:80'] = PrintValue('*.domain.com:80')
        vhost['ex.com:80'] = PrintValue('ex.com:80')
        vhost['*.*.domain.com:990'] = PrintValue('*.*.domain.com')
        vhost['*.ex.com'] = PrintValue('*.ex.com')
        vhost['*.*.ex.com:80'] = PrintValue('*.*.ex.com:80')
        vhost['*.*.*.a.com'] = PrintValue('*.*.*.a.com')
        self.app = TestApp(vhost)
        self.vhost = vhost

    def test_match(self):
        resp = self.app.get('/', extra_environ={'HTTP_HOST': 'a.www.domain.com', 'HTTP_PORT': '80'})
        assert resp.body == 'a.www.domain.com:*', resp.body

    def test_not_found(self):
        resp = self.app.get('/', extra_environ={'HTTP_HOST': 'a1.www.domain.com', 'HTTP_PORT': '80'})
        assert resp.status_int == 200
        del self.vhost['*:*']
        resp = self.app.get('/', status='*', extra_environ={'HTTP_HOST': 'a1.www.domain.com', 'HTTP_PORT': '880'})
        assert resp.status_int == 404, resp.body
        self.vhost['*:*'] = PrintValue('*:*')