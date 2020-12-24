# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mediagoblin/tests/test_notifications.py
# Compiled at: 2016-03-29 15:18:42
# Size of source mod 2**32: 8137 bytes
import pytest, six.moves.urllib.parse as urlparse
from mediagoblin.tools import template, mail
from mediagoblin.db.models import Notification, CommentSubscription
from mediagoblin.db.base import Session
from mediagoblin.notifications import mark_comment_notification_seen
from mediagoblin.tests.tools import fixture_add_comment, fixture_media_entry, fixture_add_user, fixture_comment_subscription

class TestNotifications:

    @pytest.fixture(autouse=True)
    def setup(self, test_app):
        self.test_app = test_app
        self.test_user = fixture_add_user(privileges=['active', 'commenter'])
        self.current_user = None
        self.login()

    def login(self, username='chris', password='toast'):
        response = self.test_app.post('/auth/login/', {'username': username, 
         'password': password})
        response.follow()
        assert urlparse.urlsplit(response.location)[2] == '/'
        assert 'mediagoblin/root.html' in template.TEMPLATE_TEST_CONTEXT
        ctx = template.TEMPLATE_TEST_CONTEXT['mediagoblin/root.html']
        assert Session.merge(ctx['request'].user).username == username
        self.current_user = ctx['request'].user

    def logout(self):
        self.test_app.get('/auth/logout/')
        self.current_user = None

    @pytest.mark.parametrize('wants_email', [True, False])
    def test_comment_notification(self, wants_email):
        """
        Test
        - if a notification is created when posting a comment on
          another users media entry.
        - that the comment data is consistent and exists.

        """
        user = fixture_add_user('otherperson', password='nosreprehto', wants_comment_notification=wants_email, privileges=[
         'active', 'commenter'])
        assert user.wants_comment_notification == wants_email
        user_id = user.id
        media_entry = fixture_media_entry(uploader=user.id, state='processed')
        media_entry_id = media_entry.id
        subscription = fixture_comment_subscription(media_entry)
        subscription_id = subscription.id
        media_uri_id = '/u/{0}/m/{1}/'.format(user.username, media_entry.id)
        media_uri_slug = '/u/{0}/m/{1}/'.format(user.username, media_entry.slug)
        self.test_app.post(media_uri_id + 'comment/add/', {'comment_content': 'Test comment #42'})
        notifications = Notification.query.filter_by(user_id=user.id).all()
        assert len(notifications) == 1
        notification = notifications[0]
        assert notification.seen == False
        assert notification.user_id == user.id
        assert notification.obj().comment().get_actor.id == self.test_user.id
        assert notification.obj().comment().content == 'Test comment #42'
        if wants_email == True:
            if not mail.EMAIL_TEST_MBOX_INBOX == [
             {'from': 'notice@mediagoblin.example.org',  'message': 'Content-Type: text/plain; charset="utf-8"\nMIME-Version: 1.0\nContent-Transfer-Encoding: base64\nSubject: GNU MediaGoblin - chris commented on your post\nFrom: notice@mediagoblin.example.org\nTo: otherperson@example.com\n\nSGkgb3RoZXJwZXJzb24sCmNocmlzIGNvbW1lbnRlZCBvbiB5b3VyIHBvc3QgKGh0dHA6Ly9sb2Nh\nbGhvc3Q6ODAvdS9vdGhlcnBlcnNvbi9tL3NvbWUtdGl0bGUvYy8xLyNjb21tZW50KSBhdCBHTlUg\nTWVkaWFHb2JsaW4KClRlc3QgY29tbWVudCAjNDIKCkdOVSBNZWRpYUdvYmxpbg==\n', 
              'to': [
                     'otherperson@example.com']}]:
                assert mail.EMAIL_TEST_MBOX_INBOX == [
                 {'from': 'notice@mediagoblin.example.org',  'message': 'Content-Type: text/plain; charset="utf-8"\nMIME-Version: 1.0\nContent-Transfer-Encoding: base64\nSubject: GNU MediaGoblin - chris commented on your post\nFrom: notice@mediagoblin.example.org\nTo: otherperson@example.com\n\nSGkgb3RoZXJwZXJzb24sCmNocmlzIGNvbW1lbnRlZCBvbiB5b3VyIHBvc3QgKGh0dHA6Ly9sb2Nh\nbGhvc3QvdS9vdGhlcnBlcnNvbi9tL3NvbWUtdGl0bGUvYy8xLyNjb21tZW50KSBhdCBHTlUgTWVk\naWFHb2JsaW4KClRlc3QgY29tbWVudCAjNDIKCkdOVSBNZWRpYUdvYmxpbg==\n', 
                  'to': [
                         'otherperson@example.com']}]
        else:
            assert mail.EMAIL_TEST_MBOX_INBOX == []
            notification_id = notification.id
            comment_id = notification.obj().id
            self.logout()
            self.login('otherperson', 'nosreprehto')
            self.test_app.get(media_uri_slug + 'c/{0}/'.format(comment_id))
            notification = Notification.query.filter_by(id=notification_id).first()
            assert notification.seen == True
            self.test_app.get(media_uri_slug + 'notifications/silence/')
            subscription = CommentSubscription.query.filter_by(id=subscription_id).first()
            assert subscription.notify == False
            notifications = Notification.query.filter_by(user_id=user_id).all()
            if not len(notifications) == 1:
                raise AssertionError

    def test_mark_all_comment_notifications_seen(self):
        """ Test that mark_all_comments_seen works"""
        user = fixture_add_user('otherperson', password='nosreprehto', privileges=[
         'active'])
        media_entry = fixture_media_entry(uploader=user.id, state='processed')
        fixture_comment_subscription(media_entry)
        media_uri_id = '/u/{0}/m/{1}/'.format(user.username, media_entry.id)
        self.test_app.post(media_uri_id + 'comment/add/', {'comment_content': 'Test comment #43'})
        self.test_app.post(media_uri_id + 'comment/add/', {'comment_content': 'Test comment #44'})
        notifications = Notification.query.filter_by(user_id=user.id).all()
        assert len(notifications) == 2
        assert notifications[0].seen == False
        assert notifications[1].seen == False
        self.logout()
        self.login('otherperson', 'nosreprehto')
        res = self.test_app.get('/notifications/comments/mark_all_seen/')
        res.follow()
        assert urlparse.urlsplit(res.location)[2] == '/'
        notifications = Notification.query.filter_by(user_id=user.id).all()
        assert notifications[0].seen == True
        assert notifications[1].seen == True