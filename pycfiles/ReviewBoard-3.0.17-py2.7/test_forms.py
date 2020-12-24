# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/reviews/tests/test_forms.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import unicode_literals
from django.contrib.auth.models import User
from reviewboard.reviews.forms import DefaultReviewerForm, GroupForm
from reviewboard.reviews.models import DefaultReviewer
from reviewboard.site.models import LocalSite
from reviewboard.testing import TestCase

class DefaultReviewerFormTests(TestCase):
    """Unit tests for DefaultReviewerForm."""
    fixtures = [
     b'test_scmtools']

    def setUp(self):
        super(DefaultReviewerFormTests, self).setUp()
        self.local_site = LocalSite.objects.create(name=b'test')
        self.local_site_repo = self.create_repository(name=b'Test 1', local_site=self.local_site)
        self.global_site_repo = self.create_repository(name=b'Test 2')
        self.local_site_user = User.objects.create_user(username=b'testuser1')
        self.local_site.users.add(self.local_site_user)
        self.global_site_user = User.objects.create_user(username=b'testuser2')
        self.local_site_group = self.create_review_group(name=b'test1', local_site=self.local_site)
        self.global_site_group = self.create_review_group(name=b'test2')

    def test_without_localsite(self):
        """Testing DefaultReviewerForm without a LocalSite"""
        form = DefaultReviewerForm()
        self.assertIsNone(form.limited_to_local_site)
        self.assertIn(b'local_site', form.fields)
        self.assertEqual(list(form.fields[b'repository'].queryset), [
         self.local_site_repo, self.global_site_repo])
        self.assertEqual(list(form.fields[b'people'].queryset), [
         self.local_site_user, self.global_site_user])
        self.assertEqual(list(form.fields[b'groups'].queryset), [
         self.local_site_group, self.global_site_group])
        form = DefaultReviewerForm(data={b'name': b'Test', 
           b'file_regex': b'.*', 
           b'repository': [
                         self.global_site_repo.pk], 
           b'people': [
                     self.global_site_user.pk], 
           b'groups': [
                     self.global_site_group.pk]})
        self.assertIsNone(form.limited_to_local_site)
        self.assertIn(b'local_site', form.fields)
        self.assertEqual(list(form.fields[b'repository'].queryset), [
         self.local_site_repo, self.global_site_repo])
        self.assertEqual(list(form.fields[b'people'].queryset), [
         self.local_site_user, self.global_site_user])
        self.assertEqual(list(form.fields[b'groups'].queryset), [
         self.local_site_group, self.global_site_group])
        self.assertIsNone(form.fields[b'people'].widget.local_site_name)
        self.assertTrue(form.is_valid())
        self.assertEqual(list(form.fields[b'repository'].queryset), [
         self.local_site_repo, self.global_site_repo])
        self.assertEqual(list(form.fields[b'people'].queryset), [
         self.local_site_user, self.global_site_user])
        self.assertEqual(list(form.fields[b'groups'].queryset), [
         self.local_site_group, self.global_site_group])
        default_reviewer = form.save()
        self.assertIsNone(default_reviewer.local_site)
        self.assertEqual(list(default_reviewer.repository.all()), [
         self.global_site_repo])
        self.assertEqual(list(default_reviewer.people.all()), [
         self.global_site_user])
        self.assertEqual(list(default_reviewer.groups.all()), [
         self.global_site_group])

    def test_without_localsite_and_instance(self):
        """Testing DefaultReviewerForm without a LocalSite and editing instance
        """
        default_reviewer = DefaultReviewer.objects.create(name=b'Test', file_regex=b'.*', local_site=self.local_site)
        form = DefaultReviewerForm(data={b'name': b'Test', 
           b'file_regex': b'.*'}, instance=default_reviewer)
        self.assertTrue(form.is_valid())
        new_default_reviewer = form.save()
        self.assertEqual(default_reviewer.pk, new_default_reviewer.pk)
        self.assertIsNone(new_default_reviewer.local_site)

    def test_without_localsite_and_with_local_site_user(self):
        """Testing DefaultReviewerForm without a LocalSite and User on a
        LocalSite
        """
        form = DefaultReviewerForm(data={b'name': b'Test', 
           b'file_regex': b'.*', 
           b'people': [
                     self.local_site_user.pk]})
        self.assertTrue(form.is_valid())

    def test_without_localsite_and_with_local_site_group(self):
        """Testing DefaultReviewerForm without a LocalSite and Group on a
        LocalSite
        """
        form = DefaultReviewerForm(data={b'name': b'Test', 
           b'file_regex': b'.*', 
           b'groups': [
                     self.local_site_group.pk]})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {b'groups': [
                     b'A group with ID 1 was not found.']})

    def test_without_localsite_and_with_local_site_repo(self):
        """Testing DefaultReviewerForm without a LocalSite and Repository on a
        LocalSite
        """
        form = DefaultReviewerForm(data={b'name': b'Test', 
           b'file_regex': b'.*', 
           b'repository': [
                         self.local_site_repo.pk]})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {b'repository': [
                         b'A repository with ID 1 was not found.']})

    def test_with_limited_localsite(self):
        """Testing DefaultReviewerForm limited to a LocalSite"""
        form = DefaultReviewerForm(limit_to_local_site=self.local_site)
        self.assertEqual(form.limited_to_local_site, self.local_site)
        self.assertNotIn(b'local_site', form.fields)
        self.assertEqual(list(form.fields[b'repository'].queryset), [
         self.local_site_repo])
        self.assertEqual(list(form.fields[b'people'].queryset), [
         self.local_site_user])
        self.assertEqual(list(form.fields[b'groups'].queryset), [
         self.local_site_group])
        self.assertEqual(form.fields[b'people'].widget.local_site_name, self.local_site.name)

    def test_with_limited_localsite_and_changing_site(self):
        """Testing DefaultReviewerForm limited to a LocalSite and changing
        LocalSite
        """
        site2 = LocalSite.objects.create(name=b'test-site-2')
        form = DefaultReviewerForm(data={b'name': b'Test', 
           b'file_regex': b'.*', 
           b'local_site': site2}, limit_to_local_site=self.local_site)
        self.assertEqual(form.limited_to_local_site, self.local_site)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data[b'local_site'], self.local_site)
        default_reviewer = form.save()
        self.assertEqual(default_reviewer.local_site, self.local_site)

    def test_with_limited_localsite_and_compatible_instance(self):
        """Testing DefaultReviewerForm limited to a LocalSite and editing
        compatible instance
        """
        default_reviewer = DefaultReviewer.objects.create(name=b'Test', file_regex=b'.*', local_site=self.local_site)
        DefaultReviewerForm(instance=default_reviewer, limit_to_local_site=self.local_site)

    def test_with_limited_localsite_and_incompatible_instance(self):
        """Testing DefaultReviewerForm limited to a LocalSite and editing
        incompatible instance
        """
        default_reviewer = DefaultReviewer.objects.create(name=b'Test', file_regex=b'.*')
        error_message = b'The provided instance is not associated with a LocalSite compatible with this form. Please contact support.'
        with self.assertRaisesMessage(ValueError, error_message):
            DefaultReviewerForm(instance=default_reviewer, limit_to_local_site=self.local_site)

    def test_with_limited_localsite_and_invalid_user(self):
        """Testing DefaultReviewerForm limited to a LocalSite with a User
        not on the LocalSite
        """
        form = DefaultReviewerForm(data={b'name': b'Test', 
           b'file_regex': b'.*', 
           b'people': [
                     self.global_site_user.pk]}, limit_to_local_site=self.local_site)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {b'people': [
                     b'A user with ID 2 was not found.']})

    def test_with_limited_localsite_and_invalid_group(self):
        """Testing DefaultReviewerForm limited to a LocalSite with a Group
        not on the LocalSite
        """
        form = DefaultReviewerForm(data={b'name': b'Test', 
           b'file_regex': b'.*', 
           b'groups': [
                     self.global_site_group.pk]}, limit_to_local_site=self.local_site)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {b'groups': [
                     b'A group with ID 2 was not found.']})

    def test_with_limited_localsite_and_invalid_repo(self):
        """Testing DefaultReviewerForm limited to a LocalSite with a
        Repository not on the LocalSite
        """
        form = DefaultReviewerForm(data={b'name': b'Test', 
           b'file_regex': b'.*', 
           b'repository': [
                         self.global_site_repo.pk]}, limit_to_local_site=self.local_site)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {b'repository': [
                         b'A repository with ID 2 was not found.']})

    def test_with_localsite_in_data(self):
        """Testing DefaultReviewerForm with a LocalSite in form data"""
        form = DefaultReviewerForm()
        self.assertIsNone(form.limited_to_local_site)
        self.assertIn(b'local_site', form.fields)
        self.assertEqual(list(form.fields[b'repository'].queryset), [
         self.local_site_repo, self.global_site_repo])
        self.assertEqual(list(form.fields[b'people'].queryset), [
         self.local_site_user, self.global_site_user])
        self.assertEqual(list(form.fields[b'groups'].queryset), [
         self.local_site_group, self.global_site_group])
        self.assertIsNone(form.fields[b'people'].widget.local_site_name)
        form = DefaultReviewerForm(data={b'name': b'Test', 
           b'file_regex': b'.*', 
           b'local_site': self.local_site.pk, 
           b'repository': [
                         self.local_site_repo.pk], 
           b'people': [
                     self.local_site_user.pk], 
           b'groups': [
                     self.local_site_group.pk]})
        self.assertIsNone(form.limited_to_local_site)
        self.assertIn(b'local_site', form.fields)
        self.assertEqual(list(form.fields[b'repository'].queryset), [
         self.local_site_repo, self.global_site_repo])
        self.assertEqual(list(form.fields[b'people'].queryset), [
         self.local_site_user, self.global_site_user])
        self.assertEqual(list(form.fields[b'groups'].queryset), [
         self.local_site_group, self.global_site_group])
        self.assertIsNone(form.fields[b'people'].widget.local_site_name)
        self.assertTrue(form.is_valid())
        self.assertEqual(list(form.fields[b'repository'].queryset), [
         self.local_site_repo, self.global_site_repo])
        self.assertEqual(list(form.fields[b'people'].queryset), [
         self.local_site_user, self.global_site_user])
        self.assertEqual(list(form.fields[b'groups'].queryset), [
         self.local_site_group, self.global_site_group])
        self.assertIsNone(form.fields[b'people'].widget.local_site_name)
        default_reviewer = form.save()
        self.assertEqual(default_reviewer.local_site, self.local_site)
        self.assertEqual(list(default_reviewer.repository.all()), [
         self.local_site_repo])
        self.assertEqual(list(default_reviewer.people.all()), [
         self.local_site_user])
        self.assertEqual(list(default_reviewer.groups.all()), [
         self.local_site_group])

    def test_with_localsite_in_data_and_instance(self):
        """Testing DefaultReviewerform with a LocalSite in form data and
        editing instance
        """
        default_reviewer = DefaultReviewer.objects.create(name=b'Test', file_regex=b'.*')
        form = DefaultReviewerForm(data={b'name': b'Test', 
           b'file_regex': b'.*', 
           b'local_site': self.local_site.pk}, instance=default_reviewer)
        self.assertTrue(form.is_valid())
        new_default_reviewer = form.save()
        self.assertEqual(default_reviewer.pk, new_default_reviewer.pk)
        self.assertEqual(new_default_reviewer.local_site, self.local_site)

    def test_with_localsite_in_data_and_invalid_user(self):
        """Testing DefaultReviewerForm with a LocalSite in form data and User
        not on the LocalSite
        """
        form = DefaultReviewerForm(data={b'name': b'Test', 
           b'file_regex': b'.*', 
           b'local_site': self.local_site.pk, 
           b'people': [
                     self.global_site_user.pk]})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {b'people': [
                     b'A user with ID 2 was not found.']})

    def test_with_localsite_in_data_and_invalid_group(self):
        """Testing DefaultReviewerForm with a LocalSite in form data and Group
        not on the LocalSite
        """
        form = DefaultReviewerForm(data={b'name': b'Test', 
           b'file_regex': b'.*', 
           b'local_site': self.local_site.pk, 
           b'groups': [
                     self.global_site_group.pk]})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {b'groups': [
                     b'A group with ID 2 was not found.']})

    def test_with_localsite_in_data_and_invalid_repo(self):
        """Testing DefaultReviewerForm with a LocalSite in form data and
        Repository not on the LocalSite
        """
        form = DefaultReviewerForm(data={b'name': b'Test', 
           b'file_regex': b'.*', 
           b'local_site': self.local_site.pk, 
           b'repository': [
                         self.global_site_repo.pk]})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {b'repository': [
                         b'A repository with ID 2 was not found.']})

    def test_form_with_positional_argument(self):
        """Testing DefaultReviewerForm when passing data as a positional
        argument
        """
        form = DefaultReviewerForm({b'name': b'test', 
           b'file_regex': b'.*'})
        self.assertTrue(form.is_valid())


class GroupFormTests(TestCase):
    """Unit tests for GroupForm."""

    def setUp(self):
        super(GroupFormTests, self).setUp()
        self.local_site = LocalSite.objects.create(name=b'test')
        self.local_site_user = User.objects.create_user(username=b'testuser1')
        self.local_site.users.add(self.local_site_user)
        self.global_site_user = User.objects.create_user(username=b'testuser2')

    def test_without_localsite(self):
        """Testing GroupForm without a LocalSite"""
        form = GroupForm()
        self.assertIsNone(form.limited_to_local_site)
        self.assertIn(b'local_site', form.fields)
        self.assertEqual(list(form.fields[b'users'].queryset), [
         self.local_site_user, self.global_site_user])
        self.assertIsNone(form.fields[b'users'].widget.local_site_name)
        form = GroupForm(data={b'name': b'test', 
           b'display_name': b'Test', 
           b'users': [
                    self.global_site_user.pk]})
        self.assertIsNone(form.limited_to_local_site)
        self.assertIn(b'local_site', form.fields)
        self.assertEqual(list(form.fields[b'users'].queryset), [
         self.local_site_user, self.global_site_user])
        self.assertIsNone(form.fields[b'users'].widget.local_site_name)
        self.assertTrue(form.is_valid())
        self.assertEqual(list(form.fields[b'users'].queryset), [
         self.local_site_user, self.global_site_user])
        group = form.save()
        self.assertIsNone(group.local_site)
        self.assertEqual(list(group.users.all()), [self.global_site_user])

    def test_without_localsite_and_instance(self):
        """Testing GroupForm without a LocalSite and editing instance"""
        group = self.create_review_group(local_site=self.local_site)
        form = GroupForm(data={b'name': b'test', 
           b'display_name': b'Test'}, instance=group)
        self.assertTrue(form.is_valid())
        new_group = form.save()
        self.assertEqual(group.pk, new_group.pk)
        self.assertIsNone(new_group.local_site)

    def test_without_localsite_and_with_local_site_user(self):
        """Testing GroupForm without a LocalSite and User on a LocalSite"""
        form = GroupForm(data={b'name': b'test', 
           b'display_name': b'Test', 
           b'users': [
                    self.local_site_user.pk]})
        self.assertTrue(form.is_valid())

    def test_with_limited_localsite(self):
        """Testing GroupForm limited to a LocalSite"""
        form = GroupForm(limit_to_local_site=self.local_site)
        self.assertEqual(form.limited_to_local_site, self.local_site)
        self.assertNotIn(b'local_site', form.fields)
        self.assertEqual(list(form.fields[b'users'].queryset), [
         self.local_site_user])
        self.assertEqual(form.fields[b'users'].widget.local_site_name, self.local_site.name)

    def test_with_limited_localsite_and_changing_site(self):
        """Testing GroupForm limited to a LocalSite and changing LocalSite"""
        site2 = LocalSite.objects.create(name=b'test-site-2')
        form = GroupForm(data={b'name': b'test', 
           b'display_name': b'Test', 
           b'users': [
                    self.local_site_user.pk], 
           b'local_site': site2.pk}, limit_to_local_site=self.local_site)
        self.assertEqual(form.limited_to_local_site, self.local_site)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data[b'local_site'], self.local_site)
        group = form.save()
        self.assertEqual(group.local_site, self.local_site)

    def test_with_limited_localsite_and_compatible_instance(self):
        """Testing GroupForm limited to a LocalSite and editing compatible
        instance
        """
        group = self.create_review_group(local_site=self.local_site)
        GroupForm(instance=group, limit_to_local_site=self.local_site)

    def test_with_limited_localsite_and_incompatible_instance(self):
        """Testing GroupForm limited to a LocalSite and editing incompatible
        instance
        """
        group = self.create_review_group()
        error_message = b'The provided instance is not associated with a LocalSite compatible with this form. Please contact support.'
        with self.assertRaisesMessage(ValueError, error_message):
            GroupForm(instance=group, limit_to_local_site=self.local_site)

    def test_with_limited_localsite_and_invalid_user(self):
        """Testing GroupForm limited to a LocalSite with a User not on the
        LocalSite
        """
        form = GroupForm(data={b'name': b'test', 
           b'display_name': b'Test', 
           b'users': [
                    self.global_site_user.pk]}, limit_to_local_site=self.local_site)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {b'users': [
                    b'A user with ID 2 was not found.']})

    def test_with_localsite_in_data(self):
        """Testing GroupForm with a LocalSite in form data"""
        form = GroupForm()
        self.assertIsNone(form.limited_to_local_site)
        self.assertIn(b'local_site', form.fields)
        self.assertEqual(list(form.fields[b'users'].queryset), [
         self.local_site_user, self.global_site_user])
        self.assertIsNone(form.fields[b'users'].widget.local_site_name)
        form = GroupForm(data={b'name': b'test', 
           b'display_name': b'Test', 
           b'local_site': self.local_site.pk, 
           b'users': [
                    self.local_site_user.pk]})
        self.assertIsNone(form.limited_to_local_site)
        self.assertIn(b'local_site', form.fields)
        self.assertEqual(list(form.fields[b'users'].queryset), [
         self.local_site_user, self.global_site_user])
        self.assertIsNone(form.fields[b'users'].widget.local_site_name)
        self.assertTrue(form.is_valid())
        self.assertEqual(list(form.fields[b'users'].queryset), [
         self.local_site_user, self.global_site_user])
        group = form.save()
        self.assertEqual(group.local_site, self.local_site)
        self.assertEqual(list(group.users.all()), [self.local_site_user])

    def test_with_localsite_in_data_and_instance(self):
        """Testing GroupForm with a LocalSite in form data and editing instance
        """
        group = self.create_review_group()
        form = GroupForm(data={b'name': b'test', 
           b'display_name': b'Test', 
           b'local_site': self.local_site.pk}, instance=group)
        self.assertTrue(form.is_valid())
        new_group = form.save()
        self.assertEqual(group.pk, new_group.pk)
        self.assertEqual(new_group.local_site, self.local_site)

    def test_with_localsite_in_data_and_invalid_user(self):
        """Testing GroupForm with a LocalSite in form data and User not on the
        LocalSite
        """
        form = GroupForm(data={b'name': b'test', 
           b'display_name': b'Test', 
           b'local_site': self.local_site.pk, 
           b'users': [
                    self.global_site_user.pk]})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {b'users': [
                    b'A user with ID 2 was not found.']})

    def test_form_with_positional_argument(self):
        """Testing GroupForm when passing data as a positional argument"""
        form = GroupForm({b'name': b'test', 
           b'display_name': b'Test'})
        self.assertTrue(form.is_valid())