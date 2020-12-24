# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/common/unit/inventory_client/test_client.py
# Compiled at: 2018-06-21 13:39:29
# Size of source mod 2**32: 5190 bytes
import mock
from mercury.common.clients import inventory
from mercury.common.exceptions import MercuryClientException
from tests.common.unit import base

class FakeInventoryClient(inventory.InventoryClient):
    service_name = 'Inventory'

    def __init__(self):
        self.ctx = None
        self.socket = None


class InventoryClientUnitTest(base.MercuryCommonUnitTest):
    __doc__ = 'Tests for mercury.common.inventory_client.client.InventoryClient'

    def setUp(self):
        super(InventoryClientUnitTest, self).setUp()
        self.inventory_client = FakeInventoryClient()

    @mock.patch('mercury.common.clients.router_req_client.RouterReqClient.transceiver')
    def test_insert_one(self, mock_transceiver):
        """Test insert_one()."""
        mock_transceiver.return_value = {'response': 'fake_response'}
        device_info = {'mercury_id': 1}
        payload = {'endpoint':'insert_one', 
         'args':[
          device_info]}
        response = self.inventory_client.insert_one(device_info)
        mock_transceiver.assert_called_once_with(payload)
        self.assertEqual('fake_response', response['response'])

    def test_insert_one_no_mercury_id(self):
        """Test insert_one() fails when no mercury_id in device_info."""
        device_info = {}
        self.assertRaises(MercuryClientException, self.inventory_client.insert_one, device_info)

    @mock.patch('mercury.common.clients.router_req_client.RouterReqClient.transceiver')
    def test_update_one(self, mock_transceiver):
        """Test update_one()."""
        mock_transceiver.return_value = {'response': 'fake_response'}
        mercury_id = 1
        update_data = 'fake_data'
        payload = {'endpoint':'update_one', 
         'args':[
          mercury_id], 
         'kwargs':{'update_data': update_data}}
        response = self.inventory_client.update_one(mercury_id, update_data)
        mock_transceiver.assert_called_once_with(payload)
        self.assertEqual('fake_response', response['response'])

    @mock.patch('mercury.common.clients.router_req_client.RouterReqClient.transceiver')
    def test_get_one(self, mock_transceiver):
        """Test get_one()."""
        mock_transceiver.return_value = {'response': 'fake_response'}
        mercury_id = 1
        payload = {'endpoint':'get_one', 
         'args':[
          mercury_id], 
         'kwargs':{'projection': None}}
        response = self.inventory_client.get_one(mercury_id)
        mock_transceiver.assert_called_once_with(payload)
        self.assertEqual('fake_response', response['response'])

    @mock.patch('mercury.common.clients.router_req_client.RouterReqClient.transceiver')
    def test_query(self, mock_transceiver):
        """Test query()."""
        mock_transceiver.return_value = {'response': 'fake_response'}
        query_data = 'fake_data'
        payload = {'endpoint':'query', 
         'args':[
          query_data], 
         'kwargs':{'projection':None, 
          'limit':0, 
          'sort':'_id', 
          'sort_direction':1, 
          'offset_id':None}}
        response = self.inventory_client.query(query_data)
        mock_transceiver.assert_called_once_with(payload)
        self.assertEqual('fake_response', response['response'])

    @mock.patch('mercury.common.clients.router_req_client.RouterReqClient.transceiver')
    def test_delete(self, mock_transceiver):
        """Test delete()."""
        mock_transceiver.return_value = {'response': 'fake_response'}
        mercury_id = 1
        payload = {'endpoint':'delete', 
         'args':[
          mercury_id]}
        response = self.inventory_client.delete(mercury_id)
        mock_transceiver.assert_called_once_with(payload)
        self.assertEqual('fake_response', response['response'])

    @mock.patch('mercury.common.clients.router_req_client.RouterReqClient.transceiver')
    def test_count(self, mock_transceiver):
        """Test count()."""
        mock_transceiver.return_value = {'response': 'fake_response'}
        query_data = 'fake_data'
        payload = {'endpoint':'count', 
         'args':[
          query_data]}
        response = self.inventory_client.count(query_data)
        mock_transceiver.assert_called_once_with(payload)
        self.assertEqual('fake_response', response['response'])