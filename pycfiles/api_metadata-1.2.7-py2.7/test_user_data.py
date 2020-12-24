# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/api_metadata/tests/views/test_user_data.py
# Compiled at: 2018-12-11 11:47:30
import json, unittest
from api_metadata.tests.case import APITestCase
from api_metadata.views.user_data import force_text_plain
from flask import request
from ocs.object_store import cp_backend, world_backend
from ocs.object_store.cp_backend import ServerUserData
from ocs.object_store.cp_backend.unittest import sources as cp_sources
from ocs.object_store.world_backend.unittest import sources as world_sources

def set_privileged_local_port():
    """ Fix request environment to set a privileged local port.
    """
    request.environ['REMOTE_PORT'] = '1000'


def set_unprivileged_local_port():
    """ Fix request environment to set an unprivileged local port.
    """
    request.environ['REMOTE_PORT'] = '56000'


class TestJSONViews(APITestCase):

    def setUp(self):
        super(TestJSONViews, self).setUp()
        self.client.application.before_request(set_privileged_local_port)

    def test_index(self):
        pimouss = cp_sources.PimoussFactory(ip1=self.CLIENT_IP_ADDRESS)
        server = cp_sources.ServerFactory()
        user_data = cp_sources.ServerUserDataFactory(server=server, key='userdatakey', value='value')
        session = cp_sources.SessionFactory(node=pimouss, server=server)
        world_sources.OrganizationFactory(key=server.organization_key)
        world_backend.ConfiguredEngine.scoped_session().commit()
        cp_backend.ConfiguredEngine.scoped_session().commit()
        response = self.client.get('/user_data')
        self.assertIn('USER_DATA=1', response.data)
        self.assertIn('USER_DATA_0=userdatakey', response.data)
        self.assertEqual(response.content_type, 'text/plain')
        response = self.get('/user_data?format=json')
        self.assertEqual(response.json, {'user_data': [
                       'userdatakey']})
        self.assertEqual(response.content_type, 'application/json')

    def test_delete(self):
        pimouss = cp_sources.PimoussFactory(ip1=self.CLIENT_IP_ADDRESS)
        server = cp_sources.ServerFactory()
        user_data = cp_sources.ServerUserDataFactory(server=server, key='userdatakey', value='value')
        session = cp_sources.SessionFactory(node=pimouss, server=server)
        world_sources.OrganizationFactory(key=server.organization_key)
        world_backend.ConfiguredEngine.scoped_session().commit()
        cp_session = cp_backend.ConfiguredEngine.scoped_session()
        cp_session.commit()
        response = self.delete('/user_data/userdatakey')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(cp_session.query(ServerUserData).count(), 0)


class TestTextPlainViews(APITestCase):

    def setUp(self):
        super(TestTextPlainViews, self).setUp()
        self.client.application.before_request(set_privileged_local_port)

    def test_patch(self):
        pimouss = cp_sources.PimoussFactory(ip1=self.CLIENT_IP_ADDRESS)
        server = cp_sources.ServerFactory()
        user_data = cp_sources.ServerUserDataFactory(server=server, key='userdatakey', value='value')
        session = cp_sources.SessionFactory(node=pimouss, server=server)
        world_sources.OrganizationFactory(key=server.organization_key)
        world_backend.ConfiguredEngine.scoped_session().commit()
        cp_session = cp_backend.ConfiguredEngine.scoped_session()
        cp_session.commit()
        self.http_headers['Content-Type'] = 'text/plain'
        response = self.client.patch('/user_data/userdatakey', data='hell0', headers=self.http_headers)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(cp_session.query(ServerUserData).first().value, 'hell0')

    def test_patch_no_server(self):
        self.http_headers['Content-Type'] = 'text/plain'
        response = self.client.patch('/user_data/userdatakey', data='hell0', headers=self.http_headers)
        self.assertEqual(response.status_code, 404)

    def test_patch_bad_content_type(self):
        self.http_headers['Content-Type'] = 'whatever'
        response = self.client.patch('/user_data/userdatakey', data='hell0', headers=self.http_headers)
        self.assertEqual(response.status_code, 400)

    def test_get(self):
        pimouss = cp_sources.PimoussFactory(ip1=self.CLIENT_IP_ADDRESS)
        server = cp_sources.ServerFactory()
        user_data = cp_sources.ServerUserDataFactory(server=server, key='userdatakey', value='super value')
        session = cp_sources.SessionFactory(node=pimouss, server=server)
        world_sources.OrganizationFactory(key=server.organization_key)
        world_backend.ConfiguredEngine.scoped_session().commit()
        cp_session = cp_backend.ConfiguredEngine.scoped_session()
        cp_session.commit()
        response = self.client.get('/user_data/userdatakey')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, 'super value')

    def test_get_no_server(self):
        response = self.client.get('/user_data/userdatakey')
        self.assertEqual(response.status_code, 404)

    def test_get_no_key(self):
        pimouss = cp_sources.PimoussFactory(ip1=self.CLIENT_IP_ADDRESS)
        server = cp_sources.ServerFactory()
        session = cp_sources.SessionFactory(node=pimouss, server=server)
        world_sources.OrganizationFactory(key=server.organization_key)
        world_backend.ConfiguredEngine.scoped_session().commit()
        response = self.client.get('/user_data/userdatakey')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, 'Invalid key')


class TestSecurity(APITestCase):
    """ Ensure user data aren't usable if local port is not privileged.
    """

    def setUp(self):
        super(TestSecurity, self).setUp()
        self.client.application.before_request(set_unprivileged_local_port)

    def test_ok(self):
        response = self.client.get('/user_data/userdatakey')
        self.assertEqual(response.status_code, 403)


class TestProxyConfiguration(APITestCase):
    """ Ensure HTTP/500 is raised if REMOTE_PORT isn't set.
    """

    def test_error(self):
        response = self.client.get('/user_data/userdatakey')
        self.assertEqual(response.data, 'uwsgi variable REMOTE_PORT must be set to the client port')
        self.assertEqual(response.status_code, 500)


class TestForceTextPlainDecorator(unittest.TestCase):

    def test_decorator(self):
        self.assertEqual(force_text_plain(lambda : 'response')(), (
         'response', 200, {'Content-Type': 'text/plain'}))
        self.assertEqual(force_text_plain(lambda : ('response', ))(), (
         'response', 200, {'Content-Type': 'text/plain'}))
        self.assertEqual(force_text_plain(lambda : ('response', 404))(), (
         'response', 404, {'Content-Type': 'text/plain'}))
        self.assertEqual(force_text_plain(lambda : (
         'response', 500, {'Content-Type': 'whatever'}))(), (
         'response', 500, {'Content-Type': 'text/plain'}))