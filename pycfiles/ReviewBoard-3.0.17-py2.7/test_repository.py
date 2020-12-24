# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/webapi/tests/test_repository.py
# Compiled at: 2020-02-11 04:03:57
from __future__ import unicode_literals
import os, paramiko
from django.utils import six
from djblets.testing.decorators import add_fixtures
from reviewboard import scmtools
from reviewboard.hostingsvcs.models import HostingServiceAccount
from reviewboard.reviews.models import ReviewRequest
from reviewboard.scmtools.errors import AuthenticationError, UnverifiedCertificateError
from reviewboard.scmtools.models import Repository, Tool
from reviewboard.ssh.client import SSHClient
from reviewboard.ssh.errors import BadHostKeyError, UnknownHostKeyError
from reviewboard.testing.scmtool import TestTool
from reviewboard.webapi.errors import BAD_HOST_KEY, MISSING_USER_KEY, REPO_AUTHENTICATION_ERROR, UNVERIFIED_HOST_CERT, UNVERIFIED_HOST_KEY
from reviewboard.webapi.resources import resources
from reviewboard.webapi.tests.base import BaseWebAPITestCase
from reviewboard.webapi.tests.mimetypes import repository_item_mimetype, repository_list_mimetype
from reviewboard.webapi.tests.mixins import BasicTestsMetaclass
from reviewboard.webapi.tests.urls import get_repository_item_url, get_repository_list_url
key1 = paramiko.RSAKey.generate(1024)
key2 = paramiko.RSAKey.generate(1024)

class BaseRepositoryTests(BaseWebAPITestCase):
    """Base class for the RepositoryResource test suites."""
    fixtures = [
     b'test_users', b'test_scmtools']
    sample_repo_path = b'file://' + os.path.abspath(os.path.join(os.path.dirname(scmtools.__file__), b'testdata', b'git_repo'))

    def _verify_repository_info(self, rsp, repo_name, repo_path, data):
        self.assertEqual(rsp[b'stat'], b'ok')
        self.assertIn(b'repository', rsp)
        repository = Repository.objects.get(pk=rsp[b'repository'][b'id'])
        self.assertEqual(rsp[b'repository'][b'path'], repo_path)
        self.assertEqual(repository.path, repo_path)
        if not data.get(b'archive_name', False):
            self.assertEqual(rsp[b'repository'][b'name'], repo_name)
            self.assertEqual(repository.name, repo_name)
        for key, value in six.iteritems(data):
            if hasattr(repository, key):
                self.assertEqual(getattr(repository, key), value)


@six.add_metaclass(BasicTestsMetaclass)
class ResourceListTests(BaseRepositoryTests):
    """Testing the RepositoryResource list APIs."""
    sample_api_url = b'repositories/'
    resource = resources.repository
    basic_post_fixtures = [b'test_scmtools']
    basic_post_use_admin = True

    def setUp(self):
        super(ResourceListTests, self).setUp()
        self._old_check_repository = TestTool.check_repository
        self._old_accept_certificate = TestTool.accept_certificate
        self._old_add_host_key = SSHClient.add_host_key
        self._old_replace_host_key = SSHClient.replace_host_key

    def tearDown(self):
        super(ResourceListTests, self).tearDown()
        TestTool.check_repository = self._old_check_repository
        TestTool.accept_certificate = self._old_accept_certificate
        SSHClient.add_host_key = self._old_add_host_key
        SSHClient.replace_host_key = self._old_replace_host_key

    def compare_item(self, item_rsp, repository):
        self.assertEqual(item_rsp[b'id'], repository.pk)
        self.assertEqual(item_rsp[b'path'], repository.path)

    def setup_basic_get_test(self, user, with_local_site, local_site_name, populate_items):
        if populate_items:
            items = [
             self.create_repository(tool_name=b'Test', with_local_site=with_local_site)]
        else:
            items = []
        return (
         get_repository_list_url(local_site_name),
         repository_list_mimetype,
         items)

    @add_fixtures([b'test_site'])
    def test_get_with_show_visible(self):
        """Testing the GET repositories/ API with show_invisible=True"""
        self.create_repository(name=b'test1', tool_name=b'Test', visible=False)
        self.create_repository(name=b'test2', tool_name=b'Test', visible=True)
        rsp = self.api_get(get_repository_list_url(), query={b'show-invisible': True}, expected_mimetype=repository_list_mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        self.assertEqual(len(rsp[b'repositories']), 2)
        self.assertEqual(rsp[b'repositories'][0][b'name'], b'test1')
        self.assertEqual(rsp[b'repositories'][1][b'name'], b'test2')

    def test_get_repositories_with_name(self):
        """Testing the GET repositories/?name= API"""
        self.create_repository(name=b'test1', tool_name=b'Test')
        self.create_repository(name=b'test2', tool_name=b'Test')
        rsp = self.api_get(get_repository_list_url() + b'?name=test1', expected_mimetype=repository_list_mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        self.assertEqual(len(rsp[b'repositories']), 1)
        self.assertEqual(rsp[b'repositories'][0][b'name'], b'test1')

    def test_get_repositories_with_name_many(self):
        """Testing the GET repositories/?name= API and comma-separated list"""
        self.create_repository(name=b'test1', tool_name=b'Test')
        self.create_repository(name=b'test2', tool_name=b'Test')
        self.create_repository(name=b'test3', tool_name=b'Test')
        rsp = self.api_get(get_repository_list_url() + b'?name=test1,test2', expected_mimetype=repository_list_mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        self.assertEqual(len(rsp[b'repositories']), 2)
        self.assertEqual(rsp[b'repositories'][0][b'name'], b'test1')
        self.assertEqual(rsp[b'repositories'][1][b'name'], b'test2')

    def test_get_repositories_with_path(self):
        """Testing the GET repositories/?path= API"""
        self.create_repository(name=b'test1', path=b'dummy1', tool_name=b'Test')
        self.create_repository(name=b'test2', path=b'dummy2', tool_name=b'Test')
        rsp = self.api_get(get_repository_list_url() + b'?path=dummy1', expected_mimetype=repository_list_mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        self.assertEqual(len(rsp[b'repositories']), 1)
        self.assertEqual(rsp[b'repositories'][0][b'name'], b'test1')

    def test_get_repositories_with_path_many(self):
        """Testing the GET repositories/?path= API and comma-separated lists"""
        self.create_repository(name=b'test1', path=b'dummy1', tool_name=b'Test')
        self.create_repository(name=b'test2', path=b'dummy2', tool_name=b'Test')
        self.create_repository(name=b'test3', path=b'dummy3', tool_name=b'Test')
        rsp = self.api_get(get_repository_list_url() + b'?path=dummy1,dummy2', expected_mimetype=repository_list_mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        self.assertEqual(len(rsp[b'repositories']), 2)
        self.assertEqual(rsp[b'repositories'][0][b'name'], b'test1')
        self.assertEqual(rsp[b'repositories'][1][b'name'], b'test2')

    def test_get_repositories_with_name_or_path(self):
        """Testing the GET repositories/?name-or-path= API"""
        self.create_repository(name=b'test1', path=b'dummy1', tool_name=b'Test')
        self.create_repository(name=b'test2', path=b'dummy2', tool_name=b'Test')
        self.create_repository(name=b'test3', path=b'dummy3', tool_name=b'Test')
        rsp = self.api_get(get_repository_list_url() + b'?name-or-path=test1', expected_mimetype=repository_list_mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        self.assertEqual(len(rsp[b'repositories']), 1)
        self.assertEqual(rsp[b'repositories'][0][b'name'], b'test1')
        rsp = self.api_get(get_repository_list_url() + b'?name-or-path=dummy2', expected_mimetype=repository_list_mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        self.assertEqual(len(rsp[b'repositories']), 1)
        self.assertEqual(rsp[b'repositories'][0][b'name'], b'test2')

    def test_get_repositories_with_name_or_path_many(self):
        """Testing the GET repositories/?name-or-path= API
        and comma-separated list
        """
        self.create_repository(name=b'test1', path=b'dummy1', tool_name=b'Test')
        self.create_repository(name=b'test2', path=b'dummy2', tool_name=b'Test')
        self.create_repository(name=b'test3', path=b'dummy3', tool_name=b'Test')
        rsp = self.api_get(get_repository_list_url() + b'?name-or-path=test1,dummy2', expected_mimetype=repository_list_mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        self.assertEqual(len(rsp[b'repositories']), 2)
        self.assertEqual(rsp[b'repositories'][0][b'name'], b'test1')
        self.assertEqual(rsp[b'repositories'][1][b'name'], b'test2')

    def test_get_repositories_with_tool(self):
        """Testing the GET repositories/?tool= API"""
        self.create_repository(name=b'test1', path=b'dummy1', tool_name=b'Git')
        self.create_repository(name=b'test2', path=b'dummy2', tool_name=b'Test')
        rsp = self.api_get(get_repository_list_url() + b'?tool=Git', expected_mimetype=repository_list_mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        self.assertEqual(len(rsp[b'repositories']), 1)
        self.assertEqual(rsp[b'repositories'][0][b'name'], b'test1')

    def test_get_repositories_with_tool_many(self):
        """Testing the GET repositories/?tool= API and comma-separated list"""
        self.create_repository(name=b'test1', path=b'dummy1', tool_name=b'Git')
        self.create_repository(name=b'test2', path=b'dummy2', tool_name=b'Test')
        self.create_repository(name=b'test3', path=b'dummy3', tool_name=b'Subversion')
        rsp = self.api_get(get_repository_list_url() + b'?tool=Git,Subversion', expected_mimetype=repository_list_mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        self.assertEqual(len(rsp[b'repositories']), 2)
        self.assertEqual(rsp[b'repositories'][0][b'name'], b'test1')
        self.assertEqual(rsp[b'repositories'][1][b'name'], b'test3')

    def test_get_repositories_with_hosting_service(self):
        """Testing the GET repositories/?hosting-service= API"""
        hosting_account = HostingServiceAccount.objects.create(service_name=b'github', username=b'my-username')
        Repository.objects.create(name=b'My New Repository', path=b'https://example.com', tool=Tool.objects.get(name=b'Git'), hosting_account=hosting_account)
        rsp = self.api_get(get_repository_list_url() + b'?hosting-service=github', expected_mimetype=repository_list_mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        self.assertEqual(len(rsp[b'repositories']), 1)
        self.assertEqual(rsp[b'repositories'][0][b'name'], b'My New Repository')

    def test_get_repositories_with_hosting_service_many(self):
        """Testing the GET repositories/?hosting-service= API
        and comma-separated list
        """
        hosting_account = HostingServiceAccount.objects.create(service_name=b'github', username=b'my-username')
        Repository.objects.create(name=b'My New Repository 1', path=b'https://example.com', tool=Tool.objects.get(name=b'Git'), hosting_account=hosting_account)
        hosting_account = HostingServiceAccount.objects.create(service_name=b'beanstalk', username=b'my-username')
        Repository.objects.create(name=b'My New Repository 2', path=b'https://example.com', tool=Tool.objects.get(name=b'Subversion'), hosting_account=hosting_account)
        rsp = self.api_get(get_repository_list_url() + b'?hosting-service=github,beanstalk', expected_mimetype=repository_list_mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        self.assertEqual(len(rsp[b'repositories']), 2)
        self.assertEqual(rsp[b'repositories'][0][b'name'], b'My New Repository 1')
        self.assertEqual(rsp[b'repositories'][1][b'name'], b'My New Repository 2')

    def test_get_repositories_with_username(self):
        """Testing the GET repositories/?username= API"""
        hosting_account = HostingServiceAccount.objects.create(service_name=b'github', username=b'my-username')
        Repository.objects.create(name=b'My New Repository 1', path=b'https://example.com', tool=Tool.objects.get(name=b'Git'), hosting_account=hosting_account)
        Repository.objects.create(name=b'My New Repository 2', path=b'https://example.com', username=b'my-username', tool=Tool.objects.get(name=b'Subversion'))
        rsp = self.api_get(get_repository_list_url() + b'?username=my-username', expected_mimetype=repository_list_mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        self.assertEqual(len(rsp[b'repositories']), 2)
        self.assertEqual(rsp[b'repositories'][0][b'name'], b'My New Repository 1')
        self.assertEqual(rsp[b'repositories'][1][b'name'], b'My New Repository 2')

    def test_get_repositories_with_username_many(self):
        """Testing the GET repositories/?username= API
        and comma-separated list
        """
        hosting_account = HostingServiceAccount.objects.create(service_name=b'github', username=b'my-username')
        Repository.objects.create(name=b'My New Repository 1', path=b'https://example.com', tool=Tool.objects.get(name=b'Git'), hosting_account=hosting_account)
        Repository.objects.create(name=b'My New Repository 2', path=b'https://example.com', username=b'my-username-2', tool=Tool.objects.get(name=b'Subversion'))
        rsp = self.api_get(get_repository_list_url() + b'?username=my-username,my-username-2', expected_mimetype=repository_list_mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        self.assertEqual(len(rsp[b'repositories']), 2)
        self.assertEqual(rsp[b'repositories'][0][b'name'], b'My New Repository 1')
        self.assertEqual(rsp[b'repositories'][1][b'name'], b'My New Repository 2')

    def setup_basic_post_test(self, user, with_local_site, local_site_name, post_valid_data):
        return (
         get_repository_list_url(local_site_name),
         repository_item_mimetype,
         {b'name': b'Test Repository', 
            b'path': self.sample_repo_path, 
            b'tool': b'Test'}, [])

    def check_post_result(self, user, rsp):
        self._verify_repository_info(rsp, b'Test Repository', self.sample_repo_path, {})

    def test_post_with_visible_False(self):
        """Testing the POST repositories/ API with visible=False"""
        self._login_user(admin=True)
        rsp = self._post_repository(False, data={b'visible': False})
        self.assertEqual(rsp[b'repository'][b'visible'], False)

    def test_post_with_bad_host_key(self):
        """Testing the POST repositories/ API with Bad Host Key error"""
        hostname = b'example.com'
        key = key1
        expected_key = key2

        @classmethod
        def _check_repository(cls, *args, **kwargs):
            raise BadHostKeyError(hostname, key, expected_key)

        TestTool.check_repository = _check_repository
        self._login_user(admin=True)
        rsp = self._post_repository(False, expected_status=403)
        self.assertEqual(rsp[b'stat'], b'fail')
        self.assertEqual(rsp[b'err'][b'code'], BAD_HOST_KEY.code)
        self.assertIn(b'hostname', rsp)
        self.assertIn(b'expected_key', rsp)
        self.assertIn(b'key', rsp)
        self.assertEqual(rsp[b'hostname'], hostname)
        self.assertEqual(rsp[b'expected_key'], expected_key.get_base64())
        self.assertEqual(rsp[b'key'], key.get_base64())

    def test_post_with_bad_host_key_and_trust_host(self):
        """Testing the POST repositories/ API
        with Bad Host Key error and trust_host=1
        """
        hostname = b'example.com'
        key = key1
        expected_key = key2
        saw = {b'replace_host_key': False}

        def _replace_host_key(cls, _hostname, _expected_key, _key):
            self.assertEqual(hostname, _hostname)
            self.assertEqual(expected_key, _expected_key)
            self.assertEqual(key, _key)
            saw[b'replace_host_key'] = True

        @classmethod
        def _check_repository(cls, *args, **kwargs):
            if not saw[b'replace_host_key']:
                raise BadHostKeyError(hostname, key, expected_key)

        TestTool.check_repository = _check_repository
        SSHClient.replace_host_key = _replace_host_key
        self._login_user(admin=True)
        self._post_repository(False, data={b'trust_host': 1})
        self.assertTrue(saw[b'replace_host_key'])

    def test_post_with_unknown_host_key(self):
        """Testing the POST repositories/ API with Unknown Host Key error"""
        hostname = b'example.com'
        key = key1

        @classmethod
        def _check_repository(cls, *args, **kwargs):
            raise UnknownHostKeyError(hostname, key)

        TestTool.check_repository = _check_repository
        self._login_user(admin=True)
        rsp = self._post_repository(False, expected_status=403)
        self.assertEqual(rsp[b'stat'], b'fail')
        self.assertEqual(rsp[b'err'][b'code'], UNVERIFIED_HOST_KEY.code)
        self.assertIn(b'hostname', rsp)
        self.assertIn(b'key', rsp)
        self.assertEqual(rsp[b'hostname'], hostname)
        self.assertEqual(rsp[b'key'], key.get_base64())

    def test_post_with_unknown_host_key_and_trust_host(self):
        """Testing the POST repositories/ API
        with Unknown Host Key error and trust_host=1
        """
        hostname = b'example.com'
        key = key1
        saw = {b'add_host_key': False}

        def _add_host_key(cls, _hostname, _key):
            self.assertEqual(hostname, _hostname)
            self.assertEqual(key, _key)
            saw[b'add_host_key'] = True

        @classmethod
        def _check_repository(cls, *args, **kwargs):
            if not saw[b'add_host_key']:
                raise UnknownHostKeyError(hostname, key)

        TestTool.check_repository = _check_repository
        SSHClient.add_host_key = _add_host_key
        self._login_user(admin=True)
        self._post_repository(False, data={b'trust_host': 1})
        self.assertTrue(saw[b'add_host_key'])

    def test_post_with_unknown_cert(self):
        """Testing the POST repositories/ API with Unknown Certificate error"""

        class Certificate(object):
            failures = [
             b'failures']
            fingerprint = b'fingerprint'
            hostname = b'example.com'
            issuer = b'issuer'
            valid_from = b'valid_from'
            valid_until = b'valid_until'

        cert = Certificate()

        @classmethod
        def _check_repository(cls, *args, **kwargs):
            raise UnverifiedCertificateError(cert)

        TestTool.check_repository = _check_repository
        self._login_user(admin=True)
        rsp = self._post_repository(False, expected_status=403)
        self.assertEqual(rsp[b'stat'], b'fail')
        self.assertEqual(rsp[b'err'][b'code'], UNVERIFIED_HOST_CERT.code)
        self.assertIn(b'certificate', rsp)
        self.assertEqual(rsp[b'certificate'][b'failures'], cert.failures)
        self.assertEqual(rsp[b'certificate'][b'fingerprint'], cert.fingerprint)
        self.assertEqual(rsp[b'certificate'][b'hostname'], cert.hostname)
        self.assertEqual(rsp[b'certificate'][b'issuer'], cert.issuer)
        self.assertEqual(rsp[b'certificate'][b'valid'][b'from'], cert.valid_from)
        self.assertEqual(rsp[b'certificate'][b'valid'][b'until'], cert.valid_until)

    def test_post_with_unknown_cert_and_trust_host(self):
        """Testing the POST repositories/ API
        with Unknown Certificate error and trust_host=1
        """

        class Certificate(object):
            failures = [
             b'failures']
            fingerprint = b'fingerprint'
            hostname = b'example.com'
            issuer = b'issuer'
            valid_from = b'valid_from'
            valid_until = b'valid_until'

        cert = Certificate()
        saw = {b'accept_certificate': False}

        @classmethod
        def _check_repository(cls, *args, **kwargs):
            if not saw[b'accept_certificate']:
                raise UnverifiedCertificateError(cert)

        @classmethod
        def _accept_certificate(cls, path, local_site_name=None, **kwargs):
            saw[b'accept_certificate'] = True
            return {b'fingerprint': b'123'}

        TestTool.check_repository = _check_repository
        TestTool.accept_certificate = _accept_certificate
        self._login_user(admin=True)
        rsp = self._post_repository(False, data={b'trust_host': 1})
        self.assertTrue(saw[b'accept_certificate'])
        repository = Repository.objects.get(pk=rsp[b'repository'][b'id'])
        self.assertIn(b'cert', repository.extra_data)
        self.assertEqual(repository.extra_data[b'cert'][b'fingerprint'], b'123')
        return

    def test_post_with_missing_user_key(self):
        """Testing the POST repositories/ API with Missing User Key error"""

        @classmethod
        def _check_repository(cls, *args, **kwargs):
            raise AuthenticationError(allowed_types=[b'publickey'], user_key=None)
            return

        TestTool.check_repository = _check_repository
        self._login_user(admin=True)
        rsp = self._post_repository(False, expected_status=403)
        self.assertEqual(rsp[b'stat'], b'fail')
        self.assertEqual(rsp[b'err'][b'code'], MISSING_USER_KEY.code)

    def test_post_with_authentication_error(self):
        """Testing the POST repositories/ API with Authentication Error"""

        @classmethod
        def _check_repository(cls, *args, **kwargs):
            raise AuthenticationError

        TestTool.check_repository = _check_repository
        self._login_user(admin=True)
        rsp = self._post_repository(False, expected_status=403)
        self.assertEqual(rsp[b'stat'], b'fail')
        self.assertEqual(rsp[b'err'][b'code'], REPO_AUTHENTICATION_ERROR.code)
        self.assertIn(b'reason', rsp)

    def test_post_full_info(self):
        """Testing the POST repositories/ API with all available info"""
        self._login_user(admin=True)
        self._post_repository(False, {b'bug_tracker': b'http://bugtracker/%s/', 
           b'encoding': b'UTF-8', 
           b'mirror_path': b'http://svn.example.com/', 
           b'username': b'user', 
           b'password': b'123', 
           b'public': False, 
           b'raw_file_url': b'http://example.com/<filename>/<version>'})

    def test_post_with_no_access(self):
        """Testing the POST repositories/ API with no access"""
        self._login_user()
        self._post_repository(False, expected_status=403)

    def test_post_duplicate(self):
        """Testing the POST repositories/ API with a duplicate repository"""
        self._login_user(admin=True)
        self._post_repository(False)
        self._post_repository(False, expected_status=409)

    def _post_repository(self, use_local_site, data={}, expected_status=201):
        repo_name = b'Test Repository'
        if 200 <= expected_status < 300:
            expected_mimetype = repository_item_mimetype
        else:
            expected_mimetype = None
        if use_local_site:
            local_site_name = self.local_site_name
        else:
            local_site_name = None
        rsp = self.api_post(get_repository_list_url(local_site_name), dict({b'name': repo_name, 
           b'path': self.sample_repo_path, 
           b'tool': b'Test'}, **data), expected_status=expected_status, expected_mimetype=expected_mimetype)
        if 200 <= expected_status < 300:
            self._verify_repository_info(rsp, repo_name, self.sample_repo_path, data)
            self.assertEqual(rsp[b'repository'][b'links'][b'self'][b'href'], self.base_url + get_repository_item_url(rsp[b'repository'][b'id'], local_site_name))
        return rsp


@six.add_metaclass(BasicTestsMetaclass)
class ResourceItemTests(BaseRepositoryTests):
    """Testing the RepositoryResource item APIs."""
    sample_api_url = b'repositories/<id>/'
    fixtures = [b'test_users', b'test_scmtools']
    test_http_methods = ('GET', )
    resource = resources.repository

    def compare_item(self, item_rsp, repository):
        self.assertEqual(item_rsp[b'id'], repository.pk)
        self.assertEqual(item_rsp[b'path'], repository.path)

    def test_delete(self):
        """Testing the DELETE repositories/<id>/ API"""
        self._login_user(admin=True)
        repo_id = self._delete_repository(False, with_review_request=True)
        repo = Repository.objects.get(pk=repo_id)
        self.assertTrue(repo.archived)

    def test_delete_empty_repository(self):
        """Testing the DELETE repositories/<id>/ API with no review requests"""
        self._login_user(admin=True)
        repo_id = self._delete_repository(False)
        self.assertRaises(Repository.DoesNotExist, Repository.objects.get, pk=repo_id)

    @add_fixtures([b'test_site'])
    def test_delete_with_site(self):
        """Testing the DELETE repositories/<id>/ API with a local site"""
        self._login_user(local_site=True, admin=True)
        repo_id = self._delete_repository(True, with_review_request=True)
        repo = Repository.objects.get(pk=repo_id)
        self.assertTrue(repo.archived)

    @add_fixtures([b'test_site'])
    def test_delete_empty_repository_with_site(self):
        """Testing the DELETE repositories/<id>/ API
        with a local site and no review requests
        """
        self._login_user(local_site=True, admin=True)
        repo_id = self._delete_repository(True)
        self.assertRaises(Repository.DoesNotExist, Repository.objects.get, pk=repo_id)

    def test_delete_with_no_access(self):
        """Testing the DELETE repositories/<id>/ API with no access"""
        self._login_user()
        self._delete_repository(False, expected_status=403)

    @add_fixtures([b'test_site'])
    def test_delete_with_site_no_access(self):
        """Testing the DELETE repositories/<id>/ API
        with a local site and no access
        """
        self._login_user(local_site=True)
        self._delete_repository(True, expected_status=403)

    def setup_basic_get_test(self, user, with_local_site, local_site_name):
        repository = self.create_repository(with_local_site=with_local_site)
        return (
         get_repository_item_url(repository, local_site_name),
         repository_item_mimetype,
         repository)

    def test_put(self):
        """Testing the PUT repositories/<id>/ API"""
        self._login_user(admin=True)
        self._put_repository(False, {b'bug_tracker': b'http://bugtracker/%s/', 
           b'encoding': b'UTF-8', 
           b'mirror_path': b'http://svn.example.com/', 
           b'username': b'user', 
           b'password': b'123', 
           b'public': False, 
           b'raw_file_url': b'http://example.com/<filename>/<version>'})

    @add_fixtures([b'test_site'])
    def test_put_with_site(self):
        """Testing the PUT repositories/<id>/ API with a local site"""
        self._login_user(local_site=True, admin=True)
        self._put_repository(True, {b'bug_tracker': b'http://bugtracker/%s/', 
           b'encoding': b'UTF-8', 
           b'mirror_path': b'http://svn.example.com/', 
           b'username': b'user', 
           b'password': b'123', 
           b'public': False, 
           b'raw_file_url': b'http://example.com/<filename>/<version>'})

    def test_put_with_no_access(self):
        """Testing the PUT repositories/<id>/ API with no access"""
        self._login_user()
        self._put_repository(False, expected_status=403)

    @add_fixtures([b'test_site'])
    def test_put_with_site_no_access(self):
        """Testing the PUT repositories/<id>/ API
        with a local site and no access
        """
        self._login_user(local_site=True)
        self._put_repository(False, expected_status=403)

    def test_put_with_archive(self):
        """Testing the PUT repositories/<id>/ API with archive_name=True"""
        self._login_user(admin=True)
        repo_id = self._put_repository(False, {b'archive_name': True})
        repo = Repository.objects.get(pk=repo_id)
        self.assertEqual(repo.name[:23], b'ar:New Test Repository:')
        self.assertTrue(repo.archived)
        self.assertFalse(repo.public)
        self.assertIsNotNone(repo.archived_timestamp)

    def _put_repository(self, use_local_site, data={}, expected_status=200):
        repo_name = b'New Test Repository'
        repo = self.create_repository(with_local_site=use_local_site)
        if use_local_site:
            local_site_name = self.local_site_name
        else:
            local_site_name = None
        if 200 <= expected_status < 300:
            expected_mimetype = repository_item_mimetype
        else:
            expected_mimetype = None
        rsp = self.api_put(get_repository_item_url(repo, local_site_name), dict({b'name': repo_name, 
           b'path': self.sample_repo_path}, **data), expected_status=expected_status, expected_mimetype=expected_mimetype)
        if 200 <= expected_status < 300:
            self._verify_repository_info(rsp, repo_name, self.sample_repo_path, data)
        return repo.pk

    def _delete_repository(self, use_local_site, expected_status=204, with_review_request=False):
        repo = self.create_repository(with_local_site=use_local_site)
        if use_local_site:
            local_site_name = self.local_site_name
        else:
            local_site_name = None
        if with_review_request:
            request = ReviewRequest.objects.create(self.user, repo)
            request.save()
        self.api_delete(get_repository_item_url(repo, local_site_name), expected_status=expected_status)
        return repo.pk