# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture_old/env/src/django-vkontakte-wall-statistic/vkontakte_wall_statistic/tests.py
# Compiled at: 2015-07-02 10:06:53
from datetime import date, timedelta
from django.core.exceptions import ObjectDoesNotExist
import mock, simplejson as json
from django.test import TestCase
from vkontakte_api.api import VkontakteError
from vkontakte_wall.factories import GroupFactory, PostFactory
from .models import PostStatistic
GROUP_ID = 16297716
POST_ID = '-16297716_262399'
POST_REACH_ID = '-16297716_400626'

def get_error(*args, **kwargs):
    return [
     {'error': {'error_code': 7, 'error_msg': 'Permission to perform this action is denied', 'request_params': [{'key': 'oauth', 'value': '1'}, {'key': 'method', 'value': 'stats.getPostStats'},
                                   {'key': 'timestamp', 'value': '1430579937'}, {'key': 'date_from', 'value': '2015-04-30'}, {'key': 'post_id', 'value': '262399'}, {'key': 'date_to', 'value': '2015-05-02'}, {'key': 'group_id', 'value': '22130230'}]}}]


class VkontakteWallStatisticTest(TestCase):

    def test_parse_post(self):
        response = '{"age": [{"reach": 2153, "value": "12-18"},\n                  {"reach": 1113, "value": "18-21"},\n                  {"reach": 984, "value": "21-24"},\n                  {"reach": 948, "value": "24-27"},\n                  {"reach": 642, "value": "27-30"},\n                  {"reach": 555, "value": "30-35"},\n                  {"reach": 363, "value": "35-45"},\n                  {"reach": 357, "value": "45-100"}],\n                 "cities": [{"name": "Донецк", "reach": 38, "value": 223},\n                  {"name": "Воронеж", "reach": 25, "value": 1057},\n                  {"name": "Рио", "reach": 18, "value": 136},\n                  {"name": "Тируванамалай", "reach": 14, "value": 427}],\n                 "countries": [{"code": "RU",\n                   "name": "Россия",\n                   "reach": 6548,\n                   "value": 1},\n                  {"code": "US", "name": "США", "reach": 15, "value": 9}],\n                 "day": "2014-02-27",\n                 "link_clicks": 10,\n                 "reach": 8243,\n                 "reach_subscribers": 357,\n                 "sex": [{"reach": 4420, "value": "f"}, {"reach": 3823, "value": "m"}],\n                 "sex_age": [{"reach": 1141, "value": "f;12-18"},\n                  {"reach": 464, "value": "f;18-21"},\n                  {"reach": 513, "value": "f;21-24"},\n                  {"reach": 487, "value": "f;24-27"},\n                  {"reach": 355, "value": "f;27-30"},\n                  {"reach": 337, "value": "f;30-35"},\n                  {"reach": 243, "value": "f;35-45"},\n                  {"reach": 186, "value": "f;45-100"},\n                  {"reach": 1012, "value": "m;12-18"},\n                  {"reach": 649, "value": "m;18-21"},\n                  {"reach": 471, "value": "m;21-24"},\n                  {"reach": 461, "value": "m;24-27"},\n                  {"reach": 287, "value": "m;27-30"},\n                  {"reach": 218, "value": "m;30-35"},\n                  {"reach": 120, "value": "m;35-45"},\n                  {"reach": 171, "value": "m;45-100"}]}'
        instance = PostStatistic(post=PostFactory())
        instance.parse(json.loads(response))
        instance.save()
        self.assertEqual(instance.date, date(2014, 2, 27))
        self.assertEqual(instance.reach, 8243)
        self.assertEqual(instance.reach_subscribers, 357)
        self.assertEqual(instance.link_clicks, 10)
        self.assertEqual(instance.reach_males, 3823)
        self.assertEqual(instance.reach_females, 4420)
        self.assertEqual(instance.reach_age_18, 2153)
        self.assertEqual(instance.reach_age_18_21, 1113)
        self.assertEqual(instance.reach_age_21_24, 984)
        self.assertEqual(instance.reach_age_24_27, 948)
        self.assertEqual(instance.reach_age_27_30, 642)
        self.assertEqual(instance.reach_age_30_35, 555)
        self.assertEqual(instance.reach_age_35_45, 363)
        self.assertEqual(instance.reach_age_45, 357)
        self.assertEqual(instance.reach_males_age_18, 1012)
        self.assertEqual(instance.reach_males_age_18_21, 649)
        self.assertEqual(instance.reach_males_age_21_24, 471)
        self.assertEqual(instance.reach_males_age_24_27, 461)
        self.assertEqual(instance.reach_males_age_27_30, 287)
        self.assertEqual(instance.reach_males_age_30_35, 218)
        self.assertEqual(instance.reach_males_age_35_45, 120)
        self.assertEqual(instance.reach_males_age_45, 171)
        self.assertEqual(instance.reach_females_age_18, 1141)
        self.assertEqual(instance.reach_females_age_18_21, 464)
        self.assertEqual(instance.reach_females_age_21_24, 513)
        self.assertEqual(instance.reach_females_age_24_27, 487)
        self.assertEqual(instance.reach_females_age_27_30, 355)
        self.assertEqual(instance.reach_females_age_30_35, 337)
        self.assertEqual(instance.reach_females_age_35_45, 243)
        self.assertEqual(instance.reach_females_age_45, 186)

    def test_fetch_statistic(self):
        group = GroupFactory(remote_id=GROUP_ID)
        post = PostFactory(remote_id=POST_ID, owner=group)
        self.assertEqual(PostStatistic.objects.count(), 0)
        post.fetch_statistic(date_from=date.today() - timedelta(2), date_to=date.today())
        self.assertGreater(PostStatistic.objects.count(), 0)
        stat = PostStatistic.objects.all()[0]
        self.assertIsInstance(stat.date, date)
        self.assertGreater(stat.reach, 0)

    @mock.patch('vkontakte.api.API._request', side_effect=lambda *a, **kw: (200, {}))
    @mock.patch('vkontakte.api._json_iterparse', side_effect=get_error)
    def test_fetch_statistic_error(self, *args, **kwargs):
        group = GroupFactory(remote_id=GROUP_ID)
        post = PostFactory(remote_id=POST_ID, owner=group)
        self.assertEqual(PostStatistic.objects.count(), 0)
        with self.assertRaises(VkontakteError):
            post.fetch_statistic(date_from=date.today() - timedelta(2), date_to=date.today())

    def test_fetch_post_reach(self):
        group = GroupFactory(remote_id=GROUP_ID)
        post = PostFactory(remote_id=POST_REACH_ID, owner=group)
        with self.assertRaises(ObjectDoesNotExist):
            post.reach
        post.fetch_reach()
        post = post.__class__.objects.get(pk=post.pk)
        self.assertGreaterEqual(post.reach.hide, 0)
        self.assertGreaterEqual(post.reach.join_group, 0)
        self.assertGreaterEqual(post.reach.links, 0)
        self.assertGreaterEqual(post.reach.reach_subscribers, 0)
        self.assertGreaterEqual(post.reach.reach_total, 0)
        self.assertGreaterEqual(post.reach.report, 0)
        self.assertGreaterEqual(post.reach.to_group, 0)
        self.assertGreaterEqual(post.reach.unsubscribe, 0)