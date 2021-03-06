# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture_old/env/src/django-odnoklassniki-discussions/odnoklassniki_discussions/tests.py
# Compiled at: 2015-10-27 19:37:17
from datetime import datetime, timedelta
import simplejson as json
from django.test import TestCase
from django.utils import timezone
from odnoklassniki_groups.models import Group
from odnoklassniki_api.models import OdnoklassnikiContentError
from .factories import CommentFactory, DiscussionFactory, GroupFactory, UserFactory
from .models import Comment, Discussion, User
GROUP1_ID = 47241470410797
GROUP_DISCUSSION1_ID = 62190641299501
GROUP2_ID = 53038939046008
GROUP_DISCUSSION2_ID = 62465446084728
GROUPDISCUSSION_POLL_ID = 64079715639311
GROUP3_ID = 53008333209712
GROUP_DISCUSSION_WITH_MANY_COMMENTS1_ID = 62503929662320
GROUP_DISCUSSION_WITH_MANY_COMMENTS2_ID = 62458153487216
GROUP_DISCUSSION_WITH_MANY_LIKES1_ID = 62521829903216
GROUP_COMMENT_WITH_MANY_LIKES1_DISCUSSION_ID = 62425402395504
GROUP_COMMENT_WITH_MANY_LIKES1_ID = 'MTM5NDAwMzI5NjE2MzotNjAyOToxMzk0MDAzMjk2MTYzOjYyNDI1NDAyMzk1NTA0OjE='
GROUP4_ID = 50752764379349
GROUP4_DISCUSSION_WITH_GROUP_COMMENTS_ID = 62520921350357
GROUP_DISCUSSION_GHOST = 62671523553304

class OdnoklassnikiDiscussionsTest(TestCase):

    def test_fetch_group_discussions_empty_result(self):
        group = GroupFactory(id=57110225354790)
        discussions = group.fetch_discussions(all=True, after=datetime(2014, 9, 18, 16, 13).replace(tzinfo=timezone.utc))
        self.assertGreaterEqual(discussions.count(), 48)
        self.assertEqual(discussions.count(), Discussion.objects.count())
        self.assertEqual(discussions.count(), group.discussions.count())

    def test_fetch_group_discussions(self):
        group = GroupFactory(id=GROUP3_ID)
        self.assertEqual(Discussion.objects.count(), 0)
        discussions = Discussion.remote.fetch_group(group=group)
        self.assertGreaterEqual(discussions.count(), 11)
        self.assertEqual(discussions.count(), Discussion.objects.count())
        self.assertEqual(discussions.count(), group.discussions.count())
        discussions = Discussion.remote.fetch_group(group=group, all=True)
        self.assertGreater(discussions.count(), 200)
        self.assertEqual(discussions.count(), Discussion.objects.count())
        self.assertEqual(discussions.count(), group.discussions.count())
        after = timezone.now() - timedelta(90)
        discussions_after = Discussion.remote.fetch_group(group=group, all=True, after=after)
        self.assertLess(discussions_after.count(), discussions.count())
        self.assertEqual(discussions_after.filter(date__lt=after).count(), 0)
        before = discussions_after.order_by('date')[(discussions_after.count() / 2)].date
        discussions_before = Discussion.remote.fetch_group(group=group, all=True, after=after, before=before)
        self.assertLess(discussions_before.count(), discussions_after.count())
        self.assertEqual(discussions_before.filter(date__gt=before).count(), 0)

    def test_fetch_group_discussions_less(self):
        group = GroupFactory(id=51893792211123)
        self.assertEqual(Discussion.objects.count(), 0)
        discussions = Discussion.remote.fetch_group(group=group, all=True)
        self.assertGreaterEqual(discussions.count(), 200)

    def test_fetch_discussion_likes(self):
        discussion = DiscussionFactory(id=GROUP_DISCUSSION_WITH_MANY_LIKES1_ID, object_type='GROUP_TOPIC')
        users_initial = User.objects.count()
        users = discussion.fetch_likes(all=True)
        self.assertGreater(discussion.likes_count, 980)
        self.assertEqual(discussion.likes_count, users.count())
        self.assertEqual(discussion.likes_count, User.objects.count() - users_initial)
        self.assertEqual(discussion.likes_count, discussion.like_users.count())

    def test_fetch_comment_likes(self):
        discussion = DiscussionFactory(id=GROUP_COMMENT_WITH_MANY_LIKES1_DISCUSSION_ID, object_type='GROUP_TOPIC')
        comment = CommentFactory(id=GROUP_COMMENT_WITH_MANY_LIKES1_ID, object_type='GROUP_TOPIC', discussion=discussion)
        users_initial = User.objects.count()
        users = comment.fetch_likes(all=True)
        self.assertGreater(comment.likes_count, 19)
        self.assertEqual(comment.likes_count, users.count())
        self.assertEqual(comment.likes_count, User.objects.count() - users_initial)
        self.assertEqual(comment.likes_count, comment.like_users.count())

    def test_save_comment_during_fetching_likes(self):
        discussion = DiscussionFactory(id=GROUP_COMMENT_WITH_MANY_LIKES1_DISCUSSION_ID, object_type='GROUP_TOPIC')
        comment = CommentFactory(object_type='GROUP_TOPIC', discussion=discussion)
        comment.author_id = 47241470410797
        comment.author_type = ''
        comment.save()

    def test_fetch_discussion_comments_after_before(self):
        discussion = DiscussionFactory(id=GROUP_DISCUSSION_WITH_MANY_COMMENTS1_ID, object_type='GROUP_TOPIC')
        self.assertEqual(Comment.objects.count(), 0)
        comments = discussion.fetch_comments()
        self.assertEqual(comments.count(), 100)
        self.assertEqual(comments.count(), discussion.comments_count)
        self.assertEqual(comments.count(), Comment.objects.count())
        self.assertEqual(comments.count(), discussion.comments.count())
        after = datetime(2014, 5, 1, 8, 34, 8, tzinfo=timezone.utc)
        comments_after = discussion.fetch_comments(all=True, after=after)
        self.assertGreater(comments_after.count(), 200)
        self.assertEqual(comments_after.filter(date__lt=after).count(), 0)
        before = comments_after[100].date
        comments_before = discussion.fetch_comments(all=True, after=after, before=before)
        self.assertLess(comments_before.count(), comments_after.count())
        self.assertEqual(comments_before.filter(date__lt=after).filter(date__gt=before).count(), 0)

    def test_fetch_discussion_comments_all(self):
        discussion = DiscussionFactory(id=GROUP_DISCUSSION_WITH_MANY_COMMENTS1_ID, object_type='GROUP_TOPIC')
        comments = discussion.fetch_comments(all=True)
        self.assertGreater(comments.count(), 3500)
        self.assertEqual(comments.count(), discussion.comments_count)
        self.assertEqual(comments.count(), Comment.objects.count())
        self.assertEqual(comments.count(), discussion.comments.count())

    def test_fetch_discussion_comments_wrong(self):
        discussion = DiscussionFactory(id=GROUP_DISCUSSION_WITH_MANY_COMMENTS2_ID, object_type='GROUP_TOPIC')
        self.assertEqual(Comment.objects.count(), 0)
        comments = discussion.fetch_comments(all=True)
        self.assertGreater(comments.count(), 1900)

    def test_fetch_discussion_comments_by_group(self):
        group = GroupFactory(id=GROUP4_ID)
        discussion = DiscussionFactory(owner=group, id=GROUP4_DISCUSSION_WITH_GROUP_COMMENTS_ID, object_type='GROUP_TOPIC')
        self.assertEqual(Comment.objects.count(), 0)
        comments = discussion.fetch_comments(all=True)
        comment = comments.get(author_id=group.id)
        self.assertNotEqual(Comment.objects.count(), 0)
        self.assertEqual(comment.owner, group)
        self.assertEqual(comment.author, group)

    def test_fetch_discussion(self):
        self.assertEqual(Discussion.objects.count(), 0)
        instance = Discussion.remote.fetch_one(id=GROUP_DISCUSSION1_ID, type='GROUP_TOPIC')
        self.assertEqual(Discussion.objects.count(), 1)
        self.assertEqual(instance.id, GROUP_DISCUSSION1_ID)
        self.assertEqual(instance.author, User.objects.get(pk=163873406852))
        self.assertEqual(instance.owner, Group.objects.get(pk=GROUP1_ID))
        self.assertIsInstance(instance.entities, dict)
        self.assertGreaterEqual(instance.likes_count, 3)
        self.assertEqual(instance.title, 'Кока-Кола  один из спонсоров  Олимпиады в Сочи.  Хотелось бы  видеть фото- и видео-  репортажи с Эстафеты  олимпийского огня !')
        instance = Discussion.remote.fetch_one(id=GROUP_DISCUSSION2_ID, type='GROUP_TOPIC')
        self.assertEqual(Discussion.objects.count(), 2)
        self.assertEqual(instance.id, GROUP_DISCUSSION2_ID)
        self.assertEqual(instance.author, instance.owner)
        self.assertEqual(instance.owner, Group.objects.get(pk=GROUP2_ID))
        self.assertIsInstance(instance.entities, dict)
        self.assertGreaterEqual(instance.reshares_count, 1)
        self.assertGreaterEqual(instance.likes_count, 36)
        self.assertGreaterEqual(instance.comments_count, 3)
        self.assertEqual(instance.title, 'PHP - это действительно просто. Добавьте возможность взаимодействия вашего сайта на PHP с Одноклассниками за 3 простых шага.')
        self.assertIsInstance(instance.entities['themes'][0]['images'][0], dict)
        instance = Discussion.remote.fetch_one(id=64312515425727, type='GROUP_TOPIC')

    def test_fetch_discussion_with_poll(self):
        self.assertEqual(Discussion.objects.count(), 0)
        instance = Discussion.remote.fetch_one(id=GROUPDISCUSSION_POLL_ID, type='GROUP_TOPIC')
        self.assertEqual(Discussion.objects.count(), 1)
        self.assertEqual(instance.id, GROUPDISCUSSION_POLL_ID)
        self.assertIsInstance(instance.entities, dict)
        self.assertGreaterEqual(instance.votes_count, 115)
        self.assertEqual(instance.question, 'Понравилась ли вам Неделя кошек из приютов?')

    def test_fetch_mediatopics(self):
        instances = Discussion.remote.fetch_mediatopics([GROUP_DISCUSSION2_ID, GROUP_DISCUSSION1_ID])
        self.assertEqual(Discussion.objects.count(), 2)
        instance = instances.get(pk=GROUP_DISCUSSION1_ID)
        self.assertEqual(instance.author, User.objects.get(pk=163873406852))
        self.assertEqual(instance.owner, Group.objects.get(pk=GROUP1_ID))
        self.assertIsInstance(instance.date, datetime)
        self.assertGreaterEqual(instance.likes_count, 3)
        self.assertEqual(instance.title, 'Кока-Кола  один из спонсоров  Олимпиады в Сочи.  Хотелось бы  видеть фото- и видео-  репортажи с Эстафеты  олимпийского огня !')
        instance = instances.get(pk=GROUP_DISCUSSION2_ID)
        self.assertEqual(instance.author, instance.owner)
        self.assertEqual(instance.owner, Group.objects.get(pk=GROUP2_ID))
        self.assertIsInstance(instance.date, datetime)
        self.assertGreaterEqual(instance.reshares_count, 1)
        self.assertGreaterEqual(instance.likes_count, 36)
        self.assertGreaterEqual(instance.comments_count, 3)
        self.assertEqual(instance.title, 'PHP - это действительно просто. Добавьте возможность взаимодействия вашего сайта на PHP с Одноклассниками за 3 простых шага.')
        self.assertEqual(instance.entities, None)
        return

    def test_refresh_discussion(self):
        instance = Discussion.remote.fetch_one(id=GROUP_DISCUSSION1_ID, type='GROUP_TOPIC')
        self.assertNotEqual(instance.title, 'temp')
        title = instance.title
        instance.title = 'temp'
        instance.save()
        self.assertEqual(instance.title, 'temp')
        instance.refresh()
        self.assertEqual(instance.title, title)
        with self.assertRaises(OdnoklassnikiContentError):
            instance = DiscussionFactory(id=GROUP_DISCUSSION_GHOST)
            instance.refresh()

    def test_parse_discussion(self):
        response = '{"discussion": {\n                 "attrs": {"flags": "c,l,s"},\n                 "creation_date": "2013-10-12 14:29:26",\n                 "last_activity_date": "2013-10-12 14:29:26",\n                 "last_user_access_date": "2013-10-12 14:29:26",\n                 "like_count": 1,\n                 "liked_it": false,\n                 "message": "Topic in the {group:47241470410797}Кока-Кола{group} group",\n                 "new_comments_count": 0,\n                 "object_id": "62190641299501",\n                 "object_type": "GROUP_TOPIC",\n                 "owner_uid": "163873406852",\n                 "ref_objects": [{"id": "47241470410797",\n                                   "type": "GROUP"}],\n                 "title": "Кока-Кола  один из спонсоров  Олимпиады в Сочи.  Хотелось бы  видеть фото- и видео-  репортажи с Эстафеты  олимпийского огня !",\n                 "total_comments_count": 137},\n                 "entities": {"groups": [{"main_photo": {"id": "507539161645",\n                                                    "pic128x128": "http://itd0.mycdn.me/getImage?photoId=507539161645&photoType=23&viewToken=a6WsJVtOYvuLUbMSMQVMGg",\n                                                    "pic50x50": "http://groupava2.mycdn.me/getImage?photoId=507539161645&photoType=4&viewToken=a6WsJVtOYvuLUbMSMQVMGg",\n                                                    "pic640x480": "http://dg54.mycdn.me/getImage?photoId=507539161645&photoType=0&viewToken=a6WsJVtOYvuLUbMSMQVMGg"},\n                                    "name": "Кока-Кола",\n                                    "uid": "47241470410797"}],\n                       "themes": [{"id": "62190641299501",\n                                    "title": "Кока-Кола  один из спонсоров  Олимпиады в Сочи.  Хотелось бы  видеть фото- и видео-  репортажи с Эстафеты  олимпийского огня !"}],\n                       "users": [{"first_name": "Любовь",\n                                   "gender": "female",\n                                   "last_name": "Гуревич",\n                                   "pic128x128": "http://umd2.mycdn.me/getImage?photoId=432276861828&photoType=6&viewToken=P_qCWfSCiGBGVoiqWQMgsw",\n                                   "pic50x50": "http://i508.mycdn.me/getImage?photoId=432276861828&photoType=4&viewToken=P_qCWfSCiGBGVoiqWQMgsw",\n                                   "pic640x480": "http://uld9.mycdn.me/getImage?photoId=432276861828&photoType=0&viewToken=P_qCWfSCiGBGVoiqWQMgsw",\n                                   "uid": "163873406852"}]}}'
        instance = Discussion()
        instance.parse(json.loads(response))
        instance.save()
        self.assertEqual(instance.id, 62190641299501)
        self.assertEqual(instance.object_type, 'GROUP_TOPIC')
        self.assertEqual(instance.message, 'Topic in the {group:47241470410797}Кока-Кола{group} group')
        self.assertEqual(instance.title, 'Кока-Кола  один из спонсоров  Олимпиады в Сочи.  Хотелось бы  видеть фото- и видео-  репортажи с Эстафеты  олимпийского огня !')
        self.assertEqual(instance.new_comments_count, 0)
        self.assertEqual(instance.comments_count, 137)
        self.assertEqual(instance.likes_count, 1)
        self.assertEqual(instance.liked_it, False)
        self.assertEqual(instance.author, User.objects.get(pk=163873406852))
        self.assertEqual(instance.owner, Group.objects.get(pk=47241470410797))
        self.assertIsInstance(instance.last_activity_date, datetime)
        self.assertIsInstance(instance.last_user_access_date, datetime)
        self.assertIsInstance(instance.date, datetime)
        self.assertIsInstance(instance.entities, dict)
        self.assertIsInstance(instance.attrs, dict)

    def test_parse_comment(self):
        response = '{"attrs": {"flags": "l,s"},\n            "author_id": "538901295641",\n            "date": "2014-04-11 12:53:02",\n            "id": "MTM5NzIwNjM4MjQ3MTotMTU5NDE6MTM5NzIwNjM4MjQ3MTo2MjUwMzkyOTY2MjMyMDox",\n            "like_count": 123,\n            "liked_it": false,\n            "reply_to_comment_id": "MTM5NzIwNjMzNjI2MTotODE0MzoxMzk3MjA2MzM2MjYxOjYyNTAzOTI5NjYyMzIwOjE=",\n            "reply_to_id": "134519031824",\n            "text": "наверное и я так буду делать!",\n            "type": "ACTIVE_MESSAGE"}'
        comment = CommentFactory(id='MTM5NzIwNjMzNjI2MTotODE0MzoxMzk3MjA2MzM2MjYxOjYyNTAzOTI5NjYyMzIwOjE=')
        author = UserFactory(id=134519031824)
        discussion = DiscussionFactory()
        instance = Comment(discussion=discussion)
        instance.parse(json.loads(response))
        instance.save()
        self.assertEqual(instance.id, 'MTM5NzIwNjM4MjQ3MTotMTU5NDE6MTM5NzIwNjM4MjQ3MTo2MjUwMzkyOTY2MjMyMDox')
        self.assertEqual(instance.object_type, 'ACTIVE_MESSAGE')
        self.assertEqual(instance.text, 'наверное и я так буду делать!')
        self.assertEqual(instance.likes_count, 123)
        self.assertEqual(instance.liked_it, False)
        self.assertEqual(instance.author, User.objects.get(pk=538901295641))
        self.assertEqual(instance.reply_to_comment, comment)
        self.assertEqual(instance.reply_to_author, User.objects.get(pk=134519031824))
        self.assertIsInstance(instance.date, datetime)
        self.assertIsInstance(instance.attrs, dict)