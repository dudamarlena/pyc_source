# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kula/workspace/ralph_pricing/src/ralph_pricing/tests/report_plugins/test_usage_base.py
# Compiled at: 2014-05-30 05:53:08
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import datetime
from collections import OrderedDict
from dateutil import rrule
from decimal import Decimal as D
from django.test import TestCase
from django.utils.translation import ugettext_lazy as _
from ralph_pricing import models
from ralph_pricing.tests import utils
from ralph_pricing.plugins.reports.usage import UsagePlugin

class TestUsageBasePlugin(TestCase):

    def setUp(self):
        self.usage_type = models.UsageType(name=b'UsageType1', symbol=b'ut1', by_warehouse=False, by_cost=False, type=b'BU')
        self.usage_type.save()
        self.usage_type_cost_wh = models.UsageType(name=b'UsageType2', symbol=b'ut2', by_warehouse=True, by_cost=True, type=b'BU')
        self.usage_type_cost_wh.save()
        self.usage_type_cost_sum = models.UsageType(name=b'UsageType3', symbol=b'ut3', by_warehouse=False, by_cost=True, type=b'BU', by_internet_provider=True)
        self.usage_type_cost_sum.save()
        self.usage_type_average = models.UsageType(name=b'UsageType4', symbol=b'ut4', by_warehouse=False, by_cost=False, type=b'BU', average=True)
        self.usage_type_average.save()
        self.warehouse1 = models.Warehouse(name=b'Warehouse1', show_in_report=True)
        self.warehouse1.save()
        self.warehouse2 = models.Warehouse(name=b'Warehouse2', show_in_report=True)
        self.warehouse2.save()
        self.warehouses = models.Warehouse.objects.all()
        self.net_provider1 = models.InternetProvider(name=b'InternetProvider1')
        self.net_provider1.save()
        self.net_provider2 = models.InternetProvider(name=b'InternetProvider2')
        self.net_provider2.save()
        self.net_providers = models.InternetProvider.objects.all()
        self.venture1 = models.Venture(venture_id=1, name=b'V1', is_active=True)
        self.venture1.save()
        self.venture2 = models.Venture(venture_id=2, name=b'V2', is_active=True)
        self.venture2.save()
        self.venture3 = models.Venture(venture_id=3, name=b'V3', is_active=True)
        self.venture3.save()
        self.venture4 = models.Venture(venture_id=4, name=b'V4', is_active=True)
        self.venture4.save()
        self.ventures_subset = [self.venture1, self.venture2]
        self.ventures = models.Venture.objects.all()
        start = datetime.date(2013, 10, 8)
        end = datetime.date(2013, 10, 22)
        base_usage_types = models.UsageType.objects.filter(type=b'BU')
        self.ventures_devices = {}
        for k, venture in enumerate(self.ventures, start=1):
            device = utils.get_or_create_device()
            self.ventures_devices[venture] = device
            for i, ut in enumerate(base_usage_types, start=1):
                days = rrule.rrule(rrule.DAILY, dtstart=start, until=end)
                for j, day in enumerate(days, start=1):
                    daily_usage = models.DailyUsage(date=day, pricing_venture=venture, pricing_device=device, value=10 * i * k, type=ut)
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
            (3600, 5400), (3600, 1200), (7200, 3600)]]),
         (
          self.usage_type_cost_sum,
          [
           [
            (1000, 2000), (2000, 3000), (4000, 5000)],
           [
            (10000, 20000), (20000, 30000), (40000, 50000)]]),
         (
          self.usage_type_average, [(10, 20), (20, 30), (30, 40)])]

        def add_usage_price(usage_type, prices_costs, net_provider=None, warehouse=None):
            for daterange, price_cost in zip(dates, prices_costs):
                start, end = daterange
                usage_price = models.UsagePrice(type=usage_type, start=start, end=end)
                if warehouse is not None:
                    usage_price.warehouse = warehouse
                if net_provider is not None:
                    usage_price.internet_provider = net_provider
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
                    add_usage_price(ut, prices_wh, warehouse=warehouse)

            elif ut.by_internet_provider:
                for i, prices_ip in enumerate(prices):
                    net_provider = self.net_providers[i]
                    add_usage_price(ut, prices_ip, net_provider=net_provider)

            else:
                add_usage_price(ut, prices)

        return

    def test_incomplete_price(self):
        result = UsagePlugin._incomplete_price(usage_type=self.usage_type, start=datetime.date(2013, 10, 10), end=datetime.date(2013, 10, 20))
        self.assertEquals(result, None)
        return

    def test_incomplete_price_by_warehouse(self):
        result = UsagePlugin._incomplete_price(usage_type=self.usage_type_cost_wh, start=datetime.date(2013, 10, 10), end=datetime.date(2013, 10, 20), warehouse=self.warehouse1)
        self.assertEquals(result, None)
        return

    def test_incomplete_price_no_price(self):
        result = UsagePlugin._incomplete_price(usage_type=self.usage_type, start=datetime.date(2013, 11, 10), end=datetime.date(2013, 11, 20))
        self.assertEquals(result, b'No price')

    def test_incomplete_price_incomplete_price(self):
        result = UsagePlugin._incomplete_price(usage_type=self.usage_type, start=datetime.date(2013, 10, 10), end=datetime.date(2013, 11, 20))
        self.assertEquals(result, b'Incomplete price')

    def test_incomplete_price_internet_providers(self):
        result = UsagePlugin._incomplete_price(usage_type=self.usage_type_cost_sum, start=datetime.date(2013, 10, 10), end=datetime.date(2013, 10, 20))
        self.assertEquals(result, None)
        return

    def test_incomplete_price_internet_providers_incomplete_price(self):
        result = UsagePlugin._incomplete_price(usage_type=self.usage_type_cost_sum, start=datetime.date(2013, 10, 4), end=datetime.date(2013, 10, 25))
        self.assertEquals(result, b'Incomplete price')

    def test_incomplete_price_internet_providers_incomplete_price2(self):
        result = UsagePlugin._incomplete_price(usage_type=self.usage_type_cost_sum, start=datetime.date(2013, 10, 3), end=datetime.date(2013, 10, 28))
        self.assertEquals(result, b'Incomplete price')

    def test_incomplete_price_internet_providers_no_price(self):
        result = UsagePlugin._incomplete_price(usage_type=self.usage_type_cost_sum, start=datetime.date(2013, 10, 26), end=datetime.date(2013, 11, 20))
        self.assertEquals(result, b'No price')

    def test_get_usage_type_cost(self):
        result = UsagePlugin._get_total_cost_by_warehouses(start=datetime.date(2013, 10, 10), end=datetime.date(2013, 10, 20), usage_type=self.usage_type, ventures=self.ventures_subset, forecast=False)
        self.assertEquals(result, [330.0, D(b'6600')])

    def test_get_total_cost(self):
        result = UsagePlugin.total_cost(start=datetime.date(2013, 10, 10), end=datetime.date(2013, 10, 20), usage_type=self.usage_type, ventures=self.ventures_subset, forecast=False)
        self.assertEquals(result, D(b'6600'))

    def test_get_usage_type_cost_forecast(self):
        result = UsagePlugin._get_total_cost_by_warehouses(start=datetime.date(2013, 10, 10), end=datetime.date(2013, 10, 20), usage_type=self.usage_type, ventures=[
         self.venture1], forecast=True)
        self.assertEquals(result, [110.0, D(b'6600')])

    def test_get_usage_type_cost_by_cost(self):
        result = UsagePlugin._get_total_cost_by_warehouses(start=datetime.date(2013, 10, 10), end=datetime.date(2013, 10, 20), usage_type=self.usage_type_cost_wh, ventures=self.ventures_subset, forecast=False)
        self.assertEquals(result, [
         300.0, D(b'2880'), 360.0, D(b'3240'), D(b'6120')])

    def test_get_usage_type_cost_by_cost_forecast(self):
        result = UsagePlugin._get_total_cost_by_warehouses(start=datetime.date(2013, 10, 10), end=datetime.date(2013, 10, 20), usage_type=self.usage_type_cost_wh, ventures=[
         self.venture1], forecast=True)
        self.assertEquals(result, [
         100.0, D(b'1260'), 120.0, D(b'720'), D(b'1980')])

    def test_get_usage_type_cost_sum(self):
        result = UsagePlugin._get_total_cost_by_warehouses(start=datetime.date(2013, 10, 10), end=datetime.date(2013, 10, 20), usage_type=self.usage_type_cost_sum, ventures=self.ventures_subset, forecast=False)
        self.assertEquals(result, [990.0, D(b'16500')])

    def test_get_total_cost_sum(self):
        result = UsagePlugin.total_cost(start=datetime.date(2013, 10, 10), end=datetime.date(2013, 10, 20), usage_type=self.usage_type_cost_sum, ventures=self.ventures_subset, forecast=False)
        self.assertEquals(result, D(b'16500'))

    def test_get_total_cost_sum_whole(self):
        result = UsagePlugin.total_cost(start=datetime.date(2013, 10, 5), end=datetime.date(2013, 10, 25), usage_type=self.usage_type_cost_sum, ventures=self.ventures, forecast=False)
        self.assertEquals(result, D(b'77000'))

    def test_get_total_cost_sum_beyond_usageprices(self):
        result = UsagePlugin.total_cost(start=datetime.date(2013, 10, 1), end=datetime.date(2013, 10, 28), usage_type=self.usage_type_cost_sum, ventures=self.ventures, forecast=False, no_price_msg=True)
        self.assertEquals(result, D(b'77000'))

    def test_get_usage_type_cost_sum_forecast(self):
        result = UsagePlugin._get_total_cost_by_warehouses(start=datetime.date(2013, 10, 10), end=datetime.date(2013, 10, 20), usage_type=self.usage_type_cost_sum, ventures=[
         self.venture1], forecast=True)
        self.assertEquals(result, [330.0, D(b'7920')])

    def test_get_usages(self):
        result = UsagePlugin.costs(start=datetime.date(2013, 10, 10), end=datetime.date(2013, 10, 20), usage_type=self.usage_type, ventures=self.ventures_subset, forecast=False, no_price_msg=False)
        self.assertEquals(result, {1: {b'ut_1_count': 110.0, 
               b'ut_1_cost': D(b'2200')}, 
           2: {b'ut_1_count': 220.0, 
               b'ut_1_cost': D(b'4400')}})

    def test_get_usages_incomplete_price(self):
        result = UsagePlugin.costs(start=datetime.date(2013, 10, 10), end=datetime.date(2013, 10, 30), usage_type=self.usage_type, ventures=self.ventures_subset, forecast=False, no_price_msg=True)
        self.assertEquals(result, {1: {b'ut_1_count': 130.0, 
               b'ut_1_cost': _(b'Incomplete price')}, 
           2: {b'ut_1_count': 260.0, 
               b'ut_1_cost': _(b'Incomplete price')}})

    def test_get_usages_no_price(self):
        start = datetime.date(2013, 11, 8)
        end = datetime.date(2013, 11, 22)
        base_usage_types = models.UsageType.objects.filter(type=b'BU')
        for i, ut in enumerate(base_usage_types, start=1):
            days = rrule.rrule(rrule.DAILY, dtstart=start, until=end)
            for j, day in enumerate(days, start=1):
                for k, venture in enumerate(self.ventures, start=1):
                    daily_usage = models.DailyUsage(date=day, pricing_venture=venture, value=10 * i * k, type=ut)
                    if ut.by_warehouse:
                        daily_usage.warehouse = self.warehouses[(j % len(self.warehouses))]
                    daily_usage.save()

        result = UsagePlugin.costs(start=datetime.date(2013, 11, 10), end=datetime.date(2013, 11, 20), usage_type=self.usage_type, ventures=self.ventures_subset, forecast=False, no_price_msg=True)
        self.assertEquals(result, {1: {b'ut_1_count': 110.0, 
               b'ut_1_cost': _(b'No price')}, 
           2: {b'ut_1_count': 220.0, 
               b'ut_1_cost': _(b'No price')}})

    def test_get_usages_per_warehouse_with_warehouse(self):
        result = UsagePlugin._get_usages_per_warehouse(start=datetime.date(2013, 10, 10), end=datetime.date(2013, 10, 20), usage_type=self.usage_type_cost_wh, ventures=self.ventures_subset, forecast=False)
        self.assertEquals(result, {1: {b'ut_2_count_wh_1': 100.0, 
               b'ut_2_cost_wh_1': D(b'960'), 
               b'ut_2_count_wh_2': 120.0, 
               b'ut_2_cost_wh_2': D(b'1080'), 
               b'ut_2_total_cost': D(b'2040')}, 
           2: {b'ut_2_count_wh_1': 200.0, 
               b'ut_2_cost_wh_1': D(b'1920'), 
               b'ut_2_count_wh_2': 240.0, 
               b'ut_2_cost_wh_2': D(b'2160'), 
               b'ut_2_total_cost': D(b'4080')}})

    def test_get_usages_per_warehouse_by_device(self):
        result = UsagePlugin._get_usages_per_warehouse(start=datetime.date(2013, 10, 10), end=datetime.date(2013, 10, 20), usage_type=self.usage_type_cost_wh, ventures=[
         self.venture1], forecast=False, by_device=True)
        self.assertEquals(result, {self.ventures_devices[self.venture1].id: {b'ut_2_count_wh_1': 100.0, 
                                                     b'ut_2_cost_wh_1': D(b'960'), 
                                                     b'ut_2_count_wh_2': 120.0, 
                                                     b'ut_2_cost_wh_2': D(b'1080'), 
                                                     b'ut_2_total_cost': D(b'2040')}})

    def test_usage_type_average(self):
        result = UsagePlugin.costs(start=datetime.date(2013, 10, 10), end=datetime.date(2013, 10, 20), usage_type=self.usage_type_average, ventures=self.ventures_subset, forecast=False)
        self.assertEquals(result, {1: {b'ut_4_count': 40.0, 
               b'ut_4_cost': D(b'8800')}, 
           2: {b'ut_4_count': 80.0, 
               b'ut_4_cost': D(b'17600')}})

    def test_usage_type_average_without_average(self):
        result = UsagePlugin.costs(start=datetime.date(2013, 10, 10), end=datetime.date(2013, 10, 20), usage_type=self.usage_type_average, ventures=self.ventures_subset, forecast=False, use_average=False)
        self.assertEquals(result, {1: {b'ut_4_count': 440.0, 
               b'ut_4_cost': D(b'8800')}, 
           2: {b'ut_4_count': 880.0, 
               b'ut_4_cost': D(b'17600')}})

    def test_get_usages_by_internet_provider(self):
        result = UsagePlugin._get_usages_per_warehouse(start=datetime.date(2013, 10, 10), end=datetime.date(2013, 10, 20), usage_type=self.usage_type_cost_sum, ventures=self.ventures_subset, forecast=False)
        self.assertEquals(result, {1: {b'ut_3_count': 330.0, 
               b'ut_3_cost': D(b'5500')}, 
           2: {b'ut_3_count': 660.0, 
               b'ut_3_cost': D(b'11000')}})

    def test_get_usages_by_internet_provider_incomplete_price(self):
        result = UsagePlugin._get_usages_per_warehouse(start=datetime.date(2013, 10, 4), end=datetime.date(2013, 10, 26), usage_type=self.usage_type_cost_sum, ventures=self.ventures_subset, forecast=False, no_price_msg=True)
        self.assertEquals(result, {1: {b'ut_3_count': 450.0, 
               b'ut_3_cost': b'Incomplete price'}, 
           2: {b'ut_3_count': 900.0, 
               b'ut_3_cost': b'Incomplete price'}})

    def test_get_dailyusages(self):
        du = models.DailyUsage(date=datetime.date(2013, 10, 11), pricing_venture=self.venture2, pricing_device=utils.get_or_create_device(), value=100, type=self.usage_type)
        du.save()
        result = UsagePlugin(usage_type=self.usage_type, start=datetime.date(2013, 10, 10), end=datetime.date(2013, 10, 13), ventures=self.ventures_subset, type=b'dailyusages')
        self.assertEquals(result, {datetime.date(2013, 10, 10): {self.venture1.id: 10, 
                                         self.venture2.id: 20}, 
           datetime.date(2013, 10, 11): {self.venture1.id: 10, 
                                         self.venture2.id: 120}, 
           datetime.date(2013, 10, 12): {self.venture1.id: 10, 
                                         self.venture2.id: 20}, 
           datetime.date(2013, 10, 13): {self.venture1.id: 10, 
                                         self.venture2.id: 20}})

    def test_schema(self):
        result = UsagePlugin(usage_type=self.usage_type, type=b'schema')
        self.assertEquals(result, OrderedDict([
         (
          b'ut_1_count', {b'name': _(b'UsageType1 count')}),
         (
          b'ut_1_cost',
          {b'name': _(b'UsageType1 cost'), 
             b'currency': True, 
             b'total_cost': True})]))

    def test_schema_with_warehouse(self):
        result = UsagePlugin(usage_type=self.usage_type_cost_wh, type=b'schema')
        self.assertEquals(result, OrderedDict([
         (
          b'ut_2_count_wh_1', {b'name': _(b'UsageType2 count (Warehouse1)')}),
         (
          b'ut_2_cost_wh_1',
          {b'name': _(b'UsageType2 cost (Warehouse1)'), 
             b'currency': True}),
         (
          b'ut_2_count_wh_2', {b'name': _(b'UsageType2 count (Warehouse2)')}),
         (
          b'ut_2_cost_wh_2',
          {b'name': _(b'UsageType2 cost (Warehouse2)'), 
             b'currency': True}),
         (
          b'ut_2_total_cost',
          {b'name': _(b'UsageType2 total cost'), 
             b'currency': True, 
             b'total_cost': True})]))

    def test_usages_schema(self):
        result = UsagePlugin(usage_type=self.usage_type_cost_wh, type=b'dailyusages_header')
        self.assertEquals(result, self.usage_type_cost_wh.name)