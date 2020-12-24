# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/modelversions/tests.py
# Compiled at: 2015-09-15 09:39:08
from collections import deque
from django.test import TestCase
from django.conf import settings
from django.db import models, connection
from django.db.models.signals import post_save, pre_save
from models import VersionedModel, ConcurrentModificationException

class FakeModel(VersionedModel):
    name = models.CharField(max_length=30)


def fake_postsave(sender, instance, created, **kwargs):
    instance.post_save_fired = True


def fake_presave(sender, instance, **kwargs):
    instance.pre_save_fired = True


pre_save.connect(fake_presave, sender=FakeModel)
post_save.connect(fake_postsave, sender=FakeModel)

class TestVersionedModel(TestCase):

    def setUp(self):
        self.old_debug = settings.DEBUG
        settings.DEBUG = True
        connection.queries_log = deque(maxlen=9999)

    def tearDown(self):
        settings.DEBUG = self.old_debug

    def test_save_new(self):
        m = FakeModel()
        m.name = 'Hello'
        m.save()
        self.assertTrue(m.pre_save_fired)
        self.assertTrue(m.post_save_fired)
        m = FakeModel.objects.get(name='Hello')
        self.assertTrue(m.id != None)
        return

    def test_save_altered(self):
        m = FakeModel()
        m.name = 'Hello'
        m.save()
        self.assertTrue(m.pre_save_fired)
        self.assertTrue(m.post_save_fired)
        m.pre_save_fired = False
        m.post_save_fired = False
        self.assertEquals(1, len(connection.queries))
        m = FakeModel.objects.get(name='Hello')
        m.name = 'Bob'
        m.save()
        self.assertTrue(m.pre_save_fired)
        self.assertTrue(m.post_save_fired)
        self.assertEquals(3, len(connection.queries))
        m = FakeModel.objects.get(name='Bob')
        self.assertEquals(1, FakeModel.objects.count())

    def test_save_concurrent(self):
        m = FakeModel()
        m.name = 'Hello'
        m.save()
        m1 = FakeModel.objects.get(name='Hello')
        m2 = FakeModel.objects.get(name='Hello')
        m1.name = 'Bob'
        m1.save()
        try:
            m2.name = 'Bob'
            m2.save()
            self.fail('Should have hit concurrent modification error')
        except ConcurrentModificationException:
            pass