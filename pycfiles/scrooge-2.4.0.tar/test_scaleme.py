# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kula/workspace/ralph_pricing/src/ralph_pricing/tests/collect_plugins/test_scaleme.py
# Compiled at: 2014-05-30 05:53:08
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import datetime, mock
from django.conf import settings
from django.test import TestCase
from ralph_pricing.models import DailyUsage, UsageType, Venture
from ralph_pricing.plugins.collects.scaleme import scaleme as scaleme_runner

def mock_get_ventures_capacities(date, url):
    return {b'test_venture1': {b'cache': 7878, 
                          b'backend': 987987}, 
       b'test_venture2': {b'cache': 666999, 
                          b'backend': 12346699}}


class TestScaleme(TestCase):

    def setUp(self):
        self.venture_1 = Venture(name=b'Test Venture1', symbol=b'test_venture1', venture_id=b'1')
        self.venture_1.save()
        self.venture_2 = Venture(name=b'Test Venture2', symbol=b'test_venture2', venture_id=b'2')
        self.venture_2.save()
        self.venture_3 = Venture(name=b'Test Venture3', symbol=b'test_venture3', venture_id=b'3')
        self.venture_3.save()

    def test_set_usages(self):
        """Scaleme usages Test Case"""
        settings.SCALEME_API_URL = b'/'
        with mock.patch(b'ralph_pricing.plugins.collects.scaleme.get_ventures_capacities') as (get_ventures_capacities):
            get_ventures_capacities.side_effect = mock_get_ventures_capacities
            status, message, args = scaleme_runner(today=datetime.datetime.today())
            self.assertTrue(status)
            usages = DailyUsage.objects.all()
            self.assertEqual(usages.count(), 4)
            usage_backend = UsageType.objects.get(name=b'Scaleme transforming an image 10000 events')
            usage_cache = UsageType.objects.get(name=b'Scaleme serving image from cache 10000 events')
            usages_venture1 = DailyUsage.objects.filter(pricing_venture=self.venture_1)
            usages_venture2 = DailyUsage.objects.filter(pricing_venture=self.venture_2)
            usages_venture3 = DailyUsage.objects.filter(pricing_venture=self.venture_3)
            self.assertEqual(usages_venture1.count(), 2)
            usage_backend_venture1 = usages_venture1.filter(type=usage_backend)
            usage_cache_venture1 = usages_venture1.filter(type=usage_cache)
            self.assertEqual(usage_backend_venture1[0].value, 987987)
            self.assertEqual(usage_cache_venture1[0].value, 7878)
            self.assertEqual(usages_venture2.count(), 2)
            usage_backend_venture2 = usages_venture2.filter(type=usage_backend)
            usage_cache_venture2 = usages_venture2.filter(type=usage_cache)
            self.assertEqual(usage_backend_venture2[0].value, 12346699)
            self.assertEqual(usage_cache_venture2[0].value, 666999)
            self.assertEqual(usages_venture3.count(), 0)

    def test_fail_plugin(self):
        """Testing not configured plugin"""
        with mock.patch(b'ralph_pricing.plugins.collects.scaleme.get_ventures_capacities') as (get_ventures_capacities):
            get_ventures_capacities.side_effect = mock_get_ventures_capacities
            status, message, args = scaleme_runner(today=datetime.datetime.today())
            self.assertFalse(status)