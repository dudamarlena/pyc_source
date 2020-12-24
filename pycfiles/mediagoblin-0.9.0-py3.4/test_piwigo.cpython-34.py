# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mediagoblin/tests/test_piwigo.py
# Compiled at: 2016-02-04 13:34:40
# Size of source mod 2**32: 2679 bytes
import pytest
from .tools import fixture_add_user
XML_PREFIX = "<?xml version='1.0' encoding='utf-8'?>\n"

class Test_PWG(object):

    @pytest.fixture(autouse=True)
    def setup(self, test_app):
        self.test_app = test_app
        fixture_add_user()
        self.username = 'chris'
        self.password = 'toast'

    def do_post(self, method, params):
        params['method'] = method
        return self.test_app.post('/api/piwigo/ws.php', params)

    def do_get(self, method, params=None):
        if params is None:
            params = {}
        params['method'] = method
        return self.test_app.get('/api/piwigo/ws.php', params)

    def test_session(self):
        resp = self.do_post('pwg.session.login', {'username': 'nouser',  'password': 'wrong'})
        assert resp.body == (XML_PREFIX + '<rsp stat="fail"><err code="999" msg="Invalid username/password"/></rsp>').encode('ascii')
        resp = self.do_post('pwg.session.login', {'username': self.username,  'password': 'wrong'})
        assert resp.body == (XML_PREFIX + '<rsp stat="fail"><err code="999" msg="Invalid username/password"/></rsp>').encode('ascii')
        resp = self.do_get('pwg.session.getStatus')
        assert resp.body == (XML_PREFIX + '<rsp stat="ok"><username>guest</username></rsp>').encode('ascii')
        resp = self.do_post('pwg.session.login', {'username': self.username,  'password': self.password})
        assert resp.body == (XML_PREFIX + '<rsp stat="ok">1</rsp>').encode('ascii')
        resp = self.do_get('pwg.session.getStatus')
        assert resp.body == (XML_PREFIX + '<rsp stat="ok"><username>chris</username></rsp>').encode('ascii')
        self.do_get('pwg.session.logout')
        resp = self.do_get('pwg.session.getStatus')
        assert resp.body == (XML_PREFIX + '<rsp stat="ok"><username>guest</username></rsp>').encode('ascii')