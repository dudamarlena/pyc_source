# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kula/workspace/ralph_pricing/src/ralph_pricing/tests/report_plugins/test_base_report_plugin.py
# Compiled at: 2014-06-03 05:10:47
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import datetime, mock
from dateutil import rrule
from decimal import Decimal as D
from django.test import TestCase
from ralph_pricing import models
from ralph_pricing.tests import utils
from ralph_pricing.plugins.reports.base import BaseReportPlugin

class SampleReportPlugin(BaseReportPlugin):

    def costs(self, *args, **kwargs):
        pass

    def schema(self, *args, **kwargs):
        pass

    def total_cost(self, *args, **kwargs):
        pass


class TestBaseReportPlugin(TestCase):

    def setUp(self):
        self.plugin = SampleReportPlugin()
        self.usage_type = models.UsageType(name=b'UsageType1', symbol=b'ut1', by_warehouse=False, by_cost=False, type=b'BU')
        self.usage_type.save()
        self.usage_type_cost_wh = models.UsageType(name=b'UsageType2', symbol=b'ut2', by_warehouse=True, by_cost=True, type=b'BU')
        self.usage_type_cost_wh.save()
        self.warehouse1 = models.Warehouse(name=b'Warehouse1', show_in_report=True)
        self.warehouse1.save()
        self.warehouse2 = models.Warehouse(name=b'Warehouse2', show_in_report=True)
        self.warehouse2.save()
        self.warehouses = models.Warehouse.objects.all()
        self.venture1 = models.Venture(venture_id=1, name=b'V1', is_active=True)
        self.venture1.save()
        self.venture2 = models.Venture(venture_id=2, name=b'V2', is_active=True)
        self.venture2.save()
        self.venture3 = models.Venture(venture_id=3, name=b'V3', is_active=True)
        self.venture3.save()
        self.venture4 = models.Venture(venture_id=4, name=b'V4', is_active=True)
        self.venture4.save()
        self.ventures = models.Venture.objects.all()
        start = datetime.date(2013, 10, 8)
        end = datetime.date(2013, 10, 22)
        base_usage_types = models.UsageType.objects.filter(type=b'BU')
        for i, ut in enumerate(base_usage_types, start=1):
            days = rrule.rrule(rrule.DAILY, dtstart=start, until=end)
            for j, day in enumerate(days, start=1):
                for k, venture in enumerate(self.ventures, start=1):
                    daily_usage = models.DailyUsage(date=day, pricing_venture=venture, value=10 * i * k, type=ut)
                    if ut.by_warehouse:
                        daily_usage.warehouse = self.warehouses[(j % len(self.warehouses))]
                    daily_usage.save()

        dates = [(datetime.date(2013, 10, 5), datetime.date(2013, 10, 12)),
         (
          datetime.date(2013, 10, 13), datetime.date(2013, 10, 17)),
         (
          datetime.date(2013, 10, 18), datetime.date(2013, 10, 25))]
        ut_prices_costs = [
         (
          self.usage_type, [(10, 50), (20, 60), (30, 70)]),
         (
          self.usage_type_cost_wh,
          [
           [
            (3600, 2400), (5400, 5400), (4800, 12000)],
           [
            (3600, 5400), (3600, 1200), (7200, 3600)]])]

        def add_usage_price(usage_type, prices_costs, warehouse=None):
            for daterange, price_cost in zip(dates, prices_costs):
                start, end = daterange
                usage_price = models.UsagePrice(type=usage_type, start=start, end=end)
                if warehouse is not None:
                    usage_price.warehouse = warehouse
                if usage_type.by_cost:
                    usage_price.cost = price_cost[0]
                    usage_price.forecast_cost = price_cost[1]
                else:
                    usage_price.price = price_cost[0]
                    usage_price.forecast_price = price_cost[1]
                usage_price.save()

            return

        for ut, prices in ut_prices_costs:
            if ut.by_warehouse:
                for i, prices_wh in enumerate(prices):
                    warehouse = self.warehouses[i]
                    add_usage_price(ut, prices_wh, warehouse)

            else:
                add_usage_price(ut, prices)

        return

    @mock.patch(b'ralph_pricing.plugins.reports.base.BaseReportPlugin._get_total_usage_in_period')
    def test_get_price_from_cost(self, get_total_usage_in_period_mock):
        get_total_usage_in_period_mock.return_value = 100.0
        usage_price = models.UsagePrice(start=datetime.date(2013, 10, 10), end=datetime.date(2013, 10, 10), cost=2000, type=self.usage_type_cost_wh)
        result = self.plugin._get_price_from_cost(usage_price, False)
        self.assertEquals(result, D(20))
        get_total_usage_in_period_mock.assert_called_with(datetime.date(2013, 10, 10), datetime.date(2013, 10, 10), self.usage_type_cost_wh, None, None)
        return

    @mock.patch(b'ralph_pricing.plugins.reports.base.BaseReportPlugin._get_total_usage_in_period')
    def test_get_price_from_cost_with_warehouse(self, get_total_usage_in_period_mock):
        get_total_usage_in_period_mock.return_value = 100.0
        usage_price = models.UsagePrice(start=datetime.date(2013, 10, 10), end=datetime.date(2013, 10, 10), cost=2000, type=self.usage_type_cost_wh)
        result = self.plugin._get_price_from_cost(usage_price, False, warehouse=self.warehouse1)
        self.assertEquals(result, D(20))
        get_total_usage_in_period_mock.assert_called_with(datetime.date(2013, 10, 10), datetime.date(2013, 10, 10), self.usage_type_cost_wh, self.warehouse1, None)
        return

    @mock.patch(b'ralph_pricing.plugins.reports.base.BaseReportPlugin._get_total_usage_in_period')
    def test_get_price_from_cost_with_forecast(self, get_total_usage_in_period_mock):
        get_total_usage_in_period_mock.return_value = 100.0
        usage_price = models.UsagePrice(start=datetime.date(2013, 10, 10), end=datetime.date(2013, 10, 10), forecast_cost=3000, type=self.usage_type_cost_wh)
        result = self.plugin._get_price_from_cost(usage_price, True)
        self.assertEquals(result, D(30))
        get_total_usage_in_period_mock.assert_called_with(datetime.date(2013, 10, 10), datetime.date(2013, 10, 10), self.usage_type_cost_wh, None, None)
        return

    @mock.patch(b'ralph_pricing.plugins.reports.base.BaseReportPlugin._get_total_usage_in_period')
    def test_get_price_from_cost_total_usage_0(self, get_total_usage_in_period_mock):
        get_total_usage_in_period_mock.return_value = 0.0
        usage_price = models.UsagePrice(start=datetime.date(2013, 10, 10), end=datetime.date(2013, 10, 10), cost=3000, type=self.usage_type_cost_wh)
        result = self.plugin._get_price_from_cost(usage_price, False)
        self.assertEquals(result, D(0))

    def test_get_total_usage_in_period(self):
        result = self.plugin._get_total_usage_in_period(start=datetime.date(2013, 10, 10), end=datetime.date(2013, 10, 20), usage_type=self.usage_type)
        self.assertEquals(result, 1100.0)

    def test_get_total_usage_in_period_with_warehouse(self):
        result = self.plugin._get_total_usage_in_period(start=datetime.date(2013, 10, 10), end=datetime.date(2013, 10, 20), usage_type=self.usage_type_cost_wh, warehouse=self.warehouse2)
        self.assertEquals(result, 1200.0)

    def test_get_total_usage_in_period_with_ventures(self):
        result = self.plugin._get_total_usage_in_period(start=datetime.date(2013, 10, 10), end=datetime.date(2013, 10, 20), usage_type=self.usage_type, ventures=[
         self.venture1])
        self.assertEquals(result, 110.0)

    def test_get_total_usage_in_period_with_ventures_and_warehouse(self):
        result = self.plugin._get_total_usage_in_period(start=datetime.date(2013, 10, 10), end=datetime.date(2013, 10, 20), usage_type=self.usage_type_cost_wh, warehouse=self.warehouse1, ventures=[
         self.venture2])
        self.assertEquals(result, 200.0)

    def test_get_usages_in_period_per_venture(self):
        result = self.plugin._get_usages_in_period_per_venture(start=datetime.date(2013, 10, 10), end=datetime.date(2013, 10, 20), usage_type=self.usage_type)
        self.assertEquals(result, [{b'usage': 110.0, b'pricing_venture': 1}, {b'usage': 220.0, b'pricing_venture': 2}, {b'usage': 330.0, b'pricing_venture': 3}, {b'usage': 440.0, b'pricing_venture': 4}])

    def test_get_usages_in_period_per_venture_with_warehouse(self):
        result = self.plugin._get_usages_in_period_per_venture(start=datetime.date(2013, 10, 10), end=datetime.date(2013, 10, 20), usage_type=self.usage_type_cost_wh, warehouse=self.warehouse1)
        self.assertEquals(result, [{b'usage': 100.0, b'pricing_venture': 1}, {b'usage': 200.0, b'pricing_venture': 2}, {b'usage': 300.0, b'pricing_venture': 3}, {b'usage': 400.0, b'pricing_venture': 4}])

    def test_get_usages_in_period_per_venture_with_ventures(self):
        result = self.plugin._get_usages_in_period_per_venture(start=datetime.date(2013, 10, 10), end=datetime.date(2013, 10, 20), usage_type=self.usage_type, ventures=[
         self.venture1])
        self.assertEquals(result, [{b'usage': 110.0, b'pricing_venture': 1}])

    def test_get_usages_in_period_per_venture_with_warehouse_and_venture(self):
        result = self.plugin._get_usages_in_period_per_venture(start=datetime.date(2013, 10, 10), end=datetime.date(2013, 10, 20), usage_type=self.usage_type_cost_wh, warehouse=self.warehouse2, ventures=[
         self.venture2])
        self.assertEquals(result, [{b'usage': 240.0, b'pricing_venture': 2}])

    def _devices_sample(self):
        self.device1 = utils.get_or_create_device()
        self.device2 = utils.get_or_create_device()
        self.venture_device = utils.get_or_create_venture()
        start = datetime.date(2013, 10, 8)
        end = datetime.date(2013, 10, 20)
        base_usage_types = models.UsageType.objects.filter(type=b'BU')
        for i, device in enumerate([self.device1, self.device2], start=1):
            for j, ut in enumerate(base_usage_types, start=1):
                for k, day in enumerate(rrule.rrule(rrule.DAILY, dtstart=start, until=end)):
                    daily_usage = models.DailyUsage(date=day, pricing_venture=self.venture_device, pricing_device=device, value=10 * i, type=ut)
                    if ut.by_warehouse:
                        daily_usage.warehouse = self.warehouses[(k % len(self.warehouses))]
                    daily_usage.save()

    def test_get_usages_in_period_per_device(self):
        self._devices_sample()
        result = self.plugin._get_usages_in_period_per_device(start=datetime.date(2013, 10, 10), end=datetime.date(2013, 10, 25), usage_type=self.usage_type, ventures=[
         self.venture_device])
        self.assertEquals(result, [
         {b'pricing_device': self.device1.id, 
            b'usage': 110.0},
         {b'pricing_device': self.device2.id, 
            b'usage': 220.0}])

    def test_get_usages_in_period_per_device_with_warehouse(self):
        self._devices_sample()
        result = self.plugin._get_usages_in_period_per_device(start=datetime.date(2013, 10, 10), end=datetime.date(2013, 10, 25), usage_type=self.usage_type_cost_wh, ventures=[
         self.venture_device], warehouse=self.warehouse1)
        self.assertEquals(result, [
         {b'pricing_device': self.device1.id, 
            b'usage': 60.0},
         {b'pricing_device': self.device2.id, 
            b'usage': 120.0}])

    @mock.patch(b'ralph_pricing.plugins.reports.service.BaseReportPlugin._get_usages_in_period_per_venture')
    @mock.patch(b'ralph_pricing.plugins.reports.service.BaseReportPlugin._get_total_usage_in_period')
    def test_distribute_costs(self, total_usage_mock, usages_per_venture_mock):
        percentage = {self.usage_type.id: 20, 
           self.usage_type_cost_wh.id: 80}

        def sample_usages(start, end, usage_type, warehouse=None, ventures=None):
            usages = {self.usage_type.id: [{b'pricing_venture': self.venture1.id, b'usage': 0}, {b'pricing_venture': self.venture2.id, b'usage': 0}, {b'pricing_venture': self.venture3.id, b'usage': 900}, {b'pricing_venture': self.venture4.id, b'usage': 100}], self.usage_type_cost_wh.id: [{b'pricing_venture': self.venture3.id, b'usage': 1200}, {b'pricing_venture': self.venture4.id, b'usage': 400}]}
            return usages[usage_type.id]

        def sample_total_usage(start, end, usage_type):
            total_usages = {self.usage_type.id: 1000, 
               self.usage_type_cost_wh.id: 1600}
            return total_usages[usage_type.id]

        usages_per_venture_mock.side_effect = sample_usages
        total_usage_mock.side_effect = sample_total_usage
        result = self.plugin._distribute_costs(start=datetime.date(2013, 10, 10), end=datetime.date(2013, 10, 20), ventures=self.ventures, cost=10000, percentage=percentage)
        usage_type_count = (b'ut_{0}_count').format(self.usage_type.id)
        usage_type_cost = (b'ut_{0}_cost').format(self.usage_type.id)
        usage_type_cost_wh_count = (b'ut_{0}_count').format(self.usage_type_cost_wh.id)
        usage_type_cost_wh_cost = (b'ut_{0}_cost').format(self.usage_type_cost_wh.id)
        self.assertEquals(result, {self.venture1.id: {usage_type_count: 0, 
                              usage_type_cost: D(0)}, 
           self.venture2.id: {usage_type_count: 0, 
                              usage_type_cost: D(0)}, 
           self.venture3.id: {usage_type_count: 900, 
                              usage_type_cost: D(b'1800'), 
                              usage_type_cost_wh_count: 1200, 
                              usage_type_cost_wh_cost: D(b'6000')}, 
           self.venture4.id: {usage_type_count: 100, 
                              usage_type_cost: D(b'200'), 
                              usage_type_cost_wh_count: 400, 
                              usage_type_cost_wh_cost: D(b'2000')}})
        return