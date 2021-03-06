# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mediagoblin/tests/test_edit.py
# Compiled at: 2016-03-29 15:18:42
# Size of source mod 2**32: 10128 bytes
import six, six.moves.urllib.parse as urlparse, pytest
from mediagoblin import mg_globals
from mediagoblin.db.models import User, LocalUser, MediaEntry
from mediagoblin.tests.tools import fixture_add_user, fixture_media_entry
from mediagoblin import auth
from mediagoblin.tools import template, mail

class TestUserEdit(object):

    def setup(self):
        self.user_password = 'toast'
        self.user = fixture_add_user(password=self.user_password, privileges=[
         'active'])

    def login(self, test_app):
        test_app.post('/auth/login/', {'username': self.user.username, 
         'password': self.user_password})

    def test_user_deletion(self, test_app):
        """Delete user via web interface"""
        self.login(test_app)
        assert LocalUser.query.filter(LocalUser.username == 'chris').first()
        res = test_app.post('/edit/account/delete/', {'confirmed': 'y'})
        assert LocalUser.query.filter(LocalUser.username == 'chris').first() == None
        self.user = fixture_add_user(password=self.user_password, privileges=[
         'active'])
        self.login(test_app)

    def test_change_bio_url(self, test_app):
        """Test changing bio and URL"""
        self.login(test_app)
        res = test_app.post('/edit/profile/', {'bio': 'I love toast!', 
         'url': 'http://dustycloud.org/'}, expect_errors=True)
        assert res.status_int == 302
        assert res.headers['Location'].endswith('/u/chris/edit/')
        res = test_app.post('/u/chris/edit/', {'bio': 'I love toast!', 
         'url': 'http://dustycloud.org/'})
        test_user = LocalUser.query.filter(LocalUser.username == 'chris').first()
        assert test_user.bio == 'I love toast!'
        assert test_user.url == 'http://dustycloud.org/'
        fixture_add_user(username='foo', privileges=[
         'active'])
        res = test_app.post('/u/foo/edit/', {'bio': 'I love toast!', 
         'url': 'http://dustycloud.org/'}, expect_errors=True)
        assert res.status_int == 403
        too_long_bio = 150 * 'T' + 150 * 'o' + 150 * 'a' + 150 * 's' + 150 * 't'
        test_app.post('/u/chris/edit/', {'bio': too_long_bio, 
         'url': 'this-is-no-url'})
        context = template.TEMPLATE_TEST_CONTEXT['mediagoblin/edit/edit_profile.html']
        form = context['form']
        assert form.bio.errors == [
         'Field must be between 0 and 500 characters long.']
        assert form.url.errors == [
         'This address contains errors']

    def test_email_change(self, test_app):
        self.login(test_app)
        template.clear_test_template_context()
        test_app.post('/edit/email/', {'new_email': 'chris@example.com', 
         'password': 'toast'})
        context = template.TEMPLATE_TEST_CONTEXT['mediagoblin/edit/change_email.html']
        assert context['form'].new_email.errors == [
         'Sorry, a user with that email address already exists.']
        template.clear_test_template_context()
        res = test_app.post('/edit/email/', {'new_email': 'new@example.com', 
         'password': 'toast'})
        res.follow()
        assert urlparse.urlsplit(res.location)[2] == '/edit/account/'
        assert len(mail.EMAIL_TEST_INBOX) == 1
        message = mail.EMAIL_TEST_INBOX.pop()
        assert message['To'] == 'new@example.com'
        email_context = template.TEMPLATE_TEST_CONTEXT['mediagoblin/edit/verification.txt']
        assert email_context['verification_url'].encode('ascii') in message.get_payload(decode=True)
        path = urlparse.urlsplit(email_context['verification_url'])[2]
        assert path == '/edit/verify_email/'
        template.clear_test_template_context()
        res = test_app.get('/edit/verify_email/?token=total_bs')
        res.follow()
        assert urlparse.urlsplit(res.location)[2] == '/'
        email_in_db = mg_globals.database.LocalUser.query.filter(LocalUser.email == 'new@example.com').first()
        email = LocalUser.query.filter(LocalUser.username == 'chris').first().email
        assert email_in_db is None
        assert email == 'chris@example.com'
        template.clear_test_template_context()
        get_params = urlparse.urlsplit(email_context['verification_url'])[3]
        res = test_app.get('%s?%s' % (path, get_params))
        res.follow()
        email = LocalUser.query.filter(LocalUser.username == 'chris').first().email
        assert email == 'new@example.com'


class TestMetaDataEdit:

    @pytest.fixture(autouse=True)
    def setup(self, test_app):
        self.user_password = 'toast'
        self.user = fixture_add_user(password=self.user_password, privileges=[
         'active', 'admin'])
        self.test_app = test_app

    def login(self, test_app):
        test_app.post('/auth/login/', {'username': self.user.username, 
         'password': self.user_password})

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

    def test_edit_metadata(self, test_app):
        media_entry = fixture_media_entry(uploader=self.user.id, state='processed')
        media_slug = '/u/{username}/m/{media_id}/metadata/'.format(username=str(self.user.username), media_id=str(media_entry.id))
        self.login(test_app)
        response = test_app.get(media_slug)
        assert response.status == '200 OK'
        assert media_entry.media_metadata == {}
        response, context = self.do_post({'media_metadata-0-identifier': 'dc:title', 
         'media_metadata-0-value': 'Some title', 
         'media_metadata-1-identifier': 'dc:creator', 
         'media_metadata-1-value': 'Me'}, url=media_slug)
        media_entry = MediaEntry.query.first()
        new_metadata = media_entry.media_metadata
        assert new_metadata != {}
        assert new_metadata.get('dc:title') == 'Some title'
        assert new_metadata.get('dc:creator') == 'Me'
        response, context = self.do_post({'media_metadata-0-identifier': 'dc:title', 
         'media_metadata-0-value': 'Some title'}, url=media_slug)
        media_entry = MediaEntry.query.first()
        new_metadata = media_entry.media_metadata
        assert new_metadata.get('dc:title') == 'Some title'
        assert new_metadata.get('dc:creator') is None
        response, context = self.do_post({'media_metadata-0-identifier': 'dc:title', 
         'media_metadata-0-value': 'Some title', 
         'media_metadata-1-identifier': 'dc:creator', 
         'media_metadata-1-value': 'Me', 
         'media_metadata-2-identifier': 'dc:created', 
         'media_metadata-2-value': 'On the worst day'}, url=media_slug)
        media_entry = MediaEntry.query.first()
        old_metadata = new_metadata
        new_metadata = media_entry.media_metadata
        assert new_metadata == old_metadata
        context = template.TEMPLATE_TEST_CONTEXT['mediagoblin/edit/metadata.html']
        if six.PY2:
            expected = "u'On the worst day' is not a 'date-time'"
        else:
            expected = "'On the worst day' is not a 'date-time'"
        assert context['form'].errors['media_metadata'][0]['identifier'][0] == expected