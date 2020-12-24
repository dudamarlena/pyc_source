# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/julio.rama/git/vault-opensource/storage/tests/test_swift_container_acl.py
# Compiled at: 2020-03-17 15:36:46
# Size of source mod 2**32: 3407 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, json
from unittest.mock import patch, Mock
from unittest import TestCase
from swiftclient import client
from storage.tests import fakes
from storage import views
from vault.tests.fakes import fake_request

class TestSwiftAcl(TestCase):
    __doc__ = '\n    Class to test methods related to setting a container public/private\n    through Vault interface (containerview)\n    '

    def setUp(self):
        self.request = fake_request()
        self.project_id = '1ad2d06a38c643fb8550fe35b0ef579a_test'
        self.container = 'container_test'
        patch('storage.views.log', Mock(return_value=None)).start()
        patch('identity.keystone.Keystone', Mock(return_value=None)).start()

    def tearDown(self):
        patch.stopall()

    def test_container_acl_update_needs_authentication(self):
        req = fake_request(user=False)
        response = views.container_acl_update(req, self.container)
        self.assertEqual(response.status_code, 302)

    def test_container_acl_status_needs_authentication(self):
        req = fake_request(user=False)
        response = views.container_acl_status(req, self.container)
        self.assertEqual(response.status_code, 302)

    @patch('storage.views.client.head_container')
    def test_container_acl_status(self, mock_head_container):
        mock_head_container.return_value = {}
        project_name = self.request.session.get('project_name')
        response = views.container_acl_status(self.request, project_name, self.container)
        computed = json.loads(response.content)
        self.assertEqual(computed['status'], 'disabled')
        mock_head_container.return_value = {'x-container-read': '.r:*'}
        response = views.container_acl_status(self.request, project_name, self.container)
        computed = json.loads(response.content)
        self.assertEqual(computed['status'], 'enabled')

    @patch('storage.views.client.head_container')
    @patch('storage.views.client.post_container')
    def test_container_acl_update_set_to_private(self, mock_post, mock_head):
        mock_head.return_value = {}
        self.request.method = 'GET'
        _get = self.request.GET.copy()
        _get.update({'status': 'disabled'})
        self.request.GET = _get
        project_name = self.request.session.get('project_name')
        response = views.container_acl_update(self.request, project_name, self.container)
        computed_headers = mock_post.call_args[1].get('headers')
        self.assertEqual(computed_headers['x-container-read'], '')

    @patch('storage.views.client.head_container')
    @patch('storage.views.client.post_container')
    def test_container_acl_update_set_to_public(self, mock_post, mock_head):
        mock_head.return_value = {}
        self.request.method = 'GET'
        _get = self.request.GET.copy()
        _get.update({'status': 'enabled'})
        self.request.GET = _get
        project_name = self.request.session.get('project_name')
        response = views.container_acl_update(self.request, project_name, self.container)
        computed_headers = mock_post.call_args[1].get('headers')
        self.assertEqual(computed_headers['x-container-read'], '.r:*')