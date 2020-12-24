# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/eliotberriot/Seafile/kii/kii_main/kii/stream/tests/test_views.py
# Compiled at: 2015-01-18 07:28:37
# Size of source mod 2**32: 2169 bytes
from django.core.urlresolvers import reverse
from . import base
from .. import models
from ..filterset import OwnerStreamItemFilterSet

class TestStreamViews(base.StreamTestCase):

    def test_base_stream_view_passes_current_stream_to_context(self):
        url = reverse('kii:stream:stream:index', kwargs={'stream': self.users[0].username})
        stream = models.Stream.objects.get(owner=self.users[0], title=self.users[0].username)
        self.login(self.users[0].username)
        response = self.client.get(url)
        self.assertEqual(response.context['current_stream'], stream)

    def test_anonymous_user_can_display_public_stream_item_detail_page(self):
        stream = models.Stream.objects.get(owner=self.users[0], title=self.users[0].username)
        si = models.StreamItem(root=stream, title='Hello', content='test', status='pub')
        si.save()
        stream.assign_perm('read', self.anonymous_user)
        url = si.reverse_detail()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['object'], si)

    def test_stream_item_list_filter_class_change_depending_on_user(self):
        stream = models.Stream.objects.get_user_stream(self.users[0])
        url = stream.reverse_detail()
        response = self.client.get(url)
        with self.assertRaises(KeyError):
            response.context['filterset']
        self.login(self.users[0].username)
        response = self.client.get(url)
        self.assertEqual(isinstance(response.context['filterset'], OwnerStreamItemFilterSet), True)

    def test_authenticated_user_can_update_his_default_stream(self):
        s = self.G(models.Stream, owner=self.users[0])
        url = reverse('kii:api:stream:stream:select', kwargs={'pk': s.pk})
        self.login(self.users[0].username)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('kii:glue:home'))
        self.assertEqual(response.context['selected_stream'], s)