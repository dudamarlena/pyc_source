# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture/env/src/django-twitter-api/twitter_api/tests.py
# Compiled at: 2016-02-11 09:18:14
import time
from datetime import datetime, timedelta
from django.test import TestCase
from django.utils import six, timezone
from django.utils.timezone import is_aware
import mock
from oauth_tokens.factories import UserCredentialsFactory
import tweepy
from .api import api_call, TwitterApi, TwitterError
from .factories import UserFactory, StatusFactory
from .models import User, Status
from .parser import get_replies
STATUS_ID = 327926550815207424
USER_ID = 813286
USER_SCREEN_NAME = 'BarackObama'
USER1_ID = 18807761
USER1_SCREEN_NAME = 'voronezh'
STATUS_MANY_REPLIES_ID = 538755896063832064
STATUS_MANY_RETWEETS_ID = 329231054282055680

class TwitterApiTest(TestCase):

    def raise_rate_limit(*a, **kw):
        raise tweepy.TweepError([{'message': 'Rate limit exceeded', 'code': 88}])

    def get_rate_limit_status(*a, **kw):
        return {'rate_limit_context': {'access_token': ''}, 'resources': {'trends': {'/trends/available': {'limit': 15, 'remaining': 0, 
                                                          'reset': time.time() + 100}}}}

    @mock.patch('tweepy.API.trends_available', side_effect=raise_rate_limit)
    @mock.patch('tweepy.API.rate_limit_status', side_effect=get_rate_limit_status)
    @mock.patch('twitter_api.api.TwitterApi.sleep_repeat_call')
    def test_rate_limit(self, sleep, rate_limit_status, trends_available):
        api_call('trends_available')
        self.assertTrue(trends_available.called)
        self.assertTrue(rate_limit_status.called)
        self.assertTrue(sleep.called)
        self.assertEqual(sleep.call_count, 1)
        self.assertGreater(sleep.call_args_list[0], 98)

    def test_user_screen_name_unique(self):
        user_wrong = UserFactory(pk=102732226, screen_name=USER_SCREEN_NAME)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.filter(pk=user_wrong.pk).count(), 1)
        user = User.remote.fetch(USER_SCREEN_NAME)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.filter(pk=user.pk).count(), 1)

    def test_request_error(self):
        with self.assertRaises(TwitterError):
            response = api_call('get_status')

    def test_api_instance_singleton(self):
        self.assertEqual(id(TwitterApi()), id(TwitterApi()))

    def test_request(self):
        response = api_call('get_status', STATUS_ID)
        self.assertEqual(response.text, '@mrshoranweyhey Thanks for the love! How about a follow for a follow? :) ^LF')
        self.assertEqual(response.source_url, 'http://www.exacttarget.com/social')
        response = api_call('get_user', USER_SCREEN_NAME)
        self.assertEqual(response.id, USER_ID)
        self.assertEqual(response.name, 'Barack Obama')

    def test_tweepy_properties(self):
        instance = User.remote.fetch(USER_ID)
        self.assertEqual(instance.screen_name, USER_SCREEN_NAME)
        self.assertIsInstance(instance.tweepy, tweepy.models.User)
        self.assertEqual(instance.tweepy.id_str, str(USER_ID))

    def test_fetch_negative_friends_count(self):
        user = User.remote.fetch(961050745)
        user.fetch_statuses(count=100)

    def test_fetch_status(self):
        self.assertEqual(Status.objects.count(), 0)
        instance = Status.remote.fetch(STATUS_ID)
        self.assertEqual(Status.objects.count(), 2)
        self.assertEqual(instance.id, STATUS_ID)
        self.assertEqual(instance.source, 'SocialEngage')
        self.assertEqual(instance.source_url, 'http://www.exacttarget.com/social')
        self.assertEqual(instance.text, '@mrshoranweyhey Thanks for the love! How about a follow for a follow? :) ^LF')
        self.assertEqual(instance.in_reply_to_status_id, 327912852486762497)
        self.assertEqual(instance.in_reply_to_user_id, 1323314442)
        self.assertEqual(instance.in_reply_to_status, Status.objects.get(id=327912852486762497))
        self.assertEqual(instance.in_reply_to_user, User.objects.get(id=1323314442))
        self.assertIsInstance(instance.created_at, datetime)
        self.assertTrue(is_aware(instance.created_at))

    def test_fetch_user(self):
        instance = User.remote.fetch(USER_ID)
        self.assertEqual(instance.screen_name, USER_SCREEN_NAME)
        self.assertEqual(instance.id, USER_ID)
        self.assertEqual(instance.name, 'Barack Obama')
        self.assertEqual(instance.location, 'Washington, DC')
        self.assertEqual(instance.verified, True)
        self.assertEqual(instance.lang, 'en')
        self.assertGreater(instance.followers_count, 30886141)
        self.assertGreater(instance.friends_count, 600000)
        self.assertGreater(instance.listed_count, 192107)
        instance1 = User.remote.fetch(USER_SCREEN_NAME)
        self.assertEqual(instance.name, instance1.name)
        self.assertEqual(User.objects.count(), 1)

    def test_fetch_user_statuses(self):
        instance = UserFactory(id=USER_ID)
        self.assertEqual(Status.objects.count(), 0)
        instances = instance.fetch_statuses(count=30)
        self.assertEqual(instances.count(), 30)
        self.assertEqual(instances.count(), Status.objects.filter(author=instance).count())
        instances = instance.fetch_statuses(all=True, exclude_replies=True)
        self.assertGreater(instances.count(), 3100)
        self.assertLess(instances.count(), 4000)
        self.assertEqual(instances.count(), Status.objects.filter(author=instance).count())
        after = timezone.now() - timedelta(20)
        instances_after = instance.fetch_statuses(all=True, after=after)
        self.assertLess(instances_after.count(), instances.count())
        self.assertEqual(instances_after.filter(created_at__lt=after).count(), 0)
        before = instances_after.order_by('created_at')[(instances_after.count() / 2)].created_at
        instances_before = instance.fetch_statuses(all=True, after=after, before=before)
        self.assertLess(instances_before.count(), instances_after.count())
        self.assertEqual(instances_before.filter(created_at__gt=before).count(), 0)

    def test_fetch_user_followers(self):
        instance = UserFactory(id=USER1_ID)
        self.assertEqual(User.objects.count(), 1)
        instances = instance.fetch_followers(all=True)
        self.assertGreater(instances.count(), 870)
        self.assertLess(instances.count(), 2000)
        self.assertIsInstance(instances[0], User)
        self.assertEqual(instances.count(), User.objects.count() - 1)

    def test_fetch_user_followers_ids(self):
        instance = UserFactory(id=USER1_ID)
        self.assertEqual(User.objects.count(), 1)
        ids = instance.get_followers_ids(all=True)
        self.assertGreater(len(ids), 1000)
        self.assertLess(len(ids), 2000)
        self.assertIsInstance(ids[0], six.integer_types)
        self.assertEqual(User.objects.count(), 1)

    def test_fetch_status_retweets(self):
        instance = StatusFactory(id=STATUS_MANY_RETWEETS_ID)
        self.assertEqual(Status.objects.count(), 1)
        instances = instance.fetch_retweets()
        self.assertGreaterEqual(instances.count(), 6)
        self.assertEqual(instances.count(), Status.objects.count() - 1)

    def test_get_replies(self):
        """
            Check what ids[0] < ids[1] < ids[2] ...
            this also check what there is no duplicates
        """
        status = Status.remote.fetch(STATUS_MANY_REPLIES_ID)
        ids = get_replies(status)
        self.assertListEqual(ids, sorted(ids))
        self.assertEqual(len(ids), len(set(ids)))

    def test_status_fetch_replies(self):
        status = Status.remote.fetch(STATUS_MANY_REPLIES_ID)
        self.assertEqual(Status.objects.count(), 1)
        self.assertEqual(status.replies_count, None)
        replies = status.fetch_replies()
        self.assertGreater(replies.count(), 200)
        self.assertEqual(replies.count(), status.replies_count)
        self.assertEqual(replies.count(), Status.objects.count() - 1)
        self.assertEqual(replies[0].in_reply_to_status, status)
        status = Status.remote.fetch(STATUS_MANY_REPLIES_ID)
        self.assertEqual(replies.count(), status.replies_count)
        return