# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/api_metadata/tests/views/test_conf.py
# Compiled at: 2019-02-06 12:21:52
import datetime, json
from api_metadata.tests.case import APITestCase
from ocs.object_store import cp_backend, world_backend
from ocs.object_store.cp_backend.unittest import sources as cp_sources
from ocs.object_store.world_backend.unittest import sources as world_sources

def _transform_sh_to_dict(shell_export):
    ret = {}
    for line in shell_export.split('\n'):
        line = line.strip()
        if not line:
            continue
        item = line.split('=')
        key = item[0]
        value = item[1] if len(item) > 1 else None
        ret[key] = value

    return ret


class TestConf(APITestCase):

    def test_conf_no_server(self):
        """ No server exist with this ip address.

        GET api-compute/servers?private_ip=xxx will always return an empty
        list.
        """
        response = self.client.get('conf')
        self.assertEqual(response.status_code, 404)

    def test_conf_more_than_one_server(self):
        """ More than one server has the requested ip address.

        Should probably never happend in production.
        """
        pimouss1 = cp_sources.PimoussFactory(ip1='10.0.0.100')
        server1 = cp_sources.ServerFactory()
        session = cp_sources.SessionFactory(node=pimouss1, server=server1)
        pimouss2 = cp_sources.PimoussFactory(ip1='10.0.0.100')
        server2 = cp_sources.ServerFactory()
        session2 = cp_sources.SessionFactory(node=pimouss2, server=server2)
        cp_backend.ConfiguredEngine.scoped_session().commit()
        response = self.client.get('conf?format=json')
        self.assertEqual(response.status_code, 404)
        as_json = json.loads(response.data)
        self.assertTrue(as_json['message'].startswith('More than one'))

    def test_conf(self):
        pimouss = cp_sources.PimoussFactory(ip1=self.CLIENT_IP_ADDRESS)
        server = cp_sources.ServerFactory(tags=['tag1', 'tag2'])
        session = cp_sources.SessionFactory(node=pimouss, server=server)
        world_sources.OrganizationFactory(key=server.organization_key)
        world_backend.ConfiguredEngine.scoped_session().commit()
        cp_backend.ConfiguredEngine.scoped_session().commit()
        response = self.client.get('conf?format=json')
        self.assertEqual(response.status_code, 200)
        as_json = json.loads(response.data)
        self.assertEqual(as_json['name'], server.name)
        self.assertEqual(as_json['tags'], ['tag1', 'tag2'])
        self.assertEqual(as_json['organization'], server.organization_key)

    def test_hostname(self):
        pimouss = cp_sources.PimoussFactory(ip1=self.CLIENT_IP_ADDRESS)
        server = cp_sources.ServerFactory(tags=['tag1', 'tag2'], name='host name')
        session = cp_sources.SessionFactory(node=pimouss, server=server)
        world_sources.OrganizationFactory(key=server.organization_key)
        world_backend.ConfiguredEngine.scoped_session().commit()
        cp_backend.ConfiguredEngine.scoped_session().commit()
        response = self.client.get('conf?format=json')
        self.assertEqual(response.status_code, 200)
        as_json = json.loads(response.data)
        self.assertEqual(as_json['hostname'], 'host-name')

    def test_ipv6_disabled(self):
        node = cp_sources.SuchardNodeFactory(ip_address1=self.CLIENT_IP_ADDRESS)
        server = cp_sources.ServerFactory(tags=['tag1', 'tag2'], name='host name', enable_ipv6=False)
        cp_sources.SessionFactory(node=node, server=server)
        world_sources.OrganizationFactory(key=server.organization_key)
        world_backend.ConfiguredEngine.scoped_session().commit()
        cp_backend.ConfiguredEngine.scoped_session().commit()
        response = self.client.get('conf?format=json')
        self.assertEqual(response.status_code, 200)
        as_json = json.loads(response.data)
        self.assertIsNone(as_json['ipv6'])

    def test_ipv6_enabled(self):
        node = cp_sources.SuchardNodeFactory(ip_address1=self.CLIENT_IP_ADDRESS)
        server = cp_sources.ServerFactory(tags=['tag1', 'tag2'], name='host name', enable_ipv6=True)
        cp_sources.SessionFactory(node=node, server=server)
        world_sources.OrganizationFactory(key=server.organization_key)
        world_backend.ConfiguredEngine.scoped_session().commit()
        cp_backend.ConfiguredEngine.scoped_session().commit()
        response = self.client.get('conf?format=json')
        self.assertEqual(response.status_code, 200)
        as_json = json.loads(response.data)
        self.assertIsNotNone(as_json['ipv6'])

    def test_no_extra_networks(self):
        node = cp_sources.SuchardNodeFactory(ip_address1=self.CLIENT_IP_ADDRESS, node_id=9)
        server = cp_sources.ServerFactory(tags=['tag1', 'tag2'], name='host name', enable_ipv6=False)
        cp_sources.SessionFactory(node=node, server=server)
        world_sources.OrganizationFactory(key=server.organization_key)
        world_backend.ConfiguredEngine.scoped_session().commit()
        cp_backend.ConfiguredEngine.scoped_session().commit()
        response = self.client.get('conf?format=json')
        self.assertEqual(response.status_code, 200)
        as_json = json.loads(response.data)
        self.assertEqual(0, len(as_json['extra_networks']))

    def test_extra_networks(self):
        node = cp_sources.SuchardNodeFactory(ip_address1=self.CLIENT_IP_ADDRESS, node_id=10)
        server = cp_sources.ServerFactory(tags=['tag1', 'tag2'], name='host name', enable_ipv6=False)
        cp_sources.SessionFactory(node=node, server=server)
        world_sources.OrganizationFactory(key=server.organization_key)
        world_backend.ConfiguredEngine.scoped_session().commit()
        cp_backend.ConfiguredEngine.scoped_session().commit()
        response = self.client.get('conf?format=json')
        self.assertEqual(response.status_code, 200)
        as_json = json.loads(response.data)
        self.assertEqual(1, len(as_json['extra_networks']))

    def test_extra_networks_with_ipv6(self):
        node = cp_sources.SuchardNodeFactory(ip_address1=self.CLIENT_IP_ADDRESS, node_id=10)
        server = cp_sources.ServerFactory(tags=['tag1', 'tag2'], name='host name', enable_ipv6=True)
        cp_sources.SessionFactory(node=node, server=server)
        world_sources.OrganizationFactory(key=server.organization_key)
        world_backend.ConfiguredEngine.scoped_session().commit()
        cp_backend.ConfiguredEngine.scoped_session().commit()
        response = self.client.get('conf?format=json')
        self.assertEqual(response.status_code, 200)
        as_json = json.loads(response.data)
        self.assertEqual(2, len(as_json['extra_networks']))

    def test_conf_new_sh_format(self):
        pimouss = cp_sources.PimoussFactory(ip1=self.CLIENT_IP_ADDRESS)
        server = cp_sources.ServerFactory(tags=['tag1', 'tag2'])
        cp_sources.SessionFactory(node=pimouss, server=server)
        world_sources.OrganizationFactory(key=server.organization_key)
        world_backend.ConfiguredEngine.scoped_session().commit()
        cp_backend.ConfiguredEngine.scoped_session().commit()
        response = self.client.get('conf')
        self.assertEqual(response.status_code, 200)
        data = _transform_sh_to_dict(response.data)
        self.assertEqual(data['VOLUMES_0_SERVER'][0], "'")
        self.assertNotIn('x-old-image', response.headers)
        self.assertEqual(response.status_code, 200)

    def test_conf_new_image_new_sh_format(self):
        pimouss = cp_sources.PimoussFactory(ip1=self.CLIENT_IP_ADDRESS)
        image = cp_sources.ImageFactory()
        server = cp_sources.ServerFactory(tags=['tag1', 'tag2'], image=image)
        cp_sources.SessionFactory(node=pimouss, server=server)
        world_sources.OrganizationFactory(key=server.organization_key)
        world_backend.ConfiguredEngine.scoped_session().commit()
        cp_backend.ConfiguredEngine.scoped_session().commit()
        response = self.client.get('conf')
        self.assertEqual(response.status_code, 200)
        data = _transform_sh_to_dict(response.data)
        self.assertEqual(data['VOLUMES_0_SERVER'][0], "'")
        self.assertNotIn('x-old-image', response.headers)
        self.assertEqual(response.status_code, 200)

    def test_conf_old_sh_format(self):
        pimouss = cp_sources.PimoussFactory(ip1=self.CLIENT_IP_ADDRESS)
        image = cp_sources.ImageFactory(creation_date=datetime.datetime(2014, 10, 10))
        server = cp_sources.ServerFactory(tags=['tag1', 'tag2'], image=image)
        cp_sources.SessionFactory(node=pimouss, server=server)
        world_sources.OrganizationFactory(key=server.organization_key)
        world_backend.ConfiguredEngine.scoped_session().commit()
        cp_backend.ConfiguredEngine.scoped_session().commit()
        response = self.client.get('conf')
        self.assertEqual(response.status_code, 200)
        data = _transform_sh_to_dict(response.data)
        self.assertNotEqual(data['VOLUMES_0_SERVER'][0], "'")
        self.assertNotIn('x-old-image', response.headers)
        self.assertEqual(response.status_code, 200)

    def test_conf_after_november_sh_format(self):
        pimouss = cp_sources.PimoussFactory(ip1=self.CLIENT_IP_ADDRESS)
        image = cp_sources.ImageFactory(creation_date=datetime.datetime(2014, 11, 2))
        server = cp_sources.ServerFactory(tags=['tag1', 'tag2'], image=image)
        cp_sources.SessionFactory(node=pimouss, server=server)
        world_sources.OrganizationFactory(key=server.organization_key)
        world_backend.ConfiguredEngine.scoped_session().commit()
        cp_backend.ConfiguredEngine.scoped_session().commit()
        response = self.client.get('conf')
        self.assertEqual(response.status_code, 200)
        data = _transform_sh_to_dict(response.data)
        self.assertEqual(data['VOLUMES_0_SERVER'][0], "'")
        self.assertNotIn('x-old-image', response.headers)
        self.assertEqual(response.status_code, 200)