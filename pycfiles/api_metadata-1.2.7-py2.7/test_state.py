# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/api_metadata/tests/views/test_state.py
# Compiled at: 2019-02-06 12:21:52
import json
from api_metadata.tests.case import APITestCase
from ocs.object_store import cp_backend, world_backend
from ocs.object_store.cp_backend.unittest import sources as cp_sources
from ocs.object_store.world_backend.unittest import sources as world_sources
from ocs.conf import Configuration
from api_metadata.views import CONFIGURATION_NAME

class TestState(APITestCase):

    def test_state_no_server(self):
        """ No server exist with this ip address.

        GET api-compute/servers?private_ip=xxx will always return an empty
        list.
        """
        response = self.client.patch('state', data=json.dumps({'state_detail': 'cool state'}), content_type='application/json')
        self.assertEqual(404, response.status_code)

    def test_state(self):
        pimouss = cp_sources.PimoussFactory(ip1=self.CLIENT_IP_ADDRESS)
        server = cp_sources.ServerFactory(tags=['tag1', 'tag2'])
        cp_sources.SessionFactory(node=pimouss, server=server)
        world_sources.OrganizationFactory(key=server.organization_key)
        world_backend.ConfiguredEngine.scoped_session().commit()
        cp_backend.ConfiguredEngine.scoped_session().commit()
        new_state = 'cool state'
        response = self.client.patch('state?format=json', data=json.dumps({'state_detail': new_state}), content_type='application/json')
        as_json = json.loads(response.data)
        self.assertEqual(new_state, as_json['state_detail'])

    def test_state_format_sh(self):
        pimouss = cp_sources.PimoussFactory(ip1=self.CLIENT_IP_ADDRESS)
        server = cp_sources.ServerFactory(tags=['tag1', 'tag2'])
        cp_sources.SessionFactory(node=pimouss, server=server)
        world_sources.OrganizationFactory(key=server.organization_key)
        world_backend.ConfiguredEngine.scoped_session().commit()
        cp_backend.ConfiguredEngine.scoped_session().commit()
        new_state = 'cool state'
        response = self.client.patch('state', data=json.dumps({'state_detail': new_state}), content_type='application/json')
        self.assertEqual(("STATE_DETAIL='{}'\n").format(new_state), response.data)

    def test_xforwardedfor_devcker(self):
        """ Given the app is configured for devcker mode, when a request
        contains a X-Forwarded-For header, the forwarded ip address is used
        """
        ip = '10.0.0.200'
        self.assertNotEquals(ip, self.CLIENT_IP_ADDRESS)
        conf = Configuration._conffiles[CONFIGURATION_NAME]['api-metadata']
        conf.update({'run-in-devcker': True})
        pimouss = cp_sources.PimoussFactory(ip1=ip)
        server = cp_sources.ServerFactory(tags=['tag1', 'tag2'])
        cp_sources.SessionFactory(node=pimouss, server=server)
        world_sources.OrganizationFactory(key=server.organization_key)
        world_backend.ConfiguredEngine.scoped_session().commit()
        cp_backend.ConfiguredEngine.scoped_session().commit()
        new_state = 'cool state'
        response = self.client.patch('state?format=json', data=json.dumps({'state_detail': new_state}), content_type='application/json')
        as_json = json.loads(response.data)
        self.assertTrue('state_detail' not in as_json)
        response = self.client.patch('state?format=json', data=json.dumps({'state_detail': new_state}), content_type='application/json', headers={'X-Forwarded-For': ip})
        as_json = json.loads(response.data)
        self.assertEqual(new_state, as_json['state_detail'])

    def test_xforwardedfor_prod(self):
        """ Given the app is not configured for devcker mode, when a request
        contains a X-Forwarded-For header, the forwarded ip address is ignored
        """
        ip = '10.0.0.200'
        self.assertNotEquals(ip, self.CLIENT_IP_ADDRESS)
        conf = Configuration._conffiles[CONFIGURATION_NAME]['api-metadata']
        conf.update({'run-in-devcker': False})
        pimouss = cp_sources.PimoussFactory(ip1=ip)
        server = cp_sources.ServerFactory(tags=['tag1', 'tag2'])
        cp_sources.SessionFactory(node=pimouss, server=server)
        world_sources.OrganizationFactory(key=server.organization_key)
        world_backend.ConfiguredEngine.scoped_session().commit()
        cp_backend.ConfiguredEngine.scoped_session().commit()
        new_state = 'cool state'
        response = self.client.patch('state?format=json', data=json.dumps({'state_detail': new_state}), content_type='application/json')
        as_json = json.loads(response.data)
        self.assertTrue('state_detail' not in as_json)
        response = self.client.patch('state?format=json', data=json.dumps({'state_detail': new_state}), content_type='application/json', headers={'X-Forwarded-For': ip})
        as_json = json.loads(response.data)
        self.assertTrue('state_detail' not in as_json)