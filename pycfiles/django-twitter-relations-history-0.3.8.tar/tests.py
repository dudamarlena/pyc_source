# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ramusus/workspace/manufacture/env/src/django-twitter-relations-history/twitter_relations_history/tests.py
# Compiled at: 2013-05-14 12:27:54
from django.test import TestCase
from models import RelationsHistory, NoDeltaForFirstHistory
from twitter_api.factories import UserFactory
import mock
GROUP_ID = 30221121

class TwitterRelationsHistoryMigrationTest(TestCase):

    @mock.patch('twitter_api.models.User')
    def test_relations_history(self, User, *args, **kwargs):
        user = UserFactory()
        User.remote.fetch_followers_ids_for_user.return_value = [1, 2, 3]
        RelationsHistory.objects.update_for_user(user)
        self.assertEqual(RelationsHistory.objects.count(), 1)
        instance1 = RelationsHistory.objects.all()[0]
        self.assertListEqual(instance1.followers_ids, [1, 2, 3])
        self.assertEqual(instance1.followers_count, 3)
        self.assertRaises(NoDeltaForFirstHistory, lambda : instance1.followers_entered_ids)
        self.assertRaises(NoDeltaForFirstHistory, lambda : instance1.followers_left_ids)
        User.remote.fetch_followers_ids_for_user.return_value = [
         1, 2, 3, 4, 5, 6]
        RelationsHistory.objects.update_for_user(user)
        self.assertEqual(RelationsHistory.objects.count(), 2)
        instance2 = RelationsHistory.objects.order_by('-time')[0]
        self.assertListEqual(instance2.followers_ids, [1, 2, 3, 4, 5, 6])
        self.assertListEqual(instance2.followers_entered_ids, [4, 5, 6])
        self.assertListEqual(instance2.followers_left_ids, [])
        self.assertEqual(instance2.followers_count, 6)
        self.assertEqual(instance2.followers_entered_count, 3)
        self.assertEqual(instance2.followers_left_count, 0)
        User.remote.fetch_followers_ids_for_user.return_value = [
         1, 2, 7]
        RelationsHistory.objects.update_for_user(user)
        self.assertEqual(RelationsHistory.objects.count(), 3)
        instance3 = RelationsHistory.objects.order_by('-time')[0]
        self.assertListEqual(instance3.followers_ids, [1, 2, 7])
        self.assertListEqual(instance3.followers_entered_ids, [7])
        self.assertListEqual(instance3.followers_left_ids, [3, 4, 5, 6])
        self.assertEqual(instance3.followers_count, 3)
        self.assertEqual(instance3.followers_entered_count, 1)
        self.assertEqual(instance3.followers_left_count, 4)
        self.assertListEqual(instance3.followers_entered_ids(instance1), [7])
        self.assertListEqual(instance3.followers_left_ids(instance1), [3])
        self.assertEqual(instance3.followers_entered_count(instance1), 1)
        self.assertEqual(instance3.followers_left_count(instance1), 1)