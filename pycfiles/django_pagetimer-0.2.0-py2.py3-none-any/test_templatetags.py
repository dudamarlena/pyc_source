# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/anders/work/python/django-pagetimer/pagetimer/tests/test_templatetags.py
# Compiled at: 2016-05-10 06:19:42
from django.test import TestCase
from pagetimer.templatetags.pagetimertags import pagetimer

class TestTemplateTag(TestCase):

    def test_pagetimer(self):
        fake_context = dict()
        r = pagetimer(fake_context)
        self.assertEqual(r['pagetimer_interval'], 60)
        self.assertEqual(r['pagetimer_endpoint'], '/endpoint/')

    def test_pagetimer_with_different_interval(self):
        fake_context = dict()
        with self.settings(PAGETIMER_INTERVAL=10):
            r = pagetimer(fake_context)
            self.assertEqual(r['pagetimer_interval'], 10)