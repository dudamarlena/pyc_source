# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kula/workspace/ralph_pricing/src/ralph_pricing/tests/collect_plugins/test_virtual.py
# Compiled at: 2014-05-30 05:53:08
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from datetime import datetime, date
from django.test import TestCase
from ralph_pricing.models import UsageType, DailyUsage, Device
from ralph_pricing.plugins.collects.virtual import get_or_create_usages, update_usage, update
from ralph_pricing.tests.utils import get_or_create_device, get_or_create_venture

class TestAssetPlugin(TestCase):

    def setUp(self):
        self.device = get_or_create_device()
        self.venture = get_or_create_venture()

    def _get_usages(self):
        usage_names = {b'virtual_cores': b'Virtual CPU cores', 
           b'virtual_disk': b'Virtual disk MB', 
           b'virtual_memory': b'Virtual memory MB'}
        return get_or_create_usages(usage_names)

    def test_get_usages(self):
        usages = self._get_usages()
        usages_from_database = UsageType.objects.all().order_by(b'name')
        self.assertEqual(usages[b'virtual_cores'], usages_from_database[0])
        self.assertEqual(usages[b'virtual_disk'], usages_from_database[1])
        self.assertEqual(usages[b'virtual_memory'], usages_from_database[2])

    def test_update_usage_when_there_is_no_value(self):
        update_usage(self.device, self.venture, self._get_usages()[b'virtual_cores'], datetime.today(), None)
        self.assertItemsEqual(DailyUsage.objects.all(), [])
        return

    def test_update_usage(self):
        usages = self._get_usages()
        update_usage(self.device, self.venture, usages[b'virtual_cores'], date.today(), 1)
        daily_usages = DailyUsage.objects.all()
        self.assertEqual(daily_usages.count(), 1)
        self.assertEqual(daily_usages[0].pricing_device, self.device)
        self.assertEqual(daily_usages[0].pricing_venture, self.venture)
        self.assertEqual(daily_usages[0].type, usages[b'virtual_cores'])
        self.assertEqual(daily_usages[0].value, 1)

    def test_update_when_device_id_is_none(self):
        update({}, self._get_usages(), date.today())
        self.assertItemsEqual(Device.objects.all(), [self.device])

    def test_update_when_venture_id_is_none(self):
        data = {b'device_id': 1, 
           b'virtual_cores': 1, 
           b'virtual_disk': 1, 
           b'virtual_memory': 1}
        update(data, self._get_usages(), date.today())
        daily_usages = DailyUsage.objects.all()
        self.assertEqual(daily_usages.count(), 0)
        for daily_usage in daily_usages:
            self.assertEqual(daily_usage.pricing_venture, None)

        return

    def test_update(self):
        data = {b'device_id': 1, b'venture_id': 1, 
           b'virtual_cores': 1, 
           b'virtual_disk': 1, 
           b'virtual_memory': 1}
        update(data, self._get_usages(), date.today())
        daily_usages = DailyUsage.objects.all()
        self.assertEqual(daily_usages.count(), 3)
        for daily_usage in daily_usages:
            self.assertEqual(daily_usage.pricing_venture.venture_id, 1)