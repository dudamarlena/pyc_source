# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mediagoblin/tests/test_privileges.py
# Compiled at: 2016-03-29 15:18:42
# Size of source mod 2**32: 9466 bytes
import six, pytest
from datetime import date, timedelta
from webtest import AppError
from mediagoblin.tests.tools import fixture_add_user, fixture_media_entry
from mediagoblin.db.models import User, LocalUser, UserBan
from mediagoblin.tools import template
from .resources import GOOD_JPG

class TestPrivilegeFunctionality:

    @pytest.fixture(autouse=True)
    def _setup(self, test_app):
        self.test_app = test_app
        fixture_add_user('alex', privileges=[
         'admin', 'active'])
        fixture_add_user('meow', privileges=[
         'moderator', 'active', 'reporter'])
        fixture_add_user('natalie', privileges=[
         'active'])
        self.query_for_users()

    def login(self, username):
        self.test_app.post('/auth/login/', {'username': username, 
         'password': 'toast'})
        self.query_for_users()

    def logout(self):
        self.test_app.get('/auth/logout/')
        self.query_for_users()

    def do_post(self, data, *context_keys, **kwargs):
        url = kwargs.pop('url', '/submit/')
        do_follow = kwargs.pop('do_follow', False)
        template.clear_test_template_context()
        response = self.test_app.post(url, data, **kwargs)
        if do_follow:
            response.follow()
        context_data = template.TEMPLATE_TEST_CONTEXT
        for key in context_keys:
            context_data = context_data[key]

        return (
         response, context_data)

    def query_for_users(self):
        self.admin_user = LocalUser.query.filter(LocalUser.username == 'alex').first()
        self.mod_user = LocalUser.query.filter(LocalUser.username == 'meow').first()
        self.user = LocalUser.query.filter(LocalUser.username == 'natalie').first()

    def testUserBanned(self):
        self.login('natalie')
        uid = self.user.id
        user_ban = UserBan(user_id=uid, reason='Testing whether user is banned', expiration_date=None)
        user_ban.save()
        response = self.test_app.get('/')
        assert response.status == '200 OK'
        assert b'You are Banned' in response.body
        user_ban = UserBan.query.get(uid)
        user_ban.delete()
        user_ban = UserBan(user_id=uid, reason='Testing whether user is banned', expiration_date=date.today() + timedelta(days=20))
        user_ban.save()
        response = self.test_app.get('/')
        assert response.status == '200 OK'
        assert b'You are Banned' in response.body
        user_ban = UserBan.query.get(uid)
        user_ban.delete()
        exp_date = date.today() - timedelta(days=20)
        user_ban = UserBan(user_id=uid, reason='Testing whether user is banned', expiration_date=exp_date)
        user_ban.save()
        response = self.test_app.get('/')
        assert response.status == '302 FOUND'
        assert b'You are Banned' not in response.body

    def testVariousPrivileges(self):
        self.login('natalie')
        with pytest.raises(AppError) as (excinfo):
            response = self.test_app.get('/submit/')
        excinfo = str(excinfo) if six.PY2 else str(excinfo).encode('ascii')
        assert b'Bad response: 403 FORBIDDEN' in excinfo
        with pytest.raises(AppError) as (excinfo):
            response = self.do_post({'upload_files': [('file', GOOD_JPG)],  'title': 'Normal Upload 1'}, url='/submit/')
        excinfo = str(excinfo) if six.PY2 else str(excinfo).encode('ascii')
        assert b'Bad response: 403 FORBIDDEN' in excinfo
        self.query_for_users()
        media_entry = fixture_media_entry(uploader=self.admin_user.id, state='processed')
        media_entry_id = media_entry.id
        media_uri_id = '/u/{0}/m/{1}/'.format(self.admin_user.username, media_entry.id)
        media_uri_slug = '/u/{0}/m/{1}/'.format(self.admin_user.username, media_entry.slug)
        response = self.test_app.get(media_uri_slug)
        assert b'Add a comment' not in response.body
        self.query_for_users()
        with pytest.raises(AppError) as (excinfo):
            response = self.test_app.post(media_uri_id + 'comment/add/', {'comment_content': 'Test comment #42'})
        excinfo = str(excinfo) if six.PY2 else str(excinfo).encode('ascii')
        assert b'Bad response: 403 FORBIDDEN' in excinfo
        with pytest.raises(AppError) as (excinfo):
            response = self.test_app.get(media_uri_slug + 'report/')
        excinfo = str(excinfo) if six.PY2 else str(excinfo).encode('ascii')
        assert b'Bad response: 403 FORBIDDEN' in excinfo
        with pytest.raises(AppError) as (excinfo):
            response = self.do_post({'report_reason': 'Testing Reports #1',  'reporter_id': '3'}, url=media_uri_slug + 'report/')
        excinfo = str(excinfo) if six.PY2 else str(excinfo).encode('ascii')
        assert b'Bad response: 403 FORBIDDEN' in excinfo
        with pytest.raises(AppError) as (excinfo):
            response = self.test_app.get('/mod/users/')
        excinfo = str(excinfo) if six.PY2 else str(excinfo).encode('ascii')
        assert b'Bad response: 403 FORBIDDEN' in excinfo
        with pytest.raises(AppError) as (excinfo):
            response = self.test_app.get('/mod/reports/')
        excinfo = str(excinfo) if six.PY2 else str(excinfo).encode('ascii')
        assert b'Bad response: 403 FORBIDDEN' in excinfo
        with pytest.raises(AppError) as (excinfo):
            response = self.test_app.get('/mod/media/')
        excinfo = str(excinfo) if six.PY2 else str(excinfo).encode('ascii')
        assert b'Bad response: 403 FORBIDDEN' in excinfo
        with pytest.raises(AppError) as (excinfo):
            response = self.test_app.get('/mod/users/1/')
        excinfo = str(excinfo) if six.PY2 else str(excinfo).encode('ascii')
        assert b'Bad response: 403 FORBIDDEN' in excinfo
        with pytest.raises(AppError) as (excinfo):
            response = self.test_app.get('/mod/reports/1/')
        excinfo = str(excinfo) if six.PY2 else str(excinfo).encode('ascii')
        assert b'Bad response: 403 FORBIDDEN' in excinfo
        self.query_for_users()
        with pytest.raises(AppError) as (excinfo):
            response, context = self.do_post({'action_to_resolve': ['takeaway'],  'take_away_privileges': [
                                      'active'], 
             'targeted_user': self.admin_user.id}, url='/mod/reports/1/')
            self.query_for_users()
        excinfo = str(excinfo) if six.PY2 else str(excinfo).encode('ascii')
        assert b'Bad response: 403 FORBIDDEN' in excinfo