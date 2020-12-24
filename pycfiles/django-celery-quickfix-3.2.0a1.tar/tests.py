# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bharadwaj/Desktop/django-celery/tests/someapp/tests.py
# Compiled at: 2016-04-14 06:46:44
from __future__ import absolute_import
from django.test.testcases import TestCase as DjangoTestCase
from someapp.models import Thing
from someapp.tasks import SomeModelTask

class SimpleTest(DjangoTestCase):

    def setUp(self):
        self.thing = Thing.objects.create(name='Foo')

    def test_apply_task(self):
        """Apply task function."""
        result = SomeModelTask.apply(kwargs={'pk': self.thing.pk})
        self.assertEqual(result.get(), self.thing.name)

    def test_task_function(self):
        """Run task function."""
        result = SomeModelTask(pk=self.thing.pk)
        self.assertEqual(result, self.thing.name)