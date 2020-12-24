# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/hostingsvcs/tests/test_hosting_service_auth_form.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import unicode_literals
from reviewboard.hostingsvcs.errors import AuthorizationError, TwoFactorAuthCodeRequiredError
from reviewboard.hostingsvcs.forms import HostingServiceAuthForm
from reviewboard.hostingsvcs.models import HostingServiceAccount
from reviewboard.hostingsvcs.service import register_hosting_service, unregister_hosting_service
from reviewboard.scmtools.models import Tool
from reviewboard.site.models import LocalSite
from reviewboard.testing import TestCase
from reviewboard.testing.hosting_services import SelfHostedTestService, TestService

class HostingServiceAuthFormTests(TestCase):
    """Unit tests for reviewboard.hostingsvcs.forms.HostingServiceAuthForm."""
    fixtures = [
     b'test_scmtools']

    def setUp(self):
        super(HostingServiceAuthFormTests, self).setUp()
        register_hosting_service(TestService.hosting_service_id, TestService)
        register_hosting_service(SelfHostedTestService.hosting_service_id, SelfHostedTestService)
        self.git_tool_id = Tool.objects.get(name=b'Git').pk

    def tearDown(self):
        super(HostingServiceAuthFormTests, self).tearDown()
        unregister_hosting_service(SelfHostedTestService.hosting_service_id)
        unregister_hosting_service(TestService.hosting_service_id)

    def test_override_help_texts(self):
        """Testing HostingServiceAuthForm subclasses overriding help texts"""

        class MyAuthForm(HostingServiceAuthForm):

            class Meta:
                help_texts = {b'hosting_account_username': b'My help text.'}

        form = MyAuthForm(hosting_service_cls=TestService)
        self.assertEqual(form.fields[b'hosting_account_username'].help_text, b'My help text.')

    def test_override_labels(self):
        """Testing HostingServiceAuthForm subclasses overriding labels"""

        class MyAuthForm(HostingServiceAuthForm):

            class Meta:
                labels = {b'hosting_account_username': b'My label.'}

        form = MyAuthForm(hosting_service_cls=TestService)
        self.assertEqual(form.fields[b'hosting_account_username'].label, b'My label.')

    def test_get_credentials_default(self):
        """Testing HostingServiceAuthForm.get_credentials default behavior"""
        form = HostingServiceAuthForm({b'hosting_account_username': b'myuser', 
           b'hosting_account_password': b'mypass'}, hosting_service_cls=TestService)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.get_credentials(), {b'username': b'myuser', 
           b'password': b'mypass'})

    def test_get_credentials_default_with_2fa_code(self):
        """Testing HostingServiceAuthForm.get_credentials default behavior
        with two-factor auth code
        """
        form = HostingServiceAuthForm({b'hosting_account_username': b'myuser', 
           b'hosting_account_password': b'mypass', 
           b'hosting_account_two_factor_auth_code': b'123456'}, hosting_service_cls=TestService)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.get_credentials(), {b'username': b'myuser', 
           b'password': b'mypass', 
           b'two_factor_auth_code': b'123456'})

    def test_get_credentials_with_form_prefix(self):
        """Testing HostingServiceAuthForm.get_credentials default behavior
        with form prefix
        """
        form = HostingServiceAuthForm({b'myservice-hosting_account_username': b'myuser', 
           b'myservice-hosting_account_password': b'mypass', 
           b'myservice-hosting_account_two_factor_auth_code': b'123456'}, hosting_service_cls=TestService, prefix=b'myservice')
        self.assertTrue(form.is_valid())
        self.assertEqual(form.get_credentials(), {b'username': b'myuser', 
           b'password': b'mypass', 
           b'two_factor_auth_code': b'123456'})

    def test_save_new_account(self):
        """Testing HostingServiceAuthForm.save with new account"""
        form = HostingServiceAuthForm({b'hosting_account_username': b'myuser', 
           b'hosting_account_password': b'mypass'}, hosting_service_cls=TestService)
        self.assertTrue(form.is_valid())
        hosting_account = form.save()
        self.assertIsNotNone(hosting_account.pk)
        self.assertEqual(hosting_account.service_name, b'test')
        self.assertEqual(hosting_account.username, b'myuser')
        self.assertEqual(hosting_account.data[b'password'], b'mypass')
        self.assertIsNone(hosting_account.hosting_url)
        self.assertIsNone(hosting_account.local_site)

    def test_save_new_account_with_existing_stored(self):
        """Testing HostingServiceAuthForm.save with new account matching
        existing stored account information
        """
        form = HostingServiceAuthForm({b'hosting_account_username': b'myuser', 
           b'hosting_account_password': b'mypass'}, hosting_service_cls=TestService)
        self.assertTrue(form.is_valid())
        orig_account = HostingServiceAccount.objects.create(service_name=b'test', username=b'myuser')
        hosting_account = form.save()
        self.assertIsNotNone(hosting_account.pk)
        self.assertEqual(hosting_account.pk, orig_account.pk)
        self.assertEqual(hosting_account.service_name, b'test')
        self.assertEqual(hosting_account.username, b'myuser')
        self.assertEqual(hosting_account.data[b'password'], b'mypass')
        self.assertIsNone(hosting_account.hosting_url)
        self.assertIsNone(hosting_account.local_site)

    def test_save_new_account_with_hosting_url(self):
        """Testing HostingServiceAuthForm.save with new account and hosting URL
        """
        form = HostingServiceAuthForm({b'hosting_account_username': b'myuser', 
           b'hosting_account_password': b'mypass', 
           b'hosting_url': b'example.com'}, hosting_service_cls=SelfHostedTestService)
        self.assertTrue(form.is_valid())
        hosting_account = form.save()
        self.assertIsNotNone(hosting_account.pk)
        self.assertEqual(hosting_account.service_name, b'self_hosted_test')
        self.assertEqual(hosting_account.username, b'myuser')
        self.assertEqual(hosting_account.data[b'password'], b'mypass')
        self.assertEqual(hosting_account.hosting_url, b'example.com')
        self.assertIsNone(hosting_account.local_site)

    def test_save_new_account_with_hosting_url_not_self_hosted(self):
        """Testing HostingServiceAuthForm.save with new account and hosting URL
        with non-self-hosted service
        """
        form = HostingServiceAuthForm({b'hosting_account_username': b'myuser', 
           b'hosting_account_password': b'mypass', 
           b'hosting_url': b'example.com'}, hosting_service_cls=TestService)
        self.assertTrue(form.is_valid())
        self.assertNotIn(b'hosting_url', form.cleaned_data)
        hosting_account = form.save()
        self.assertIsNone(hosting_account.hosting_url)

    def test_save_new_account_without_hosting_url_self_hosted(self):
        """Testing HostingServiceAuthForm.save with new account and no
        hosting URL with a self-hosted service
        """
        form = HostingServiceAuthForm({b'hosting_account_username': b'myuser', 
           b'hosting_account_password': b'mypass'}, hosting_service_cls=SelfHostedTestService)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {b'hosting_url': [
                          b'This field is required.']})

    def test_save_new_account_with_local_site(self):
        """Testing HostingServiceAuthForm.save with new account and Local Site
        """
        local_site = LocalSite.objects.create(name=b'test-site')
        form = HostingServiceAuthForm({b'hosting_account_username': b'myuser', 
           b'hosting_account_password': b'mypass'}, hosting_service_cls=TestService, local_site=local_site)
        self.assertTrue(form.is_valid())
        hosting_account = form.save()
        self.assertIsNotNone(hosting_account.pk)
        self.assertEqual(hosting_account.service_name, b'test')
        self.assertEqual(hosting_account.username, b'myuser')
        self.assertEqual(hosting_account.data[b'password'], b'mypass')
        self.assertEqual(hosting_account.local_site, local_site)
        self.assertIsNone(hosting_account.hosting_url)

    def test_save_new_account_without_username(self):
        """Testing HostingServiceAuthForm.save with new account and no
        username in credentials
        """

        class MyAuthForm(HostingServiceAuthForm):

            def get_credentials(self):
                return {}

        form = MyAuthForm({b'hosting_account_username': b'myuser', 
           b'hosting_account_password': b'mypass'}, hosting_service_cls=TestService)
        self.assertTrue(form.is_valid())
        expected_message = b'Hosting service implementation error: MyAuthForm.get_credentials() must return a "username" key.'
        with self.assertRaisesMessage(AuthorizationError, expected_message):
            form.save()

    def test_save_existing_account(self):
        """Testing HostingServiceAuthForm.save with updating existing account
        """
        orig_account = HostingServiceAccount.objects.create(service_name=b'test', username=b'myuser')
        form = HostingServiceAuthForm({b'hosting_account_username': b'myuser', 
           b'hosting_account_password': b'mypass'}, hosting_service_cls=TestService, hosting_account=orig_account)
        self.assertTrue(form.is_valid())
        hosting_account = form.save()
        self.assertIs(hosting_account, orig_account)
        self.assertEqual(hosting_account.pk, orig_account.pk)
        self.assertEqual(hosting_account.service_name, b'test')
        self.assertEqual(hosting_account.username, b'myuser')
        self.assertEqual(hosting_account.data[b'password'], b'mypass')
        self.assertIsNone(hosting_account.hosting_url)
        self.assertIsNone(hosting_account.local_site)

    def test_save_existing_account_new_username(self):
        """Testing HostingServiceAuthForm.save with updating existing account
        with new username
        """
        orig_account = HostingServiceAccount.objects.create(service_name=b'test', username=b'myuser')
        form = HostingServiceAuthForm({b'hosting_account_username': b'mynewuser', 
           b'hosting_account_password': b'mypass'}, hosting_service_cls=TestService, hosting_account=orig_account)
        self.assertTrue(form.is_valid())
        hosting_account = form.save()
        self.assertIs(hosting_account, orig_account)
        self.assertEqual(hosting_account.pk, orig_account.pk)
        self.assertEqual(hosting_account.service_name, b'test')
        self.assertEqual(hosting_account.username, b'mynewuser')
        self.assertEqual(hosting_account.data[b'password'], b'mypass')
        self.assertIsNone(hosting_account.hosting_url)
        self.assertIsNone(hosting_account.local_site)

    def test_save_existing_account_new_hosting_url(self):
        """Testing HostingServiceAuthForm.save with updating existing account
        with new hosting URL
        """
        orig_account = HostingServiceAccount.objects.create(service_name=b'self_hosted_test', username=b'myuser', hosting_url=b'example1.com')
        form = HostingServiceAuthForm({b'hosting_account_username': b'myuser', 
           b'hosting_account_password': b'mypass', 
           b'hosting_url': b'example2.com'}, hosting_service_cls=SelfHostedTestService, hosting_account=orig_account)
        self.assertTrue(form.is_valid())
        hosting_account = form.save()
        self.assertIs(hosting_account, orig_account)
        self.assertEqual(hosting_account.pk, orig_account.pk)
        self.assertEqual(hosting_account.service_name, b'self_hosted_test')
        self.assertEqual(hosting_account.username, b'myuser')
        self.assertEqual(hosting_account.data[b'password'], b'mypass')
        self.assertEqual(hosting_account.hosting_url, b'example2.com')
        self.assertIsNone(hosting_account.local_site)

    def test_save_existing_account_new_service_fails(self):
        """Testing HostingServiceAuthForm.save with updating existing account
        with new hosting service fails
        """
        orig_account = HostingServiceAccount.objects.create(service_name=b'self_hosted_test', username=b'myuser', hosting_url=b'example1.com')
        expected_message = b'This account is not compatible with this hosting service configuration.'
        with self.assertRaisesMessage(ValueError, expected_message):
            HostingServiceAuthForm(hosting_service_cls=TestService, hosting_account=orig_account)

    def test_save_existing_account_new_local_site_fails(self):
        """Testing HostingServiceAuthForm.save with updating existing account
        with new Local Site fails
        """
        orig_account = HostingServiceAccount.objects.create(service_name=b'text', username=b'myuser')
        expected_message = b'This account is not compatible with this hosting service configuration.'
        with self.assertRaisesMessage(ValueError, expected_message):
            HostingServiceAuthForm(hosting_service_cls=TestService, hosting_account=orig_account, local_site=LocalSite.objects.create(name=b'test-site'))

    def test_save_with_2fa_code_required(self):
        """Testing HostingServiceAuthForm.save with two-factor auth code
        required
        """
        form = HostingServiceAuthForm({b'hosting_account_username': b'2fa-user', 
           b'hosting_account_password': b'mypass'}, hosting_service_cls=TestService)
        self.assertTrue(form.is_valid())
        self.assertFalse(form.fields[b'hosting_account_two_factor_auth_code'].required)
        with self.assertRaises(TwoFactorAuthCodeRequiredError):
            form.save()
        self.assertTrue(form.fields[b'hosting_account_two_factor_auth_code'].required)

    def test_save_with_2fa_code_provided(self):
        """Testing HostingServiceAuthForm.save with two-factor auth code
        provided
        """
        form = HostingServiceAuthForm({b'hosting_account_username': b'2fa-user', 
           b'hosting_account_password': b'mypass', 
           b'hosting_account_two_factor_auth_code': b'123456'}, hosting_service_cls=TestService)
        self.assertTrue(form.is_valid())
        hosting_account = form.save()
        self.assertEqual(hosting_account.service_name, b'test')
        self.assertEqual(hosting_account.username, b'2fa-user')