# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kula/workspace/ralph_pricing/src/ralph_pricing/tests/report_plugins/test_team_plugin.py
# Compiled at: 2014-05-30 05:53:08
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import mock
from collections import OrderedDict
from datetime import date
from decimal import Decimal as D
from django.test import TestCase
from django.utils.translation import ugettext_lazy as _
from ralph_pricing import models
from ralph_pricing.plugins.reports.team import Team

class TestTeamPlugin(TestCase):

    def setUp(self):
        self.plugin = Team
        self.usage_type = models.UsageType(name=b'Teams', symbol=b'Teams', by_team=True, type=b'BU')
        self.usage_type.save()
        self.team_time = models.Team(name=b'T1', billing_type=b'TIME')
        self.team_time.save()
        self.team_devices_cores = models.Team(name=b'T2', billing_type=b'DEVICES_CORES')
        self.team_devices_cores.save()
        self.team_devices = models.Team(name=b'T3', billing_type=b'DEVICES')
        self.team_devices.save()
        self.team_distribute = models.Team(name=b'T4', billing_type=b'DISTRIBUTE')
        self.team_distribute.save()
        self.teams = models.Team.objects.all()
        self.daterange1 = models.TeamDaterange(team=self.team_time, start=date(2013, 10, 1), end=date(2013, 10, 10))
        self.daterange1.save()
        self.daterange2 = models.TeamDaterange(team=self.team_time, start=date(2013, 10, 11), end=date(2013, 10, 30))
        self.daterange2.save()
        up = models.UsagePrice(type=self.usage_type, cost=300, forecast_cost=600, start=date(2013, 10, 1), end=date(2013, 10, 15), team=self.team_time, team_members_count=10)
        up.save()
        up = models.UsagePrice(type=self.usage_type, cost=900, forecast_cost=450, start=date(2013, 10, 16), end=date(2013, 10, 30), team=self.team_time, team_members_count=20)
        up.save()
        up = models.UsagePrice(type=self.usage_type, cost=300, forecast_cost=600, start=date(2013, 10, 1), end=date(2013, 10, 30), team=self.team_devices_cores, team_members_count=20)
        up.save()
        up = models.UsagePrice(type=self.usage_type, cost=800, forecast_cost=1600, start=date(2013, 10, 1), end=date(2013, 10, 10), team=self.team_devices, team_members_count=20)
        up.save()
        up = models.UsagePrice(type=self.usage_type, cost=100, forecast_cost=200, start=date(2013, 10, 11), end=date(2013, 10, 30), team=self.team_devices, team_members_count=10)
        up.save()
        up = models.UsagePrice(type=self.usage_type, cost=3000, forecast_cost=1500, start=date(2013, 10, 1), end=date(2013, 10, 15), team=self.team_distribute, team_members_count=10)
        up.save()
        up = models.UsagePrice(type=self.usage_type, cost=6000, forecast_cost=3000, start=date(2013, 10, 16), end=date(2013, 10, 30), team=self.team_distribute, team_members_count=10)
        up.save()
        self.venture1 = models.Venture(name=b'V1', venture_id=1, is_active=True)
        self.venture1.save()
        self.venture2 = models.Venture(name=b'V2', venture_id=2, is_active=True)
        self.venture2.save()
        self.venture3 = models.Venture(name=b'V3', venture_id=3, is_active=True)
        self.venture3.save()
        self.ventures = models.Venture.objects.all()
        percentage = (
         (
          self.daterange1, [30, 30, 40]),
         (
          self.daterange2, [20, 50, 30]))
        for team_daterange, percent in percentage:
            for venture, p in zip(self.ventures, percent):
                tvp = models.TeamVenturePercent(team_daterange=team_daterange, venture=venture, percent=p)
                tvp.save()

    def test_get_team_dateranges_percentage(self):
        result = self.plugin._get_team_dateranges_percentage(start=date(2013, 10, 3), end=date(2013, 10, 27), team=self.team_time)
        self.assertEquals(result, {(date(2013, 10, 3), date(2013, 10, 10)): {self.venture1.id: 30, 
                                                     self.venture2.id: 30, 
                                                     self.venture3.id: 40}, 
           (date(2013, 10, 11), date(2013, 10, 27)): {self.venture1.id: 20, 
                                                      self.venture2.id: 50, 
                                                      self.venture3.id: 30}})

    def test_get_teams_dateranges_members_count(self):
        result = self.plugin._get_teams_dateranges_members_count(start=date(2013, 10, 3), end=date(2013, 10, 27), teams=self.teams)
        self.assertEquals(result, {(date(2013, 10, 3), date(2013, 10, 10)): {self.team_time.id: 10, 
                                                     self.team_devices_cores.id: 20, 
                                                     self.team_devices.id: 20, 
                                                     self.team_distribute.id: 10}, 
           (date(2013, 10, 11), date(2013, 10, 15)): {self.team_time.id: 10, 
                                                      self.team_devices_cores.id: 20, 
                                                      self.team_devices.id: 10, 
                                                      self.team_distribute.id: 10}, 
           (date(2013, 10, 16), date(2013, 10, 27)): {self.team_time.id: 20, 
                                                      self.team_devices_cores.id: 20, 
                                                      self.team_devices.id: 10, 
                                                      self.team_distribute.id: 10}})

    def test_team_time_cost(self):
        result = self.plugin._get_team_cost_per_venture(start=date(2013, 10, 3), end=date(2013, 10, 27), team=self.team_time, usage_type=self.usage_type, ventures=self.ventures, forecast=False)
        cost_key = (b'ut_{0}_team_{1}_cost').format(self.usage_type.id, self.team_time.id)
        self.assertEquals(result, {self.venture1.id: {cost_key: D(b'212')}, 
           self.venture2.id: {cost_key: D(b'458')}, 
           self.venture3.id: {cost_key: D(b'310')}})

    def test_team_time_cost_incomplete_price(self):
        result = self.plugin._get_team_cost_per_venture(start=date(2013, 10, 3), end=date(2013, 11, 5), team=self.team_time, usage_type=self.usage_type, ventures=self.ventures, forecast=False, no_price_msg=True)
        cost_key = (b'ut_{0}_team_{1}_cost').format(self.usage_type.id, self.team_time.id)
        self.assertEquals(result, {self.venture1.id: {cost_key: _(b'Incomplete price')}, 
           self.venture2.id: {cost_key: _(b'Incomplete price')}, 
           self.venture3.id: {cost_key: _(b'Incomplete price')}})

    def test_team_time_cost_no_price(self):
        daterange = models.TeamDaterange(team=self.team_time, start=date(2013, 11, 1), end=date(2013, 11, 10))
        daterange.save()
        for venture, percent in zip(self.ventures, [30, 20, 50]):
            tvp = models.TeamVenturePercent(team_daterange=daterange, venture=venture, percent=percent)
            tvp.save()

        result = self.plugin._get_team_cost_per_venture(start=date(2013, 11, 3), end=date(2013, 11, 5), team=self.team_time, usage_type=self.usage_type, ventures=self.ventures, forecast=False, no_price_msg=True)
        cost_key = (b'ut_{0}_team_{1}_cost').format(self.usage_type.id, self.team_time.id)
        self.assertEquals(result, {self.venture1.id: {cost_key: _(b'No price')}, 
           self.venture2.id: {cost_key: _(b'No price')}, 
           self.venture3.id: {cost_key: _(b'No price')}})

    def test_team_time_cost_forecast(self):
        result = self.plugin._get_team_cost_per_venture(start=date(2013, 10, 3), end=date(2013, 10, 27), team=self.team_time, usage_type=self.usage_type, ventures=self.ventures, forecast=True)
        cost_key = (b'ut_{0}_team_{1}_cost').format(self.usage_type.id, self.team_time.id)
        self.assertEquals(result, {self.venture1.id: {cost_key: D(b'208')}, 
           self.venture2.id: {cost_key: D(b'376')}, 
           self.venture3.id: {cost_key: D(b'296')}})

    @mock.patch(b'ralph_pricing.plugins.reports.team.Team._get_total_cores_count')
    @mock.patch(b'ralph_pricing.plugins.reports.team.Team._get_cores_count_by_venture')
    @mock.patch(b'ralph_pricing.plugins.reports.team.Team._get_total_devices_count')
    @mock.patch(b'ralph_pricing.plugins.reports.team.Team._get_devices_count_by_venture')
    def test_team_devices_cores_cost(self, devices_count_mock, total_devices_mock, cores_count_mock, total_cores_mock):
        devices_count_mock.return_value = {self.venture1.id: 200, 
           self.venture2.id: 200, 
           self.venture3.id: 100}
        total_devices_mock.return_value = 500
        cores_count_mock.return_value = {self.venture1.id: 20, 
           self.venture2.id: 40, 
           self.venture3.id: 40}
        total_cores_mock.return_value = 100
        result = self.plugin._get_team_cost_per_venture(start=date(2013, 10, 3), end=date(2013, 10, 27), team=self.team_devices_cores, usage_type=self.usage_type, ventures=self.ventures, forecast=False)
        cost_key = (b'ut_{0}_team_{1}_cost').format(self.usage_type.id, self.team_devices_cores.id)
        self.assertEquals(result, {self.venture1.id: {cost_key: D(b'75')}, 
           self.venture2.id: {cost_key: D(b'100')}, 
           self.venture3.id: {cost_key: D(b'75')}})

    @mock.patch(b'ralph_pricing.plugins.reports.team.Team._get_total_cores_count')
    @mock.patch(b'ralph_pricing.plugins.reports.team.Team._get_cores_count_by_venture')
    @mock.patch(b'ralph_pricing.plugins.reports.team.Team._get_total_devices_count')
    @mock.patch(b'ralph_pricing.plugins.reports.team.Team._get_devices_count_by_venture')
    def test_team_devices_cores_cost_forecast(self, devices_count_mock, total_devices_mock, cores_count_mock, total_cores_mock):
        devices_count_mock.return_value = {self.venture1.id: 200, 
           self.venture2.id: 200, 
           self.venture3.id: 100}
        total_devices_mock.return_value = 500
        cores_count_mock.return_value = {self.venture1.id: 20, 
           self.venture2.id: 40, 
           self.venture3.id: 40}
        total_cores_mock.return_value = 100
        result = self.plugin._get_team_cost_per_venture(start=date(2013, 10, 3), end=date(2013, 10, 27), team=self.team_devices_cores, usage_type=self.usage_type, ventures=self.ventures, forecast=True)
        cost_key = (b'ut_{0}_team_{1}_cost').format(self.usage_type.id, self.team_devices_cores.id)
        self.assertEquals(result, {self.venture1.id: {cost_key: D(b'150')}, 
           self.venture2.id: {cost_key: D(b'200')}, 
           self.venture3.id: {cost_key: D(b'150')}})

    @mock.patch(b'ralph_pricing.plugins.reports.team.Team._get_total_cores_count')
    @mock.patch(b'ralph_pricing.plugins.reports.team.Team._get_cores_count_by_venture')
    @mock.patch(b'ralph_pricing.plugins.reports.team.Team._get_total_devices_count')
    @mock.patch(b'ralph_pricing.plugins.reports.team.Team._get_devices_count_by_venture')
    def test_team_devices_cores_cost_incomplete_price(self, devices_count_mock, total_devices_mock, cores_count_mock, total_cores_mock):
        devices_count_mock.return_value = {self.venture1.id: 200, 
           self.venture2.id: 200, 
           self.venture3.id: 100}
        total_devices_mock.return_value = 500
        cores_count_mock.return_value = {self.venture1.id: 20, 
           self.venture2.id: 40, 
           self.venture3.id: 40}
        total_cores_mock.return_value = 100
        result = self.plugin._get_team_cost_per_venture(start=date(2013, 10, 3), end=date(2013, 11, 5), team=self.team_devices_cores, usage_type=self.usage_type, ventures=self.ventures, forecast=False, no_price_msg=True)
        cost_key = (b'ut_{0}_team_{1}_cost').format(self.usage_type.id, self.team_devices_cores.id)
        self.assertEquals(result, {self.venture1.id: {cost_key: _(b'Incomplete price')}, 
           self.venture2.id: {cost_key: _(b'Incomplete price')}, 
           self.venture3.id: {cost_key: _(b'Incomplete price')}})

    @mock.patch(b'ralph_pricing.plugins.reports.team.Team._get_total_cores_count')
    @mock.patch(b'ralph_pricing.plugins.reports.team.Team._get_cores_count_by_venture')
    @mock.patch(b'ralph_pricing.plugins.reports.team.Team._get_total_devices_count')
    @mock.patch(b'ralph_pricing.plugins.reports.team.Team._get_devices_count_by_venture')
    def test_team_devices_cores_cost_no_price(self, devices_count_mock, total_devices_mock, cores_count_mock, total_cores_mock):
        devices_count_mock.return_value = {self.venture1.id: 30, 
           self.venture2.id: 30, 
           self.venture3.id: 60}
        total_devices_mock.return_value = 120
        cores_count_mock.return_value = {self.venture1.id: 30, 
           self.venture2.id: 60, 
           self.venture3.id: 60}
        total_cores_mock.return_value = 150
        result = self.plugin._get_team_cost_per_venture(start=date(2013, 11, 3), end=date(2013, 11, 5), team=self.team_devices_cores, usage_type=self.usage_type, ventures=self.ventures, forecast=False, no_price_msg=True)
        cost_key = (b'ut_{0}_team_{1}_cost').format(self.usage_type.id, self.team_devices_cores.id)
        self.assertEquals(result, {self.venture1.id: {cost_key: _(b'No price')}, 
           self.venture2.id: {cost_key: _(b'No price')}, 
           self.venture3.id: {cost_key: _(b'No price')}})

    @mock.patch(b'ralph_pricing.plugins.reports.team.Team._get_total_devices_count')
    @mock.patch(b'ralph_pricing.plugins.reports.team.Team._get_devices_count_by_venture')
    def test_team_devices_cost(self, devices_count_mock, total_devices_mock):
        devices_count_mock.return_value = {self.venture1.id: 200, 
           self.venture2.id: 200, 
           self.venture3.id: 100}
        total_devices_mock.return_value = 500
        result = self.plugin._get_team_cost_per_venture(start=date(2013, 10, 3), end=date(2013, 10, 27), team=self.team_devices, usage_type=self.usage_type, ventures=self.ventures, forecast=False)
        cost_key = (b'ut_{0}_team_{1}_cost').format(self.usage_type.id, self.team_devices.id)
        self.assertEquals(result, {self.venture1.id: {cost_key: D(b'290')}, 
           self.venture2.id: {cost_key: D(b'290')}, 
           self.venture3.id: {cost_key: D(b'145')}})

    @mock.patch(b'ralph_pricing.plugins.reports.team.Team._get_total_devices_count')
    @mock.patch(b'ralph_pricing.plugins.reports.team.Team._get_devices_count_by_venture')
    def test_team_devices_cost_forecast(self, devices_count_mock, total_devices_mock):
        devices_count_mock.return_value = {self.venture1.id: 30, 
           self.venture2.id: 180, 
           self.venture3.id: 90}
        total_devices_mock.return_value = 300
        result = self.plugin._get_team_cost_per_venture(start=date(2013, 10, 3), end=date(2013, 10, 27), team=self.team_devices, usage_type=self.usage_type, ventures=self.ventures, forecast=True)
        cost_key = (b'ut_{0}_team_{1}_cost').format(self.usage_type.id, self.team_devices.id)
        self.assertEquals(result, {self.venture1.id: {cost_key: D(b'145')}, 
           self.venture2.id: {cost_key: D(b'870')}, 
           self.venture3.id: {cost_key: D(b'435')}})

    @mock.patch(b'ralph_pricing.plugins.reports.team.Team._get_total_devices_count')
    @mock.patch(b'ralph_pricing.plugins.reports.team.Team._get_devices_count_by_venture')
    def test_team_devices_cost_incomplete_price(self, devices_count_mock, total_devices_mock):
        devices_count_mock.return_value = {self.venture1.id: 200, 
           self.venture2.id: 200, 
           self.venture3.id: 100}
        total_devices_mock.return_value = 500
        result = self.plugin._get_team_cost_per_venture(start=date(2013, 10, 20), end=date(2013, 11, 5), team=self.team_devices, usage_type=self.usage_type, ventures=self.ventures, forecast=False, no_price_msg=True)
        cost_key = (b'ut_{0}_team_{1}_cost').format(self.usage_type.id, self.team_devices.id)
        self.assertEquals(result, {self.venture1.id: {cost_key: _(b'Incomplete price')}, 
           self.venture2.id: {cost_key: _(b'Incomplete price')}, 
           self.venture3.id: {cost_key: _(b'Incomplete price')}})

    @mock.patch(b'ralph_pricing.plugins.reports.team.Team._get_total_devices_count')
    @mock.patch(b'ralph_pricing.plugins.reports.team.Team._get_devices_count_by_venture')
    def test_team_devices_cost_no_price(self, devices_count_mock, total_devices_mock):
        devices_count_mock.return_value = {self.venture1.id: 30, 
           self.venture2.id: 30, 
           self.venture3.id: 60}
        total_devices_mock.return_value = 120
        result = self.plugin._get_team_cost_per_venture(start=date(2013, 11, 3), end=date(2013, 11, 5), team=self.team_devices, usage_type=self.usage_type, ventures=self.ventures, forecast=False, no_price_msg=True)
        cost_key = (b'ut_{0}_team_{1}_cost').format(self.usage_type.id, self.team_devices.id)
        self.assertEquals(result, {self.venture1.id: {cost_key: _(b'No price')}, 
           self.venture2.id: {cost_key: _(b'No price')}, 
           self.venture3.id: {cost_key: _(b'No price')}})

    @mock.patch(b'ralph_pricing.plugins.reports.team.Team._get_total_cores_count')
    @mock.patch(b'ralph_pricing.plugins.reports.team.Team._get_cores_count_by_venture')
    @mock.patch(b'ralph_pricing.plugins.reports.team.Team._get_total_devices_count')
    @mock.patch(b'ralph_pricing.plugins.reports.team.Team._get_devices_count_by_venture')
    def test_team_distribute_cost(self, devices_count_mock, total_devices_mock, cores_count_mock, total_cores_mock):
        devices_count_mock.return_value = {self.venture1.id: 30, 
           self.venture2.id: 30, 
           self.venture3.id: 60}
        total_devices_mock.return_value = 120
        cores_count_mock.return_value = {self.venture1.id: 30, 
           self.venture2.id: 60, 
           self.venture3.id: 60}
        total_cores_mock.return_value = 150
        result = self.plugin._get_team_cost_per_venture(start=date(2013, 10, 3), end=date(2013, 10, 27), team=self.team_distribute, usage_type=self.usage_type, ventures=self.ventures, forecast=False, no_price_msg=True)
        cost_key = (b'ut_{0}_team_{1}_cost').format(self.usage_type.id, self.team_distribute.id)
        self.assertEquals(result, {self.venture1.id: {cost_key: D(b'1681')}, 
           self.venture2.id: {cost_key: D(b'2638')}, 
           self.venture3.id: {cost_key: D(b'3081')}})

    @mock.patch(b'ralph_pricing.plugins.reports.team.Team._get_total_cores_count')
    @mock.patch(b'ralph_pricing.plugins.reports.team.Team._get_cores_count_by_venture')
    @mock.patch(b'ralph_pricing.plugins.reports.team.Team._get_total_devices_count')
    @mock.patch(b'ralph_pricing.plugins.reports.team.Team._get_devices_count_by_venture')
    def test_team_distribute_cost_forecast(self, devices_count_mock, total_devices_mock, cores_count_mock, total_cores_mock):
        devices_count_mock.return_value = {self.venture1.id: 30, 
           self.venture2.id: 30, 
           self.venture3.id: 60}
        total_devices_mock.return_value = 120
        cores_count_mock.return_value = {self.venture1.id: 30, 
           self.venture2.id: 60, 
           self.venture3.id: 60}
        total_cores_mock.return_value = 150
        result = self.plugin._get_team_cost_per_venture(start=date(2013, 10, 3), end=date(2013, 10, 27), team=self.team_distribute, usage_type=self.usage_type, ventures=self.ventures, forecast=True, no_price_msg=True)
        cost_key = (b'ut_{0}_team_{1}_cost').format(self.usage_type.id, self.team_distribute.id)
        self.assertEquals(result, {self.venture1.id: {cost_key: D(b'840.5')}, 
           self.venture2.id: {cost_key: D(b'1319')}, 
           self.venture3.id: {cost_key: D(b'1540.5')}})

    @mock.patch(b'ralph_pricing.plugins.reports.team.Team._get_total_cores_count')
    @mock.patch(b'ralph_pricing.plugins.reports.team.Team._get_cores_count_by_venture')
    @mock.patch(b'ralph_pricing.plugins.reports.team.Team._get_total_devices_count')
    @mock.patch(b'ralph_pricing.plugins.reports.team.Team._get_devices_count_by_venture')
    def test_team_distribute_cost_incomplete_price(self, devices_count_mock, total_devices_mock, cores_count_mock, total_cores_mock):
        devices_count_mock.return_value = {self.venture1.id: 30, 
           self.venture2.id: 30, 
           self.venture3.id: 60}
        total_devices_mock.return_value = 120
        cores_count_mock.return_value = {self.venture1.id: 30, 
           self.venture2.id: 60, 
           self.venture3.id: 60}
        total_cores_mock.return_value = 150
        result = self.plugin._get_team_cost_per_venture(start=date(2013, 10, 3), end=date(2013, 11, 5), team=self.team_distribute, usage_type=self.usage_type, ventures=self.ventures, forecast=False, no_price_msg=True)
        cost_key = (b'ut_{0}_team_{1}_cost').format(self.usage_type.id, self.team_distribute.id)
        self.assertEquals(result, {self.venture1.id: {cost_key: _(b'Incomplete price')}, 
           self.venture2.id: {cost_key: _(b'Incomplete price')}, 
           self.venture3.id: {cost_key: _(b'Incomplete price')}})

    @mock.patch(b'ralph_pricing.plugins.reports.team.Team._get_total_cores_count')
    @mock.patch(b'ralph_pricing.plugins.reports.team.Team._get_cores_count_by_venture')
    @mock.patch(b'ralph_pricing.plugins.reports.team.Team._get_total_devices_count')
    @mock.patch(b'ralph_pricing.plugins.reports.team.Team._get_devices_count_by_venture')
    def test_team_distribute_cost_no_price(self, devices_count_mock, total_devices_mock, cores_count_mock, total_cores_mock):
        devices_count_mock.return_value = {self.venture1.id: 30, 
           self.venture2.id: 30, 
           self.venture3.id: 60}
        total_devices_mock.return_value = 120
        cores_count_mock.return_value = {self.venture1.id: 30, 
           self.venture2.id: 60, 
           self.venture3.id: 60}
        total_cores_mock.return_value = 150
        result = self.plugin._get_team_cost_per_venture(start=date(2013, 11, 3), end=date(2013, 11, 5), team=self.team_distribute, usage_type=self.usage_type, ventures=self.ventures, forecast=False, no_price_msg=True)
        cost_key = (b'ut_{0}_team_{1}_cost').format(self.usage_type.id, self.team_distribute.id)
        self.assertEquals(result, {self.venture1.id: {cost_key: _(b'No price')}, 
           self.venture2.id: {cost_key: _(b'No price')}, 
           self.venture3.id: {cost_key: _(b'No price')}})

    @mock.patch(b'ralph_pricing.plugins.reports.team.Team._get_total_cores_count')
    @mock.patch(b'ralph_pricing.plugins.reports.team.Team._get_cores_count_by_venture')
    @mock.patch(b'ralph_pricing.plugins.reports.team.Team._get_total_devices_count')
    @mock.patch(b'ralph_pricing.plugins.reports.team.Team._get_devices_count_by_venture')
    def test_usages(self, devices_count_mock, total_devices_mock, cores_count_mock, total_cores_mock):
        devices_count_mock.return_value = {self.venture1.id: 200, 
           self.venture2.id: 200, 
           self.venture3.id: 100}
        total_devices_mock.return_value = 500
        cores_count_mock.return_value = {self.venture1.id: 20, 
           self.venture2.id: 40, 
           self.venture3.id: 40}
        total_cores_mock.return_value = 100
        result = self.plugin.costs(start=date(2013, 10, 3), end=date(2013, 10, 27), usage_type=self.usage_type, ventures=self.ventures, forecast=False, no_price_msg=True)
        self.assertEquals(result, {self.venture1.id: {b'ut_1_team_1_cost': D(b'212'), 
                              b'ut_1_team_2_cost': D(b'75'), 
                              b'ut_1_team_3_cost': D(b'290'), 
                              b'ut_1_team_4_cost': D(b'2188'), 
                              b'ut_1_total_cost': D(b'2765')}, 
           self.venture2.id: {b'ut_1_team_1_cost': D(b'458'), 
                              b'ut_1_team_2_cost': D(b'100'), 
                              b'ut_1_team_3_cost': D(b'290'), 
                              b'ut_1_team_4_cost': D(b'3145'), 
                              b'ut_1_total_cost': D(b'3993')}, 
           self.venture3.id: {b'ut_1_team_1_cost': D(b'310'), 
                              b'ut_1_team_2_cost': D(b'75'), 
                              b'ut_1_team_3_cost': D(b'145'), 
                              b'ut_1_team_4_cost': D(b'2067'), 
                              b'ut_1_total_cost': D(b'2597')}})

    @mock.patch(b'ralph_pricing.plugins.reports.team.Team._get_total_cores_count')
    @mock.patch(b'ralph_pricing.plugins.reports.team.Team._get_cores_count_by_venture')
    @mock.patch(b'ralph_pricing.plugins.reports.team.Team._get_total_devices_count')
    @mock.patch(b'ralph_pricing.plugins.reports.team.Team._get_devices_count_by_venture')
    def test_usages_subventures(self, devices_count_mock, total_devices_mock, cores_count_mock, total_cores_mock):
        devices_count_mock.return_value = {self.venture1.id: 200}
        total_devices_mock.return_value = 500
        cores_count_mock.return_value = {self.venture1.id: 20}
        total_cores_mock.return_value = 100
        result = self.plugin.costs(start=date(2013, 10, 3), end=date(2013, 10, 27), usage_type=self.usage_type, ventures=[
         self.venture1], forecast=False, no_price_msg=True)
        self.assertEquals(result, {self.venture1.id: {b'ut_1_team_1_cost': D(b'212'), 
                              b'ut_1_team_2_cost': D(b'75'), 
                              b'ut_1_team_3_cost': D(b'290'), 
                              b'ut_1_team_4_cost': D(b'2188'), 
                              b'ut_1_total_cost': D(b'2765')}})

    @mock.patch(b'ralph_pricing.plugins.reports.team.Team._get_total_cores_count')
    @mock.patch(b'ralph_pricing.plugins.reports.team.Team._get_cores_count_by_venture')
    @mock.patch(b'ralph_pricing.plugins.reports.team.Team._get_total_devices_count')
    @mock.patch(b'ralph_pricing.plugins.reports.team.Team._get_devices_count_by_venture')
    def test_total_cost(self, devices_count_mock, total_devices_mock, cores_count_mock, total_cores_mock):
        devices_count_mock.return_value = {self.venture1.id: 200}
        total_devices_mock.return_value = 500
        cores_count_mock.return_value = {self.venture1.id: 20}
        total_cores_mock.return_value = 100
        result = self.plugin.total_cost(start=date(2013, 10, 3), end=date(2013, 10, 27), usage_type=self.usage_type, ventures=[
         self.venture1], forecast=False, no_price_msg=True)
        self.assertEquals(result, D(b'2765'))

    def test_schema(self):
        result = self.plugin.schema(self.usage_type)
        ut_id = self.usage_type.id
        self.assertEquals(result, OrderedDict([
         (
          (b'ut_{0}_team_{1}_cost').format(ut_id, self.team_time.id),
          {b'name': _((b'{0} - {1} cost').format(self.usage_type.name, self.team_time.name)), 
             b'currency': True, 
             b'total_cost': False}),
         (
          (b'ut_{0}_team_{1}_cost').format(ut_id, self.team_devices_cores.id),
          {b'name': _((b'{0} - {1} cost').format(self.usage_type.name, self.team_devices_cores.name)), 
             b'currency': True, 
             b'total_cost': False}),
         (
          (b'ut_{0}_team_{1}_cost').format(ut_id, self.team_devices.id),
          {b'name': _((b'{0} - {1} cost').format(self.usage_type.name, self.team_devices.name)), 
             b'currency': True, 
             b'total_cost': False}),
         (
          (b'ut_{0}_team_{1}_cost').format(ut_id, self.team_distribute.id),
          {b'name': _((b'{0} - {1} cost').format(self.usage_type.name, self.team_distribute.name)), 
             b'currency': True, 
             b'total_cost': False}),
         (
          (b'ut_{0}_total_cost').format(ut_id),
          {b'name': _((b'{0} total cost').format(self.usage_type.name)), 
             b'currency': True, 
             b'total_cost': True})]))