# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/nodeshot/networking/services/tests.py
# Compiled at: 2013-10-25 12:54:19
import simplejson as json
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from nodeshot.core.base.tests import BaseTestCase
from nodeshot.core.base.tests import user_fixtures

class ServiceTest(BaseTestCase):
    fixtures = [
     'initial_data.json',
     user_fixtures,
     'test_layers.json',
     'test_status.json',
     'test_nodes.json',
     'test_routing_protocols.json',
     'test_devices.json',
     'test_interfaces.json',
     'test_ip_addresses.json',
     'test_services.json']

    def test_api_service_category_list(self):
        url = reverse('api_service_category_list')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_api_service_category_details(self):
        url = reverse('api_service_category_details', args=[1])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_api_service_list(self):
        url = reverse('api_service_list')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_api_service_details(self):
        url = reverse('api_service_details', args=[1])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)