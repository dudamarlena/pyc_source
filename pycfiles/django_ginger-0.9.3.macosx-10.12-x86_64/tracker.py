# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/shodh/Projects/django_ginger/ginger/tests/tracker.py
# Compiled at: 2014-12-02 12:32:25
import mock
from django import test
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from ginger.models import track_fields
from ginger.models.tracker import FieldTracker

@track_fields(('name', 'age'))
class Dummy(models.Model):
    name = models.CharField(max_length=120)
    age = models.PositiveIntegerField(default=0)


class TestTracker(test.SimpleTestCase):

    def test_class_attr(self):
        self.assertRaises(ImproperlyConfigured, lambda : Dummy.tracker)

    def test_instance_attr(self):
        self.assertIsInstance(Dummy().tracker, FieldTracker)

    def test_tracker_cached(self):
        ins = Dummy()
        self.assertIs(ins.tracker, ins.tracker)

    def test_save_signal(self):
        ins = Dummy(name=120, age=13)
        with mock.patch('ginger.models.tracker.FieldTracker.reset') as (mock_reset):
            ins.name = 'Hello'
            ins.save()
            self.assertTrue(mock_reset.called)

    def test_init_signal(self):
        with mock.patch('ginger.models.tracker.FieldTracker.reset') as (mock_reset):
            ins = Dummy(name=120, age=13)
            self.assertTrue(mock_reset.called)

    def test_tracker_has_changed(self):
        ins = Dummy()
        tracker = FieldTracker(ins, ('name', ))
        self.assertFalse(tracker.has_changed('name'))
        ins.age = 12
        self.assertFalse(tracker.has_changed('age'))
        ins.name = 'Hello'
        self.assertTrue(tracker.has_changed('name'))

    def test_tracker_reset(self):
        ins = Dummy()
        tracker = FieldTracker(ins, ('name', ))
        ins.name = 'Spider'
        self.assertTrue(tracker.has_changed('name'))
        tracker.reset()
        self.assertFalse(tracker.has_changed('name'))