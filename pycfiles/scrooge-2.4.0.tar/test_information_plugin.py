# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kula/workspace/ralph_pricing/src/ralph_pricing/tests/report_plugins/test_information_plugin.py
# Compiled at: 2014-06-03 05:10:47
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import datetime
from dateutil import rrule
from django.test import TestCase
from ralph_pricing import models
from ralph_pricing.tests import utils
from ralph_pricing.plugins.reports.information import Information

class TestInformationPlugin(TestCase):

    def setUp(self):
        self.venture1 = utils.get_or_create_venture(is_active=True, business_segment=b'bs1', department=b'd1', profit_center=b'p1')
        self.venture2 = utils.get_or_create_venture(is_active=True, business_segment=b'bs1', department=b'd1', profit_center=b'p1')
        self.venture3 = utils.get_or_create_venture(is_active=True, business_segment=b'bs1', department=b'd1', profit_center=b'p1')
        self.ventures_subset = [
         self.venture1, self.venture2]
        self.ventures = models.Venture.objects.all()

    def test_costs(self):
        result = Information(ventures=self.ventures_subset)
        self.assertEquals(result, {self.venture1.id: {b'business_segment': b'bs1', 
                              b'department': b'd1', 
                              b'profit_center': b'p1', 
                              b'venture': self.venture1.name, 
                              b'venture_id': self.venture1.venture_id}, 
           self.venture2.id: {b'business_segment': b'bs1', 
                              b'department': b'd1', 
                              b'profit_center': b'p1', 
                              b'venture': self.venture2.name, 
                              b'venture_id': self.venture2.venture_id}})

    def test_costs_per_device(self):
        device1 = utils.get_or_create_device(asset_id=1234, barcode=b'12345', sn=b'1111-1111-1111')
        device2 = utils.get_or_create_device(asset_id=1235, barcode=b'12346', sn=b'1111-1111-1112')
        start = datetime.date(2013, 10, 8)
        end = datetime.date(2013, 10, 22)
        for i, device in enumerate([device1, device2]):
            for day in rrule.rrule(rrule.DAILY, dtstart=start, until=end):
                utils.get_or_create_dailydevice(date=day, name=(b'Device{0}').format(i), price=100 * i, deprecation_rate=0.25, is_deprecated=False, venture=self.venture1, device=device)

        result = Information(start=datetime.date(2013, 10, 10), end=datetime.date(2013, 10, 25), ventures=[
         self.venture1], type=b'costs_per_device')
        self.assertEquals(result, {device1.id: {b'asset_id': 1234, 
                        b'barcode': b'12345', 
                        b'id': device1.id, 
                        b'name': b'Default1234', 
                        b'sn': b'1111-1111-1111'}, 
           device2.id: {b'asset_id': 1235, 
                        b'barcode': b'12346', 
                        b'id': device2.id, 
                        b'name': b'Default1235', 
                        b'sn': b'1111-1111-1112'}})