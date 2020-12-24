# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/privacy/tests/test_consent_tracker.py
# Compiled at: 2019-06-12 01:17:17
"""Unit tests for djblets.privacy.consent.tracker."""
from __future__ import unicode_literals
from datetime import datetime
from django.contrib.auth.models import User
from django.core.cache import cache
from django.test.utils import override_settings
from django.utils import timezone
from kgb import SpyAgency
from djblets.cache.backend import make_cache_key
from djblets.privacy.consent import BaseConsentRequirement, BaseConsentTracker, Consent, ConsentData, DatabaseConsentTracker, get_consent_requirements_registry, get_consent_tracker
from djblets.privacy.models import StoredConsentData
from djblets.privacy.tests.testcases import ConsentTestCase

class CustomConsentTracker(BaseConsentTracker):
    pass


class MyConsentRequirement1(BaseConsentRequirement):
    requirement_id = b'my-requirement-1'
    name = b'My Requirement 1'
    summary = b'We would like to use this thing'
    intent_description = b'We need this for testing.'
    data_use_description = b'Sending all the things.'
    icons = {b'1x': b'/static/consent.png', 
       b'2x': b'/static/consent@2x.png'}


class MyConsentRequirement2(BaseConsentRequirement):
    requirement_id = b'my-requirement-2'
    name = b'My Requirement 2'
    summary = b'We would also like this'
    intent_description = b'We need this for dancing.'
    data_use_description = b'Dancing all the things.'


class DatabaseConsentTrackerTests(SpyAgency, ConsentTestCase):
    """Unit tests for DatabaseConsentTracker."""

    def setUp(self):
        super(DatabaseConsentTrackerTests, self).setUp()
        self.tracker = DatabaseConsentTracker()
        self.user = User.objects.create(username=b'test-user', email=b'test@example.com')
        self.timestamp = datetime(2018, 1, 2, 13, 14, 15, tzinfo=timezone.utc)
        self.spy_on(timezone.now, call_fake=lambda : self.timestamp)

    def test_record_consent_data(self):
        """Testing DatabaseConsentTracker.record_consent_data"""
        consent_data = ConsentData(requirement_id=b'test-requirement-1', granted=True, source=b'http://example.com/account/profile/#consent', extra_data={b'test': True})
        self.tracker.record_consent_data(self.user, consent_data)
        stored_consents = list(StoredConsentData.objects.all())
        self.assertEqual(len(stored_consents), 1)
        stored_consent = stored_consents[0]
        self.assertEqual(stored_consent.user, self.user)
        self.assertEqual(stored_consent.audit_identifier, b'973dfe463ec85785f5f95af5ba3906eedb2d931c24e69824a89ea65dba4e813b')
        self.assertEqual(stored_consent.time_added, self.timestamp)
        self.assertEqual(stored_consent.last_updated, self.timestamp)
        self.assertEqual(stored_consent.consent_grants, {b'test-requirement-1': True})
        self.assertEqual(stored_consent.audit_trail, {b'test-requirement-1': [
                                 {b'identifier': b'973dfe463ec85785f5f95af5ba3906eedb2d931c24e69824a89ea65dba4e813b', 
                                    b'granted': True, 
                                    b'timestamp': b'2018-01-02T13:14:15+00:00', 
                                    b'source': b'http://example.com/account/profile/#consent', 
                                    b'extra_data': {b'test': True}}]})

    def test_record_consent_data_list(self):
        """Testing DatabaseConsentTracker.record_consent_data_list"""
        consent_data_1 = ConsentData(requirement_id=b'test-requirement-1', granted=True, source=b'http://example.com/account/profile/#consent', extra_data={b'test': True})
        consent_data_2 = ConsentData(requirement_id=b'test-requirement-2', granted=False, source=b'http://example.com/account/profile/#consent')
        self.tracker.record_consent_data_list(self.user, [
         consent_data_1, consent_data_2])
        stored_consents = list(StoredConsentData.objects.all())
        self.assertEqual(len(stored_consents), 1)
        stored_consent = stored_consents[0]
        self.assertEqual(stored_consent.user, self.user)
        self.assertEqual(stored_consent.audit_identifier, b'973dfe463ec85785f5f95af5ba3906eedb2d931c24e69824a89ea65dba4e813b')
        self.assertEqual(stored_consent.time_added, self.timestamp)
        self.assertEqual(stored_consent.last_updated, self.timestamp)
        self.assertEqual(stored_consent.consent_grants, {b'test-requirement-1': True, 
           b'test-requirement-2': False})
        self.assertEqual(stored_consent.audit_trail, {b'test-requirement-1': [
                                 {b'identifier': b'973dfe463ec85785f5f95af5ba3906eedb2d931c24e69824a89ea65dba4e813b', 
                                    b'granted': True, 
                                    b'timestamp': b'2018-01-02T13:14:15+00:00', 
                                    b'source': b'http://example.com/account/profile/#consent', 
                                    b'extra_data': {b'test': True}}], 
           b'test-requirement-2': [
                                 {b'identifier': b'973dfe463ec85785f5f95af5ba3906eedb2d931c24e69824a89ea65dba4e813b', 
                                    b'granted': False, 
                                    b'timestamp': b'2018-01-02T13:14:15+00:00', 
                                    b'source': b'http://example.com/account/profile/#consent'}]})

    def test_record_consent_data_list_clears_cache(self):
        """Testing DatabaseConsentTracker.record_consent_data_list clears cache
        """
        consent_data_1 = ConsentData(requirement_id=b'test-requirement-1', granted=True)
        consent_data_2 = ConsentData(requirement_id=b'test-requirement-2', granted=False)
        cache_key = make_cache_key(b'privacy-consent:%s' % self.user.pk)
        cache.add(cache_key, [b'test-requirement-1'])
        self.assertEqual(cache.get(cache_key), [b'test-requirement-1'])
        self.tracker.record_consent_data_list(self.user, [
         consent_data_1, consent_data_2])
        self.assertIsNone(cache.get(cache_key))

    def test_get_consent(self):
        """Testing DatabaseConsentTracker.get_consent"""
        self.test_record_consent_data_list()
        self.assertEqual(self.tracker.get_consent(self.user, b'test-requirement-1'), Consent.GRANTED)
        self.assertEqual(self.tracker.get_consent(self.user, b'test-requirement-2'), Consent.DENIED)
        self.assertEqual(self.tracker.get_consent(self.user, b'test-requirement-3'), Consent.UNSET)
        self.assertEqual(cache.get(make_cache_key(b'privacy-consent:%s' % self.user.pk)), {b'test-requirement-1': Consent.GRANTED, 
           b'test-requirement-2': Consent.DENIED})

    def test_get_consent_with_no_user_data(self):
        """Testing DatabaseConsentTracker.get_consent with user without any
        consent data
        """
        self.assertEqual(self.tracker.get_consent(self.user, b'test'), Consent.UNSET)
        self.assertEqual(cache.get(make_cache_key(b'privacy-consent:%s' % self.user.pk)), {})

    def test_get_all_consent(self):
        """Testing DatabaseConsentTracker.get_all_consent"""
        self.test_record_consent_data_list()
        self.assertEqual(self.tracker.get_all_consent(self.user), {b'test-requirement-1': Consent.GRANTED, 
           b'test-requirement-2': Consent.DENIED})
        self.assertEqual(cache.get(make_cache_key(b'privacy-consent:%s' % self.user.pk)), {b'test-requirement-1': Consent.GRANTED, 
           b'test-requirement-2': Consent.DENIED})

    def test_get_all_consent_with_no_user_data(self):
        """Testing DatabaseConsentTracker.get_all_consent with user without any
        consent data
        """
        self.assertEqual(self.tracker.get_all_consent(self.user), {})
        self.assertEqual(cache.get(make_cache_key(b'privacy-consent:%s' % self.user.pk)), {})

    def test_get_pending_consent_requirements(self):
        """Testing DatabaseConsentTracker.get_pending_consent_requirements"""
        requirement1 = MyConsentRequirement1()
        requirement2 = MyConsentRequirement2()
        registry = get_consent_requirements_registry()
        try:
            registry.register(requirement1)
            registry.register(requirement2)
            self.assertEqual(self.tracker.get_pending_consent_requirements(self.user), [
             requirement1, requirement2])
            consent_data_1 = requirement1.build_consent_data(granted=True)
            self.tracker.record_consent_data_list(self.user, [consent_data_1])
            self.assertEqual(self.tracker.get_pending_consent_requirements(self.user), [
             requirement2])
            consent_data_2 = requirement2.build_consent_data(granted=True)
            self.tracker.record_consent_data_list(self.user, [consent_data_2])
            self.assertEqual(self.tracker.get_pending_consent_requirements(self.user), [])
        finally:
            registry.unregister(requirement1)
            registry.unregister(requirement2)


class ConsentTrackerInstanceTests(ConsentTestCase):
    """Unit tests for consent tracker instance management."""

    def test_get_consent_tracker_with_default(self):
        """Testing get_consent_tracker with default tracker"""
        self.assertIsInstance(get_consent_tracker(), DatabaseConsentTracker)

    @override_settings(DJBLETS_PRIVACY_CONSENT_TRACKER=b'%s.CustomConsentTracker' % __name__)
    def test_get_consent_tracker_with_custom(self):
        """Testing get_consent_tracker with custom tracker"""
        self.assertIsInstance(get_consent_tracker(), CustomConsentTracker)