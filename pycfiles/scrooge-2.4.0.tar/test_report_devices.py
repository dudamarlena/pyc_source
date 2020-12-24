# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kula/workspace/ralph_pricing/src/ralph_pricing/tests/reports/test_report_devices.py
# Compiled at: 2014-06-03 05:10:47
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import datetime, mock
from collections import OrderedDict
from decimal import Decimal as D
from dateutil import rrule
from django.test import TestCase
from django.utils.translation import ugettext_lazy as _
from ralph_pricing import models
from ralph_pricing.tests import utils
from ralph_pricing.views.devices import Devices

class TestReportDevices(TestCase):

    def setUp(self):
        self.report_start = datetime.date(2013, 4, 20)
        self.report_end = datetime.date(2013, 4, 30)
        self.venture = utils.get_or_create_venture()
        self.subventure = utils.get_or_create_venture(parent=self.venture)
        self.usage_type = models.UsageType(name=b'UT1', symbol=b'ut1', type=b'BU', show_in_devices_report=True)
        self.usage_type.save()
        usage_type2 = models.UsageType(name=b'UT2', symbol=b'ut2', type=b'BU', show_in_devices_report=False)
        usage_type2.save()
        self.warehouse_usage_type = models.UsageType(name=b'UT3', symbol=b'ut3', by_warehouse=True, order=3, type=b'BU', use_universal_plugin=False, show_in_devices_report=True)
        self.warehouse_usage_type.save()
        self.device1 = utils.get_or_create_device()
        self.device2 = utils.get_or_create_device()
        self.device3 = utils.get_or_create_device()
        self.device_virtual = utils.get_or_create_device(is_virtual=True)
        days = rrule.rrule(rrule.DAILY, dtstart=self.report_start, until=self.report_end)
        for device in (self.device1, self.device2, self.device_virtual):
            for j, day in enumerate(days, start=1):
                dailydevice = utils.get_or_create_dailydevice(date=day, device=device, venture=self.venture)
                dailydevice.save()

    def test_get_plugins(self):
        """
        Test plugins list based on visible usage types
        """
        plugins = Devices.get_plugins()
        self.assertEquals(plugins, [
         dict(name=b'Information', plugin_name=b'information'),
         dict(name=b'UT3', plugin_name=self.warehouse_usage_type.get_plugin_name(), plugin_kwargs=dict(usage_type=self.warehouse_usage_type, no_price_msg=True)),
         dict(name=b'UT1', plugin_name=self.usage_type.get_plugin_name(), plugin_kwargs=dict(usage_type=self.usage_type, no_price_msg=True))])

    def test_get_devices(self):
        """
        Test if field is properly prepared for placing it in report. Value
        in venture data.
        """
        devices = Devices._get_devices(self.report_start, self.report_end, [
         self.venture])
        self.assertEquals(list(devices), [self.device1, self.device2])

    def test_get_ventures(self):
        ventures = Devices._get_ventures(self.venture, use_subventures=False)
        self.assertEquals(ventures, [self.venture])

    def test_get_ventures_with_subventures(self):
        ventures = Devices._get_ventures(self.venture, use_subventures=True)
        self.assertEquals(ventures, [self.venture, self.subventure])

    def _sample_schema(self):
        return [
         OrderedDict([
          (
           b'field1', {b'name': b'Field1'}),
          (
           b'field2',
           {b'name': b'Field2', 
              b'currency': True, 
              b'total_cost': True})]),
         OrderedDict([
          (
           b'field3', {b'name': b'Field3'}),
          (
           b'field4',
           {b'name': b'Field4', 
              b'currency': True, 
              b'total_cost': True})])]

    @mock.patch(b'ralph.util.plugin.run')
    def test_get_report_data(self, plugin_run_mock):
        """
        Test generating data for whole report
        """

        def pl(chain, func_name, type, **kwargs):
            """
            Mock for plugin run. Should replace every schema and report plugin
            """
            data = {b'information': {b'schema_devices': OrderedDict([
                                                  (
                                                   b'barcode', {b'name': b'Barcode'}),
                                                  (
                                                   b'sn', {b'name': b'SN'}),
                                                  (
                                                   b'name', {b'name': b'Device name'})]), 
                                b'costs_per_device': {self.device1.id: {b'sn': b'1111-1111-1111', 
                                                                        b'barcode': b'12345', 
                                                                        b'name': b'device1'}, 
                                                      self.device2.id: {b'sn': b'1111-1111-1112', 
                                                                        b'barcode': b'12346', 
                                                                        b'name': b'device2'}}}, 
               b'usage_plugin': {b'schema_devices': OrderedDict([
                                                   (
                                                    b'ut1_count', {b'name': b'UT1 count'}),
                                                   (
                                                    b'ut1_cost',
                                                    {b'name': b'UT1 cost', 
                                                       b'currency': True, 
                                                       b'total_cost': True})]), 
                                 b'costs_per_device': {self.device2.id: {b'ut1_count': 123, 
                                                                         b'ut1_cost': D(b'23.23')}}}, 
               b'ut3': {b'schema_devices': OrderedDict([
                                          (
                                           b'ut3_count_warehouse_1', {b'name': b'UT3 count wh 1'}),
                                          (
                                           b'ut3_count_warehouse_2', {b'name': b'UT3 count wh 2'}),
                                          (
                                           b'ut3_cost_warehouse_1',
                                           {b'name': b'UT3 cost wh 1', 
                                              b'currency': True}),
                                          (
                                           b'ut3_cost_warehouse_2',
                                           {b'name': b'UT3 cost wh 2', 
                                              b'currency': True}),
                                          (
                                           b'ut3_cost_total',
                                           {b'name': b'UT3 total cost', 
                                              b'currency': True, 
                                              b'total_cost': True})]), 
                        b'costs_per_device': {self.device1.id: {b'ut3_count_warehouse_1': 267, 
                                                                b'ut3_cost_warehouse_1': D(b'4764.21'), 
                                                                b'ut3_count_warehouse_2': 36774, 
                                                                b'ut3_cost_warehouse_2': _(b'Incomplete price'), 
                                                                b'ut3_cost_total': D(b'4764.21')}, 
                                              self.device2.id: {b'ut3_count_warehouse_1': 213, 
                                                                b'ut3_cost_warehouse_1': D(b'434.21'), 
                                                                b'ut3_count_warehouse_2': 3234, 
                                                                b'ut3_cost_warehouse_2': D(b'123.21'), 
                                                                b'ut3_cost_total': D(b'557.42')}}}}
            if type == b'costs_per_device':
                self.assertTrue(kwargs.get(b'forecast'))
            result = data.get(func_name, {}).get(type)
            if result is not None:
                return result
            else:
                raise KeyError()
                return

        plugin_run_mock.side_effect = pl
        result = None
        for percent, result in Devices.get_data(self.report_start, self.report_end, venture=self.venture, forecast=True):
            pass

        self.assertEquals(result, [
         [
          b'12345',
          b'1111-1111-1111',
          b'device1',
          267,
          36774,
          b'4764.21',
          b'Incomplete price',
          b'4764.21',
          0.0,
          b'0.00',
          b'4764.21'],
         [
          b'12346',
          b'1111-1111-1112',
          b'device2',
          213.0,
          3234.0,
          b'434.21',
          b'123.21',
          b'557.42',
          123.0,
          b'23.23',
          b'580.65']])
        return

    @mock.patch.object(Devices, b'_get_schema')
    def test_get_header(self, get_schema_mock):
        """
        Test getting headers for report
        """
        get_schema_mock.return_value = self._sample_schema()
        result = Devices.get_header()
        self.assertEquals(result, [
         [
          b'Field1',
          b'Field2 - PLN',
          b'Field3',
          b'Field4 - PLN',
          b'Total cost']])