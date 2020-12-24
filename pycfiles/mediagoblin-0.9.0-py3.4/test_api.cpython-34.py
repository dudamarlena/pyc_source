# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mediagoblin/tests/test_api.py
# Compiled at: 2016-03-29 15:18:42
# Size of source mod 2**32: 23972 bytes
import json
try:
    import mock
except ImportError:
    import unittest.mock as mock

import pytest
from webtest import AppError
from .resources import GOOD_JPG
from mediagoblin import mg_globals
from mediagoblin.db.models import User, Activity, MediaEntry, TextComment
from mediagoblin.tools.routing import extract_url_arguments
from mediagoblin.tests.tools import fixture_add_user
from mediagoblin.moderation.tools import take_away_privileges

class TestAPI(object):
    __doc__ = " Test mediagoblin's pump.io complient APIs "

    @pytest.fixture(autouse=True)
    def setup(self, test_app):
        self.test_app = test_app
        self.db = mg_globals.database
        self.user = fixture_add_user(privileges=['active', 'uploader', 'commenter'])
        self.other_user = fixture_add_user(username='otheruser', privileges=[
         'active', 'uploader', 'commenter'])
        self.active_user = self.user

    def _activity_to_feed(self, test_app, activity, headers=None):
        """ Posts an activity to the user's feed """
        if headers:
            headers.setdefault('Content-Type', 'application/json')
        else:
            headers = {'Content-Type': 'application/json'}
        with self.mock_oauth():
            response = test_app.post('/api/user/{0}/feed'.format(self.active_user.username), json.dumps(activity), headers=headers)
        return (
         response, json.loads(response.body.decode()))

    def _upload_image(self, test_app, image):
        """ Uploads and image to MediaGoblin via pump.io API """
        data = open(image, 'rb').read()
        headers = {'Content-Type': 'image/jpeg', 
         'Content-Length': str(len(data))}
        with self.mock_oauth():
            response = test_app.post('/api/user/{0}/uploads'.format(self.active_user.username), data, headers=headers)
            image = json.loads(response.body.decode())
        return (response, image)

    def _post_image_to_feed(self, test_app, image):
        """ Posts an already uploaded image to feed """
        activity = {'verb': 'post', 
         'object': image}
        return self._activity_to_feed(test_app, activity)

    def mocked_oauth_required(self, *args, **kwargs):
        """ Mocks mediagoblin.decorator.oauth_required to always validate """

        def fake_controller(controller, request, *args, **kwargs):
            request.user = User.query.filter_by(id=self.active_user.id).first()
            return controller(request, *args, **kwargs)

        def oauth_required(c):
            return lambda *args**args: fake_controller(c, *args, **kwargs)

        return oauth_required

    def mock_oauth(self):
        """ Returns a mock.patch for the oauth_required decorator """
        return mock.patch(target='mediagoblin.decorators.oauth_required', new_callable=self.mocked_oauth_required)

    def test_can_post_image(self, test_app):
        """ Tests that an image can be posted to the API """
        response, image = self._upload_image(test_app, GOOD_JPG)
        assert response.status_code == 200
        assert 'id' in image
        assert 'fullImage' in image
        assert 'url' in image['fullImage']
        assert 'url' in image
        assert 'author' in image
        assert 'published' in image
        assert 'updated' in image
        assert image['objectType'] == 'image'
        response, _ = self._post_image_to_feed(test_app, image)
        assert response.status_code == 200

    def test_unable_to_upload_as_someone_else(self, test_app):
        """ Test that can't upload as someoen else """
        data = open(GOOD_JPG, 'rb').read()
        headers = {'Content-Type': 'image/jpeg', 
         'Content-Length': str(len(data))}
        with self.mock_oauth():
            with pytest.raises(AppError) as (excinfo):
                test_app.post('/api/user/{0}/uploads'.format(self.other_user.username), data, headers=headers)
            assert '403 FORBIDDEN' in excinfo.value.args[0]

    def test_unable_to_post_feed_as_someone_else(self, test_app):
        """ Tests that can't post an image to someone else's feed """
        response, data = self._upload_image(test_app, GOOD_JPG)
        activity = {'verb': 'post', 
         'object': data}
        headers = {'Content-Type': 'application/json'}
        with self.mock_oauth():
            with pytest.raises(AppError) as (excinfo):
                test_app.post('/api/user/{0}/feed'.format(self.other_user.username), json.dumps(activity), headers=headers)
            assert '403 FORBIDDEN' in excinfo.value.args[0]

    def test_only_able_to_update_own_image(self, test_app):
        """ Test's that the uploader is the only person who can update an image """
        response, data = self._upload_image(test_app, GOOD_JPG)
        response, data = self._post_image_to_feed(test_app, data)
        activity = {'verb': 'update', 
         'object': data['object']}
        headers = {'Content-Type': 'application/json'}
        media = MediaEntry.query.filter_by(public_id=data['object']['id']).first()
        media.actor = self.other_user.id
        media.save()
        with self.mock_oauth():
            with pytest.raises(AppError) as (excinfo):
                test_app.post('/api/user/{0}/feed'.format(self.user.username), json.dumps(activity), headers=headers)
            assert '403 FORBIDDEN' in excinfo.value.args[0]

    def test_upload_image_with_filename(self, test_app):
        """ Tests that you can upload an image with filename and description """
        response, data = self._upload_image(test_app, GOOD_JPG)
        response, data = self._post_image_to_feed(test_app, data)
        image = data['object']
        title = 'My image ^_^'
        description = 'This is my super awesome image :D'
        license = 'CC-BY-SA'
        image['displayName'] = title
        image['content'] = description
        image['license'] = license
        activity = {'verb': 'update',  'object': image}
        with self.mock_oauth():
            response = test_app.post('/api/user/{0}/feed'.format(self.user.username), json.dumps(activity), headers={'Content-Type': 'application/json'})
        image = json.loads(response.body.decode())['object']
        media = MediaEntry.query.filter_by(public_id=image['id']).first()
        assert media.title == title
        assert media.description == description
        assert media.license == license
        assert image['id'] == media.public_id
        assert image['displayName'] == title
        assert image['content'] == description
        assert image['license'] == license

    def test_only_uploaders_post_image(self, test_app):
        """ Test that only uploaders can upload images """
        take_away_privileges(self.user.username, 'uploader')
        data = open(GOOD_JPG, 'rb').read()
        headers = {'Content-Type': 'image/jpeg', 
         'Content-Length': str(len(data))}
        with self.mock_oauth():
            with pytest.raises(AppError) as (excinfo):
                test_app.post('/api/user/{0}/uploads'.format(self.user.username), data, headers=headers)
            assert '403 FORBIDDEN' in excinfo.value.args[0]

    def test_object_endpoint(self, test_app):
        """ Tests that object can be looked up at endpoint """
        response, data = self._upload_image(test_app, GOOD_JPG)
        response, data = self._post_image_to_feed(test_app, data)
        image = data['object']
        assert 'links' in image
        assert 'self' in image['links']
        object_uri = image['links']['self']['href']
        object_uri = object_uri.replace('http://localhost:80', '')
        with self.mock_oauth():
            request = test_app.get(object_uri)
        image = json.loads(request.body.decode())
        entry = MediaEntry.query.filter_by(public_id=image['id']).first()
        assert request.status_code == 200
        assert 'image' in image
        assert 'fullImage' in image
        assert 'pump_io' in image
        assert 'links' in image

    def test_post_comment(self, test_app):
        """ Tests that I can post an comment media """
        response, data = self._upload_image(test_app, GOOD_JPG)
        response, data = self._post_image_to_feed(test_app, data)
        content = 'Hai this is a comment on this lovely picture ^_^'
        activity = {'verb': 'post', 
         'object': {'objectType': 'comment', 
                    'content': content, 
                    'inReplyTo': data['object']}}
        response, comment_data = self._activity_to_feed(test_app, activity)
        assert response.status_code == 200
        media = MediaEntry.query.filter_by(public_id=data['object']['id']).first()
        comment = media.get_comments()[0].comment()
        assert comment.actor == self.user.id
        assert comment.content == content
        assert comment.content == comment_data['object']['content']

    def test_unable_to_post_comment_as_someone_else(self, test_app):
        """ Tests that you're unable to post a comment as someone else. """
        response, data = self._upload_image(test_app, GOOD_JPG)
        response, data = self._post_image_to_feed(test_app, data)
        activity = {'verb': 'post', 
         'object': {'objectType': 'comment', 
                    'content': 'comment commenty comment ^_^', 
                    'inReplyTo': data['object']}}
        headers = {'Content-Type': 'application/json'}
        with self.mock_oauth():
            with pytest.raises(AppError) as (excinfo):
                test_app.post('/api/user/{0}/feed'.format(self.other_user.username), json.dumps(activity), headers=headers)
            assert '403 FORBIDDEN' in excinfo.value.args[0]

    def test_unable_to_update_someone_elses_comment(self, test_app):
        """ Test that you're able to update someoen elses comment. """
        response, data = self._upload_image(test_app, GOOD_JPG)
        response, data = self._post_image_to_feed(test_app, data)
        activity = {'verb': 'post', 
         'object': {'objectType': 'comment', 
                    'content': 'comment commenty comment ^_^', 
                    'inReplyTo': data['object']}}
        headers = {'Content-Type': 'application/json'}
        response, comment_data = self._activity_to_feed(test_app, activity)
        comment = TextComment.query.filter_by(public_id=comment_data['object']['id']).first()
        comment.actor = self.other_user.id
        comment.save()
        comment_data['object']['content'] = 'Yep'
        activity = {'verb': 'update', 
         'object': comment_data['object']}
        with self.mock_oauth():
            with pytest.raises(AppError) as (excinfo):
                test_app.post('/api/user/{0}/feed'.format(self.user.username), json.dumps(activity), headers=headers)
            assert '403 FORBIDDEN' in excinfo.value.args[0]

    def test_profile(self, test_app):
        """ Tests profile endpoint """
        uri = '/api/user/{0}/profile'.format(self.user.username)
        with self.mock_oauth():
            response = test_app.get(uri)
            profile = json.loads(response.body.decode())
            assert response.status_code == 200
            assert profile['preferredUsername'] == self.user.username
            assert profile['objectType'] == 'person'
            assert 'links' in profile

    def test_user(self, test_app):
        """ Test the user endpoint """
        uri = '/api/user/{0}/'.format(self.user.username)
        with self.mock_oauth():
            response = test_app.get(uri)
            user = json.loads(response.body.decode())
            assert response.status_code == 200
            assert user['nickname'] == self.user.username
            assert user['updated'] == self.user.created.isoformat()
            assert user['published'] == self.user.created.isoformat()
            assert 'profile' in response

    def test_whoami_without_login(self, test_app):
        """ Test that whoami endpoint returns error when not logged in """
        with pytest.raises(AppError) as (excinfo):
            response = test_app.get('/api/whoami')
        assert '401 UNAUTHORIZED' in excinfo.value.args[0]

    def test_read_feed(self, test_app):
        """ Test able to read objects from the feed """
        response, image_data = self._upload_image(test_app, GOOD_JPG)
        response, data = self._post_image_to_feed(test_app, image_data)
        uri = '/api/user/{0}/feed'.format(self.active_user.username)
        with self.mock_oauth():
            response = test_app.get(uri)
            feed = json.loads(response.body.decode())
            assert response.status_code == 200
            assert 'displayName' in feed
            assert 'objectTypes' in feed
            assert 'url' in feed
            assert 'links' in feed
            assert 'author' in feed
            assert 'items' in feed
            assert feed['items'][0]['verb'] == 'post'
            assert feed['items'][0]['id'] == data['id']
            assert feed['items'][0]['object']['objectType'] == 'image'
            assert feed['items'][0]['object']['id'] == data['object']['id']
        default_limit = 20
        items_count = default_limit * 2
        for i in range(items_count):
            response, image_data = self._upload_image(test_app, GOOD_JPG)
            self._post_image_to_feed(test_app, image_data)

        items_count += 1
        with self.mock_oauth():
            response = test_app.get(uri)
            feed = json.loads(response.body.decode())
            assert len(feed['items']) == default_limit
        with self.mock_oauth():
            response = test_app.get(uri + '?count=BAD&offset=WORSE')
            feed = json.loads(response.body.decode())
            assert len(feed['items']) == default_limit
        with self.mock_oauth():
            near_the_end = items_count - default_limit / 2
            response = test_app.get(uri + '?offset=%d' % near_the_end)
            feed = json.loads(response.body.decode())
            assert len(feed['items']) < default_limit
        with self.mock_oauth():
            response = test_app.get(uri + '?count=5')
            feed = json.loads(response.body.decode())
            assert len(feed['items']) == 5

    def test_read_another_feed(self, test_app):
        """ Test able to read objects from someone else's feed """
        response, data = self._upload_image(test_app, GOOD_JPG)
        response, data = self._post_image_to_feed(test_app, data)
        self.active_user = self.other_user
        url = '/api/user/{0}/feed'.format(self.user.username)
        with self.mock_oauth():
            response = test_app.get(url)
            feed = json.loads(response.body.decode())
            assert response.status_code == 200
            assert 'displayName' in feed
            assert 'objectTypes' in feed
            assert 'url' in feed
            assert 'links' in feed
            assert 'author' in feed
            assert 'items' in feed
            assert feed['items'][0]['verb'] == 'post'
            assert feed['items'][0]['id'] == data['id']
            assert feed['items'][0]['object']['objectType'] == 'image'
            assert feed['items'][0]['object']['id'] == data['object']['id']

    def test_cant_post_to_someone_elses_feed(self, test_app):
        """ Test that can't post to someone elses feed """
        response, data = self._upload_image(test_app, GOOD_JPG)
        self.active_user = self.other_user
        with self.mock_oauth():
            with pytest.raises(AppError) as (excinfo):
                self._post_image_to_feed(test_app, data)
            assert '403 FORBIDDEN' in excinfo.value.args[0]

    def test_object_endpoint_requestable(self, test_app):
        """ Test that object endpoint can be requested """
        response, data = self._upload_image(test_app, GOOD_JPG)
        response, data = self._post_image_to_feed(test_app, data)
        object_id = data['object']['id']
        with self.mock_oauth():
            response = test_app.get(data['object']['links']['self']['href'])
            data = json.loads(response.body.decode())
            assert response.status_code == 200
            assert object_id == data['id']
            assert 'url' in data
            assert 'links' in data
            assert data['objectType'] == 'image'

    def test_delete_media_by_activity(self, test_app):
        """ Test that an image can be deleted by a delete activity to feed """
        response, data = self._upload_image(test_app, GOOD_JPG)
        response, data = self._post_image_to_feed(test_app, data)
        object_id = data['object']['id']
        activity = {'verb': 'delete', 
         'object': {'id': object_id, 
                    'objectType': 'image'}}
        response = self._activity_to_feed(test_app, activity)[1]
        media = MediaEntry.query.filter_by(public_id=object_id).first()
        assert media is None
        assert 'id' in response
        assert response['verb'] == 'delete'
        assert 'object' in response
        assert response['object']['id'] == object_id
        assert response['object']['objectType'] == 'image'

    def test_delete_comment_by_activity(self, test_app):
        """ Test that a comment is deleted by a delete activity to feed """
        response, data = self._upload_image(test_app, GOOD_JPG)
        response, data = self._post_image_to_feed(test_app, data)
        activity = {'verb': 'post', 
         'object': {'objectType': 'comment', 
                    'content': 'This is a comment.', 
                    'inReplyTo': data['object']}}
        comment = self._activity_to_feed(test_app, activity)[1]
        activity = {'verb': 'delete', 
         'object': {'id': comment['object']['id'], 
                    'objectType': 'comment'}}
        delete = self._activity_to_feed(test_app, activity)[1]
        assert TextComment.query.filter_by(public_id=comment['object']['id']).first() is None
        comment_id = comment['object']['id']
        assert 'id' in delete
        assert delete['verb'] == 'delete'
        assert 'object' in delete
        assert delete['object']['id'] == comment['object']['id']
        assert delete['object']['objectType'] == 'comment'

    def test_edit_comment(self, test_app):
        """ Test that someone can update their own comment """
        response, data = self._upload_image(test_app, GOOD_JPG)
        response, data = self._post_image_to_feed(test_app, data)
        activity = {'verb': 'post', 
         'object': {'objectType': 'comment', 
                    'content': 'This is a comment', 
                    'inReplyTo': data['object']}}
        comment = self._activity_to_feed(test_app, activity)[1]
        activity = {'verb': 'update', 
         'object': {'id': comment['object']['id'], 
                    'content': 'This is my fancy new content string!', 
                    'objectType': 'comment'}}
        comment = self._activity_to_feed(test_app, activity)[1]
        model = TextComment.query.filter_by(public_id=comment['object']['id']).first()
        assert model.content == activity['object']['content']