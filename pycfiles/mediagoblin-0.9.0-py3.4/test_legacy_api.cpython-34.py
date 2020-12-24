# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mediagoblin/tests/test_legacy_api.py
# Compiled at: 2016-02-04 13:34:40
# Size of source mod 2**32: 2990 bytes
import logging, base64, json, pytest
from mediagoblin import mg_globals
from mediagoblin.tools import template, pluginapi
from mediagoblin.tests.tools import fixture_add_user
from .resources import GOOD_JPG, GOOD_PNG, EVIL_FILE, EVIL_JPG, EVIL_PNG, BIG_BLUE
_log = logging.getLogger(__name__)

class TestAPI(object):

    def setup(self):
        self.db = mg_globals.database
        self.user_password = '4cc355_70k3N'
        self.user = fixture_add_user('joapi', self.user_password, privileges=[
         'active', 'uploader'])

    def login(self, test_app):
        test_app.post('/auth/login/', {'username': self.user.username, 
         'password': self.user_password})

    def get_context(self, template_name):
        return template.TEMPLATE_TEST_CONTEXT[template_name]

    def http_auth_headers(self):
        return {'Authorization': 'Basic {0}'.format(base64.b64encode(':'.join([
                           self.user.username,
                           self.user_password]).encode('ascii')).decode())}

    def do_post(self, data, test_app, **kwargs):
        url = kwargs.pop('url', '/api/submit')
        do_follow = kwargs.pop('do_follow', False)
        if 'headers' not in kwargs.keys():
            kwargs['headers'] = self.http_auth_headers()
        response = test_app.post(url, data, **kwargs)
        if do_follow:
            response.follow()
        return response

    def upload_data(self, filename):
        return {'upload_files': [('file', filename)]}

    def test_1_test_test_view(self, test_app):
        self.login(test_app)
        response = test_app.get('/api/test', headers=self.http_auth_headers())
        assert json.loads(response.body.decode()) == {'username': 'joapi', 
         'email': 'joapi@example.com'}

    def test_2_test_submission(self, test_app):
        self.login(test_app)
        response = self.do_post({'title': 'Great JPG!'}, test_app, **self.upload_data(GOOD_JPG))
        assert response.status_int == 200
        assert self.db.MediaEntry.query.filter_by(title='Great JPG!').first()