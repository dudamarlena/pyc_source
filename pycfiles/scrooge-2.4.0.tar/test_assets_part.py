# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kula/workspace/ralph_pricing/src/ralph_pricing/tests/collect_plugins/test_assets_part.py
# Compiled at: 2014-05-30 05:53:08
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import datetime
from django.test import TestCase
from ralph_pricing.models import DailyPart
from ralph_pricing.plugins.collects.assets_part import update_assets_parts

class TestAssetPlugin(TestCase):

    def setUp(self):
        self.today = datetime.date.today()

    def get_asset_part(self):
        """Simulated api result"""
        yield {b'asset_id': 1123, 
           b'ralph_id': 113, 
           b'model': b'Noname SSD', 
           b'price': 130, 
           b'is_deprecated': True, 
           b'deprecation_rate': 0}

    def test_sync_asset_device_part(self):
        count = sum(update_assets_parts(data, self.today) for data in self.get_asset_part())
        part = DailyPart.objects.get(asset_id=1123)
        self.assertEqual(count, 1)
        self.assertEqual(part.is_deprecated, True)
        self.assertEqual(part.name, b'Noname SSD')
        self.assertEqual(part.price, 130)