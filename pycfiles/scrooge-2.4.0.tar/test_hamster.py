# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kula/workspace/ralph_pricing/src/ralph_pricing/tests/collect_plugins/test_hamster.py
# Compiled at: 2014-05-30 05:53:08
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import datetime, mock
from django.conf import settings
from django.test import TestCase
from ralph_pricing.models import DailyUsage, Venture
from ralph_pricing.plugins.collects.hamster import hamster as hamster_runner

def mock_get_venture_capacity(venture_symbol, url):
    if venture_symbol == b'test_venture1':
        capacity = 2131231233.0
    elif venture_symbol == b'test_venture2':
        capacity = 4234233423.0
    else:
        capacity = 0
    return capacity


class TestHamster(TestCase):

    def setUp(self):
        self.venture_1 = Venture(name=b'Test Venture1', symbol=b'test_venture1', venture_id=b'1')
        self.venture_1.save()
        self.venture_2 = Venture(name=b'Test Venture2', symbol=b'test_venture2', venture_id=b'2')
        self.venture_2.save()
        self.venture_3 = Venture(name=b'Test Venture3', symbol=b'test_venture3', venture_id=b'3')
        self.venture_3.save()

    def test_set_usages(self):
        """ Hamster usages Test Case """
        settings.HAMSTER_API_URL = b'/'
        with mock.patch(b'ralph_pricing.plugins.collects.hamster.get_venture_capacity') as (get_venture_capacity):
            get_venture_capacity.side_effect = mock_get_venture_capacity
            status, message, args = hamster_runner(today=datetime.datetime.today())
            self.assertTrue(status)
            usages = DailyUsage.objects.all()
            self.assertEqual(len(usages), 2)
            usage_venture1 = DailyUsage.objects.get(pricing_venture=self.venture_1)
            usage_venture2 = DailyUsage.objects.get(pricing_venture=self.venture_2)
            self.assertEqual(usage_venture1.value, 2131231233.0 / 1048576)
            self.assertEqual(usage_venture2.value, 4234233423.0 / 1048576)

    def test_fail_plugin(self):
        """ Testing not configured plugin """
        with mock.patch(b'ralph_pricing.plugins.collects.hamster.get_venture_capacity') as (get_venture_capacity):
            get_venture_capacity.side_effect = mock_get_venture_capacity
            status, message, args = hamster_runner(today=datetime.datetime.today())
            self.assertFalse(status)