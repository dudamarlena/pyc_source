# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/privacy/tests/test_consent_views.py
# Compiled at: 2019-06-12 01:17:17
"""Unit tests for djblets.privacy.consent.views."""
from __future__ import unicode_literals
from django.contrib.auth.models import AnonymousUser, User
from django.core.cache import cache
from django.http import HttpResponse, HttpResponseRedirect
from django.test.client import RequestFactory
from django.test.utils import override_settings
from django.utils.six.moves.urllib.parse import quote
from django.views.generic.base import View
from djblets.privacy.consent import BaseConsentRequirement, ConsentData, get_consent_requirements_registry, get_consent_tracker
from djblets.privacy.consent.common import PolicyConsentRequirement
from djblets.privacy.consent.tracker import clear_consent_tracker
from djblets.privacy.consent.views import CheckPendingConsentMixin, check_pending_consent
from djblets.testing.testcases import TestCase
from djblets.views.generic.base import PrePostDispatchViewMixin

class NefariousConsentRequirement(BaseConsentRequirement):
    """A consent requirement for testing."""
    requirement_id = b'nefarious'
    name = b'Nefarious Requirement'
    intent_description = b'We want your data'
    data_use_description = b'We want to use your data for nefarious purposes.'


class BenevolentConsentRequirement(BaseConsentRequirement):
    """A consent requirement for testing."""
    requirement_id = b'Benevolent'
    name = b'Some Requirement'
    intent_description = b'We want your data'
    data_use_description = b'We want to use your data for benevolent purposes.'


class MixinView(CheckPendingConsentMixin, PrePostDispatchViewMixin, View):
    """A view for testing."""

    def get(self, request):
        return HttpResponse(b'ok', status=200)


@check_pending_consent
def decorated_view(request):
    """A view for testing."""
    return HttpResponse(b'ok', status=200)


@override_settings(DJBLETS_PRIVACY_PENDING_CONSENT_REDIRECT_URL=b'/consent')
class CheckPendingConsentTests(TestCase):
    """Unit tests for djblets.privacy.consent.views."""

    @classmethod
    def setUpClass(cls):
        super(CheckPendingConsentTests, cls).setUpClass()
        cls.request_factory = RequestFactory()
        cls.registry = get_consent_requirements_registry()

    def setUp(self):
        super(CheckPendingConsentTests, self).setUp()
        self.registry.register(NefariousConsentRequirement())
        self.registry.register(BenevolentConsentRequirement())

    def tearDown(self):
        super(CheckPendingConsentTests, self).tearDown()
        self.registry.reset()
        clear_consent_tracker()
        cache.clear()

    def test_decorator_anonymous(self):
        """Testing @check_pending_consent when the user is anonymous"""
        request = self.request_factory.get(b'/')
        request.user = AnonymousUser()
        rsp = decorated_view(request)
        self.assertIsInstance(rsp, HttpResponse)
        self.assertEqual(rsp.status_code, 200)
        self.assertEqual(rsp.content, b'ok')

    def test_decorator_all_met(self):
        """Testing @check_pending_consent when a user has no pending consent
        decisions
        """
        request = self.request_factory.get(b'/')
        request.user = User.objects.create_user(username=b'user', email=b'user@example.com')
        tracker = get_consent_tracker()
        tracker.record_consent_data_list(request.user, [
         ConsentData(BenevolentConsentRequirement.requirement_id, granted=True),
         ConsentData(NefariousConsentRequirement.requirement_id, granted=False)])
        rsp = decorated_view(request)
        self.assertNotIsInstance(rsp, HttpResponseRedirect)
        self.assertIsInstance(rsp, HttpResponse)
        self.assertEqual(rsp.content, b'ok')

    def test_decorator_some_met(self):
        """Testing @check_pending_consent when a user has some pending consent
        decisions
        """
        request = self.request_factory.get(b'/')
        request.user = User.objects.create_user(username=b'user', email=b'user@example.com')
        get_consent_tracker().record_consent_data(request.user, ConsentData(BenevolentConsentRequirement.requirement_id, granted=True))
        rsp = decorated_view(request)
        self.assertIsInstance(rsp, HttpResponseRedirect)
        self.assertEqual(rsp.url, b'/consent')

    def test_decorator_none_met(self):
        """Testing @check_pending_consent when a user has all consent
        decisions pending
        """
        request = self.request_factory.get(b'/')
        request.user = User.objects.create_user(username=b'user', email=b'user@example.com')
        rsp = decorated_view(request)
        self.assertIsInstance(rsp, HttpResponseRedirect)
        self.assertEqual(rsp.url, b'/consent')

    def test_decorator_function_url(self):
        """Testing @check_pending_consent when
        DJBLETS_PRIVACY_PENDING_CONSENT_REDIRECT_URL is a function
        """

        def redirect_url(request):
            return b'/consent?next=%s' % quote(request.get_full_path())

        request = self.request_factory.get(b'/foo/')
        request.user = User.objects.create_user(username=b'user', email=b'user@example.com')
        with self.settings(DJBLETS_PRIVACY_PENDING_CONSENT_REDIRECT_URL=redirect_url):
            rsp = decorated_view(request)
        self.assertIsInstance(rsp, HttpResponseRedirect)
        self.assertEqual(rsp.url, b'/consent?next=/foo/')

    def test_decorator_reject_policy(self):
        """Testing @check_pending_consent when the user has rejected the policy
        requirement
        """
        policy_requirement = PolicyConsentRequirement(b'https://example.com/', b'https://example.com/', reject_instructions=b'Obey.')
        self.registry.register(policy_requirement)
        request = self.request_factory.get(b'/')
        request.user = User.objects.create_user(username=b'user', email=b'user@example.com')
        get_consent_tracker().record_consent_data_list(request.user, [
         ConsentData(BenevolentConsentRequirement.requirement_id, granted=True),
         ConsentData(NefariousConsentRequirement.requirement_id, granted=False),
         policy_requirement.build_consent_data(granted=False)])
        rsp = decorated_view(request)
        self.assertIsInstance(rsp, HttpResponseRedirect)
        self.assertEqual(rsp.url, b'/consent')

    def test_mixin_anonymous(self):
        """Testing CheckPendingConsentMixin when the user is anonymous"""
        request = self.request_factory.get(b'/')
        request.user = AnonymousUser()
        rsp = MixinView.as_view()(request)
        self.assertIsInstance(rsp, HttpResponse)
        self.assertEqual(rsp.status_code, 200)
        self.assertEqual(rsp.content, b'ok')

    def test_mixin_all_met(self):
        """Testing CheckPendingConsentMixin when a user has no pending consent
        decisions
        """
        request = self.request_factory.get(b'/')
        request.user = User.objects.create_user(username=b'user', email=b'user@example.com')
        get_consent_tracker().record_consent_data_list(request.user, [
         ConsentData(BenevolentConsentRequirement.requirement_id, granted=True),
         ConsentData(NefariousConsentRequirement.requirement_id, granted=False)])
        rsp = MixinView.as_view()(request)
        self.assertNotIsInstance(rsp, HttpResponseRedirect)
        self.assertIsInstance(rsp, HttpResponse)
        self.assertEqual(rsp.content, b'ok')

    def test_mixin_some_met(self):
        """Testing CheckPendingConsentMixin when a user has some pending
        consent decisions
        """
        request = self.request_factory.get(b'/')
        request.user = User.objects.create_user(username=b'user', email=b'user@example.com')
        get_consent_tracker().record_consent_data(request.user, ConsentData(BenevolentConsentRequirement.requirement_id, granted=True))
        rsp = MixinView.as_view()(request)
        self.assertIsInstance(rsp, HttpResponseRedirect)
        self.assertEqual(rsp.url, b'/consent')

    def test_mixin_none_met(self):
        """Testing CheckPendingConsentMixin when a user has all consent
        decisions pending
        """
        request = self.request_factory.get(b'/')
        request.user = User.objects.create_user(username=b'user', email=b'user@example.com')
        rsp = MixinView.as_view()(request)
        self.assertIsInstance(rsp, HttpResponseRedirect)
        self.assertEqual(rsp.url, b'/consent')

    def test_mixin_function_url(self):
        """Testing CheckPendingConsentMixin when
        DJBLETS_PRIVACY_PENDING_CONSENT_REDIRECT_URL is a function
        """

        def redirect_url(request):
            return b'/consent?next=%s' % quote(request.get_full_path())

        request = self.request_factory.get(b'/foo/')
        request.user = User.objects.create_user(username=b'user', email=b'user@example.com')
        with self.settings(DJBLETS_PRIVACY_PENDING_CONSENT_REDIRECT_URL=redirect_url):
            rsp = MixinView.as_view()(request)
        self.assertIsInstance(rsp, HttpResponseRedirect)
        self.assertEqual(rsp.url, b'/consent?next=/foo/')

    def test_mixin_reject_policy(self):
        """Testing CheckPendingConsentMixin when the user has rejected the
        policy requirement
        """
        policy_requirement = PolicyConsentRequirement(b'https://example.com/', b'https://example.com/', reject_instructions=b'Obey.')
        self.registry.register(policy_requirement)
        request = self.request_factory.get(b'/')
        request.user = User.objects.create_user(username=b'user', email=b'user@example.com')
        get_consent_tracker().record_consent_data_list(request.user, [
         ConsentData(BenevolentConsentRequirement.requirement_id, granted=True),
         ConsentData(NefariousConsentRequirement.requirement_id, granted=False),
         policy_requirement.build_consent_data(granted=False)])
        rsp = MixinView.as_view()(request)
        self.assertIsInstance(rsp, HttpResponseRedirect)
        self.assertEqual(rsp.url, b'/consent')