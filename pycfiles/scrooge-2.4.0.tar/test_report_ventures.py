# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kula/workspace/ralph_pricing/src/ralph_pricing/tests/reports/test_report_ventures.py
# Compiled at: 2014-05-30 05:53:08
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import datetime, mock
from collections import OrderedDict
from decimal import Decimal as D
from django.test import TestCase
from django.utils.translation import ugettext_lazy as _
from ralph_pricing import models
from ralph_pricing.tests import utils
from ralph_pricing.views.ventures import AllVentures

class TestReportVentures(TestCase):

    def setUp(self):
        self.report_start = datetime.date(2013, 4, 20)
        self.report_end = datetime.date(2013, 4, 30)
        self.venture = models.Venture(venture_id=1, name=b'b', is_active=True)
        self.venture.save()
        self.subventure = models.Venture(venture_id=2, parent=self.venture, name=b'bb', is_active=False)
        self.subventure.save()
        self.venture2 = models.Venture(venture_id=3, name=b'a', is_active=True)
        self.venture2.save()
        self.usage_type = models.UsageType(name=b'UT1', symbol=b'ut1')
        self.usage_type.save()
        usage_type2 = models.UsageType(name=b'UT2', symbol=b'ut2', show_in_ventures_report=False)
        usage_type2.save()
        self.warehouse_usage_type = models.UsageType(name=b'UT3', symbol=b'ut3', by_warehouse=True, order=3, use_universal_plugin=False)
        self.warehouse_usage_type.save()
        self.service = models.Service(name=b'Service1')
        self.service.save()

    def test_get_plugins(self):
        """
        Test plugins list based on visible usage types
        """
        plugins = AllVentures.get_plugins()
        self.maxDiff = None
        self.assertEquals(plugins, [
         dict(name=b'Information', plugin_name=b'information'),
         dict(name=b'UT3', plugin_name=self.warehouse_usage_type.get_plugin_name(), plugin_kwargs=dict(usage_type=self.warehouse_usage_type, no_price_msg=True)),
         dict(name=b'UT1', plugin_name=self.usage_type.get_plugin_name(), plugin_kwargs=dict(usage_type=self.usage_type, no_price_msg=True)),
         dict(name=b'Service1', plugin_name=self.service.get_plugin_name(), plugin_kwargs=dict(service=self.service)),
         dict(name=b'ExtraCostsPlugin', plugin_name=b'extra_cost_plugin')])
        return

    def test_get_ventures(self):
        """
        Test if ventures are correctly filtered
        """
        get_ids = lambda l: [ i.id for i in l ]
        ventures1 = AllVentures._get_ventures(is_active=True)
        self.assertEquals(get_ids(ventures1), get_ids([self.venture2, self.venture]))
        ventures1 = AllVentures._get_ventures(is_active=False)
        self.assertEquals(get_ids(ventures1), get_ids([self.venture2, self.venture, self.subventure]))

    @mock.patch(b'ralph.util.plugin.run')
    def test_get_report_data(self, plugin_run_mock):
        """
        Test generating data for whole report
        """

        def pl(chain, func_name, type, **kwargs):
            """
            Mock for plugin run. Should replace every schema and report plugin
            """
            data = {b'information': {b'schema': OrderedDict([
                                          (
                                           b'venture_id', {b'name': b'ID'}),
                                          (
                                           b'venture', {b'name': b'Venture'}),
                                          (
                                           b'department', {b'name': b'Department'})]), 
                                b'costs': {1: {b'venture_id': 1, 
                                               b'venture': b'b', 
                                               b'department': b'aaaa'}, 
                                           3: {b'venture_id': 3, 
                                               b'venture': b'a', 
                                               b'department': b'bbbb'}}}, 
               b'usage_plugin': {b'schema': OrderedDict([
                                           (
                                            b'ut1_count', {b'name': b'UT1 count'}),
                                           (
                                            b'ut1_cost',
                                            {b'name': b'UT1 cost', 
                                               b'currency': True, 
                                               b'total_cost': True})]), 
                                 b'costs': {1: {b'ut1_count': 123, b'ut1_cost': D(b'23.23')}}}, 
               b'ut3': {b'schema': OrderedDict([
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
                        b'costs': {1: {b'ut3_count_warehouse_1': 213, 
                                       b'ut3_cost_warehouse_1': D(b'434.21'), 
                                       b'ut3_count_warehouse_2': 3234, 
                                       b'ut3_cost_warehouse_2': D(b'123.21'), 
                                       b'ut3_cost_total': D(b'557.42')}, 
                                   3: {b'ut3_count_warehouse_1': 267, 
                                       b'ut3_cost_warehouse_1': D(b'4764.21'), 
                                       b'ut3_count_warehouse_2': 36774, 
                                       b'ut3_cost_warehouse_2': _(b'Incomplete price'), 
                                       b'ut3_cost_total': D(b'4764.21')}}}, 
               b'service_plugin': {b'schema': OrderedDict([
                                             (
                                              b'sut_3_count', {b'name': b'UT3 count'}),
                                             (
                                              b'sut_3_cost',
                                              {b'name': b'UT3 cost wh 1', 
                                                 b'currency': True}),
                                             (
                                              b'sut_4_count', {b'name': b'UT4 count'}),
                                             (
                                              b'sut_4_cost',
                                              {b'name': b'UT4 cost', 
                                                 b'currency': True}),
                                             (
                                              b'1_service_cost',
                                              {b'name': b'Service1 cost', 
                                                 b'currency': True, 
                                                 b'total_cost': True})]), 
                                   b'costs': {1: {b'sut_4_count': 40.0, 
                                                  b'sut_4_cost': D(b'2212.11'), 
                                                  b'1_service_cost': D(b'2212.11')}, 
                                              3: {b'sut_3_count': 10.0, 
                                                  b'sut_3_cost': D(b'20.22'), 
                                                  b'sut_4_count': 20.0, 
                                                  b'sut_4_cost': D(b'1212.11'), 
                                                  b'1_service_cost': D(b'1232.33')}}}}
            result = data.get(func_name, {}).get(type)
            if result is not None:
                return result
            else:
                raise KeyError()
                return

        plugin_run_mock.side_effect = pl
        result = None
        for percent, result in AllVentures.get_data(self.report_start, self.report_end, is_active=True):
            pass

        self.assertEquals(result, [
         [
          3,
          b'a',
          b'bbbb',
          267,
          36774,
          b'4764.21',
          b'Incomplete price',
          b'4764.21',
          0.0,
          b'0.00',
          10.0,
          b'20.22',
          20.0,
          b'1212.11',
          b'1232.33',
          b'5996.54'],
         [
          1,
          b'b',
          b'aaaa',
          213.0,
          3234.0,
          b'434.21',
          b'123.21',
          b'557.42',
          123.0,
          b'23.23',
          0.0,
          b'0.00',
          40.0,
          b'2212.11',
          b'2212.11',
          b'2792.76']])
        return

    @mock.patch.object(AllVentures, b'_get_schema')
    def test_get_header(self, get_schema_mock):
        """
        Test getting headers for report
        """
        get_schema_mock.return_value = utils.sample_schema()
        result = AllVentures.get_header()
        self.assertEquals(result, [
         [
          b'Field1',
          b'Field2 - PLN',
          b'Field3',
          b'Field4 - PLN',
          b'Total cost']])