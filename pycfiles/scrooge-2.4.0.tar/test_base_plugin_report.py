# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kula/workspace/ralph_pricing/src/ralph_pricing/tests/reports/test_base_plugin_report.py
# Compiled at: 2014-05-30 05:53:08
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import datetime, mock
from decimal import Decimal as D
from django.test import TestCase
from ralph_pricing import models
from ralph_pricing.tests import utils
from ralph_pricing.views.base_plugin_report import BasePluginReport

class TestBasePluginReport(TestCase):

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

    def test_prepare_field_value_in_data(self):
        """
        Test if field is properly prepared for placing it in report. Value
        in data.
        """
        data = {b'field1': b'1234'}
        rules = {b'currency': False}
        result = BasePluginReport._prepare_field(b'field1', rules, data)
        self.assertEquals(result, (b'1234', D(b'0')))

    def test_prepare_field_value_in_data_currency(self):
        """
        Test if field is properly prepared for placing it in report. Value
        in data.
        """
        data = {b'field1': 1234}
        rules = {b'currency': True, 
           b'total_cost': True}
        result = BasePluginReport._prepare_field(b'field1', rules, data)
        self.assertEquals(result, (b'1234.00', D(b'1234')))

    def test_prepare_field_value_not_in_data_default(self):
        """
        Test if field is properly prepared for placing it in report. Value not
        in data and there is no default rule.
        """
        data = {}
        rules = {b'currency': True, 
           b'total_cost': True, 
           b'default': 3}
        result = BasePluginReport._prepare_field(b'field1', rules, data)
        self.assertEquals(result, (b'3.00', D(b'3')))

    def test_prepare_field_value_not_in_data(self):
        """
        Test if field is properly prepared for placing it in report. Value not
        in data and there is default rule.
        """
        data = {}
        rules = {b'currency': True, 
           b'total_cost': True}
        result = BasePluginReport._prepare_field(b'field1', rules, data)
        self.assertEquals(result, (b'0.00', D(b'0')))

    def test_prepare_field_value_basestring(self):
        """
        Test if field is properly prepared for placing it in report. Value is
        string.
        """
        data = {b'field1': b'123'}
        rules = {b'currency': True, 
           b'total_cost': True}
        result = BasePluginReport._prepare_field(b'field1', rules, data)
        self.assertEquals(result, (b'123', D(b'0')))

    @mock.patch.object(BasePluginReport, b'_get_schema')
    def test_prepare_row(self, get_schema_mock):
        """
        Test if whole row is properly prepared for placing it in report
        """
        data = {b'field1': 123, 
           b'field2': D(b'3'), 
           b'field3': 3123, 
           b'field4': 33}
        get_schema_mock.return_value = utils.sample_schema()
        result = BasePluginReport._prepare_row(data)
        self.assertEquals(result, [
         123, b'3.00', 3123, b'33.00', b'36.00'])