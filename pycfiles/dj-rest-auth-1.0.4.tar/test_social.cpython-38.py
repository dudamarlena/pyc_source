# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/michael/Projects/dj-rest-auth/dj_rest_auth/tests/test_social.py
# Compiled at: 2020-03-22 07:38:27
# Size of source mod 2**32: 13849 bytes
import json, responses
from allauth.socialaccount.models import SocialApp
from allauth.socialaccount.providers.facebook.provider import GRAPH_API_URL
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.test import TestCase
from django.test.utils import override_settings
from rest_framework import status
from .mixins import TestsMixin
try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse
else:

    @override_settings(ROOT_URLCONF='tests.urls')
    class TestSocialAuth(TestsMixin, TestCase):
        USERNAME = 'person'
        PASS = 'person'
        EMAIL = 'person1@world.com'
        REGISTRATION_DATA = {'username':USERNAME, 
         'password1':PASS, 
         'password2':PASS, 
         'email':EMAIL}

        def setUp(self):
            self.init()
            social_app = SocialApp.objects.create(provider='facebook',
              name='Facebook',
              client_id='123123123',
              secret='321321321')
            twitter_social_app = SocialApp.objects.create(provider='twitter',
              name='Twitter',
              client_id='11223344',
              secret='55667788')
            site = Site.objects.get_current()
            social_app.sites.add(site)
            twitter_social_app.sites.add(site)
            self.graph_api_url = GRAPH_API_URL + '/me'
            self.twitter_url = 'http://twitter.com/foobarme'

        @responses.activate
        def test_failed_social_auth(self):
            responses.add((responses.GET),
              (self.graph_api_url),
              body='',
              status=400,
              content_type='application/json')
            payload = {'access_token': 'abc123'}
            self.post((self.fb_login_url), data=payload, status_code=400)

        @responses.activate
        def test_social_auth(self):
            resp_body = {'id':'123123123123', 
             'first_name':'John', 
             'gender':'male', 
             'last_name':'Smith', 
             'link':'https://www.facebook.com/john.smith', 
             'locale':'en_US', 
             'name':'John Smith', 
             'timezone':2, 
             'updated_time':'2014-08-13T10:14:38+0000', 
             'username':'john.smith', 
             'verified':True}
            responses.add((responses.GET),
              (self.graph_api_url),
              body=(json.dumps(resp_body)),
              status=200,
              content_type='application/json')
            users_count = get_user_model().objects.all().count()
            payload = {'access_token': 'abc123'}
            self.post((self.fb_login_url), data=payload, status_code=200)
            self.assertIn('key', self.response.json.keys())
            self.assertEqual(get_user_model().objects.all().count(), users_count + 1)
            self.post((self.fb_login_url), data=payload, status_code=200)
            self.assertIn('key', self.response.json.keys())
            self.assertEqual(get_user_model().objects.all().count(), users_count + 1)

        def _twitter_social_auth(self):
            resp_body = {'id': '123123123123'}
            responses.add((responses.GET),
              'https://api.twitter.com/1.1/account/verify_credentials.json',
              body=(json.dumps(resp_body)),
              status=200,
              content_type='application/json')
            users_count = get_user_model().objects.all().count()
            payload = {'access_token':'abc123', 
             'token_secret':'1111222233334444'}
            self.post((self.tw_login_url), data=payload)
            self.assertIn('key', self.response.json.keys())
            self.assertEqual(get_user_model().objects.all().count(), users_count + 1)
            self.post((self.tw_login_url), data=payload, status_code=200)
            self.assertIn('key', self.response.json.keys())
            self.assertEqual(get_user_model().objects.all().count(), users_count + 1)

        @responses.activate
        @override_settings(SOCIALACCOUNT_AUTO_SIGNUP=True)
        def test_twitter_social_auth(self):
            self._twitter_social_auth()

        @responses.activate
        @override_settings(SOCIALACCOUNT_AUTO_SIGNUP=False)
        def test_twitter_social_auth_without_auto_singup(self):
            self._twitter_social_auth()

        @responses.activate
        def test_twitter_social_auth_request_error(self):
            resp_body = {'id': '123123123123'}
            responses.add((responses.GET),
              'https://api.twitter.com/1.1/account/verify_credentials.json',
              body=(json.dumps(resp_body)),
              status=400,
              content_type='application/json')
            users_count = get_user_model().objects.all().count()
            payload = {'access_token':'abc123', 
             'token_secret':'1111222233334444'}
            self.post((self.tw_login_url), data=payload, status_code=400)
            self.assertNotIn('key', self.response.json.keys())
            self.assertEqual(get_user_model().objects.all().count(), users_count)

        @responses.activate
        def test_twitter_social_auth_no_view_in_context(self):
            resp_body = {'id': '123123123123'}
            responses.add((responses.GET),
              'https://api.twitter.com/1.1/account/verify_credentials.json',
              body=(json.dumps(resp_body)),
              status=400,
              content_type='application/json')
            users_count = get_user_model().objects.all().count()
            payload = {'access_token':'abc123', 
             'token_secret':'1111222233334444'}
            self.post((self.tw_login_no_view_url), data=payload, status_code=400)
            self.assertEqual(get_user_model().objects.all().count(), users_count)

        @responses.activate
        def test_twitter_social_auth_no_adapter(self):
            resp_body = {'id': '123123123123'}
            responses.add((responses.GET),
              'https://api.twitter.com/1.1/account/verify_credentials.json',
              body=(json.dumps(resp_body)),
              status=400,
              content_type='application/json')
            users_count = get_user_model().objects.all().count()
            payload = {'access_token':'abc123', 
             'token_secret':'1111222233334444'}
            self.post((self.tw_login_no_adapter_url), data=payload, status_code=400)
            self.assertEqual(get_user_model().objects.all().count(), users_count)

        @responses.activate
        @override_settings(ACCOUNT_EMAIL_VERIFICATION='mandatory',
          ACCOUNT_EMAIL_REQUIRED=True,
          REST_SESSION_LOGIN=False,
          ACCOUNT_EMAIL_CONFIRMATION_HMAC=False)
        def test_email_clash_with_existing_account(self):
            resp_body = {'id':'123123123123', 
             'first_name':'John', 
             'gender':'male', 
             'last_name':'Smith', 
             'link':'https://www.facebook.com/john.smith', 
             'locale':'en_US', 
             'name':'John Smith', 
             'timezone':2, 
             'updated_time':'2014-08-13T10:14:38+0000', 
             'username':'john.smith', 
             'verified':True, 
             'email':self.EMAIL}
            responses.add((responses.GET),
              (self.graph_api_url),
              body=(json.dumps(resp_body)),
              status=200,
              content_type='application/json')
            self.post((self.register_url), data={}, status_code=400)
            self.post((self.register_url),
              data=(self.REGISTRATION_DATA),
              status_code=201)
            new_user = get_user_model().objects.latest('id')
            self.assertEqual(new_user.username, self.REGISTRATION_DATA['username'])
            email_confirmation = new_user.emailaddress_set.get(email=(self.EMAIL)).emailconfirmation_set.order_by('-created')[0]
            self.post((self.verify_email_url),
              data={'key': email_confirmation.key},
              status_code=(status.HTTP_200_OK))
            self._login()
            self._logout()
            payload = {'access_token': 'abc123'}
            self.post((self.fb_login_url), data=payload, status_code=400)

        @responses.activate
        @override_settings(REST_USE_JWT=True)
        def test_jwt(self):
            resp_body = '{"id":"123123123123","first_name":"John","gender":"male","last_name":"Smith","link":"https:\\/\\/www.facebook.com\\/john.smith","locale":"en_US","name":"John Smith","timezone":2,"updated_time":"2014-08-13T10:14:38+0000","username":"john.smith","verified":true}'
            responses.add((responses.GET),
              (self.graph_api_url),
              body=resp_body,
              status=200,
              content_type='application/json')
            users_count = get_user_model().objects.all().count()
            payload = {'access_token': 'abc123'}
            self.post((self.fb_login_url), data=payload, status_code=200)
            self.assertIn('access_token', self.response.json.keys())
            self.assertIn('user', self.response.json.keys())
            self.assertEqual(get_user_model().objects.all().count(), users_count + 1)


    @override_settings(ROOT_URLCONF='tests.urls')
    class TestSocialConnectAuth(TestsMixin, TestCase):
        USERNAME = 'person'
        PASS = 'person'
        EMAIL = 'person1@world.com'
        REGISTRATION_DATA = {'username':USERNAME, 
         'password1':PASS, 
         'password2':PASS, 
         'email':EMAIL}

        def setUp(self):
            self.init()
            facebook_social_app = SocialApp.objects.create(provider='facebook',
              name='Facebook',
              client_id='123123123',
              secret='321321321')
            twitter_social_app = SocialApp.objects.create(provider='twitter',
              name='Twitter',
              client_id='11223344',
              secret='55667788')
            site = Site.objects.get_current()
            facebook_social_app.sites.add(site)
            twitter_social_app.sites.add(site)
            self.graph_api_url = GRAPH_API_URL + '/me'
            self.twitter_url = 'https://api.twitter.com/1.1/account/verify_credentials.json'

        @responses.activate
        def test_social_connect_no_auth(self):
            responses.add((responses.GET),
              (self.graph_api_url),
              body='',
              status=200,
              content_type='application/json')
            payload = {'access_token': 'abc123'}
            self.post((self.fb_connect_url), data=payload, status_code=403)
            self.post((self.tw_connect_url), data=payload, status_code=403)

        @responses.activate
        def test_social_connect(self):
            self.post((self.register_url),
              data=(self.REGISTRATION_DATA),
              status_code=201)
            resp_body = {'id':'123123123123', 
             'first_name':'John', 
             'gender':'male', 
             'last_name':'Smith', 
             'link':'https://www.facebook.com/john.smith', 
             'locale':'en_US', 
             'name':'John Smith', 
             'timezone':2, 
             'updated_time':'2014-08-13T10:14:38+0000', 
             'username':'john.smith', 
             'verified':True}
            responses.add((responses.GET),
              (self.graph_api_url),
              body=(json.dumps(resp_body)),
              status=200,
              content_type='application/json')
            payload = {'access_token': 'abc123'}
            self.post((self.fb_connect_url), data=payload, status_code=200)
            self.assertIn('key', self.response.json.keys())
            resp_body = {'id': '123123123123'}
            responses.add((responses.GET),
              (self.twitter_url),
              body=(json.dumps(resp_body)),
              status=200,
              content_type='application/json')
            payload = {'access_token':'abc123', 
             'token_secret':'1111222233334444'}
            self.post((self.tw_connect_url), data=payload)
            self.assertIn('key', self.response.json.keys())
            self.get(self.social_account_list_url)
            self.assertEqual(len(self.response.json), 2)
            self.assertEqual(self.response.json[0]['provider'], 'facebook')
            self.assertEqual(self.response.json[1]['provider'], 'twitter')
            facebook_social_account_id = self.response.json[0]['id']
            self.incorrect_disconnect_url = reverse('social_account_disconnect',
              args=[999999999])
            self.post((self.incorrect_disconnect_url), status_code=404)
            self.disconnect_url = reverse('social_account_disconnect',
              args=[facebook_social_account_id])
            self.post((self.disconnect_url), status_code=200)
            self.get(self.social_account_list_url)
            self.assertEqual(len(self.response.json), 1)
            self.assertEqual(self.response.json[0]['provider'], 'twitter')