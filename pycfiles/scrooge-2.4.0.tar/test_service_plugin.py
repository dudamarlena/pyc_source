# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kula/workspace/ralph_pricing/src/ralph_pricing/tests/report_plugins/test_service_plugin.py
# Compiled at: 2014-05-30 05:53:08
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import datetime, mock
from collections import OrderedDict
from dateutil import rrule
from decimal import Decimal as D
from django.test import TestCase
from django.utils.translation import ugettext_lazy as _
from ralph_pricing import models
from ralph_pricing.plugins.reports.service import ServicePlugin

class TestServicePlugin(TestCase):

    def setUp(self):
        self.usage_type = models.UsageType(name=b'UsageType1', symbol=b'ut1', by_warehouse=False, by_cost=False, type=b'BU')
        self.usage_type.save()
        self.usage_type_cost_wh = models.UsageType(name=b'UsageType2', symbol=b'ut2', by_warehouse=True, by_cost=True, type=b'BU')
        self.usage_type_cost_wh.save()
        self.service_usage_type1 = models.UsageType(name=b'ServiceUsageType1', symbol=b'sut1', type=b'SU')
        self.service_usage_type1.save()
        self.service_usage_type2 = models.UsageType(name=b'ServiceUsageType2', type=b'SU')
        self.service_usage_type2.save()
        self.warehouse1 = models.Warehouse(name=b'Warehouse1', show_in_report=True)
        self.warehouse1.save()
        self.warehouse2 = models.Warehouse(name=b'Warehouse2', show_in_report=True)
        self.warehouse2.save()
        self.warehouses = models.Warehouse.objects.all()
        self.service = models.Service(name=b'Service1')
        self.service.save()
        self.service.base_usage_types.add(self.usage_type_cost_wh, self.usage_type)
        models.ServiceUsageTypes(usage_type=self.service_usage_type1, service=self.service, start=datetime.date(2013, 10, 1), end=datetime.date(2013, 10, 15), percent=30).save()
        models.ServiceUsageTypes(usage_type=self.service_usage_type2, service=self.service, start=datetime.date(2013, 10, 1), end=datetime.date(2013, 10, 15), percent=70).save()
        models.ServiceUsageTypes(usage_type=self.service_usage_type1, service=self.service, start=datetime.date(2013, 10, 16), end=datetime.date(2013, 10, 30), percent=40).save()
        models.ServiceUsageTypes(usage_type=self.service_usage_type2, service=self.service, start=datetime.date(2013, 10, 16), end=datetime.date(2013, 10, 30), percent=60).save()
        self.service.save()
        self.venture1 = models.Venture(venture_id=1, name=b'V1', is_active=True, service=self.service)
        self.venture1.save()
        self.venture2 = models.Venture(venture_id=2, name=b'V2', is_active=True, service=self.service)
        self.venture2.save()
        self.venture3 = models.Venture(venture_id=3, name=b'V3', is_active=True)
        self.venture3.save()
        self.venture4 = models.Venture(venture_id=4, name=b'V4', is_active=True)
        self.venture4.save()
        self.service_ventures = list(self.service.venture_set.all())
        self.not_service_ventures = list(models.Venture.objects.exclude(id__in=[ i.id for i in self.service_ventures ]))
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

        start = datetime.date(2013, 10, 8)
        end = datetime.date(2013, 10, 22)
        service_usage_types = models.UsageType.objects.filter(type=b'SU')
        for i, ut in enumerate(service_usage_types, start=1):
            days = rrule.rrule(rrule.DAILY, dtstart=start, until=end)
            for j, day in enumerate(days, start=1):
                for k, venture in enumerate(self.not_service_ventures, start=1):
                    daily_usage = models.DailyUsage(date=day, pricing_venture=venture, value=10 * i * k, type=ut)
                    daily_usage.save()

        self.maxDiff = None
        return

    @mock.patch(b'ralph.util.plugin.run')
    def test_get_usage_type_cost(self, plugin_run_mock):
        plugin_run_mock.return_value = 100
        result = ServicePlugin._get_usage_type_cost(start=datetime.date(2013, 10, 10), end=datetime.date(2013, 10, 20), usage_type=self.usage_type, forecast=True, ventures=self.ventures)
        self.assertEquals(result, 100)
        plugin_run_mock.assert_called_with(b'reports', self.usage_type.get_plugin_name(), start=datetime.date(2013, 10, 10), end=datetime.date(2013, 10, 20), usage_type=self.usage_type, forecast=True, ventures=self.ventures, type=b'total_cost')

    @mock.patch(b'ralph.util.plugin.run')
    def test_get_usage_type_cost_with_exception(self, plugin_run_mock):
        for exc in (KeyError(), AttributeError()):
            plugin_run_mock.side_effect = exc
            result = ServicePlugin._get_usage_type_cost(start=datetime.date(2013, 10, 10), end=datetime.date(2013, 10, 20), usage_type=self.usage_type, forecast=True, ventures=self.ventures)
            self.assertEquals(result, 0)

    def test_get_date_ranges_percentage(self):
        result = ServicePlugin._get_date_ranges_percentage(start=datetime.date(2013, 10, 10), end=datetime.date(2013, 10, 20), service=self.service)
        self.assertEquals(result, {(datetime.date(2013, 10, 10), datetime.date(2013, 10, 15)): {3: 30.0, 
                                                                        4: 70.0}, 
           (datetime.date(2013, 10, 16), datetime.date(2013, 10, 20)): {3: 40.0, 
                                                                        4: 60.0}})

    def test_get_date_ranges_percentage2(self):
        self.service = models.Service(name=b'Service2')
        self.service.save()
        self.service.base_usage_types.add(self.usage_type_cost_wh, self.usage_type)
        self.service_usage_type3 = models.UsageType(name=b'ServiceUsageType3', symbol=b'sut3', type=b'SU')
        self.service_usage_type3.save()
        models.ServiceUsageTypes(usage_type=self.service_usage_type1, service=self.service, start=datetime.date(2013, 10, 1), end=datetime.date(2013, 10, 20), percent=50).save()
        models.ServiceUsageTypes(usage_type=self.service_usage_type2, service=self.service, start=datetime.date(2013, 10, 1), end=datetime.date(2013, 10, 10), percent=30).save()
        models.ServiceUsageTypes(usage_type=self.service_usage_type3, service=self.service, start=datetime.date(2013, 10, 1), end=datetime.date(2013, 10, 10), percent=20).save()
        models.ServiceUsageTypes(usage_type=self.service_usage_type2, service=self.service, start=datetime.date(2013, 10, 11), end=datetime.date(2013, 10, 20), percent=10).save()
        models.ServiceUsageTypes(usage_type=self.service_usage_type3, service=self.service, start=datetime.date(2013, 10, 11), end=datetime.date(2013, 10, 30), percent=40).save()
        models.ServiceUsageTypes(usage_type=self.service_usage_type1, service=self.service, start=datetime.date(2013, 10, 21), end=datetime.date(2013, 10, 30), percent=30).save()
        models.ServiceUsageTypes(usage_type=self.service_usage_type2, service=self.service, start=datetime.date(2013, 10, 21), end=datetime.date(2013, 10, 30), percent=30).save()
        self.service.save()
        result = ServicePlugin._get_date_ranges_percentage(start=datetime.date(2013, 10, 5), end=datetime.date(2013, 10, 25), service=self.service)
        self.assertEquals(result, {(datetime.date(2013, 10, 5), datetime.date(2013, 10, 10)): {3: 50.0, 
                                                                       4: 30.0, 
                                                                       5: 20.0}, 
           (datetime.date(2013, 10, 11), datetime.date(2013, 10, 20)): {3: 50.0, 
                                                                        4: 10.0, 
                                                                        5: 40.0}, 
           (datetime.date(2013, 10, 21), datetime.date(2013, 10, 25)): {3: 30.0, 
                                                                        4: 30.0, 
                                                                        5: 40.0}})

    @mock.patch(b'ralph.util.plugin.run')
    def test_get_service_extra_cost(self, plugin_run_mock):
        plugin_run_mock.side_effect = [
         122]
        self.assertEqual(122, ServicePlugin._get_service_extra_cost(datetime.date(2013, 10, 10), datetime.date(2013, 10, 20), [
         self.venture1]))
        plugin_run_mock.side_effect = KeyError()
        self.assertEqual(D(0), ServicePlugin._get_service_extra_cost(datetime.date(2013, 10, 10), datetime.date(2013, 10, 20), [
         self.venture1]))

    def test_get_service_base_usage_types_cost(self):
        result = ServicePlugin._get_service_base_usage_types_cost(start=datetime.date(2013, 10, 10), end=datetime.date(2013, 10, 20), service=self.service, forecast=False, ventures=self.service_ventures)
        self.assertEquals(result, D(b'12720'))

    def test_get_service_base_usage_types_cost_forecast(self):
        result = ServicePlugin._get_service_base_usage_types_cost(start=datetime.date(2013, 10, 10), end=datetime.date(2013, 10, 20), service=self.service, forecast=True, ventures=[
         self.venture1])
        self.assertEquals(result, D(b'8580'))

    @mock.patch(b'ralph.util.plugin.run')
    def test_get_dependent_services_cost(self, plugin_run_mock):
        dependent_service1 = models.Service(name=b'Service2')
        dependent_service1.save()
        dependent_service2 = models.Service(name=b'Service3', use_universal_plugin=False)
        dependent_service2.save()
        self.service.dependency.add(dependent_service1, dependent_service2)
        self.service.save()

        def pl(chain, func_name, type, service, **kwargs):
            data = {b'Service2_schema': {b'sut_1_count': {}, b'sut_1_cost': {b'total_cost': False}, b'sut_2_count': {}, b'sut_2_cost': {b'total_cost': False, b'currency': True}, b'2_service_cost': {b'total_cost': True, b'currency': True}}, b'Service2_costs': {1: {b'sut_1_count': 10, 
                                       b'sut_1_cost': D(100), 
                                       b'2_service_cost': D(100)}, 
                                   2: {b'sut_1_count': 10, 
                                       b'sut_1_cost': D(100), 
                                       b'sut_2_count': 10, 
                                       b'sut_2_cost': D(200), 
                                       b'2_service_cost': D(300)}}, 
               b'Service3_schema': {b'sut_1_count': {}, b'sut_1_cost': {b'total_cost': True, b'currency': True}}, b'Service3_costs': {1: {b'sut_1_count': 10, 
                                       b'sut_1_cost': D(300)}, 
                                   2: {b'sut_1_count': 10, 
                                       b'sut_1_cost': D(500)}}}
            key = (b'{0}_{1}').format(service.name, type)
            return data[key]

        plugin_run_mock.side_effect = pl
        start = datetime.date(2013, 10, 10)
        end = datetime.date(2013, 10, 20)
        forecast = True
        result = ServicePlugin._get_dependent_services_cost(start=start, end=end, service=self.service, forecast=forecast, ventures=self.service_ventures)
        self.assertEquals(result, 1200)
        plugin_run_mock.assert_any_call(b'reports', b'service_plugin', service=dependent_service1, ventures=self.service_ventures, start=start, end=end, forecast=forecast, type=b'costs')
        plugin_run_mock.assert_any_call(b'reports', b'service3', service=dependent_service2, ventures=self.service_ventures, start=start, end=end, forecast=forecast, type=b'costs')

    def test_usage(self):
        result = ServicePlugin(service=self.service, start=datetime.date(2013, 10, 10), end=datetime.date(2013, 10, 20), ventures=self.ventures, forecast=False)
        self.assertEquals(result, {3: {b'sut_3_count': 220.0, 
               b'sut_3_cost': D(b'1510'), 
               b'sut_4_count': 440.0, 
               b'sut_4_cost': D(b'2730'), 
               b'1_service_cost': D(b'4240')}, 
           4: {b'sut_3_count': 440.0, 
               b'sut_3_cost': D(b'3020'), 
               b'sut_4_count': 880.0, 
               b'sut_4_cost': D(b'5460'), 
               b'1_service_cost': D(b'8480')}})

    def test_schema(self):
        result = ServicePlugin(service=self.service, type=b'schema')
        self.assertEquals(result, OrderedDict([
         (
          b'sut_3_count', {b'name': _(b'ServiceUsageType1 count')}),
         (
          b'sut_3_cost',
          {b'name': _(b'ServiceUsageType1 cost'), 
             b'currency': True, 
             b'total_cost': False}),
         (
          b'sut_4_count', {b'name': _(b'ServiceUsageType2 count')}),
         (
          b'sut_4_cost',
          {b'name': _(b'ServiceUsageType2 cost'), 
             b'currency': True, 
             b'total_cost': False}),
         (
          b'1_service_cost',
          {b'name': _(b'Service1 cost'), 
             b'currency': True, 
             b'total_cost': True})]))

    def test_total_cost(self):
        self.assertEqual(D(4240), ServicePlugin.total_cost(datetime.date(2013, 10, 10), datetime.date(2013, 10, 20), self.service, False, [
         self.venture1]))