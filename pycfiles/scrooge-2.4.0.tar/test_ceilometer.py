# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kula/workspace/ralph_pricing/src/ralph_pricing/tests/collect_plugins/test_ceilometer.py
# Compiled at: 2014-05-30 05:53:08
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import datetime, mock
from django.test import TestCase
from ralph_pricing.plugins.collects import ceilometer
from ralph_pricing.models import DailyUsage, Venture
ceilometer.settings.OPENSTACK_SITES = [
 {b'OS_METERING_URL': b'http://127.0.0.1:8777', 
    b'OS_TENANT_NAME': b'testtenant', 
    b'OS_USERNAME': b'testuser', 
    b'OS_PASSWORD': b'supersecretpass', 
    b'OS_AUTH_URL': b'http://127.0.0.1:5000/v2.0'},
 {b'OS_METERING_URL': b'http://127.0.0.2:8777', 
    b'OS_TENANT_NAME': b'testtenant2', 
    b'OS_USERNAME': b'testuser2', 
    b'OS_PASSWORD': b'supersecretpass2', 
    b'OS_AUTH_URL': b'http://127.0.0.2:5000/v2.0'}]

class TestCeilometer(TestCase):

    def test_get_ceilometer_usages(self):
        tenant_mock = mock.Mock()
        tenant_mock.description = b'test;ralph;whatever'
        tenant_mock.id = b'abcdef12345'
        tenant_mock.name = b'ralph-test'
        tenants = [tenant_mock]
        client_mock = mock.MagicMock()
        today = datetime.date(2014, 1, 21)
        flavors = [b'test_flav']

        def statistics_mock(meter_name, q, *args, **kwargs):
            cpu = mock.MagicMock(unit=b'unit', sum=1234)
            neti = mock.MagicMock(unit=b'unit', sum=2345)
            neto = mock.MagicMock(unit=b'unit', sum=3456)
            diskr = mock.MagicMock(unit=b'unit', sum=5678)
            diskw = mock.MagicMock(unit=b'unit', sum=4567)
            inst = [
             mock.MagicMock(unit=b'unit', aggregate={b'cardinality/resource_id': 45.0}),
             mock.MagicMock(unit=b'unit', aggregate={b'cardinality/resource_id': 85.0})]
            meters = {b'cpu': [
                      cpu], 
               b'network.outgoing.bytes': [
                                         neto], 
               b'network.incoming.bytes': [
                                         neti], 
               b'disk.write.requests': [
                                      diskw], 
               b'disk.read.requests': [
                                     diskr], 
               b'instance:test_flav': inst}
            correct_query = [
             {b'field': b'project_id', 
                b'op': b'eq', 
                b'value': b'abcdef12345'},
             {b'field': b'timestamp', 
                b'op': b'ge', 
                b'value': b'2014-01-20T00:00:00'},
             {b'field': b'timestamp', 
                b'op': b'lt', 
                b'value': b'2014-01-21T00:00:00'}]
            self.assertEqual(correct_query, q)
            return meters[meter_name]

        client_mock.statistics.list.side_effect = statistics_mock
        res = ceilometer.get_ceilometer_usages(client_mock, tenants, date=today, flavors=flavors, statistics={})
        correct_res = {b'ralph': {b'openstack.instance.test_flav': 130.0}}
        self.assertEqual(res, correct_res)

    def test_save_ceilometer_usages(self):
        v = Venture.objects.create(venture_id=12345, name=b'ralph-ceilo', symbol=b'ralph-ceilo')
        v.save()
        usages = {b'ralph-ceilo': {b'cpu': 1234, 
                            b'network.incoming.bytes': 2345, 
                            b'network.outgoing.bytes': 3456, 
                            b'disk.write.requests': 4567, 
                            b'disk.read.requests': 5678}}
        date = datetime.date(2014, 1, 21)
        ceilometer.save_ceilometer_usages(usages, date)
        usages = DailyUsage.objects.filter(pricing_venture=v)
        self.assertEqual(5, usages.count())