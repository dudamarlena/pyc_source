# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/eliotberriot/Seafile/kii/kii_main/kii/stream/tests/test_stream_item.py
# Compiled at: 2015-01-18 07:28:37
# Size of source mod 2**32: 3207 bytes
import django
from django.utils import timezone
from . import base
from .. import models, forms
from kii import stream, hook
from ...tests import test_stream
from kii.tests.test_stream.models import StreamItemChild1

class TestStreamItem(base.StreamTestCase):

    def test_status_default_to_pub(self):
        m = self.G(stream.models.StreamItem)
        self.assertEqual(m.status, 'pub')

    def test_creation_and_modification_date(self):
        now = timezone.now()
        m = self.G(stream.models.StreamItem)
        self.assertEqual(m.created > now, True)
        self.assertEqual(m.last_modified > now, True)

    def test_permission_inheritance(self):
        m = stream.models.StreamItem(title='test', root=self.streams[0])
        m.save()
        u = self.users[1]
        self.assertEqual(m.readable_by(u), False)
        m.root.assign_perm('read', self.anonymous_user)
        self.assertEqual(m.readable_by(u), True)
        m.inherit_permissions = False
        m.save()
        self.assertEqual(m.readable_by(u), False)
        m.assign_perm('delete', u)
        self.assertEqual(m.readable_by(u), True)

    def test_polymorphic_integration(self):
        m1 = test_stream.models.StreamItemChild1(title='test', root=self.streams[0])
        m2 = test_stream.models.StreamItemChild2(title='test', root=self.streams[0])
        m1.save()
        m2.save()
        self.assertQuerysetEqualIterable(self.streams[0].children.all(), [m1, m2], ordered=False)

    def test_form_select_user_stream_as_default_stream(self):
        form = forms.StreamItemForm(user=self.users[0])
        self.assertEqual(form.initial['root'], models.Stream.objects.get(title=self.users[0].username))

    def test_readable_queryset_does_not_include_drafts(self):
        self.streams[0].assign_perm('read', self.anonymous_user)
        m1 = stream.models.StreamItem(title='test', status='pub', root=self.streams[0])
        m2 = stream.models.StreamItem(title='test', status='pub', root=self.streams[0])
        m3 = stream.models.StreamItem(title='test', status='draft', root=self.streams[0])
        m4 = stream.models.StreamItem(title='test', status='draft', root=self.streams[0])
        m1.save()
        m2.save()
        m3.save()
        m4.save()
        self.assertQuerysetEqualIterable(stream.models.StreamItem.objects.all().readable_by(self.anonymous_user), [m1, m2], ordered=False)

    def test_streamitem_hooks(self):
        m1 = stream.models.StreamItem(title='test', root=self.streams[0])
        m1.save()

        def uppercase(value, **kwargs):
            return value.upper()

        hook.model_filters.register(stream.models.StreamItem, 'title', uppercase)
        self.assertEqual(m1.filtered_title, 'TEST')

    def test_stream_item_detail_redirect_to_clean_url_if_any(self):
        m1 = StreamItemChild1(title='Test', root=self.streams[0])
        m1.save()
        m1.root.assign_perm('read', self.anonymous_user)
        url = m1.reverse_detail()
        self.assertEqual(url, '/kii/items/{0}'.format(m1.pk))
        response = self.client.get(url)
        self.assertRedirects(response, '/kii/test_stream/streamitemchild1/{0}/'.format(m1.pk))