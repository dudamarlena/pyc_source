# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kula/workspace/ralph_pricing/src/ralph_pricing/tests/report_plugins/test_deprecation_plugin.py
# Compiled at: 2014-06-03 05:10:47
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import datetime
from dateutil import rrule
from decimal import Decimal as D
from django.test import TestCase
from django.utils.translation import ugettext_lazy as _
from ralph_pricing import models
from ralph_pricing.tests import utils
from ralph_pricing.plugins.reports.deprecation import Deprecation

class TestDeprecationReportPlugin(TestCase):

    def setUp(self):
        self.venture1 = utils.get_or_create_venture()
        self.venture2 = utils.get_or_create_venture()
        self.venture3 = utils.get_or_create_venture()
        self.ventures_subset = [self.venture1, self.venture2]
        self.ventures = models.Venture.objects.all()
        self.ventures_devices = {}
        start = datetime.date(2013, 10, 8)
        end = datetime.date(2013, 10, 22)
        for j, venture in enumerate(self.ventures, start=1):
            self.ventures_devices[venture.id] = []
            for k in range(j * 5):
                device = utils.get_or_create_device()
                self.ventures_devices[venture.id].append(device.id)
                for day in rrule.rrule(rrule.DAILY, dtstart=start, until=end):
                    utils.get_or_create_dailydevice(date=day, venture=venture, device=device, name=device.name, price=1460 * j, deprecation_rate=25, is_deprecated=False)

    def test_dailyusages(self):
        device = utils.get_or_create_device()
        utils.get_or_create_dailydevice(date=datetime.date(2013, 10, 12), venture=self.venture1, device=device, name=device.name, price=100, deprecation_rate=0.25, is_deprecated=False)
        result = Deprecation(start=datetime.date(2013, 10, 10), end=datetime.date(2013, 10, 13), ventures=self.ventures_subset, type=b'dailyusages')
        self.assertEquals(result, {datetime.date(2013, 10, 10): {self.venture1.id: 5, 
                                         self.venture2.id: 10}, 
           datetime.date(2013, 10, 11): {self.venture1.id: 5, 
                                         self.venture2.id: 10}, 
           datetime.date(2013, 10, 12): {self.venture1.id: 6, 
                                         self.venture2.id: 10}, 
           datetime.date(2013, 10, 13): {self.venture1.id: 5, 
                                         self.venture2.id: 10}})

    def test_costs(self):
        result = Deprecation(start=datetime.date(2013, 10, 10), end=datetime.date(2013, 10, 20), ventures=self.ventures_subset)
        self.assertEquals(result, {self.venture1.id: {b'assets_cost': D(b'55'), 
                              b'assets_count': 5.0}, 
           self.venture2.id: {b'assets_cost': D(b'220'), 
                              b'assets_count': 10.0}})

    def test_costs_per_device(self):
        result = Deprecation(start=datetime.date(2013, 10, 10), end=datetime.date(2013, 10, 20), ventures=[
         self.venture1], type=b'costs_per_device')
        expected = dict((v, {b'assets_cost': D(b'11'), b'assets_count': 1.0, b'deprecation_rate': D(b'25'), b'is_deprecated': _(b'No')}) for v in self.ventures_devices[self.venture1.id])
        self.assertEquals(result, expected)

    def test_costs_per_device_partially_deprecated(self):
        venture = utils.get_or_create_venture()
        device = utils.get_or_create_device()
        utils.get_or_create_dailydevice(datetime.date(2013, 10, 10), device, venture, price=1460, deprecation_rate=25, is_deprecated=False)
        utils.get_or_create_dailydevice(datetime.date(2013, 10, 11), device, venture, price=1460, deprecation_rate=25, is_deprecated=True)
        result = Deprecation(start=datetime.date(2013, 10, 10), end=datetime.date(2013, 10, 13), ventures=[
         venture], type=b'costs_per_device')
        self.assertEquals(result, {device.id: {b'assets_cost': D(b'1'), 
                       b'assets_count': 0.5, 
                       b'deprecation_rate': D(b'25'), 
                       b'is_deprecated': _(b'Partially')}})

    def test_costs_per_device_deprecated(self):
        venture = utils.get_or_create_venture()
        device = utils.get_or_create_device()
        utils.get_or_create_dailydevice(datetime.date(2013, 10, 10), device, venture, price=1460, deprecation_rate=25, is_deprecated=True)
        utils.get_or_create_dailydevice(datetime.date(2013, 10, 11), device, venture, price=1460, deprecation_rate=25, is_deprecated=True)
        result = Deprecation(start=datetime.date(2013, 10, 10), end=datetime.date(2013, 10, 13), ventures=[
         venture], type=b'costs_per_device')
        self.assertEquals(result, {device.id: {b'assets_cost': D(b'0'), 
                       b'assets_count': 0.5, 
                       b'deprecation_rate': D(b'25'), 
                       b'is_deprecated': _(b'Yes')}})

    def test_total_cost(self):
        result = Deprecation(start=datetime.date(2013, 10, 10), end=datetime.date(2013, 10, 25), ventures=self.ventures_subset, type=b'total_cost')
        self.assertEquals(result, D(b'325'))

    def test_get_asset_count_and_cost(self):
        result = Deprecation.get_assets_count_and_cost(start=datetime.date(2013, 10, 10), end=datetime.date(2013, 10, 20), ventures=self.ventures_subset)
        self.assertEquals(list(result), [
         {b'assets_cost': D(b'55'), 
            b'assets_count': 55.0, 
            b'pricing_venture': self.venture1.id},
         {b'assets_cost': D(b'220'), 
            b'assets_count': 110.0, 
            b'pricing_venture': self.venture2.id}])

    def test_get_asset_count_and_cost_group_by_device(self):
        venture = utils.get_or_create_venture()
        device1 = utils.get_or_create_device()
        device2 = utils.get_or_create_device()
        utils.get_or_create_dailydevice(datetime.date(2013, 10, 10), device1, venture, price=1460, deprecation_rate=25, is_deprecated=False)
        utils.get_or_create_dailydevice(datetime.date(2013, 10, 11), device2, venture, price=1460, deprecation_rate=25, is_deprecated=False)
        utils.get_or_create_dailydevice(datetime.date(2013, 10, 12), device2, self.venture1, price=1460, deprecation_rate=25, is_deprecated=False)
        result = Deprecation.get_assets_count_and_cost(start=datetime.date(2013, 10, 10), end=datetime.date(2013, 10, 20), ventures=[
         venture], group_by=b'pricing_device')
        self.assertEquals(list(result), [
         {b'assets_cost': D(b'1'), 
            b'assets_count': 1.0, 
            b'pricing_device': device1.id},
         {b'assets_cost': D(b'1'), 
            b'assets_count': 1.0, 
            b'pricing_device': device2.id}])