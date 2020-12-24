# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture/env/src/django-vkontakte-polls/vkontakte_polls/tests.py
# Compiled at: 2016-03-11 12:35:10
import mock, simplejson as json
from vkontakte_groups.factories import GroupFactory
from vkontakte_users.factories import UserFactory
from vkontakte_wall.factories import PostFactory
from vkontakte_api.tests import VkontakteApiTestCase
from .factories import PollFactory, AnswerFactory
from .models import Poll, Answer, Post
GROUP_ID = 16297716
POST_ID = '-16297716_190770'
POLL_ID = 83838453
GROUP2_ID = 45346748
GROUP2_POLLPOST_ID = '-45346748_4'

class VkontaktePollsTest(VkontakteApiTestCase):

    def test_parse_poll(self):
        response = '\n            {"response":{"answer_id": 0,\n             "answers": [{"id": 266067655,\n               "rate": 26.76,\n               "text": "Да, профессионально!",\n               "votes": 569},\n             {"id": 266067661,\n               "rate": 5.41,\n               "text": "Свой вариант (расскажу в комментариях).",\n               "votes": 115}],\n             "created": 1365411542,\n             "owner_id": -16297716,\n             "id": 83838453,\n             "question": "А ты занимаешься спортом? (открытое голосование)",\n             "votes": 2126}}'
        group = GroupFactory.create(remote_id=GROUP_ID)
        post = PostFactory.create(owner=group)
        instance = Poll.remote.parse_response_dict(json.loads(response)['response'], {'post_id': post.id})
        instance.save()
        self.assertEqual(instance.pk, POLL_ID)
        self.assertEqual(instance.question, 'А ты занимаешься спортом? (открытое голосование)')
        self.assertEqual(instance.owner, group)
        self.assertEqual(instance.post, post)
        self.assertEqual(instance.votes_count, 2126)
        self.assertIsNotNone(instance.created)
        self.assertEqual(instance.answers.count(), 2)
        answer = instance.answers.get(pk=266067661)
        self.assertEqual(answer.text, 'Свой вариант (расскажу в комментариях).')
        self.assertEqual(answer.votes_count, 115)
        self.assertEqual(answer.rate, 5.41)
        answer = instance.answers.get(pk=266067655)
        self.assertEqual(answer.text, 'Да, профессионально!')
        self.assertEqual(answer.votes_count, 569)
        self.assertEqual(answer.rate, 26.76)

    def test_fetching_poll(self):
        group = GroupFactory.create(remote_id=GROUP_ID)
        post = PostFactory.create(remote_id=POST_ID, owner=group)
        instance = Poll.remote.fetch(POLL_ID, post)
        self.assertEqual(instance.pk, POLL_ID)
        self.assertEqual(instance.question, 'А ты занимаешься спортом?')
        self.assertEqual(instance.owner, group)
        self.assertEqual(instance.post, post)
        self.assertGreater(instance.votes_count, 2126)
        self.assertIsNotNone(instance.created)
        self.assertEqual(instance.answers.count(), 7)
        answer = instance.answers.get(pk=266067661)
        self.assertEqual(answer.text, 'Свой вариант (расскажу в комментариях).')
        self.assertGreater(answer.votes_count, 100)
        self.assertIsNotNone(answer.rate)
        answer = instance.answers.get(pk=266067655)
        self.assertEqual(answer.text, 'Да, профессионально!')
        self.assertGreater(answer.votes_count, 560)
        self.assertIsNotNone(answer.rate)

    @mock.patch('vkontakte_users.models.User.remote.get_by_slug', side_effect=lambda s: UserFactory.create())
    def test_fetching_answer_users_by_parser(self, *args, **kwargs):
        group = GroupFactory.create(remote_id=GROUP_ID)
        post = PostFactory.create(remote_id=POST_ID, owner=group)
        poll = PollFactory.create(remote_id=POLL_ID, owner=group, post=post)
        answer = AnswerFactory.create(pk=266067661, poll=poll)
        answer.fetch_voters_by_parser()
        self.assertEqual(answer.voters.count(), answer.votes_count)
        self.assertGreaterEqual(answer.voters.count(), 155)
        self.assertGreater(answer.rate, 0)

    def test_fetch_group_post_with_poll(self, *args, **kwargs):
        self.assertEqual(Poll.objects.count(), 0)
        self.assertEqual(Answer.objects.count(), 0)
        Post.remote.fetch(ids=[POST_ID])
        self.assertEqual(Poll.objects.count(), 1)
        self.assertEqual(Answer.objects.count(), 7)

    def test_fetch_user_post_with_poll(self, *args, **kwargs):
        group = GroupFactory.create(remote_id=GROUP2_ID)
        self.assertEqual(Post.objects.count(), 0)
        self.assertEqual(Poll.objects.count(), 0)
        self.assertEqual(Answer.objects.count(), 0)
        posts = group.fetch_posts(own=True)
        self.assertGreaterEqual(posts.count(), 14)
        self.assertTrue(GROUP2_POLLPOST_ID in [ post.remote_id for post in posts ])
        self.assertGreater(Post.objects.count(), 0)

    @mock.patch('vkontakte_users.models.User.remote.get_by_slug', side_effect=lambda s: UserFactory.create())
    def test_fetching_answer_users_by_api(self, *args, **kwargs):

        def calc_percentage(poll, answer_votes):
            pp = Poll.remote.fetch(poll.pk, poll.post)
            if pp and pp.votes_count:
                return answer_votes * 100.0 / pp.votes_count
            return 0

        group = GroupFactory.create(remote_id=GROUP_ID)
        post = PostFactory.create(remote_id=POST_ID, owner=group)
        poll = PollFactory.create(remote_id=POLL_ID, owner=group, post=post)
        answer = AnswerFactory.create(pk=266067661, poll=poll)
        answer.fetch_voters_by_api()
        self.assertEqual(answer.voters.count(), answer.votes_count)
        self.assertGreaterEqual(answer.voters.count(), 155)
        self.assertGreater(answer.rate, 0)
        percentage = calc_percentage(poll, answer.votes_count)
        self.assertEqual(answer.rate, percentage)

    @mock.patch('vkontakte_users.models.User.remote.get_by_slug', side_effect=lambda s: UserFactory.create())
    def test_fetching_answer_users(self, *args, **kwargs):
        group = GroupFactory.create(remote_id=GROUP_ID)
        post = PostFactory.create(remote_id=POST_ID, owner=group)
        poll = PollFactory.create(remote_id=POLL_ID, owner=group, post=post)
        answer = AnswerFactory.create(pk=266067661, poll=poll)
        answer.fetch_voters(source='api')
        self.assertEqual(answer.voters.count(), answer.votes_count)
        self.assertGreaterEqual(answer.voters.count(), 155)
        self.assertGreater(answer.rate, 0)
        answer.fetch_voters(source=None)
        self.assertEqual(answer.voters.count(), answer.votes_count)
        self.assertGreaterEqual(answer.voters.count(), 155)
        self.assertGreater(answer.rate, 0)
        return