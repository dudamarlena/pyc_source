# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kula/workspace/ralph_pricing/src/ralph_pricing/tests/test_api.py
# Compiled at: 2014-05-30 05:53:08
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import datetime
from django.contrib.auth.models import User
from tastypie.test import ResourceTestCase
from ralph_pricing.models import DailyUsage, Service, Venture, UsageType
from ralph_pricing.api import ServiceUsageObject, ServiceUsageResource, VentureUsageObject, UsageObject

class TestServiceUsagesApi(ResourceTestCase):

    def setUp(self):
        super(TestServiceUsagesApi, self).setUp()
        self.resource = b'serviceusages'
        self.user = User.objects.create_user(b'ralph', b'ralph@ralph.local', b'ralph')
        date2datetime = lambda d: datetime.datetime.combine(d, datetime.datetime.min.time())
        self.date = datetime.date(2013, 10, 10)
        self.datetime = date2datetime(self.date)
        self.today = datetime.date.today()
        self.today_datetime = date2datetime(self.today)
        self.service = Service(name=b'Service1', symbol=b's1')
        self.service.save()
        self.venture1 = Venture(name=b'Venture1', venture_id=1, symbol=b'v1', is_active=True)
        self.venture1.save()
        self.venture2 = Venture(name=b'Venture2', venture_id=2, symbol=b'v2', is_active=True)
        self.venture2.save()
        self.venture3 = Venture(name=b'Venture3', venture_id=3, symbol=b'v3', is_active=True)
        self.venture3.save()
        self.inactive_venture = Venture(name=b'Venture4', venture_id=4, symbol=b'v4', is_active=False)
        self.inactive_venture.save()
        self.usage_type1 = UsageType(name=b'UsageType1', symbol=b'ut1')
        self.usage_type1.save()
        self.usage_type2 = UsageType(name=b'UsageType2', symbol=b'ut2')
        self.usage_type2.save()
        self.api_key = self.create_apikey(self.user.username, self.user.api_key.key)

    def _get_sample_service_usages_object(self, overwrite=None):
        service_usages = ServiceUsageObject(date=self.date, service=self.service.symbol, venture_usages=[
         VentureUsageObject(venture=self.venture1.symbol, usages=[
          UsageObject(symbol=self.usage_type1.symbol, value=123),
          UsageObject(symbol=self.usage_type2.symbol, value=1.2)]),
         VentureUsageObject(venture=self.venture2.symbol, usages=[
          UsageObject(symbol=self.usage_type1.symbol, value=3.3),
          UsageObject(symbol=self.usage_type2.symbol, value=44)])])
        if overwrite is not None:
            service_usages.overwrite = overwrite
        return service_usages

    def test_save_usages(self):
        service_usages = self._get_sample_service_usages_object()
        ServiceUsageResource.save_usages(service_usages)
        self.assertEquals(DailyUsage.objects.count(), 4)
        daily_usage_1 = DailyUsage.objects.order_by(b'id')[0]
        self.assertEquals(daily_usage_1.pricing_venture, self.venture1)
        self.assertEquals(daily_usage_1.date, self.datetime)
        self.assertEquals(daily_usage_1.type, self.usage_type1)
        self.assertEquals(daily_usage_1.value, 123)

    def test_to_dict(self):
        service_usages = self._get_sample_service_usages_object()
        self.assertEquals(service_usages.to_dict(), {b'service': self.service.symbol, 
           b'date': self.date, 
           b'overwrite': None, 
           b'venture_usages': [
                             {b'venture': self.venture1.symbol, 
                                b'usages': [
                                          {b'symbol': self.usage_type1.symbol, 
                                             b'value': 123},
                                          {b'symbol': self.usage_type2.symbol, 
                                             b'value': 1.2}]},
                             {b'venture': self.venture2.symbol, 
                                b'usages': [
                                          {b'symbol': self.usage_type1.symbol, 
                                             b'value': 3.3},
                                          {b'symbol': self.usage_type2.symbol, 
                                             b'value': 44}]}]})
        return

    def test_api(self):
        service_usages = self._get_sample_service_usages_object()
        data = service_usages.to_dict()
        resp = self.api_client.post((b'/scrooge/api/v0.9/{0}/').format(self.resource), format=b'json', authentication=self.api_key, data=data)
        self.assertEquals(resp.status_code, 201)
        self.assertEquals(DailyUsage.objects.count(), 4)
        daily_usage_1 = DailyUsage.objects.order_by(b'id')[0]
        self.assertEquals(daily_usage_1.pricing_venture, self.venture1)
        self.assertEquals(daily_usage_1.date, self.datetime)
        self.assertEquals(daily_usage_1.type, self.usage_type1)
        self.assertEquals(daily_usage_1.value, 123)

    def test_api_invalid_service(self):
        service_usages = self._get_sample_service_usages_object()
        data = service_usages.to_dict()
        data[b'service'] = b'invalid_service'
        resp = self.api_client.post((b'/scrooge/api/v0.9/{0}/').format(self.resource), format=b'json', authentication=self.api_key, data=data)
        self.assertEquals(resp.status_code, 400)
        self.assertEquals(resp.content, b'Invalid service symbol')
        self.assertEquals(DailyUsage.objects.count(), 0)

    def test_api_invalid_venture(self):
        service_usages = self._get_sample_service_usages_object()
        data = service_usages.to_dict()
        data[b'venture_usages'][1][b'venture'] = b'invalid_venture'
        resp = self.api_client.post((b'/scrooge/api/v0.9/{0}/').format(self.resource), format=b'json', authentication=self.api_key, data=data)
        self.assertEquals(resp.status_code, 400)
        self.assertEquals(resp.content, b'Invalid venture symbol or venture is inactive')
        self.assertEquals(DailyUsage.objects.count(), 0)

    def test_api_invalid_usage(self):
        service_usages = self._get_sample_service_usages_object()
        data = service_usages.to_dict()
        data[b'venture_usages'][1][b'usages'][1][b'symbol'] = b'invalid_usage'
        resp = self.api_client.post((b'/scrooge/api/v0.9/{0}/').format(self.resource), format=b'json', authentication=self.api_key, data=data)
        self.assertEquals(resp.status_code, 400)
        self.assertEquals(resp.content, b'Invalid usage type symbol')
        self.assertEquals(DailyUsage.objects.count(), 0)

    def test_api_inactive_venture(self):
        service_usages = self._get_sample_service_usages_object()
        service_usages.venture_usages[0].venture = self.inactive_venture.symbol
        data = service_usages.to_dict()
        resp = self.api_client.post((b'/scrooge/api/v0.9/{0}/').format(self.resource), format=b'json', authentication=self.api_key, data=data)
        self.assertEquals(resp.status_code, 400)
        self.assertEquals(resp.content, b'Invalid venture symbol or venture is inactive')
        self.assertEquals(DailyUsage.objects.count(), 0)

    def _basic_call(self):
        service_usages = self._get_sample_service_usages_object()
        data = service_usages.to_dict()
        resp = self.api_client.post((b'/scrooge/api/v0.9/{0}/').format(self.resource), format=b'json', authentication=self.api_key, data=data)
        self.assertEquals(resp.status_code, 201)
        usages = DailyUsage.objects.filter(type=self.usage_type1).values_list(b'pricing_venture__symbol', b'value')
        self.assertEquals(dict(usages), {self.venture1.symbol: 123.0, 
           self.venture2.symbol: 3.3})

    def test_overwrite_values_only(self):
        self._basic_call()
        service_usages = self._get_sample_service_usages_object(overwrite=b'values_only')
        service_usages.venture_usages[0].venture = self.venture3.symbol
        data = service_usages.to_dict()
        resp = self.api_client.post((b'/scrooge/api/v0.9/{0}/').format(self.resource), format=b'json', authentication=self.api_key, data=data)
        self.assertEquals(resp.status_code, 201)
        usages = DailyUsage.objects.filter(type=self.usage_type1).values_list(b'pricing_venture__symbol', b'value')
        self.assertEquals(dict(usages), {self.venture1.symbol: 123.0, 
           self.venture2.symbol: 3.3, 
           self.venture3.symbol: 123.0})

    def test_overwrite_delete_all_previous(self):
        self._basic_call()
        service_usages = self._get_sample_service_usages_object(overwrite=b'delete_all_previous')
        service_usages.venture_usages[0].venture = self.venture3.symbol
        data = service_usages.to_dict()
        resp = self.api_client.post((b'/scrooge/api/v0.9/{0}/').format(self.resource), format=b'json', authentication=self.api_key, data=data)
        self.assertEquals(resp.status_code, 201)
        usages = DailyUsage.objects.filter(type=self.usage_type1).values_list(b'pricing_venture__symbol', b'value')
        self.assertEquals(dict(usages), {self.venture2.symbol: 3.3, 
           self.venture3.symbol: 123.0})

    def test_not_overwriting(self):
        self._basic_call()
        service_usages = self._get_sample_service_usages_object(overwrite=b'no')
        service_usages.venture_usages[0].venture = self.venture3.symbol
        data = service_usages.to_dict()
        resp = self.api_client.post((b'/scrooge/api/v0.9/{0}/').format(self.resource), format=b'json', authentication=self.api_key, data=data)
        self.assertEquals(resp.status_code, 201)
        usages = DailyUsage.objects.filter(type=self.usage_type1).values_list(b'pricing_venture__symbol', b'value')
        self.assertEquals([ a for a in usages ], [
         (
          self.venture1.symbol, 123.0),
         (
          self.venture2.symbol, 3.3),
         (
          self.venture3.symbol, 123.0),
         (
          self.venture2.symbol, 3.3)])