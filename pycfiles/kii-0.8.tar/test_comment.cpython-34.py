# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/eliotberriot/Seafile/kii/kii_main/kii/discussion/tests/test_comment.py
# Compiled at: 2014-12-31 04:01:40
# Size of source mod 2**32: 5326 bytes
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from kii.tests.test_discussion import models
from ...user.tests import base
from ..models import AnonymousCommenterProfile

class CommentTestCase(base.UserTestCase):

    def test_comment_can_belong_to_user(self):
        c = self.G(models.DiscussionModelComment, user=self.users[0])
        self.assertEqual(c.user, self.users[0])

    def test_can_comment_discussion_model(self):
        m = self.G(models.DiscussionModel)
        c = self.G(models.DiscussionModelComment, subject=m, user=self.users[0])
        self.assertEqual(m.comments.all().first(), c)

    def test_comment_can_have_markdown_content(self):
        c = self.G(models.DiscussionModelComment, content='# nice', user=self.users[0])
        self.assertEqual(c.content.rendered, '<h1>nice</h1>')

    def test_comment_anonymous_comment_requires_username_and_email(self):
        m = self.G(models.DiscussionModel)
        p = self.G(AnonymousCommenterProfile, email='hello@me.com', username='something')
        c = models.DiscussionModelComment(subject=m, content='test')
        with self.assertRaises(ValidationError):
            c.save()
        c.user_profile = p
        c.save()

    def test_comment_with_both_user_and_user_profile_raise_integrity_error(self):
        m = self.G(models.DiscussionModel)
        p = self.G(AnonymousCommenterProfile, email='hello@me.com', username='something')
        with self.assertRaises(ValidationError):
            c1 = models.DiscussionModelComment(user_profile=p, user=self.users[0], subject=m)
            c1.save()

    def test_can_access_authenticated_and_anonymous_user_infos_with_the_same_api(self):
        m = self.G(models.DiscussionModel)
        p = self.G(AnonymousCommenterProfile, email='hello@me.com', username='something')
        c1 = self.G(models.DiscussionModelComment, user_profile=p)
        c2 = self.G(models.DiscussionModelComment, user=self.users[0])
        self.assertEqual(c1.profile.username, 'something')
        self.assertEqual(c2.profile.username, self.users[0].username)
        self.assertEqual(c1.profile.email, 'hello@me.com')
        self.assertEqual(c2.profile.email, self.users[0].email)

    def test_cannot_comment_if_dicussion_is_closed(self):
        m = self.G(models.DiscussionModel, discussion_open=False)
        c = models.DiscussionModelComment(subject=m, user=self.users[0])
        with self.assertRaises(ValidationError):
            c.save()

    def test_cannot_comment_with_empty_content(self):
        m = self.G(models.DiscussionModel)
        c = models.DiscussionModelComment(user=self.users[0], subject=m, content='')
        with self.assertRaises(ValidationError):
            c.save()

    def test_comment_status_default_to_awaiting_moderation_for_anonymous_users(self):
        p = self.G(AnonymousCommenterProfile, email='mail@me.com', username='something')
        m = self.G(models.DiscussionModel)
        c = self.G(models.DiscussionModelComment, subject=m, user_profile=p)
        self.assertEqual(c.status, 'awaiting_moderation')

    def test_comment_status_default_to_published_for_authenticated_users(self):
        c = self.G(models.DiscussionModelComment, user=self.users[0])
        self.assertEqual(c.status, 'published')

    def test_can_hook_into_detect_junk(self):
        p = self.G(AnonymousCommenterProfile, email='hello@spam', username='something')
        m = self.G(models.DiscussionModel)
        c = models.DiscussionModelComment(subject=m, user_profile=p, content='YOLO')
        c.save()
        self.assertEqual(c.status, 'junk')

    def test_can_post_comment_as_logged_in_user(self):
        m = self.G(models.DiscussionModel)
        self.login(self.users[1].username)
        response = self.client.post(m.reverse_comment_create(), {'content': 'yolo'})
        self.assertRedirects(response, m.reverse_detail())
        self.assertEqual(m.comments.all().first().content.raw, 'yolo')

    def test_can_post_comment_as_anonymous_user(self):
        m = self.G(models.DiscussionModel)
        response = self.client.post(m.reverse_comment_create(), {'username': 'Roger',  'email': 'test@test.com',  'url': 'http://example.com',  'content': 'yolo'})
        comment = m.comments.all().first()
        self.assertEqual(comment.profile.username, 'Roger')
        self.assertEqual(comment.profile.email, 'test@test.com')
        self.assertEqual(comment.profile.url, 'http://example.com/')

    def test_can_queryset_public_comments(self):
        profile = AnonymousCommenterProfile(username='test', email='test@test.com')
        profile.save()
        m0 = self.G(models.DiscussionModelComment, status='published', user=self.users[0])
        m1 = self.G(models.DiscussionModelComment, status='junk', user_profile=profile)
        m2 = self.G(models.DiscussionModelComment, status='awaiting_moderation', user_profile=profile)
        m3 = self.G(models.DiscussionModelComment, status='published', user=self.users[0])
        queryset = models.DiscussionModelComment.objects.public()
        self.assertQuerysetEqualIterable(queryset, [m0, m3])