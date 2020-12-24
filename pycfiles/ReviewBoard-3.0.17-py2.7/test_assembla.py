# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/hostingsvcs/tests/test_assembla.py
# Compiled at: 2020-02-11 04:03:56
"""Unit tests for the Assembla hosting service."""
from __future__ import unicode_literals
import nose
from reviewboard.admin.server import get_hostname
from reviewboard.hostingsvcs.testing import HostingServiceTestCase
from reviewboard.scmtools.crypto_utils import encrypt_password
from reviewboard.scmtools.models import Repository, Tool

class AssemblaTestCase(HostingServiceTestCase):
    """Base class for Assembla test suites."""
    service_name = b'assembla'
    fixtures = [b'test_scmtools']
    default_account_data = {b'password': encrypt_password(b'abc123')}


class AssemblaTests(AssemblaTestCase):
    """Unit tests for the Assembla hosting service."""

    def test_service_support(self):
        """Testing Assembla service support capabilities"""
        self.assertTrue(self.service_class.needs_authorization)
        self.assertTrue(self.service_class.supports_bug_trackers)
        self.assertTrue(self.service_class.supports_repositories)
        self.assertEqual(self.service_class.supported_scmtools, [
         b'Perforce', b'Subversion'])

    def test_get_repository_fields_with_perforce(self):
        """Testing Assembla.get_repository_fields for Perforce"""
        self.assertEqual(self.get_repository_fields(b'Perforce', fields={b'assembla_project_id': b'myproject'}), {b'path': b'perforce.assembla.com:1666', 
           b'encoding': b'utf8'})

    def test_get_repository_fields_with_subversion(self):
        """Testing Assembla.get_repository_fields for Subversion"""
        self.assertEqual(self.get_repository_fields(b'Subversion', fields={b'assembla_project_id': b'myproject', 
           b'assembla_repo_name': b'myrepo'}), {b'path': b'https://subversion.assembla.com/svn/myproject/'})

    def test_authorize(self):
        """Testing Assembla.authorize"""
        account = self.create_hosting_account(data={})
        service = account.service
        self.assertFalse(service.is_authorized())
        service.authorize(b'myuser', b'abc123', None)
        self.assertIn(b'password', account.data)
        self.assertNotEqual(account.data[b'password'], b'abc123')
        self.assertTrue(service.is_authorized())
        return

    def test_check_repository_perforce(self):
        """Testing Assembla.check_repository with Perforce"""
        try:
            account = self.create_hosting_account()
            service = account.service
            service.authorize(b'myuser', b'abc123', None)
            repository = Repository(hosting_account=account, tool=Tool.objects.get(name=b'Perforce'))
            scmtool = repository.get_scmtool()
            self.spy_on(scmtool.check_repository, call_original=False)
            service.check_repository(path=b'mypath', username=b'myusername', password=b'mypassword', scmtool_class=scmtool.__class__, local_site_name=None, assembla_project_id=b'myproject')
            self.assertTrue(scmtool.check_repository.called)
            self.assertIn(b'p4_host', scmtool.check_repository.last_call.kwargs)
            self.assertEqual(scmtool.check_repository.last_call.kwargs[b'p4_host'], b'myproject')
        except ImportError:
            raise nose.SkipTest

        return

    def test_check_repository_subversion(self):
        """Testing Assembla.check_repository with Subversion"""
        try:
            account = self.create_hosting_account()
            service = account.service
            service.authorize(b'myuser', b'abc123', None)
            repository = Repository(path=b'https://svn.example.com/', hosting_account=account, tool=Tool.objects.get(name=b'Subversion'))
            scmtool = repository.get_scmtool()
            self.spy_on(scmtool.check_repository, call_original=False)
            service.check_repository(path=b'https://svn.example.com/', username=b'myusername', password=b'mypassword', scmtool_class=scmtool.__class__, local_site_name=None)
            self.assertTrue(scmtool.check_repository.called)
            self.assertNotIn(b'p4_host', scmtool.check_repository.last_call.kwargs)
        except ImportError:
            raise nose.SkipTest

        return


class AssemblaFormTests(AssemblaTestCase):
    """Unit tests for reviewboard.hostingsvcs.assembla.AssemblaForm."""

    def setUp(self):
        super(AssemblaFormTests, self).setUp()
        self.account = self.create_hosting_account()

    def test_save_form_perforce(self):
        """Testing AssemblaForm with Perforce"""
        try:
            repository = self.create_repository(hosting_account=self.account, tool_name=b'Perforce')
            form = self.get_form(fields={b'assembla_project_id': b'myproject'})
            self.spy_on(get_hostname, call_fake=lambda : b'myhost.example.com')
            form.save(repository)
            self.assertIn(b'use_ticket_auth', repository.extra_data)
            self.assertTrue(repository.extra_data[b'use_ticket_auth'])
            self.assertIn(b'p4_host', repository.extra_data)
            self.assertIn(b'p4_client', repository.extra_data)
            self.assertEqual(repository.extra_data[b'p4_host'], b'myproject')
            self.assertEqual(repository.extra_data[b'p4_client'], b'myhost.example.com-myproject')
        except ImportError:
            raise nose.SkipTest(b'Perforce support is not installed')

    def test_save_form_perforce_with_portfolio(self):
        """Testing AssemblaForm with Perforce and Assembla portfolio IDs"""
        try:
            repository = self.create_repository(hosting_account=self.account, tool_name=b'Perforce')
            form = self.get_form(fields={b'assembla_project_id': b'myportfolio/myproject'})
            self.spy_on(get_hostname, call_fake=lambda : b'myhost.example.com')
            form.save(repository)
            self.assertIn(b'use_ticket_auth', repository.extra_data)
            self.assertTrue(repository.extra_data[b'use_ticket_auth'])
            self.assertIn(b'p4_host', repository.extra_data)
            self.assertIn(b'p4_client', repository.extra_data)
            self.assertEqual(repository.extra_data[b'p4_host'], b'myportfolio/myproject')
            self.assertEqual(repository.extra_data[b'p4_client'], b'myhost.example.com-myportfolio-myproject')
        except ImportError:
            raise nose.SkipTest(b'Perforce support is not installed')

    def test_save_form_subversion(self):
        """Testing AssemblaForm with Subversion"""
        try:
            repository = self.create_repository(path=b'https://svn.example.com/', hosting_account=self.account, tool_name=b'Subversion')
            form = self.get_form(fields={b'assembla_project_id': b'myproject'})
            form.save(repository)
            self.assertNotIn(b'use_ticket_auth', repository.extra_data)
            self.assertNotIn(b'p4_host', repository.extra_data)
        except ImportError:
            raise nose.SkipTest