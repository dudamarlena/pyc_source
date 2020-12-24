# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\Dylan\projects\simple_django_twitter_auth_example\django_twitter_auth\tests\test_models.py
# Compiled at: 2015-03-28 15:38:13
from django.test import TestCase
from django_twitter_auth.models import TwitterProfile
from django.contrib.auth import get_user_model
User = get_user_model()
from mock import patch

class TwitterProfileModelTest(TestCase):

    def setUp(self):
        patcher = patch('django_twitter_auth.models.Twython')
        self.mock_Twython = patcher.start()
        self.addCleanup(patcher.stop)
        self.mock_Twython_instance = self.mock_Twython.return_value
        self.mock_Twython_instance.verify_credentials.return_value = {'screen_name': 'YouveGotFox'}

    def test_username_retrieved_and_stored_on_first_save(self):
        profile = TwitterProfile(OAUTH_TOKEN='oauthtoken', OAUTH_TOKEN_SECRET='oauthtokensecret')
        profile.save()
        self.assertEqual(profile.username, 'YouveGotFox')

    def test_username_only_retrieved_on_first_save(self):
        profile = TwitterProfile(OAUTH_TOKEN='oauthtoken', OAUTH_TOKEN_SECRET='oauthtokensecret')
        profile.save()
        profile.save()
        self.assertEqual(len(self.mock_Twython.call_args_list), 1)

    def test_User_created_on_save_and_tied_to_TwitterProfile(self):
        profile = TwitterProfile(OAUTH_TOKEN='oauthtoken', OAUTH_TOKEN_SECRET='oauthtokensecret')
        profile.save()
        self.assertTrue(profile.user)
        user = User.objects.first()
        self.assertEqual(profile.user, user)

    def test_User_only_created_on_first_save(self):
        profile = TwitterProfile(OAUTH_TOKEN='oauthtoken', OAUTH_TOKEN_SECRET='oauthtokensecret')
        profile.save()
        user = profile.user
        profile.save()
        users = User.objects.count()
        self.assertTrue(users == 1)
        self.assertEqual(user, profile.user)

    def test_OAuth2_tokens_updated_if_User_with_username_found(self):
        """
                A user could have revoked access, and then logged
                back in. If so, the tokens will be new. But we
                shouldn't create a new TwitterProfile or User.
                """
        profile_1 = TwitterProfile(OAUTH_TOKEN='oauthtoken', OAUTH_TOKEN_SECRET='oauthtokensecret')
        profile_1.save()
        profile_1_id = profile_1.pk
        profile_2 = TwitterProfile(OAUTH_TOKEN='NEWoauthtoken', OAUTH_TOKEN_SECRET='NEWoauthtokensecret')
        profile_2.save()
        profile_1 = TwitterProfile.objects.get(pk=profile_1_id)
        self.assertEqual(profile_1.OAUTH_TOKEN, 'NEWoauthtoken')
        self.assertEqual(profile_1.OAUTH_TOKEN_SECRET, 'NEWoauthtokensecret')
        self.assertTrue(TwitterProfile.objects.count() == 1)