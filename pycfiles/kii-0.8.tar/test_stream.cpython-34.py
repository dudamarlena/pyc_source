# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/eliotberriot/Seafile/kii/kii_main/kii/stream/tests/test_stream.py
# Compiled at: 2015-01-18 07:28:37
# Size of source mod 2**32: 2171 bytes
from django.core.urlresolvers import reverse
import feedparser
from . import base
from kii import stream

class TestStream(base.StreamTestCase):

    def test_new_user_gets_a_dedicated_stream(self):
        u = self.user_model(username='new_user')
        u.save()
        s = stream.models.Stream.objects.get(owner=u)

    def test_default_user_stream_is_titled_with_owner_username(self):
        u = self.user_model(username='this_is_my_username')
        u.save()
        s = stream.models.Stream.objects.get(title='this_is_my_username')
        self.assertEqual(s.owner, u)

    def test_can_update_stream(self):
        url = reverse('kii:stream:stream:update', kwargs={'stream': self.users[0].username})
        self.login(self.users[0].username)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['object'].title, 'test0')

    def test_stream_atom_feed(self):
        i = stream.models.Stream.objects.get(title=self.users[0].username, owner=self.users[0])
        i.content = '#hello'
        i.save()
        si = stream.models.StreamItem(root=i, title='Hello world', status='pub', content='#yolo')
        si.save()
        i.assign_perm('read', self.anonymous_user)
        url = i.reverse_feed()
        response = self.client.get(url)
        parsed_content = feedparser.parse(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertIn(parsed_content['feed']['title'], i.title)

    def test_empty_stream_atom_feed_does_not_raise_500(self):
        i = stream.models.Stream.objects.get(title=self.users[0].username, owner=self.users[0])
        i.assign_perm('read', self.anonymous_user)
        url = i.reverse_feed()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_can_get_user_stream(self):
        i = stream.models.Stream.objects.get(title=self.users[0].username, owner=self.users[0])
        self.assertEqual(stream.models.Stream.objects.get_user_stream(self.users[0]), i)