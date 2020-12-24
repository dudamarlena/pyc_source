# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kula/workspace/ralph_pricing/src/ralph_pricing/tests/collect_plugins/test_assets.py
# Compiled at: 2014-05-30 05:53:08
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import datetime
from django.test import TestCase
from ralph_pricing.models import Device, DailyDevice, DailyUsage, UsageType, Warehouse
from ralph_pricing.plugins.collects.assets import update_assets

class TestAssetPlugin(TestCase):

    def setUp(self):
        self.today = datetime.date.today()
        self.core_usage_type, created = UsageType.objects.get_or_create(name=b'Physical CPU cores', symbol=b'physical_cpu_cores', average=True)
        self.core_usage_type.save()
        self.power_consumption_usage_type, created = UsageType.objects.get_or_create(name=b'Power consumption', symbol=b'power_consumption', by_warehouse=True, by_cost=True)
        self.power_consumption_usage_type.save()
        self.collocation_usage_type, created = UsageType.objects.get_or_create(name=b'Collocation', symbol=b'collocation', by_warehouse=True, by_cost=True)
        self.collocation_usage_type.save()
        self.warehouse, created = Warehouse.objects.get_or_create(name=b'Sample warehouse')
        self.warehouse.save()

    def _get_asset(self):
        """Simulated api result"""
        yield {b'asset_id': 1123, 
           b'ralph_id': 13342, 
           b'slots': 10.0, 
           b'power_consumption': 1000, 
           b'height_of_device': 10.0, 
           b'price': 100, 
           b'is_deprecated': True, 
           b'sn': b'1234-1234-1234-1234', 
           b'barcode': b'4321-4321-4321-4321', 
           b'deprecation_rate': 0, 
           b'is_blade': True, 
           b'venture_id': 12, 
           b'cores_count': 8, 
           b'warehouse_id': self.warehouse.id}

    def test_sync_asset_device(self):
        count = sum(update_assets(data, self.today, {b'core': self.core_usage_type, b'power_consumption': self.power_consumption_usage_type, b'collocation': self.collocation_usage_type}) for data in self._get_asset())
        self.assertEqual(count, 1)
        device = Device.objects.get(device_id=13342)
        self.assertEqual(device.device_id, 13342)
        self.assertEqual(device.asset_id, 1123)
        self.assertEqual(device.slots, 10.0)
        self.assertEqual(device.sn, b'1234-1234-1234-1234')
        self.assertEqual(device.barcode, b'4321-4321-4321-4321')

    def test_sync_asset_daily(self):
        count = sum(update_assets(data, self.today, {b'core': self.core_usage_type, b'power_consumption': self.power_consumption_usage_type, b'collocation': self.collocation_usage_type}) for data in self._get_asset())
        self.assertEqual(count, 1)
        daily = DailyDevice.objects.get(date=self.today)
        self.assertEqual(daily.is_deprecated, True)
        self.assertEqual(daily.price, 100)
        self.assertEqual(daily.pricing_device_id, 1)

    def test_sync_asset_dailyusage_core(self):
        count = sum(update_assets(data, self.today, {b'core': self.core_usage_type, b'power_consumption': self.power_consumption_usage_type, b'collocation': self.collocation_usage_type}) for data in self._get_asset())
        self.assertEqual(count, 1)
        usage = DailyUsage.objects.get(date=self.today, type=self.core_usage_type)
        self.assertEqual(usage.value, 8)
        self.assertEqual(usage.pricing_device_id, 1)
        self.assertEqual(usage.warehouse_id, None)
        self.assertEqual(usage.type, self.core_usage_type)
        return

    def test_sync_asset_dailyusage_power_consumption(self):
        count = sum(update_assets(data, self.today, {b'core': self.core_usage_type, b'power_consumption': self.power_consumption_usage_type, b'collocation': self.collocation_usage_type}) for data in self._get_asset())
        self.assertEqual(count, 1)
        usage = DailyUsage.objects.get(date=self.today, type=self.power_consumption_usage_type)
        self.assertEqual(usage.value, 1000)
        self.assertEqual(usage.pricing_device_id, 1)
        self.assertEqual(usage.warehouse_id, self.warehouse.id)
        usage = DailyUsage.objects.get(date=self.today, type=self.core_usage_type)
        self.assertEqual(usage.value, 8)
        usage = DailyUsage.objects.get(date=self.today, type=self.collocation_usage_type)
        self.assertEqual(usage.value, 10.0)

    def test_sync_asset_device_without_ralph_id(self):
        data = {b'asset_id': 1123, 
           b'ralph_id': None, 
           b'slots': 10.0, 
           b'power_consumption': 1000, 
           b'collocation': 10.0, 
           b'price': 100, 
           b'is_deprecated': True, 
           b'sn': b'1234-1234-1234-1234', 
           b'barcode': b'4321-4321-4321-4321', 
           b'deprecation_rate': 0, 
           b'warehouse_id': 1, 
           b'is_blade': True, 
           b'cores_count': 0}
        self.assertFalse(update_assets(data, self.today, {b'core': self.core_usage_type, 
           b'power_consumption': self.power_consumption_usage_type, 
           b'collocation': self.collocation_usage_type}), False)
        return

    def test_sync_asset_device_update(self):
        data = {b'asset_id': 1123, 
           b'ralph_id': 123, 
           b'slots': 10.0, 
           b'power_consumption': 1000, 
           b'collocation': 10.0, 
           b'price': 100, 
           b'is_deprecated': True, 
           b'sn': b'1234-1234-1234-1234', 
           b'barcode': b'4321-4321-4321-4321', 
           b'deprecation_rate': 0, 
           b'warehouse_id': 1, 
           b'is_blade': True, 
           b'cores_count': 0}
        update_assets(data, self.today, {b'core': self.core_usage_type, 
           b'power_consumption': self.power_consumption_usage_type, 
           b'collocation': self.collocation_usage_type})
        device = Device.objects.get(device_id=123)
        self.assertEqual(device.sn, b'1234-1234-1234-1234')
        data = {b'asset_id': 1123, 
           b'ralph_id': 123, 
           b'slots': 10.0, 
           b'power_consumption': 1000, 
           b'collocation': 10.0, 
           b'price': 100, 
           b'is_deprecated': True, 
           b'sn': b'5555-5555-5555-5555', 
           b'barcode': b'4321-4321-4321-4321', 
           b'deprecation_rate': 0, 
           b'warehouse_id': 1, 
           b'is_blade': False, 
           b'cores_count': 2}
        update_assets(data, self.today, {b'core': self.core_usage_type, 
           b'power_consumption': self.power_consumption_usage_type, 
           b'collocation': self.collocation_usage_type})
        device = Device.objects.get(device_id=123)
        self.assertEqual(device.sn, b'5555-5555-5555-5555')

    def test_sync_asset_sn_barcode_device_id_update(self):
        data = self._get_asset().next()
        created = update_assets(data, self.today, {b'core': self.core_usage_type, 
           b'power_consumption': self.power_consumption_usage_type, 
           b'collocation': self.collocation_usage_type})
        self.assertEqual(created, True)
        asset = Device.objects.get(asset_id=1123)
        self.assertEqual(asset.device_id, 13342)
        self.assertEqual(asset.sn, b'1234-1234-1234-1234')
        self.assertEqual(asset.barcode, b'4321-4321-4321-4321')
        data[b'asset_id'] = 1124
        created = update_assets(data, self.today, {b'core': self.core_usage_type, 
           b'power_consumption': self.power_consumption_usage_type, 
           b'collocation': self.collocation_usage_type})
        self.assertEqual(created, True)
        asset = Device.objects.get(asset_id=1124)
        self.assertEqual(asset.device_id, 13342)
        self.assertEqual(asset.sn, b'1234-1234-1234-1234')
        self.assertEqual(asset.barcode, b'4321-4321-4321-4321')
        old_asset = Device.objects.get(asset_id=1123)
        self.assertEqual(old_asset.device_id, None)
        self.assertEqual(old_asset.sn, None)
        self.assertEqual(old_asset.barcode, None)
        return