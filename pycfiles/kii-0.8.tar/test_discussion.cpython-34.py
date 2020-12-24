# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/eliotberriot/Seafile/kii/kii_main/kii/stream/tests/test_discussion.py
# Compiled at: 2015-01-18 07:28:37
# Size of source mod 2**32: 5463 bytes
from django.core.urlresolvers import reverse
from actstream import models as actstream_models
import json
from kii.discussion.models import AnonymousCommenterProfile
from . import base
from .. import models

class TestDiscussion(base.StreamTestCase):

    def test_can_attach_comments_to_stream_items(self):
        si = models.StreamItem(root=self.streams[0], title='test', status='published')
        si.save()
        c = models.ItemComment(subject=si, user=self.users[1], content='Hello world')
        c.save()
        self.assertEqual(si.comments.all().first(), c)

    def test_can_post_comment_as_logged_in_user(self):
        self.streams[0].assign_perm('read', self.anonymous_user)
        si = models.StreamItem(root=self.streams[0], title='test', status='published')
        si.save()
        url = si.reverse_comment_create()
        self.login(self.users[0].username)
        response = self.client.post(url, {'content': 'yolo'})
        self.assertEqual(si.comments.all().first().content.raw, 'yolo')

    def test_can_post_comment_as_anonymous_user(self):
        self.streams[0].assign_perm('read', self.anonymous_user)
        si = models.StreamItem(root=self.streams[0], title='test', status='published')
        si.save()
        url = si.reverse_comment_create()
        response = self.client.post(url, {'username': 'Edgar',  'email': 'contact@edgar.com',  'content': 'yolo'})
        comment = si.comments.all().first()
        self.assertEqual(comment.profile.username, 'Edgar')
        self.assertEqual(comment.profile.email, 'contact@edgar.com')

    def test_moderation_page_require_to_be_stream_owner(self):
        s = models.Stream.objects.get(title=self.users[0].username, owner=self.users[0])
        url = reverse('kii:stream:stream:itemcomment:moderation', kwargs={'stream': s.slug})
        response = self.client.get(url)
        self.assertRedirectsLogin(response, url)
        self.login(self.users[0].username)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_moderation_return_awaiting_moderation_comments_by_default(self):
        s = models.Stream.objects.get(title=self.users[1].username, owner=self.users[1])
        si0 = self.G(models.StreamItem, root=s)
        si1 = self.G(models.StreamItem)
        profile = self.G(AnonymousCommenterProfile)
        c0 = self.G(models.ItemComment, subject=si0, user_profile=profile)
        c1 = self.G(models.ItemComment, subject=si0, user_profile=profile)
        c2 = self.G(models.ItemComment, subject=si1, user_profile=profile)
        c3 = self.G(models.ItemComment, subject=si1, user_profile=profile)
        url = reverse('kii:stream:stream:itemcomment:moderation', kwargs={'stream': s.slug})
        self.login(self.users[1].username)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqualIterable(response.context['object_list'], [c1, c0])
        self.assertEqual(response.context['can_moderate'], True)

    def test_moderation_can_filter_by_status(self):
        s = models.Stream.objects.get(title=self.users[1].username, owner=self.users[1])
        si0 = self.G(models.StreamItem, root=s)
        si1 = self.G(models.StreamItem)
        profile = self.G(AnonymousCommenterProfile)
        c0 = self.G(models.ItemComment, subject=si0, user_profile=profile, status='junk')
        c1 = self.G(models.ItemComment, subject=si0, user_profile=profile)
        url = reverse('kii:stream:stream:itemcomment:moderation', kwargs={'stream': s.slug})
        self.login(self.users[1].username)
        response = self.client.get(url + '?status=junk')
        self.assertQuerysetEqualIterable(response.context['object_list'], [c0])

    def test_patch_comment_view_require_stream_owner(self):
        s = models.Stream.objects.get(title=self.users[1].username, owner=self.users[1])
        si0 = self.G(models.StreamItem, root=s)
        c0 = self.G(models.ItemComment, subject=si0, user=self.users[0], content='Hello')
        url = reverse('kii:api:stream:itemcomment:update', kwargs={'pk': c0.pk})
        response = self.client.patch(url)
        self.assertEqual(response.status_code, 403)
        self.login(self.users[1].username)
        response = self.client.patch(url, json.dumps({'status': 'disapproved'}), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        c = models.ItemComment.objects.get(pk=c0.pk)
        self.assertEqual(c.status, 'disapproved')

    def test_addding_comment_send_notificatation_to_stream_owner(self):
        s = models.Stream.objects.get_user_stream(self.users[1])
        si0 = self.G(models.StreamItem, root=s)
        c = self.G(models.ItemComment, subject=si0, user=self.users[0])
        activity = actstream_models.user_stream(self.users[1])
        self.assertEqual(activity[0].action_object, c)
        self.assertEqual(activity[0].target, s)

    def test_each_comment_gets_an_absolute_url(self):
        s = models.Stream.objects.get_user_stream(self.users[1])
        si0 = self.G(models.StreamItem, root=s)
        c = self.G(models.ItemComment, subject=si0, user=self.users[0])
        self.assertEqual(c.get_absolute_url(), si0.get_absolute_url() + '#comment-{0}'.format(c.pk))