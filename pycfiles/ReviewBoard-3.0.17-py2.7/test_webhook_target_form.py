# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/notifications/tests/test_webhook_target_form.py
# Compiled at: 2020-02-11 04:03:56
"""Unit tests for reviewboard.notifications.forms.WebHookTargetForm."""
from __future__ import unicode_literals
from reviewboard.notifications.forms import WebHookTargetForm
from reviewboard.notifications.models import WebHookTarget
from reviewboard.site.models import LocalSite
from reviewboard.testing import TestCase

class WebHookTargetFormTests(TestCase):
    """Unit tests for reviewboard.notifications.forms.WebHookTargetForm."""
    fixtures = [
     b'test_scmtools']

    def setUp(self):
        super(WebHookTargetFormTests, self).setUp()
        self.local_site = LocalSite.objects.create(name=b'test')
        self.local_site_repo = self.create_repository(name=b'local-site-repo', local_site=self.local_site)
        self.global_site_repo = self.create_repository(name=b'global-site-repo')

    def test_without_localsite(self):
        """Testing WebHookTargetForm without a LocalSite"""
        form = WebHookTargetForm()
        self.assertIsNone(form.limited_to_local_site)
        self.assertIn(b'local_site', form.fields)
        self.assertEqual(list(form.fields[b'repositories'].queryset), [
         self.local_site_repo, self.global_site_repo])
        form = WebHookTargetForm(data={b'apply_to': WebHookTarget.APPLY_TO_SELECTED_REPOS, 
           b'encoding': WebHookTarget.ENCODING_JSON, 
           b'events': [
                     b'*'], 
           b'url': b'https://example.com/', 
           b'repositories': [
                           self.global_site_repo.pk]})
        self.assertIsNone(form.limited_to_local_site)
        self.assertIn(b'local_site', form.fields)
        self.assertEqual(list(form.fields[b'repositories'].queryset), [
         self.local_site_repo, self.global_site_repo])
        self.assertTrue(form.is_valid())
        self.assertEqual(list(form.fields[b'repositories'].queryset), [
         self.local_site_repo, self.global_site_repo])
        webhook = form.save()
        self.assertIsNone(webhook.local_site)
        self.assertEqual(list(webhook.repositories.all()), [
         self.global_site_repo])

    def test_without_localsite_and_instance(self):
        """Testing WebHookTargetForm without a LocalSite and editing instance
        """
        webhook = WebHookTarget.objects.create()
        form = WebHookTargetForm(data={b'apply_to': WebHookTarget.APPLY_TO_ALL, 
           b'encoding': WebHookTarget.ENCODING_JSON, 
           b'events': [
                     b'*'], 
           b'url': b'https://example.com/', 
           b'repositories': [
                           self.global_site_repo.pk]}, instance=webhook)
        self.assertTrue(form.is_valid())
        new_webhook = form.save()
        self.assertEqual(webhook.pk, new_webhook.pk)
        self.assertIsNone(new_webhook.local_site)

    def test_without_localsite_and_with_local_site_repo(self):
        """Testing WebHookTargetForm without a LocalSite and Repository on a
        LocalSite
        """
        form = WebHookTargetForm(data={b'apply_to': WebHookTarget.APPLY_TO_ALL, 
           b'encoding': WebHookTarget.ENCODING_JSON, 
           b'events': [
                     b'*'], 
           b'url': b'https://example.com/', 
           b'repositories': [
                           self.local_site_repo.pk]})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {b'repositories': [
                           b'A repository with ID 1 was not found.']})

    def test_with_limited_localsite(self):
        """Testing WebHookTargetForm limited to a LocalSite"""
        form = WebHookTargetForm(limit_to_local_site=self.local_site)
        self.assertEqual(form.limited_to_local_site, self.local_site)
        self.assertNotIn(b'local_site', form.fields)
        self.assertEqual(list(form.fields[b'repositories'].queryset), [
         self.local_site_repo])

    def test_with_limited_localsite_and_changing_site(self):
        """Testing WebHookTargetForm limited to a LocalSite and changing
        LocalSite
        """
        site2 = LocalSite.objects.create(name=b'test-site-2')
        form = WebHookTargetForm(data={b'apply_to': WebHookTarget.APPLY_TO_ALL, 
           b'encoding': WebHookTarget.ENCODING_JSON, 
           b'events': [
                     b'*'], 
           b'url': b'https://example.com/', 
           b'repositories': [
                           self.local_site_repo.pk], 
           b'local_site': site2.pk}, limit_to_local_site=self.local_site)
        self.assertEqual(form.limited_to_local_site, self.local_site)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data[b'local_site'], self.local_site)
        webhook = form.save()
        self.assertEqual(webhook.local_site, self.local_site)

    def test_with_limited_localsite_and_compatible_instance(self):
        """Testing WebHookTargetForm limited to a LocalSite and editing
        compatible instance
        """
        webhook = WebHookTarget(local_site=self.local_site)
        WebHookTargetForm(instance=webhook, limit_to_local_site=self.local_site)

    def test_with_limited_localsite_and_incompatible_instance(self):
        """Testing WebHookTargetForm limited to a LocalSite and editing
        incompatible instance
        """
        webhook = WebHookTarget.objects.create()
        error_message = b'The provided instance is not associated with a LocalSite compatible with this form. Please contact support.'
        with self.assertRaisesMessage(ValueError, error_message):
            WebHookTargetForm(instance=webhook, limit_to_local_site=self.local_site)

    def test_with_limited_localsite_and_invalid_repository(self):
        """Testing WebHookTargetForm limited to a LocalSite with a Repository
        not on the LocalSite
        """
        form = WebHookTargetForm(data={b'apply_to': WebHookTarget.APPLY_TO_ALL, 
           b'encoding': WebHookTarget.ENCODING_JSON, 
           b'events': [
                     b'*'], 
           b'url': b'https://example.com/', 
           b'repositories': [
                           self.global_site_repo.pk]}, limit_to_local_site=self.local_site)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {b'repositories': [
                           b'A repository with ID 2 was not found.']})

    def test_with_localsite_in_data(self):
        """Testing WebHookTargetForm with a LocalSite in form data"""
        form = WebHookTargetForm()
        self.assertIsNone(form.limited_to_local_site)
        self.assertIn(b'local_site', form.fields)
        self.assertEqual(list(form.fields[b'repositories'].queryset), [
         self.local_site_repo, self.global_site_repo])
        form = WebHookTargetForm(data={b'apply_to': WebHookTarget.APPLY_TO_SELECTED_REPOS, 
           b'encoding': WebHookTarget.ENCODING_JSON, 
           b'events': [
                     b'*'], 
           b'url': b'https://example.com/', 
           b'local_site': self.local_site.pk, 
           b'repositories': [
                           self.local_site_repo.pk]})
        self.assertIsNone(form.limited_to_local_site)
        self.assertIn(b'local_site', form.fields)
        self.assertEqual(list(form.fields[b'repositories'].queryset), [
         self.local_site_repo, self.global_site_repo])
        self.assertTrue(form.is_valid())
        self.assertEqual(list(form.fields[b'repositories'].queryset), [
         self.local_site_repo, self.global_site_repo])
        webhook = form.save()
        self.assertEqual(webhook.local_site, self.local_site)
        self.assertEqual(list(webhook.repositories.all()), [
         self.local_site_repo])

    def test_with_localsite_in_data_and_instance(self):
        """Testing WebHookTargetForm with a LocalSite in form data and editing
        instance
        """
        webhook = WebHookTarget.objects.create()
        form = WebHookTargetForm(data={b'apply_to': WebHookTarget.APPLY_TO_ALL, 
           b'encoding': WebHookTarget.ENCODING_JSON, 
           b'events': [
                     b'*'], 
           b'url': b'https://example.com/', 
           b'local_site': self.local_site.pk}, instance=webhook)
        self.assertTrue(form.is_valid())
        new_webhook = form.save()
        self.assertEqual(webhook.pk, new_webhook.pk)
        self.assertEqual(new_webhook.local_site, self.local_site)

    def test_with_localsite_in_data_and_invalid_repository(self):
        """Testing WebHookTargetForm with a LocalSite in form data and
        Repository not on the LocalSite
        """
        form = WebHookTargetForm(data={b'apply_to': WebHookTarget.APPLY_TO_ALL, 
           b'encoding': WebHookTarget.ENCODING_JSON, 
           b'events': [
                     b'*'], 
           b'url': b'https://example.com/', 
           b'local_site': self.local_site.pk, 
           b'repositories': [
                           self.global_site_repo.pk]})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {b'repositories': [
                           b'A repository with ID 2 was not found.']})