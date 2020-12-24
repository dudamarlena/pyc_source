# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/hostingsvcs/tests/test_kiln.py
# Compiled at: 2020-02-11 04:03:56
"""Unit tests for the Kiln hosting service."""
from __future__ import unicode_literals
from reviewboard.hostingsvcs.errors import RepositoryError
from reviewboard.hostingsvcs.service import HostingServiceClient
from reviewboard.hostingsvcs.testing import HostingServiceTestCase

class KilnTests(HostingServiceTestCase):
    """Unit tests for the Kiln hosting service."""
    service_name = b'kiln'
    fixtures = [b'test_scmtools']
    default_account_data = {b'auth_token': b'my-token', 
       b'kiln_account_domain': b'mydomain'}
    default_repository_extra_data = {b'kiln_account_domain': b'mydomain', 
       b'kiln_project_name': b'myproject', 
       b'kiln_group_name': b'mygroup', 
       b'kiln_repo_name': b'myrepo'}

    def test_service_support(self):
        """Testing Kiln service support capabilities"""
        self.assertTrue(self.service_class.supports_repositories)
        self.assertTrue(self.service_class.needs_authorization)
        self.assertFalse(self.service_class.supports_bug_trackers)
        self.assertFalse(self.service_class.supports_post_commit)
        self.assertFalse(self.service_class.supports_two_factor_auth)

    def test_repo_field_values_git(self):
        """Testing Kiln.get_repository_fields for Git"""
        self.assertEqual(self.get_repository_fields(b'Git', fields={b'kiln_account_domain': b'mydomain', 
           b'kiln_project_name': b'myproject', 
           b'kiln_group_name': b'mygroup', 
           b'kiln_repo_name': b'myrepo'}), {b'path': b'https://mydomain.kilnhg.com/Code/myproject/mygroup/myrepo.git', 
           b'mirror_path': b'ssh://mydomain@mydomain.kilnhg.com/myproject/mygroup/myrepo'})

    def test_repo_field_values_mercurial(self):
        """Testing Kiln.get_repository_fields for Mercurial"""
        self.assertEqual(self.get_repository_fields(b'Mercurial', fields={b'kiln_account_domain': b'mydomain', 
           b'kiln_project_name': b'myproject', 
           b'kiln_group_name': b'mygroup', 
           b'kiln_repo_name': b'myrepo'}), {b'path': b'https://mydomain.kilnhg.com/Code/myproject/mygroup/myrepo', 
           b'mirror_path': b'ssh://mydomain@mydomain.kilnhg.com/myproject/mygroup/myrepo'})

    def test_authorize(self):
        """Testing Kiln.authorize"""
        hosting_account = self.create_hosting_account(data={})
        self.spy_on(HostingServiceClient._make_form_data_boundary, call_fake=lambda : b'BOUNDARY')
        with self.setup_http_test(payload=b'"my-token"', hosting_account=hosting_account, expected_http_calls=1) as (ctx):
            self.assertFalse(ctx.service.is_authorized())
            ctx.service.authorize(username=b'myuser', password=b'abc123', kiln_account_domain=b'mydomain')
        ctx.assertHTTPCall(0, url=b'https://mydomain.kilnhg.com/Api/1.0/Auth/Login', method=b'POST', username=None, password=None, body=b'--BOUNDARY\r\nContent-Disposition: form-data; name="sPassword"\r\n\r\nabc123\r\n--BOUNDARY\r\nContent-Disposition: form-data; name="sUser"\r\n\r\nmyuser\r\n--BOUNDARY--', headers={b'Content-Length': b'152', 
           b'Content-Type': b'multipart/form-data; boundary=BOUNDARY'})
        self.assertIn(b'auth_token', hosting_account.data)
        self.assertEqual(hosting_account.data[b'auth_token'], b'my-token')
        self.assertTrue(ctx.service.is_authorized())
        return

    def test_check_repository(self):
        """Testing Kiln.check_repository"""
        payload = self.dump_json([
         {b'sSlug': b'myproject', 
            b'repoGroups': [
                          {b'sSlug': b'mygroup', 
                             b'repos': [
                                      {b'sSlug': b'myrepo'}]}]}])
        with self.setup_http_test(payload=payload, expected_http_calls=1) as (ctx):
            ctx.service.check_repository(kiln_account_domain=b'mydomain', kiln_project_name=b'myproject', kiln_group_name=b'mygroup', kiln_repo_name=b'myrepo', tool_name=b'Mercurial')
        ctx.assertHTTPCall(0, url=b'https://mydomain.kilnhg.com/Api/1.0/Project?token=my-token', username=None, password=None)
        return

    def test_check_repository_with_incorrect_repo_info(self):
        """Testing Kiln.check_repository with incorrect repo info"""
        payload = self.dump_json([
         {b'sSlug': b'otherproject', 
            b'repoGroups': [
                          {b'sSlug': b'othergroup', 
                             b'repos': [
                                      {b'sSlug': b'otherrepo'}]}]}])
        expected_message = b'The repository with this project, group, and name was not found. Please verify that the information exactly matches the configuration on Kiln.'
        with self.setup_http_test(payload=payload, expected_http_calls=1) as (ctx):
            with self.assertRaisesMessage(RepositoryError, expected_message):
                ctx.service.check_repository(kiln_account_domain=b'mydomain', kiln_project_name=b'myproject', kiln_group_name=b'mygroup', kiln_repo_name=b'myrepo', tool_name=b'Mercurial')
        ctx.assertHTTPCall(0, url=b'https://mydomain.kilnhg.com/Api/1.0/Project?token=my-token', username=None, password=None)
        return

    def test_get_file(self):
        """Testing Kiln.get_file"""
        paths = {b'/Api/1.0/Project': {b'payload': self.dump_json([
                                            {b'sSlug': b'myproject', 
                                               b'repoGroups': [
                                                             {b'sSlug': b'mygroup', 
                                                                b'repos': [
                                                                         {b'sSlug': b'myrepo', 
                                                                            b'ixRepo': 123}]}]}])}, 
           b'/Api/1.0/Repo/123/Raw/File/2F70617468': {b'payload': b'My data'}}
        with self.setup_http_test(self.make_handler_for_paths(paths), expected_http_calls=2) as (ctx):
            repository = ctx.create_repository(tool_name=b'Mercurial')
            result = ctx.service.get_file(repository=repository, path=b'/path', revision=b'123')
        self.assertIsInstance(result, bytes)
        self.assertEqual(result, b'My data')
        ctx.assertHTTPCall(0, url=b'https://mydomain.kilnhg.com/Api/1.0/Project?token=my-token', method=b'GET', username=None, password=None)
        ctx.assertHTTPCall(1, url=b'https://mydomain.kilnhg.com/Api/1.0/Repo/123/Raw/File/2F70617468?rev=123&token=my-token', username=None, password=None)
        return

    def test_get_file_exists(self):
        """Testing Kiln.get_file_exists"""
        paths = {b'/Api/1.0/Project': {b'payload': self.dump_json([
                                            {b'sSlug': b'myproject', 
                                               b'repoGroups': [
                                                             {b'sSlug': b'mygroup', 
                                                                b'repos': [
                                                                         {b'sSlug': b'myrepo', 
                                                                            b'ixRepo': 123}]}]}])}, 
           b'/Api/1.0/Repo/123/Raw/File/2F70617468': {b'payload': b'My data'}}
        with self.setup_http_test(self.make_handler_for_paths(paths), expected_http_calls=2) as (ctx):
            repository = ctx.create_repository()
            result = ctx.service.get_file_exists(repository=repository, path=b'/path', revision=b'123')
        self.assertTrue(result)
        ctx.assertHTTPCall(0, url=b'https://mydomain.kilnhg.com/Api/1.0/Project?token=my-token', username=None, password=None)
        ctx.assertHTTPCall(1, url=b'https://mydomain.kilnhg.com/Api/1.0/Repo/123/Raw/File/2F70617468?rev=123&token=my-token', username=None, password=None)
        return