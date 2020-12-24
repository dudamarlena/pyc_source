# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/scmtools/tests/test_repository_form.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.utils import six
from kgb import SpyAgency
from reviewboard.hostingsvcs.models import HostingServiceAccount
from reviewboard.hostingsvcs.service import get_hosting_service, register_hosting_service, unregister_hosting_service
from reviewboard.scmtools.forms import RepositoryForm
from reviewboard.scmtools.models import Repository, Tool
from reviewboard.site.models import LocalSite
from reviewboard.testing.hosting_services import SelfHostedTestService, TestService
from reviewboard.testing.testcase import TestCase

class HiddenTestService(TestService):
    hosting_service_id = b'hidden-test'
    name = b'Hidden Test Service'
    visible = False


class RepositoryFormTests(SpyAgency, TestCase):
    """Unit tests for the repository form."""
    fixtures = [
     b'test_scmtools']

    def setUp(self):
        super(RepositoryFormTests, self).setUp()
        register_hosting_service(b'test', TestService)
        register_hosting_service(b'self_hosted_test', SelfHostedTestService)
        register_hosting_service(b'hidden-test', HiddenTestService)

    def tearDown(self):
        super(RepositoryFormTests, self).tearDown()
        unregister_hosting_service(b'self_hosted_test')
        unregister_hosting_service(b'test')
        unregister_hosting_service(b'hidden-test')

    def test_without_localsite(self):
        """Testing RepositoryForm without a LocalSite"""
        local_site = LocalSite.objects.create(name=b'test')
        local_site_user = User.objects.create_user(username=b'testuser1')
        local_site.users.add(local_site_user)
        global_site_user = User.objects.create_user(username=b'testuser2')
        local_site_group = self.create_review_group(name=b'test1', invite_only=True, local_site=local_site)
        global_site_group = self.create_review_group(name=b'test2', invite_only=True)
        local_site_account = HostingServiceAccount.objects.create(username=b'local-test-user', service_name=b'test', local_site=local_site)
        global_site_account = HostingServiceAccount.objects.create(username=b'global-test-user', service_name=b'test')
        form = RepositoryForm()
        self.assertIsNone(form.limited_to_local_site)
        self.assertIn(b'local_site', form.fields)
        self.assertEqual(list(form.fields[b'users'].queryset), [
         local_site_user, global_site_user])
        self.assertEqual(list(form.fields[b'review_groups'].queryset), [
         local_site_group, global_site_group])
        self.assertEqual(list(form.fields[b'hosting_account'].queryset), [
         local_site_account, global_site_account])
        form = self._build_form({b'name': b'test', 
           b'tool': b'git', 
           b'path': b'/path/to/test.git', 
           b'public': False, 
           b'users': [
                    global_site_user.pk], 
           b'review_groups': [
                            global_site_group.pk]})
        self.assertIsNone(form.limited_to_local_site)
        self.assertIn(b'local_site', form.fields)
        self.assertEqual(list(form.fields[b'users'].queryset), [
         local_site_user, global_site_user])
        self.assertEqual(list(form.fields[b'review_groups'].queryset), [
         local_site_group, global_site_group])
        self.assertIsNone(form.fields[b'users'].widget.local_site_name)
        self.assertEqual(list(form.fields[b'hosting_account'].queryset), [
         local_site_account, global_site_account])
        self.assertEqual(list(form.iter_subforms(bound_only=True)), [
         form.scmtool_repository_forms[b'git']])
        self.assertTrue(form.is_valid())
        self.assertEqual(list(form.fields[b'users'].queryset), [
         local_site_user, global_site_user])
        self.assertEqual(list(form.fields[b'review_groups'].queryset), [
         local_site_group, global_site_group])
        self.assertEqual(list(form.fields[b'hosting_account'].queryset), [
         local_site_account, global_site_account])
        repository = form.save()
        form.save_m2m()
        self.assertIsNone(repository.local_site)
        self.assertEqual(repository.extra_data, {})
        self.assertEqual(list(repository.users.all()), [global_site_user])
        self.assertEqual(list(repository.review_groups.all()), [
         global_site_group])

    def test_without_localsite_and_instance(self):
        """Testing RepositoryForm without a LocalSite and editing instance"""
        local_site = LocalSite.objects.create(name=b'test')
        git_tool = Tool.objects.get(name=b'Git')
        repository = self.create_repository(local_site=local_site)
        form = self._build_form(data={b'name': b'test', 
           b'tool': b'git', 
           b'path': b'/path/to/test.git'}, instance=repository)
        self.assertEqual(form.fields[b'tool'].initial, b'git')
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data[b'tool'], git_tool)
        self.assertEqual(list(form.iter_subforms(bound_only=True)), [
         form.scmtool_repository_forms[b'git']])
        new_repository = form.save()
        self.assertEqual(repository.pk, new_repository.pk)
        self.assertEqual(repository.extra_data, {})
        self.assertIsNone(new_repository.local_site)
        self.assertEqual(new_repository.tool, git_tool)

    def test_without_localsite_and_with_local_site_user(self):
        """Testing RepositoryForm without a LocalSite and User on a LocalSite
        """
        local_site = LocalSite.objects.create(name=b'test')
        user = User.objects.create_user(username=b'testuser1')
        local_site.users.add(user)
        form = self._build_form({b'name': b'test', 
           b'tool': b'git', 
           b'path': b'/path/to/test.git', 
           b'users': [
                    user.pk]})
        self.assertTrue(form.is_valid())
        self.assertEqual(list(form.iter_subforms(bound_only=True)), [
         form.scmtool_repository_forms[b'git']])

    def test_without_localsite_and_with_local_site_group(self):
        """Testing RepositoryForm without a LocalSite and Group on a LocalSite
        """
        local_site = LocalSite.objects.create(name=b'test')
        group = self.create_review_group(local_site=local_site)
        form = self._build_form({b'name': b'test', 
           b'tool': b'git', 
           b'path': b'/path/to/test.git', 
           b'review_groups': [
                            group.pk]})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {b'review_groups': [
                            b'Select a valid choice. 1 is not one of the available choices.']})
        self.assertEqual(list(form.iter_subforms(bound_only=True)), [
         form.scmtool_repository_forms[b'git']])

    def test_without_localsite_and_with_local_site_hosting_account(self):
        """Testing RepositoryForm without a LocalSite and
        HostingServiceAccount on a LocalSite
        """
        local_site = LocalSite.objects.create(name=b'test')
        hosting_account = HostingServiceAccount.objects.create(username=b'test-user', service_name=b'test', local_site=local_site)
        form = self._build_form({b'name': b'test', 
           b'hosting_type': b'test', 
           b'hosting_account': hosting_account.pk, 
           b'test_repo_name': b'test', 
           b'tool': b'git'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {b'hosting_account': [
                              b'Select a valid choice. That choice is not one of the available choices.']})
        self.assertEqual(list(form.iter_subforms(bound_only=True)), [
         form.hosting_repository_forms[b'test'][b'default']])

    def test_with_limited_localsite(self):
        """Testing RepositoryForm limited to a LocalSite"""
        local_site = LocalSite.objects.create(name=b'test')
        local_site_user = User.objects.create_user(username=b'testuser1')
        local_site.users.add(local_site_user)
        User.objects.create_user(username=b'testuser2')
        local_site_group = self.create_review_group(name=b'test1', invite_only=True, local_site=local_site)
        self.create_review_group(name=b'test2', invite_only=True)
        form = self._build_form(limit_to_local_site=local_site)
        self.assertEqual(form.limited_to_local_site, local_site)
        self.assertNotIn(b'local_site', form.fields)
        self.assertEqual(list(form.fields[b'users'].queryset), [
         local_site_user])
        self.assertEqual(list(form.fields[b'review_groups'].queryset), [
         local_site_group])
        self.assertEqual(form.fields[b'users'].widget.local_site_name, local_site.name)
        self.assertEqual(list(form.iter_subforms(bound_only=True)), [])

    def test_with_limited_localsite_and_changing_site(self):
        """Testing RepositoryForm limited to a LocalSite and changing
        LocalSite
        """
        local_site1 = LocalSite.objects.create(name=b'test-site-1')
        local_site2 = LocalSite.objects.create(name=b'test-site-2')
        form = self._build_form({b'name': b'test', 
           b'tool': b'git', 
           b'path': b'/path/to/test.git', 
           b'local_site': local_site2.pk}, limit_to_local_site=local_site1)
        self.assertEqual(form.limited_to_local_site, local_site1)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data[b'local_site'], local_site1)
        self.assertEqual(list(form.iter_subforms(bound_only=True)), [
         form.scmtool_repository_forms[b'git']])
        repository = form.save()
        self.assertEqual(repository.local_site, local_site1)

    def test_with_limited_localsite_and_compatible_instance(self):
        """Testing RepositoryForm limited to a LocalSite and editing compatible
        instance
        """
        local_site = LocalSite.objects.create(name=b'test')
        repository = self.create_repository(local_site=local_site)
        RepositoryForm(instance=repository, limit_to_local_site=local_site)

    def test_with_limited_localsite_and_incompatible_instance(self):
        """Testing RepositoryForm limited to a LocalSite and editing
        incompatible instance
        """
        local_site = LocalSite.objects.create(name=b'test')
        repository = self.create_repository()
        error_message = b'The provided instance is not associated with a LocalSite compatible with this form. Please contact support.'
        with self.assertRaisesMessage(ValueError, error_message):
            RepositoryForm(instance=repository, limit_to_local_site=local_site)

    def test_with_limited_localsite_and_invalid_user(self):
        """Testing DefaultReviewerForm limited to a LocalSite with a User
        not on the LocalSite
        """
        local_site = LocalSite.objects.create(name=b'test')
        user = User.objects.create_user(username=b'test')
        form = self._build_form({b'name': b'test', 
           b'tool': b'git', 
           b'path': b'/path/to/test.git', 
           b'users': [
                    user.pk]}, limit_to_local_site=local_site)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {b'users': [
                    b'Select a valid choice. 1 is not one of the available choices.']})
        self.assertEqual(list(form.iter_subforms(bound_only=True)), [
         form.scmtool_repository_forms[b'git']])

    def test_with_limited_localsite_and_invalid_group(self):
        """Testing DefaultReviewerForm limited to a LocalSite with a Group
        not on the LocalSite
        """
        local_site = LocalSite.objects.create(name=b'test')
        group = self.create_review_group()
        form = self._build_form({b'name': b'test', 
           b'tool': b'git', 
           b'path': b'/path/to/test.git', 
           b'review_groups': [
                            group.pk]}, limit_to_local_site=local_site)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {b'review_groups': [
                            b'Select a valid choice. 1 is not one of the available choices.']})
        self.assertEqual(list(form.iter_subforms(bound_only=True)), [
         form.scmtool_repository_forms[b'git']])

    def test_with_limited_localsite_and_invalid_hosting_account(self):
        """Testing DefaultReviewerForm limited to a LocalSite with a
        HostingServiceAccount not on the LocalSite
        """
        local_site = LocalSite.objects.create(name=b'test')
        hosting_account = HostingServiceAccount.objects.create(username=b'test-user', service_name=b'test')
        form = self._build_form({b'name': b'test', 
           b'hosting_type': b'test', 
           b'hosting_account': hosting_account.pk, 
           b'test_repo_name': b'test', 
           b'tool': b'git'}, limit_to_local_site=local_site)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {b'hosting_account': [
                              b'Select a valid choice. That choice is not one of the available choices.']})
        self.assertEqual(list(form.iter_subforms(bound_only=True)), [
         form.hosting_repository_forms[b'test'][b'default']])

    def test_with_localsite_in_data(self):
        """Testing RepositoryForm with a LocalSite in form data"""
        local_site = LocalSite.objects.create(name=b'test')
        local_site_user = User.objects.create_user(username=b'testuser1')
        local_site.users.add(local_site_user)
        global_site_user = User.objects.create_user(username=b'testuser2')
        local_site_group = self.create_review_group(name=b'test1', invite_only=True, local_site=local_site)
        global_site_group = self.create_review_group(name=b'test2', invite_only=True)
        local_site_account = HostingServiceAccount.objects.create(username=b'local-test-user', service_name=b'test', local_site=local_site)
        local_site_account.data[b'password'] = b'testpass'
        local_site_account.save(update_fields=('data', ))
        global_site_account = HostingServiceAccount.objects.create(username=b'global-test-user', service_name=b'test')
        form = RepositoryForm()
        self.assertIsNone(form.limited_to_local_site)
        self.assertIn(b'local_site', form.fields)
        self.assertEqual(list(form.fields[b'users'].queryset), [
         local_site_user, global_site_user])
        self.assertEqual(list(form.fields[b'review_groups'].queryset), [
         local_site_group, global_site_group])
        self.assertIsNone(form.fields[b'users'].widget.local_site_name)
        self.assertEqual(list(form.fields[b'hosting_account'].queryset), [
         local_site_account, global_site_account])
        form = self._build_form({b'name': b'test', 
           b'hosting_type': b'test', 
           b'hosting_account': local_site_account.pk, 
           b'test_repo_name': b'test', 
           b'tool': b'git', 
           b'path': b'/path/to/test.git', 
           b'public': False, 
           b'local_site': local_site.pk, 
           b'users': [
                    local_site_user.pk], 
           b'review_groups': [
                            local_site_group.pk]})
        self.assertIsNone(form.limited_to_local_site)
        self.assertIn(b'local_site', form.fields)
        self.assertEqual(list(form.fields[b'users'].queryset), [
         local_site_user, global_site_user])
        self.assertEqual(list(form.fields[b'review_groups'].queryset), [
         local_site_group, global_site_group])
        self.assertIsNone(form.fields[b'users'].widget.local_site_name)
        self.assertEqual(list(form.fields[b'hosting_account'].queryset), [
         local_site_account, global_site_account])
        self.assertEqual(list(form.iter_subforms(bound_only=True)), [
         form.hosting_repository_forms[b'test'][b'default']])
        self.assertTrue(form.is_valid())
        self.assertEqual(list(form.fields[b'users'].queryset), [
         local_site_user, global_site_user])
        self.assertEqual(list(form.fields[b'review_groups'].queryset), [
         local_site_group, global_site_group])
        self.assertEqual(list(form.fields[b'hosting_account'].queryset), [
         local_site_account, global_site_account])
        repository = form.save()
        form.save_m2m()
        self.assertEqual(repository.local_site, local_site)
        self.assertEqual(repository.hosting_account, local_site_account)
        self.assertEqual(repository.extra_data, {b'bug_tracker_use_hosting': False, 
           b'repository_plan': b'', 
           b'test_repo_name': b'test'})
        self.assertEqual(list(repository.users.all()), [local_site_user])
        self.assertEqual(list(repository.review_groups.all()), [
         local_site_group])

    def test_with_localsite_in_data_and_instance(self):
        """Testing RepositoryForm with a LocalSite in form data and editing
        instance
        """
        local_site = LocalSite.objects.create(name=b'test')
        git_tool = Tool.objects.get(name=b'Git')
        repository = self.create_repository()
        form = self._build_form({b'name': b'test', 
           b'tool': b'git', 
           b'path': b'/path/to/test.git', 
           b'local_site': local_site.pk}, instance=repository)
        self.assertEqual(form.fields[b'tool'].initial, b'git')
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data[b'tool'], git_tool)
        self.assertEqual(list(form.iter_subforms(bound_only=True)), [
         form.scmtool_repository_forms[b'git']])
        new_repository = form.save()
        self.assertEqual(repository.pk, new_repository.pk)
        self.assertEqual(new_repository.local_site, local_site)
        self.assertEqual(new_repository.tool, git_tool)
        self.assertEqual(repository.extra_data, {})

    def test_with_localsite_in_data_and_invalid_user(self):
        """Testing RepositoryForm with a LocalSite in form data and User not
        on the LocalSite
        """
        local_site = LocalSite.objects.create(name=b'test')
        user = User.objects.create_user(username=b'test-user')
        form = self._build_form({b'name': b'test', 
           b'tool': b'git', 
           b'path': b'/path/to/test.git', 
           b'local_site': local_site.pk, 
           b'users': [
                    user.pk]})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {b'users': [
                    b'Select a valid choice. 1 is not one of the available choices.']})
        self.assertEqual(list(form.iter_subforms(bound_only=True)), [
         form.scmtool_repository_forms[b'git']])

    def test_with_localsite_in_data_and_invalid_group(self):
        """Testing RepositoryForm with a LocalSite in form data and Group not
        on the LocalSite
        """
        local_site = LocalSite.objects.create(name=b'test')
        group = self.create_review_group()
        form = self._build_form({b'name': b'test', 
           b'tool': b'git', 
           b'path': b'/path/to/test.git', 
           b'local_site': local_site.pk, 
           b'review_groups': [
                            group.pk]})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {b'review_groups': [
                            b'Select a valid choice. 1 is not one of the available choices.']})
        self.assertEqual(list(form.iter_subforms(bound_only=True)), [
         form.scmtool_repository_forms[b'git']])

    def test_with_instance_and_no_hosting_service(self):
        """Testing RepositoryForm with instance= and no hosting service"""
        repository = self.create_repository(name=b'Test Repository', path=b'/path/', mirror_path=b'/mirror_path/', raw_file_url=b'/raw_file/', username=b'test-user', password=b'test-pass', encoding=b'utf-128', tool_name=b'Test')
        form = RepositoryForm(instance=repository)
        self.assertEqual(form[b'encoding'].value(), b'utf-128')
        self.assertEqual(form[b'name'].value(), b'Test Repository')
        self.assertEqual(form[b'tool'].value(), b'test')
        auth_form = form.scmtool_auth_forms[b'test']
        self.assertEqual(auth_form[b'username'].value(), b'test-user')
        self.assertEqual(auth_form[b'password'].value(), b'test-pass')
        scmtool_form = form.scmtool_repository_forms[b'test']
        self.assertEqual(scmtool_form[b'mirror_path'].value(), b'/mirror_path/')
        self.assertEqual(scmtool_form[b'path'].value(), b'/path/')
        self.assertEqual(scmtool_form[b'raw_file_url'].value(), b'/raw_file/')
        self.assertEqual(form[b'bug_tracker'].value(), b'')
        self.assertEqual(form[b'bug_tracker_type'].value(), form.NO_BUG_TRACKER_ID)
        self.assertEqual(form[b'hosting_type'].value(), form.NO_HOSTING_SERVICE_ID)
        self.assertIsNone(form[b'bug_tracker_hosting_account_username'].value())
        self.assertIsNone(form[b'bug_tracker_hosting_url'].value())
        self.assertIsNone(form[b'bug_tracker_plan'].value())
        self.assertIsNone(form[b'hosting_account'].value())
        self.assertIsNone(form[b'repository_plan'].value())
        self.assertTrue(form[b'public'].value())
        self.assertTrue(form[b'visible'].value())
        self.assertFalse(form[b'associate_ssh_key'].value())
        self.assertFalse(form[b'bug_tracker_use_hosting'].value())
        self.assertFalse(form[b'force_authorize'].value())
        self.assertFalse(form[b'reedit_repository'].value())
        self.assertFalse(form[b'trust_host'].value())
        auth_form = form.scmtool_auth_forms[b'git']
        self.assertIsNone(auth_form[b'username'].value())
        self.assertIsNone(auth_form[b'password'].value())
        scmtool_form = form.scmtool_repository_forms[b'git']
        self.assertIsNone(scmtool_form[b'mirror_path'].value())
        self.assertIsNone(scmtool_form[b'path'].value())
        self.assertIsNone(scmtool_form[b'raw_file_url'].value())

    def test_with_instance_and_hosting_service(self):
        """Testing RepositoryForm with instance= and hosting service"""
        account = HostingServiceAccount.objects.create(username=b'test-user', service_name=b'github')
        account.data[b'password'] = b'test-pass'
        account.save()
        repository = self.create_repository(name=b'Test Repository', path=b'/path/', mirror_path=b'/mirror_path/', raw_file_url=b'/raw_file/', encoding=b'utf-128', tool_name=b'Git', hosting_account=account)
        repository.extra_data.update({b'bug_tracker_hosting_url': b'http://example.com/', 
           b'bug_tracker_type': b'github', 
           b'bug_tracker-hosting_account_username': b'test-user', 
           b'bug_tracker-github_repo_name': b'test-repo', 
           b'bug_tracker_plan': b'private', 
           b'repository_plan': b'public'})
        form = RepositoryForm(instance=repository)
        self.assertEqual(form[b'bug_tracker_hosting_account_username'].value(), b'test-user')
        self.assertEqual(form[b'bug_tracker_hosting_url'].value(), b'http://example.com/')
        self.assertEqual(form[b'bug_tracker_plan'].value(), b'private')
        self.assertEqual(form[b'bug_tracker_type'].value(), b'github')
        self.assertEqual(form[b'encoding'].value(), b'utf-128')
        self.assertEqual(form[b'hosting_account'].value(), account.pk)
        self.assertEqual(form[b'hosting_type'].value(), b'github')
        self.assertEqual(form[b'name'].value(), b'Test Repository')
        self.assertEqual(form[b'repository_plan'].value(), b'public')
        self.assertEqual(form[b'tool'].value(), b'git')
        scmtool_form = form.scmtool_repository_forms[b'git']
        self.assertIsNone(scmtool_form[b'mirror_path'].value())
        self.assertIsNone(scmtool_form[b'path'].value())
        self.assertIsNone(scmtool_form[b'raw_file_url'].value())
        self.assertTrue(form[b'visible'].value())
        self.assertTrue(form[b'public'].value())
        self.assertFalse(form[b'reedit_repository'].value())
        self.assertFalse(form[b'trust_host'].value())
        self.assertFalse(form[b'force_authorize'].value())
        self.assertFalse(form[b'associate_ssh_key'].value())
        self.assertFalse(form[b'bug_tracker_use_hosting'].value())

    def test_with_instance_and_public_and_acl(self):
        """Testing RepositoryForm with instance= and access lists set"""
        repository = self.create_repository(tool_name=b'Test', public=True)
        repository.users.add(self.create_user())
        repository.review_groups.add(self.create_review_group())
        form = RepositoryForm(instance=repository)
        self.assertEqual(form[b'users'].value(), [])
        self.assertEqual(form[b'review_groups'].value(), [])

    def test_plain_repository(self):
        """Testing RepositoryForm with a plain repository"""
        form = self._build_form({b'name': b'test', 
           b'tool': b'git', 
           b'path': b'/path/to/test.git'})
        self.assertTrue(form.is_valid())
        repository = form.save()
        self.assertEqual(repository.name, b'test')
        self.assertEqual(repository.tool, Tool.objects.get(name=b'Git'))
        self.assertEqual(repository.hosting_account, None)
        self.assertEqual(repository.extra_data, {})
        self.assertEqual(list(form.iter_subforms(bound_only=True)), [
         form.scmtool_repository_forms[b'git']])
        for auth_form in six.itervalues(form.hosting_auth_forms):
            self.assertEqual(auth_form.errors, {})

        return

    def test_plain_repository_with_missing_fields(self):
        """Testing RepositoryForm with a plain repository with missing fields
        """
        form = self._build_form({b'name': b'test', 
           b'tool': b'git'})
        self.assertFalse(form.is_valid())
        self.assertIn(b'path', form.errors)
        self.assertEqual(list(form.iter_subforms(bound_only=True)), [
         form.scmtool_repository_forms[b'git']])
        for auth_form in six.itervalues(form.hosting_auth_forms):
            self.assertEqual(auth_form.errors, {})

    def test_with_hosting_service_new_account(self):
        """Testing RepositoryForm with a hosting service and new account"""
        form = self._build_form({b'name': b'test', 
           b'hosting_type': b'test', 
           b'test-hosting_account_username': b'testuser', 
           b'test-hosting_account_password': b'testpass', 
           b'tool': b'git', 
           b'test_repo_name': b'testrepo'})
        self.assertTrue(form.is_valid())
        self.assertTrue(form.hosting_account_linked)
        repository = form.save()
        self.assertEqual(repository.name, b'test')
        self.assertEqual(repository.hosting_account.username, b'testuser')
        self.assertEqual(repository.hosting_account.service_name, b'test')
        self.assertEqual(repository.hosting_account.local_site, None)
        self.assertEqual(repository.path, b'http://example.com/testrepo/')
        self.assertEqual(repository.mirror_path, b'')
        self.assertEqual(repository.extra_data, {b'bug_tracker_use_hosting': False, 
           b'repository_plan': b'', 
           b'test_repo_name': b'testrepo'})
        self.assertEqual(list(form.iter_subforms(bound_only=True)), [
         form.hosting_repository_forms[b'test'][b'default']])
        for auth_form in six.itervalues(form.hosting_auth_forms):
            self.assertEqual(auth_form.errors, {})

        return

    def test_with_hosting_service_new_account_auth_error(self):
        """Testing RepositoryForm with a hosting service and new account and
        authorization error
        """
        form = self._build_form({b'name': b'test', 
           b'hosting_type': b'test', 
           b'test-hosting_account_username': b'baduser', 
           b'test-hosting_account_password': b'testpass', 
           b'tool': b'git', 
           b'test_repo_name': b'testrepo'})
        self.assertFalse(form.is_valid())
        self.assertFalse(form.hosting_account_linked)
        self.assertIn(b'hosting_account', form.errors)
        self.assertEqual(form.errors[b'hosting_account'], [
         b'Unable to link the account: The username is very very bad.'])
        self.assertEqual(list(form.iter_subforms(bound_only=True)), [
         form.hosting_repository_forms[b'test'][b'default']])
        for auth_form in six.itervalues(form.hosting_auth_forms):
            self.assertEqual(auth_form.errors, {})

    def test_with_hosting_service_new_account_2fa_code_required(self):
        """Testing RepositoryForm with a hosting service and new account and
        two-factor auth code required
        """
        form = self._build_form({b'name': b'test', 
           b'hosting_type': b'test', 
           b'test-hosting_account_username': b'2fa-user', 
           b'test-hosting_account_password': b'testpass', 
           b'tool': b'git', 
           b'test_repo_name': b'testrepo'})
        self.assertFalse(form.is_valid())
        self.assertFalse(form.hosting_account_linked)
        self.assertIn(b'hosting_account', form.errors)
        self.assertEqual(form.errors[b'hosting_account'], [
         b'Enter your 2FA code.'])
        self.assertTrue(form.hosting_service_info[b'test'][b'needs_two_factor_auth_code'])
        self.assertEqual(list(form.iter_subforms(bound_only=True)), [
         form.hosting_repository_forms[b'test'][b'default']])
        for auth_form in six.itervalues(form.hosting_auth_forms):
            self.assertEqual(auth_form.errors, {})

    def test_with_hosting_service_new_account_2fa_code_provided(self):
        """Testing RepositoryForm with a hosting service and new account and
        two-factor auth code provided
        """
        form = self._build_form({b'name': b'test', 
           b'hosting_type': b'test', 
           b'test-hosting_account_username': b'2fa-user', 
           b'test-hosting_account_password': b'testpass', 
           b'test-hosting_account_two_factor_auth_code': b'123456', 
           b'tool': b'git', 
           b'test_repo_name': b'testrepo'})
        self.assertTrue(form.is_valid())
        self.assertTrue(form.hosting_account_linked)
        self.assertFalse(form.hosting_service_info[b'test'][b'needs_two_factor_auth_code'])
        self.assertEqual(list(form.iter_subforms(bound_only=True)), [
         form.hosting_repository_forms[b'test'][b'default']])
        for auth_form in six.itervalues(form.hosting_auth_forms):
            self.assertEqual(auth_form.errors, {})

    def test_with_hosting_service_new_account_missing_fields(self):
        """Testing RepositoryForm with a hosting service and new account and
        missing fields
        """
        form = self._build_form({b'name': b'test', 
           b'hosting_type': b'test', 
           b'tool': b'git', 
           b'test_repo_name': b'testrepo'})
        self.assertFalse(form.is_valid())
        self.assertFalse(form.hosting_account_linked)
        self.assertEqual(list(form.iter_subforms(bound_only=True)), [
         form.hosting_repository_forms[b'test'][b'default']])
        self.assertIn(b'hosting_account_username', form.errors)
        self.assertIn(b'hosting_account_password', form.errors)
        auth_form = form.hosting_auth_forms.pop(b'test')
        self.assertIn(b'hosting_account_username', auth_form.errors)
        self.assertIn(b'hosting_account_password', auth_form.errors)
        for auth_form in six.itervalues(form.hosting_auth_forms):
            self.assertEqual(auth_form.errors, {})

    def test_with_hosting_service_self_hosted_and_new_account(self):
        """Testing RepositoryForm with a self-hosted hosting service and new
        account
        """
        form = self._build_form({b'name': b'test', 
           b'hosting_type': b'self_hosted_test', 
           b'self_hosted_test-hosting_url': b'https://example.com', 
           b'self_hosted_test-hosting_account_username': b'testuser', 
           b'self_hosted_test-hosting_account_password': b'testpass', 
           b'test_repo_name': b'myrepo', 
           b'tool': b'git'})
        self.assertTrue(form.is_valid())
        self.assertTrue(form.hosting_account_linked)
        self.assertEqual(list(form.iter_subforms(bound_only=True)), [
         form.hosting_repository_forms[b'self_hosted_test'][b'default']])
        repository = form.save()
        self.assertEqual(repository.name, b'test')
        self.assertEqual(repository.hosting_account.hosting_url, b'https://example.com')
        self.assertEqual(repository.hosting_account.username, b'testuser')
        self.assertEqual(repository.hosting_account.service_name, b'self_hosted_test')
        self.assertEqual(repository.hosting_account.local_site, None)
        self.assertEqual(repository.path, b'https://example.com/myrepo/')
        self.assertEqual(repository.mirror_path, b'git@example.com:myrepo/')
        self.assertEqual(repository.extra_data, {b'bug_tracker_use_hosting': False, 
           b'hosting_url': b'https://example.com', 
           b'repository_plan': b'', 
           b'test_repo_name': b'myrepo'})
        for auth_form in six.itervalues(form.hosting_auth_forms):
            self.assertEqual(auth_form.errors, {})

        return

    def test_with_hosting_service_self_hosted_and_blank_url(self):
        """Testing RepositoryForm with a self-hosted hosting service and blank
        URL
        """
        form = self._build_form({b'name': b'test', 
           b'hosting_type': b'self_hosted_test', 
           b'self_hosted_test-hosting_url': b'', 
           b'self_hosted_test-hosting_account_username': b'testuser', 
           b'self_hosted_test-hosting_account_password': b'testpass', 
           b'test_repo_name': b'myrepo', 
           b'tool': b'git'})
        self.assertFalse(form.is_valid())
        self.assertFalse(form.hosting_account_linked)
        self.assertEqual(list(form.iter_subforms(bound_only=True)), [
         form.hosting_repository_forms[b'self_hosted_test'][b'default']])

    def test_with_hosting_service_new_account_localsite(self):
        """Testing RepositoryForm with a hosting service, new account and
        LocalSite
        """
        local_site = LocalSite.objects.create(name=b'testsite')
        form = self._build_form({b'name': b'test', 
           b'hosting_type': b'test', 
           b'test-hosting_account_username': b'testuser', 
           b'test-hosting_account_password': b'testpass', 
           b'tool': b'git', 
           b'test_repo_name': b'testrepo', 
           b'local_site': local_site.pk}, limit_to_local_site=local_site)
        self.assertTrue(form.is_valid())
        self.assertTrue(form.hosting_account_linked)
        self.assertEqual(list(form.iter_subforms(bound_only=True)), [
         form.hosting_repository_forms[b'test'][b'default']])
        repository = form.save()
        self.assertEqual(repository.name, b'test')
        self.assertEqual(repository.local_site, local_site)
        self.assertEqual(repository.hosting_account.username, b'testuser')
        self.assertEqual(repository.hosting_account.service_name, b'test')
        self.assertEqual(repository.hosting_account.local_site, local_site)
        self.assertEqual(repository.extra_data, {b'bug_tracker_use_hosting': False, 
           b'repository_plan': b'', 
           b'test_repo_name': b'testrepo'})

    def test_with_hosting_service_existing_account(self):
        """Testing RepositoryForm with a hosting service and existing
        account
        """
        account = HostingServiceAccount.objects.create(username=b'testuser', service_name=b'test')
        account.data[b'password'] = b'testpass'
        account.save()
        form = self._build_form({b'name': b'test', 
           b'hosting_type': b'test', 
           b'hosting_account': account.pk, 
           b'tool': b'git', 
           b'test_repo_name': b'testrepo'})
        self.assertTrue(form.is_valid())
        self.assertFalse(form.hosting_account_linked)
        self.assertEqual(list(form.iter_subforms(bound_only=True)), [
         form.hosting_repository_forms[b'test'][b'default']])
        repository = form.save()
        self.assertEqual(repository.name, b'test')
        self.assertEqual(repository.hosting_account, account)
        self.assertEqual(repository.extra_data, {b'bug_tracker_use_hosting': False, 
           b'repository_plan': b'', 
           b'test_repo_name': b'testrepo'})

    def test_with_hosting_service_existing_account_needs_reauth(self):
        """Testing RepositoryForm with a hosting service and existing
        account needing re-authorization
        """
        account = HostingServiceAccount.objects.create(username=b'testuser', service_name=b'test')
        form = self._build_form({b'name': b'test', 
           b'hosting_type': b'test', 
           b'hosting_account': account.pk, 
           b'tool': b'git', 
           b'test_repo_name': b'testrepo'})
        self.assertFalse(form.is_valid())
        self.assertFalse(form.hosting_account_linked)
        self.assertEqual(set(form.errors.keys()), set([b'hosting_account_username',
         b'hosting_account_password']))
        self.assertEqual(list(form.iter_subforms(bound_only=True)), [
         form.hosting_repository_forms[b'test'][b'default']])

    def test_with_hosting_service_existing_account_reauthing(self):
        """Testing RepositoryForm with a hosting service and existing
        account with re-authorizating
        """
        account = HostingServiceAccount.objects.create(username=b'testuser', service_name=b'test')
        form = self._build_form({b'name': b'test', 
           b'hosting_type': b'test', 
           b'hosting_account': account.pk, 
           b'test-hosting_account_username': b'testuser2', 
           b'test-hosting_account_password': b'testpass2', 
           b'tool': b'git', 
           b'test_repo_name': b'testrepo'})
        self.assertTrue(form.is_valid())
        self.assertTrue(form.hosting_account_linked)
        self.assertEqual(list(form.iter_subforms(bound_only=True)), [
         form.hosting_repository_forms[b'test'][b'default']])
        account = HostingServiceAccount.objects.get(pk=account.pk)
        self.assertEqual(account.username, b'testuser2')
        self.assertEqual(account.data[b'password'], b'testpass2')

    def test_with_hosting_service_self_hosted_and_existing_account(self):
        """Testing RepositoryForm with a self-hosted hosting service and
        existing account
        """
        account = HostingServiceAccount.objects.create(username=b'testuser', service_name=b'self_hosted_test', hosting_url=b'https://example.com')
        account.data[b'password'] = b'testpass'
        account.save()
        form = self._build_form({b'name': b'test', 
           b'hosting_type': b'self_hosted_test', 
           b'self_hosted_test-hosting_url': b'https://example.com', 
           b'hosting_account': account.pk, 
           b'tool': b'git', 
           b'test_repo_name': b'myrepo'})
        self.assertTrue(form.is_valid())
        self.assertFalse(form.hosting_account_linked)
        self.assertEqual(list(form.iter_subforms(bound_only=True)), [
         form.hosting_repository_forms[b'self_hosted_test'][b'default']])
        repository = form.save()
        self.assertEqual(repository.name, b'test')
        self.assertEqual(repository.hosting_account, account)
        self.assertEqual(repository.extra_data, {b'bug_tracker_use_hosting': False, 
           b'hosting_url': b'https://example.com', 
           b'repository_plan': b'', 
           b'test_repo_name': b'myrepo'})

    def test_with_self_hosted_and_invalid_account_service(self):
        """Testing RepositoryForm with a self-hosted hosting service and
        invalid existing account due to mismatched service type
        """
        account = HostingServiceAccount.objects.create(username=b'testuser', service_name=b'self_hosted_test', hosting_url=b'https://example1.com')
        account.data[b'password'] = b'testpass'
        account.save()
        form = self._build_form({b'name': b'test', 
           b'hosting_type': b'test', 
           b'hosting_account': account.pk, 
           b'tool': b'git', 
           b'test_repo_name': b'myrepo'})
        self.assertEqual(list(form.iter_subforms(bound_only=True)), [
         form.hosting_repository_forms[b'test'][b'default']])
        self.assertFalse(form.is_valid())
        self.assertFalse(form.hosting_account_linked)

    def test_with_self_hosted_and_invalid_account_local_site(self):
        """Testing RepositoryForm with a self-hosted hosting service and
        invalid existing account due to mismatched Local Site
        """
        account = HostingServiceAccount.objects.create(username=b'testuser', service_name=b'self_hosted_test', hosting_url=b'https://example1.com', local_site=LocalSite.objects.create(name=b'test-site'))
        account.data[b'password'] = b'testpass'
        account.save()
        form = self._build_form({b'name': b'test', 
           b'hosting_type': b'test', 
           b'hosting_account': account.pk, 
           b'tool': b'git', 
           b'test_repo_name': b'myrepo'})
        self.assertFalse(form.is_valid())
        self.assertFalse(form.hosting_account_linked)
        self.assertEqual(list(form.iter_subforms(bound_only=True)), [
         form.hosting_repository_forms[b'test'][b'default']])

    def test_with_hosting_service_custom_bug_tracker(self):
        """Testing RepositoryForm with a custom bug tracker"""
        account = HostingServiceAccount.objects.create(username=b'testuser', service_name=b'test')
        account.data[b'password'] = b'testpass'
        account.save()
        form = self._build_form({b'name': b'test', 
           b'hosting_type': b'test', 
           b'hosting_account': account.pk, 
           b'tool': b'git', 
           b'test_repo_name': b'testrepo', 
           b'bug_tracker_type': b'custom', 
           b'bug_tracker': b'http://example.com/issue/%s'})
        self.assertTrue(form.is_valid())
        repository = form.save()
        self.assertEqual(repository.bug_tracker, b'http://example.com/issue/%s')
        self.assertEqual(repository.extra_data, {b'bug_tracker_use_hosting': False, 
           b'repository_plan': b'', 
           b'test_repo_name': b'testrepo'})
        self.assertEqual(list(form.iter_subforms(bound_only=True)), [
         form.hosting_repository_forms[b'test'][b'default']])

    def test_with_hosting_service_bug_tracker_service(self):
        """Testing RepositoryForm with a bug tracker service"""
        account = HostingServiceAccount.objects.create(username=b'testuser', service_name=b'test')
        account.data[b'password'] = b'testpass'
        account.save()
        form = self._build_form({b'name': b'test', 
           b'hosting_type': b'test', 
           b'hosting_account': account.pk, 
           b'tool': b'git', 
           b'test_repo_name': b'testrepo', 
           b'bug_tracker_type': b'test', 
           b'bug_tracker_hosting_account_username': b'testuser', 
           b'bug_tracker-test_repo_name': b'testrepo'})
        self.assertTrue(form.is_valid())
        repository = form.save()
        self.assertEqual(repository.bug_tracker, b'http://example.com/testuser/testrepo/issue/%s')
        self.assertEqual(repository.extra_data, {b'bug_tracker_plan': b'default', 
           b'bug_tracker_type': b'test', 
           b'bug_tracker_use_hosting': False, 
           b'bug_tracker-test_repo_name': b'testrepo', 
           b'bug_tracker-hosting_account_username': b'testuser', 
           b'repository_plan': b'', 
           b'test_repo_name': b'testrepo'})
        self.assertEqual(list(form.iter_subforms(bound_only=True)), [
         form.hosting_repository_forms[b'test'][b'default'],
         form.hosting_bug_tracker_forms[b'test'][b'default']])

    def test_with_hosting_service_self_hosted_bug_tracker_service(self):
        """Testing RepositoryForm with a self-hosted bug tracker service"""
        account = HostingServiceAccount.objects.create(username=b'testuser', service_name=b'self_hosted_test', hosting_url=b'https://example.com')
        account.data[b'password'] = b'testpass'
        account.save()
        form = self._build_form({b'name': b'test', 
           b'hosting_type': b'self_hosted_test', 
           b'hosting_url': b'https://example.com', 
           b'hosting_account': account.pk, 
           b'tool': b'git', 
           b'test_repo_name': b'testrepo', 
           b'bug_tracker_type': b'self_hosted_test', 
           b'bug_tracker_hosting_url': b'https://example.com', 
           b'bug_tracker-test_repo_name': b'testrepo'})
        self.assertTrue(form.is_valid())
        repository = form.save()
        self.assertEqual(repository.bug_tracker, b'https://example.com/testrepo/issue/%s')
        self.assertEqual(repository.extra_data, {b'bug_tracker_hosting_url': b'https://example.com', 
           b'bug_tracker_plan': b'default', 
           b'bug_tracker_type': b'self_hosted_test', 
           b'bug_tracker_use_hosting': False, 
           b'bug_tracker-test_repo_name': b'testrepo', 
           b'hosting_url': b'https://example.com', 
           b'repository_plan': b'', 
           b'test_repo_name': b'testrepo'})
        self.assertEqual(list(form.iter_subforms(bound_only=True)), [
         form.hosting_repository_forms[b'self_hosted_test'][b'default'],
         form.hosting_bug_tracker_forms[b'self_hosted_test'][b'default']])

    def test_with_hosting_service_with_hosting_bug_tracker(self):
        """Testing RepositoryForm with hosting service's bug tracker"""
        account = HostingServiceAccount.objects.create(username=b'testuser', service_name=b'github')
        account.data[b'authorization'] = {b'token': b'abc123'}
        account.save()
        form = self._build_form({b'name': b'test', 
           b'hosting_type': b'github', 
           b'hosting_account': account.pk, 
           b'repository_plan': b'public', 
           b'tool': b'git', 
           b'github_public_repo_name': b'testrepo', 
           b'bug_tracker_use_hosting': True, 
           b'bug_tracker_type': b'github', 
           b'bug_tracker_plan': b'public'})
        self.assertTrue(form.is_valid())
        self.assertEqual(list(form.iter_subforms(bound_only=True)), [
         form.hosting_repository_forms[b'github'][b'public']])
        repository = form.save()
        self.assertEqual(repository.bug_tracker, b'http://github.com/testuser/testrepo/issues#issue/%s')
        self.assertEqual(repository.extra_data, {b'bug_tracker_use_hosting': True, 
           b'github_public_repo_name': b'testrepo', 
           b'repository_plan': b'public'})

    def test_with_hosting_service_with_hosting_bug_tracker_and_self_hosted(self):
        """Testing RepositoryForm with self-hosted hosting service's bug
        tracker
        """
        account = HostingServiceAccount.objects.create(username=b'testuser', service_name=b'self_hosted_test', hosting_url=b'https://example.com')
        account.data[b'password'] = b'testpass'
        account.save()
        account.data[b'authorization'] = {b'token': b'1234'}
        account.save()
        form = self._build_form({b'name': b'test', 
           b'hosting_type': b'self_hosted_test', 
           b'hosting_url': b'https://example.com', 
           b'hosting_account': account.pk, 
           b'tool': b'git', 
           b'test_repo_name': b'testrepo', 
           b'bug_tracker_use_hosting': True, 
           b'bug_tracker_type': b'github'})
        self.assertTrue(form.is_valid())
        self.assertEqual(list(form.iter_subforms(bound_only=True)), [
         form.hosting_repository_forms[b'self_hosted_test'][b'default']])
        repository = form.save()
        self.assertEqual(repository.bug_tracker, b'https://example.com/testrepo/issue/%s')
        self.assertEqual(repository.extra_data, {b'bug_tracker_use_hosting': True, 
           b'hosting_url': b'https://example.com', 
           b'repository_plan': b'', 
           b'test_repo_name': b'testrepo'})

    def test_with_hosting_service_no_bug_tracker(self):
        """Testing RepositoryForm with no bug tracker"""
        account = HostingServiceAccount.objects.create(username=b'testuser', service_name=b'test')
        account.data[b'password'] = b'testpass'
        account.save()
        form = self._build_form({b'name': b'test', 
           b'hosting_type': b'test', 
           b'hosting_account': account.pk, 
           b'tool': b'git', 
           b'test_repo_name': b'testrepo'})
        self.assertTrue(form.is_valid())
        self.assertEqual(list(form.iter_subforms(bound_only=True)), [
         form.hosting_repository_forms[b'test'][b'default']])
        repository = form.save()
        self.assertEqual(repository.bug_tracker, b'')
        self.assertEqual(repository.extra_data, {b'bug_tracker_use_hosting': False, 
           b'repository_plan': b'', 
           b'test_repo_name': b'testrepo'})

    def test_with_hosting_service_with_existing_custom_bug_tracker(self):
        """Testing RepositoryForm with existing custom bug tracker"""
        repository = Repository(name=b'test', bug_tracker=b'http://example.com/issue/%s')
        form = RepositoryForm(instance=repository)
        self.assertFalse(form._get_field_data(b'bug_tracker_use_hosting'))
        self.assertEqual(form._get_field_data(b'bug_tracker_type'), b'custom')
        self.assertEqual(form.initial[b'bug_tracker'], b'http://example.com/issue/%s')
        self.assertEqual(list(form.iter_subforms(bound_only=True)), [])

    def test_with_hosting_service_with_existing_bug_tracker_service(self):
        """Testing RepositoryForm with existing bug tracker service"""
        repository = Repository(name=b'test', extra_data={b'bug_tracker_type': b'test', 
           b'bug_tracker-hosting_account_username': b'testuser', 
           b'bug_tracker-test_repo_name': b'testrepo'})
        form = RepositoryForm(instance=repository)
        self.assertFalse(form._get_field_data(b'bug_tracker_use_hosting'))
        self.assertEqual(form._get_field_data(b'bug_tracker_type'), b'test')
        self.assertEqual(form._get_field_data(b'bug_tracker_hosting_account_username'), b'testuser')
        self.assertIn(b'test', form.hosting_bug_tracker_forms)
        self.assertIn(b'default', form.hosting_bug_tracker_forms[b'test'])
        bitbucket_form = form.hosting_bug_tracker_forms[b'test'][b'default']
        self.assertEqual(bitbucket_form.fields[b'test_repo_name'].initial, b'testrepo')

    def test_with_hosting_service_with_existing_bug_tracker_using_hosting(self):
        """Testing RepositoryForm with existing bug tracker using hosting
        service
        """
        account = HostingServiceAccount.objects.create(username=b'testuser', service_name=b'test')
        repository = Repository(name=b'test', hosting_account=account, extra_data={b'bug_tracker_use_hosting': True, 
           b'test_repo_name': b'testrepo'})
        form = RepositoryForm(instance=repository)
        self.assertTrue(form._get_field_data(b'bug_tracker_use_hosting'))

    def test_bound_forms_with_post_with_repository_service(self):
        """Testing RepositoryForm binds hosting service forms only if matching
        posted repository hosting_service using default plan
        """
        form = self._build_form({b'name': b'test', 
           b'hosting_type': b'test'})
        self.assertEqual(list(form.iter_subforms(bound_only=True, with_auth_forms=True)), [
         form.hosting_repository_forms[b'test'][b'default']])

    def test_bound_forms_with_post_with_bug_tracker_service(self):
        """Testing RepositoryForm binds hosting service forms only if matching
        posted bug tracker hosting_service using default plan
        """
        form = self._build_form({b'name': b'test', 
           b'bug_tracker_type': b'test'})
        self.assertEqual(list(form.iter_subforms(bound_only=True, with_auth_forms=True)), [
         form.hosting_bug_tracker_forms[b'test'][b'default']])

    def test_bound_forms_with_post_with_repo_service_and_plan(self):
        """Testing RepositoryForm binds hosting service forms only if matching
        posted repository hosting_service with specific plans
        """
        form = self._build_form({b'name': b'test', 
           b'hosting_type': b'github', 
           b'repository_plan': b'public'})
        self.assertEqual(list(form.iter_subforms(bound_only=True, with_auth_forms=True)), [
         form.hosting_repository_forms[b'github'][b'public']])

    def test_bound_forms_with_post_with_bug_tracker_service_and_plan(self):
        """Testing RepositoryForm binds hosting service forms only if matching
        posted bug tracker hosting_service with specific plans
        """
        form = self._build_form({b'name': b'test', 
           b'bug_tracker_type': b'github', 
           b'bug_tracker_plan': b'public'})
        self.assertEqual(list(form.iter_subforms(bound_only=True, with_auth_forms=True)), [
         form.hosting_bug_tracker_forms[b'github'][b'public']])

    def test_with_set_access_list(self):
        """Testing RepositoryForm with setting users access list"""
        user1 = User.objects.create(username=b'user1')
        user2 = User.objects.create(username=b'user2')
        User.objects.create(username=b'user3')
        group1 = self.create_review_group(name=b'group1', invite_only=True)
        group2 = self.create_review_group(name=b'group2', invite_only=True)
        self.create_review_group(name=b'group3', invite_only=True)
        form = self._build_form({b'name': b'test', 
           b'tool': b'git', 
           b'path': b'/path/to/test.git', 
           b'public': False, 
           b'users': [
                    user1.pk, user2.pk], 
           b'review_groups': [
                            group1.pk, group2.pk]})
        form.is_valid()
        self.assertTrue(form.is_valid())
        repository = form.save()
        self.assertFalse(repository.public)
        self.assertEqual(repository.extra_data, {})
        self.assertEqual(list(repository.users.all()), [user1, user2])
        self.assertEqual(list(repository.review_groups.all()), [
         group1, group2])
        self.assertEqual(list(form.iter_subforms(bound_only=True)), [
         form.scmtool_repository_forms[b'git']])

    def test_with_set_public_and_prev_access_list(self):
        """Testing RepositoryForm with setting public=True when an access list
        is set
        """
        user = self.create_user()
        review_group = self.create_review_group(invite_only=True)
        repository = self.create_repository(tool_name=b'Test', public=False)
        repository.users.add(user)
        repository.review_groups.add(review_group)
        form = self._build_form({b'name': b'test', 
           b'tool': b'git', 
           b'path': b'/path/to/test.git', 
           b'public': True, 
           b'users': [
                    user.pk], 
           b'review_groups': [
                            review_group.pk]}, instance=repository)
        self.assertEqual(form[b'users'].value(), [user.pk])
        self.assertEqual(form[b'review_groups'].value(), [review_group.pk])
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data[b'users'], [])
        self.assertEqual(form.cleaned_data[b'review_groups'], [])
        repository = form.save()
        self.assertEqual(repository.users.count(), 0)
        self.assertEqual(repository.review_groups.count(), 0)

    def test_public_checkbox_with_login_required(self):
        """Testing RepositoryForm public checkbox with site-wide login required
        """
        with self.siteconfig_settings({b'auth_require_sitewide_login': True}):
            form = RepositoryForm()
            field = form.fields[b'public']
            self.assertEqual(field.label, b'Accessible to all logged-in users')
            self.assertEqual(field.help_text, b'Review requests and files on this repository will be visible to any logged-in users. Uncheck this box to grant access only to specific users and/or to users who are members of specific invite-only review groups.')

    def test_public_checkbox_with_login_not_required(self):
        """Testing RepositoryForm public checkbox with site-wide login not
        required
        """
        with self.siteconfig_settings({b'auth_require_sitewide_login': False}):
            form = RepositoryForm()
            field = form.fields[b'public']
            self.assertEqual(field.label, b'Accessible to everyone')
            self.assertEqual(field.help_text, b'Review requests and files on this repository will be visible to any anonymous or logged-in users. Uncheck this box to grant access only to specific users and/or to users who are members of specific invite-only review groups.')

    def test_public_checkbox_with_limit_local_site_not_public(self):
        """Testing RepositoryForm public checkbox with form limited to
        LocalSite and site not public
        """
        with self.siteconfig_settings({b'auth_require_sitewide_login': True}):
            local_site = LocalSite.objects.create(name=b'test-site')
            form = RepositoryForm(limit_to_local_site=local_site)
            field = form.fields[b'public']
            self.assertEqual(field.label, b'Accessible to all users on test-site')
            self.assertEqual(field.help_text, b'Review requests and files on this repository will be visible to anyone on test-site. Uncheck this box to grant access only to specific users and/or to users who are members of specific invite-only review groups.')

    def test_public_checkbox_with_limit_local_site_public(self):
        """Testing RepositoryForm public checkbox with form limited to
        LocalSite and site is public
        """
        with self.siteconfig_settings({b'auth_require_sitewide_login': True}):
            local_site = LocalSite.objects.create(name=b'test-site', public=True)
            form = RepositoryForm(limit_to_local_site=local_site)
            field = form.fields[b'public']
            self.assertEqual(field.label, b'Accessible to all logged-in users')
            self.assertEqual(field.help_text, b'Review requests and files on this repository will be visible to any logged-in users. Uncheck this box to grant access only to specific users and/or to users who are members of specific invite-only review groups.')

    def test_public_checkbox_with_instance_local_site_not_public(self):
        """Testing RepositoryForm public checkbox with LocalSite-owned
        repository and site not public
        """
        with self.siteconfig_settings({b'auth_require_sitewide_login': True}):
            local_site = LocalSite.objects.create(name=b'test-site')
            repository = self.create_repository(tool_name=b'Test', local_site=local_site)
            form = RepositoryForm(instance=repository)
            field = form.fields[b'public']
            self.assertEqual(field.label, b'Accessible to all users on test-site')
            self.assertEqual(field.help_text, b'Review requests and files on this repository will be visible to anyone on test-site. Uncheck this box to grant access only to specific users and/or to users who are members of specific invite-only review groups.')

    def test_public_checkbox_with_instance_local_site_public(self):
        """Testing RepositoryForm public checkbox with LocalSite-owned
        repository and site is public
        """
        with self.siteconfig_settings({b'auth_require_sitewide_login': True}):
            local_site = LocalSite.objects.create(name=b'test-site', public=True)
            repository = self.create_repository(tool_name=b'Test', local_site=local_site)
            form = RepositoryForm(instance=repository)
            field = form.fields[b'public']
            self.assertEqual(field.label, b'Accessible to all logged-in users')
            self.assertEqual(field.help_text, b'Review requests and files on this repository will be visible to any logged-in users. Uncheck this box to grant access only to specific users and/or to users who are members of specific invite-only review groups.')

    def test_extra_data_with_new_repo(self):
        """Testing RepositoryForm preserves extra_data by default on new
        repositories
        """
        account = HostingServiceAccount.objects.create(username=b'testuser', service_name=b'github')
        account.data[b'authorization'] = {b'token': b'abc123'}
        account.save()
        form = self._build_form({b'name': b'test', 
           b'hosting_type': b'github', 
           b'hosting_account': account.pk, 
           b'repository_plan': b'public', 
           b'tool': b'git', 
           b'github_public_repo_name': b'testrepo', 
           b'bug_tracker_use_hosting': True, 
           b'bug_tracker_type': b'github', 
           b'bug_tracker_plan': b'public', 
           b'extra_data': {b'test-key': b'test-value', 
                           b'another-key': 123}})
        self.assertTrue(form.is_valid())
        repository = form.save()
        self.assertEqual(repository.name, b'test')
        self.assertEqual(repository.tool, Tool.objects.get(name=b'Git'))
        self.assertEqual(repository.hosting_account, account)
        self.assertEqual(repository.extra_data, {b'another-key': 123, 
           b'bug_tracker_use_hosting': True, 
           b'github_public_repo_name': b'testrepo', 
           b'repository_plan': b'public', 
           b'test-key': b'test-value'})
        self.assertEqual(list(form.iter_subforms(bound_only=True)), [
         form.hosting_repository_forms[b'github'][b'public']])

    def test_extra_data_with_existing_repo(self):
        """Testing RepositoryForm preserves extra_data by default on existing
        repositories
        """
        account = HostingServiceAccount.objects.create(username=b'testuser', service_name=b'github')
        account.data[b'authorization'] = {b'token': b'abc123'}
        account.save()
        repository = self.create_repository(name=b'Test Repository', path=b'/path/', mirror_path=b'/mirror_path/', raw_file_url=b'/raw_file/', encoding=b'utf-128', tool_name=b'Git', hosting_account=account)
        repository.extra_data.update({b'github_public_repo_name': b'testrepo', 
           b'bug_tracker_hosting_url': b'http://example.com/', 
           b'bug_tracker_type': b'github', 
           b'bug_tracker-hosting_account_username': b'test-user', 
           b'bug_tracker-github_repo_name': b'test-repo', 
           b'bug_tracker_plan': b'private', 
           b'repository_plan': b'public', 
           b'test-key': b'test-value', 
           b'another-key': 123})
        form = self._build_form({b'name': b'test', 
           b'hosting_type': b'github', 
           b'hosting_account': account.pk, 
           b'repository_plan': b'private', 
           b'tool': b'git', 
           b'github_private_repo_name': b'testrepo', 
           b'bug_tracker_use_hosting': True, 
           b'bug_tracker_type': b'github', 
           b'bug_tracker_plan': b'private', 
           b'extra_data': repository.extra_data}, instance=repository)
        self.assertTrue(form.is_valid())
        repository = form.save()
        self.assertEqual(repository.name, b'test')
        self.assertEqual(repository.tool, Tool.objects.get(name=b'Git'))
        self.assertEqual(repository.hosting_account, account)
        self.assertEqual(repository.extra_data, {b'another-key': 123, 
           b'bug_tracker_use_hosting': True, 
           b'github_private_repo_name': b'testrepo', 
           b'repository_plan': b'private', 
           b'test-key': b'test-value'})
        self.assertEqual(list(form.iter_subforms(bound_only=True)), [
         form.hosting_repository_forms[b'github'][b'private']])

    def test_extra_data_with_invalid_type(self):
        """Testing RepositoryForm validates extra_data as dictionary"""
        form = self._build_form({b'name': b'test', 
           b'tool': b'git', 
           b'path': b'/path/to/repo.git', 
           b'extra_data': [
                         1, 2, 3]})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors[b'extra_data'], [
         b'This must be a JSON object/dictionary.'])

    def _build_form(self, data=None, check_repository=False, **kwargs):
        """Build the repository form with some standard data.

        This will pre-fill any supplied data will defaults based on the form's
        initial data, and also supports disabling repository checks.

        Args:
            data (dict, optional):
                Posted data to provide to the form. If supplied, it will also
                consist of defaults from the form.

            check_repository (bool, optional):
                Whether to check the validity of repositories.

            **kwargs (dict, optional):
                Additional keyword arguments to pass to the form.

        Returns:
            reviewboard.scmtools.forms.RepositoryForm:
            The form instance.
        """
        if data is not None:
            data = dict({name:field.initial for name, field in six.iteritems(RepositoryForm.base_fields)}, **data)
        form = RepositoryForm(data, **kwargs)
        if data is not None and not check_repository:
            hosting_type = data[b'hosting_type']
            tool_id = data[b'tool']
            if hosting_type != b'custom':
                hosting_service = get_hosting_service(hosting_type)
                self.spy_on(hosting_service.check_repository, call_original=False)
            elif tool_id:
                tool_cls = form.tool_models_by_id[tool_id].get_scmtool_class()
                self.spy_on(tool_cls.check_repository, call_original=False)
        return form

    def test_skips_hosting_service_with_visible_services(self):
        """Testing RepositoryForm shows only visible HostingServices"""
        form = RepositoryForm()
        hosting_types = {key for key, value in form.fields[b'hosting_type'].choices}
        self.assertIn(b'test', hosting_types)
        self.assertNotIn(b'hidden-test', hosting_types)
        self.assertIn(b'test', form.hosting_service_info)
        self.assertNotIn(b'hidden-test', form.hosting_service_info)

    def test_skips_hosting_service_with_visible_services_and_instance(self):
        """Testing RepositoryForm shows hidden HostingService if set by
        instance
        """
        hosting_account = HostingServiceAccount.objects.create(username=b'test-user', service_name=b'hidden-test')
        repository = self.create_repository(hosting_account=hosting_account, tool_name=b'Git')
        form = RepositoryForm(instance=repository)
        hosting_types = {key for key, value in form.fields[b'hosting_type'].choices}
        self.assertIn(b'test', hosting_types)
        self.assertIn(b'hidden-test', hosting_types)
        self.assertIn(b'test', form.hosting_service_info)
        self.assertIn(b'hidden-test', form.hosting_service_info)

    def test_hosting_service_info_with_visible_scms(self):
        """Testing RepositoryForm.hosting_service_info contains visible
        SCMTools
        """
        form = RepositoryForm()
        self.assertEqual(form.hosting_service_info[b'test'][b'scmtools'], [
         b'git', b'test'])

    def test_hosting_service_info_with_visible_scms_and_instance(self):
        """Testing RepositoryForm.hosting_service_info contains both
        visible SCMTools and instance's service
        """
        hosting_account = HostingServiceAccount.objects.create(username=b'test-user', service_name=b'test')
        repository = self.create_repository(hosting_account=hosting_account, tool_name=b'Perforce')
        form = RepositoryForm(instance=repository)
        self.assertEqual(form.hosting_service_info[b'test'][b'scmtools'], [
         b'git', b'perforce', b'test'])