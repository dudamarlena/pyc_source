# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kula/workspace/ralph_pricing/src/ralph_pricing/tests/report_plugins/test_extra_cost.py
# Compiled at: 2014-05-30 05:53:08
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import datetime
from decimal import Decimal as D
from django.test import TestCase
from ralph_pricing.plugins.reports.extracost import ExtraCostPlugin
from ralph_pricing.tests.utils import get_or_create_daily_extra_cost, get_or_create_venture, get_or_create_extra_cost_type

class TestExtraCostReportPlugin(TestCase):

    def setUp(self):
        self.start = datetime.date(year=2014, month=5, day=1)
        self.end = datetime.date(year=2014, month=5, day=2)
        self.venture = get_or_create_venture()
        self.type = get_or_create_extra_cost_type()
        self.value = D(100)
        self.daily_extra_cost = get_or_create_daily_extra_cost(venture=self.venture, type=self.type, value=self.value)

    def test_get_extra_costs(self):
        self.assertEqual(self.venture, ExtraCostPlugin.get_extra_costs(self.start, self.end, [
         self.venture])[0].pricing_venture)
        self.assertEqual(self.type, ExtraCostPlugin.get_extra_costs(self.start, self.end, [
         self.venture])[0].type)

    def test_costs(self):
        self.assertEqual(self.value, ExtraCostPlugin.costs(self.start, self.end, [
         self.venture])[1][(b'extra_cost_{}').format(self.type.id)])
        self.assertEqual(self.value, ExtraCostPlugin.costs(self.start, self.end, [
         self.venture])[1][b'extra_costs_total'])

    def test_schema(self):
        self.assertEqual(True, ExtraCostPlugin.schema()[(b'extra_cost_{}').format(self.type.id)][b'currency'])
        self.assertEqual(self.type.name, ExtraCostPlugin.schema()[(b'extra_cost_{}').format(self.type.id)][b'name'])
        self.assertEqual(True, ExtraCostPlugin.schema()[b'extra_costs_total'][b'total_cost'])
        self.assertEqual(b'Extra Costs Total', ExtraCostPlugin.schema()[b'extra_costs_total'][b'name'])

    def test_total_cost(self):
        self.assertEqual(self.value, ExtraCostPlugin.total_cost(self.start, self.end, [
         self.venture]))