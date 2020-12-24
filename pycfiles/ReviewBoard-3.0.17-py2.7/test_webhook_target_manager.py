# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/notifications/tests/test_webhook_target_manager.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import unicode_literals
from djblets.testing.decorators import add_fixtures
from reviewboard.notifications.models import WebHookTarget
from reviewboard.site.models import LocalSite
from reviewboard.testing import TestCase

class WebHookTargetManagerTests(TestCase):
    """Unit tests for WebHookTargetManager."""
    ENDPOINT_URL = b'http://example.com/endpoint/'

    def test_for_event(self):
        """Testing WebHookTargetManager.for_event"""
        WebHookTarget.objects.create(events=b'event1', url=self.ENDPOINT_URL, enabled=True, apply_to=WebHookTarget.APPLY_TO_ALL)
        WebHookTarget.objects.create(events=b'event3', url=self.ENDPOINT_URL, enabled=False, apply_to=WebHookTarget.APPLY_TO_ALL)
        target1 = WebHookTarget.objects.create(events=b'event2,event3', url=self.ENDPOINT_URL, enabled=True, apply_to=WebHookTarget.APPLY_TO_ALL)
        target2 = WebHookTarget.objects.create(events=b'*', url=self.ENDPOINT_URL, enabled=True, apply_to=WebHookTarget.APPLY_TO_ALL)
        targets = WebHookTarget.objects.for_event(b'event3')
        self.assertEqual(targets, [target1, target2])

    def test_for_event_with_local_site(self):
        """Testing WebHookTargetManager.for_event with Local Sites"""
        site = LocalSite.objects.create(name=b'test-site')
        WebHookTarget.objects.create(events=b'event1', url=self.ENDPOINT_URL, enabled=True, apply_to=WebHookTarget.APPLY_TO_ALL)
        WebHookTarget.objects.create(events=b'event1', url=self.ENDPOINT_URL, enabled=False, local_site=site, apply_to=WebHookTarget.APPLY_TO_ALL)
        target = WebHookTarget.objects.create(events=b'event1,event2', url=self.ENDPOINT_URL, enabled=True, local_site=site, apply_to=WebHookTarget.APPLY_TO_ALL)
        targets = WebHookTarget.objects.for_event(b'event1', local_site_id=site.pk)
        self.assertEqual(targets, [target])

    @add_fixtures([b'test_scmtools'])
    def test_for_event_with_repository(self):
        """Testing WebHookTargetManager.for_event with repository"""
        repository1 = self.create_repository()
        repository2 = self.create_repository()
        unused_target1 = WebHookTarget.objects.create(events=b'event1', url=self.ENDPOINT_URL, enabled=False, apply_to=WebHookTarget.APPLY_TO_SELECTED_REPOS)
        unused_target1.repositories.add(repository2)
        unused_target2 = WebHookTarget.objects.create(events=b'event1', url=self.ENDPOINT_URL, enabled=False, apply_to=WebHookTarget.APPLY_TO_SELECTED_REPOS)
        unused_target2.repositories.add(repository1)
        WebHookTarget.objects.create(events=b'event3', url=self.ENDPOINT_URL, enabled=True, apply_to=WebHookTarget.APPLY_TO_ALL)
        WebHookTarget.objects.create(events=b'event1', url=self.ENDPOINT_URL, enabled=True, apply_to=WebHookTarget.APPLY_TO_NO_REPOS)
        target1 = WebHookTarget.objects.create(events=b'event1,event2', url=self.ENDPOINT_URL, enabled=True, apply_to=WebHookTarget.APPLY_TO_ALL)
        target2 = WebHookTarget.objects.create(events=b'event1', url=self.ENDPOINT_URL, enabled=True, apply_to=WebHookTarget.APPLY_TO_SELECTED_REPOS)
        target2.repositories.add(repository1)
        targets = WebHookTarget.objects.for_event(b'event1', repository_id=repository1.pk)
        self.assertEqual(targets, [target1, target2])

    @add_fixtures([b'test_scmtools'])
    def test_for_event_with_no_repository(self):
        """Testing WebHookTargetManager.for_event with no repository"""
        repository = self.create_repository()
        unused_target1 = WebHookTarget.objects.create(events=b'event1', url=self.ENDPOINT_URL, enabled=True, apply_to=WebHookTarget.APPLY_TO_SELECTED_REPOS)
        unused_target1.repositories.add(repository)
        WebHookTarget.objects.create(events=b'event1', url=self.ENDPOINT_URL, enabled=False, apply_to=WebHookTarget.APPLY_TO_NO_REPOS)
        WebHookTarget.objects.create(events=b'event2', url=self.ENDPOINT_URL, enabled=True, apply_to=WebHookTarget.APPLY_TO_NO_REPOS)
        target1 = WebHookTarget.objects.create(events=b'event1,event2', url=self.ENDPOINT_URL, enabled=True, apply_to=WebHookTarget.APPLY_TO_ALL)
        target2 = WebHookTarget.objects.create(events=b'event1', url=self.ENDPOINT_URL, enabled=True, apply_to=WebHookTarget.APPLY_TO_NO_REPOS)
        targets = WebHookTarget.objects.for_event(b'event1')
        self.assertEqual(targets, [target1, target2])

    def test_for_event_with_all_events(self):
        """Testing WebHookTargetManager.for_event with ALL_EVENTS"""
        with self.assertRaisesMessage(ValueError, b'"*" is not a valid event choice'):
            WebHookTarget.objects.for_event(WebHookTarget.ALL_EVENTS)