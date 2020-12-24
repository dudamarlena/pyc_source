# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/hostingsvcs/tests/test_registration.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import unicode_literals
from django.conf.urls import url
from django.core.urlresolvers import NoReverseMatch
from django.http import HttpResponse
from djblets.registries.errors import AlreadyRegisteredError, ItemLookupError
from reviewboard.hostingsvcs.service import HostingService, register_hosting_service, unregister_hosting_service
from reviewboard.site.urlresolvers import local_site_reverse
from reviewboard.testing import TestCase

def hosting_service_url_test_view(request, repo_id):
    """View to test URL pattern addition when registering a hosting service"""
    return HttpResponse(str(repo_id))


class HostingServiceRegistrationTests(TestCase):
    """Unit tests for Hosting Service registration."""

    class DummyService(HostingService):
        name = b'DummyService'

    class DummyServiceWithURLs(HostingService):
        name = b'DummyServiceWithURLs'
        repository_url_patterns = [
         url(b'^hooks/pre-commit/$', hosting_service_url_test_view, name=b'dummy-service-post-commit-hook')]

    def tearDown(self):
        super(HostingServiceRegistrationTests, self).tearDown()
        try:
            unregister_hosting_service(b'dummy-service')
        except ItemLookupError:
            pass

    def test_register_without_urls(self):
        """Testing HostingService registration"""
        register_hosting_service(b'dummy-service', self.DummyService)
        with self.assertRaises(AlreadyRegisteredError):
            register_hosting_service(b'dummy-service', self.DummyService)

    def test_unregister(self):
        """Testing HostingService unregistration"""
        register_hosting_service(b'dummy-service', self.DummyService)
        unregister_hosting_service(b'dummy-service')

    def test_registration_with_urls(self):
        """Testing HostingService registration with URLs"""
        register_hosting_service(b'dummy-service', self.DummyServiceWithURLs)
        self.assertEqual(local_site_reverse(b'dummy-service-post-commit-hook', kwargs={b'repository_id': 1, 
           b'hosting_service_id': b'dummy-service'}), b'/repos/1/dummy-service/hooks/pre-commit/')
        self.assertEqual(local_site_reverse(b'dummy-service-post-commit-hook', local_site_name=b'test-site', kwargs={b'repository_id': 1, 
           b'hosting_service_id': b'dummy-service'}), b'/s/test-site/repos/1/dummy-service/hooks/pre-commit/')
        with self.assertRaises(AlreadyRegisteredError):
            register_hosting_service(b'dummy-service', self.DummyServiceWithURLs)

    def test_unregistration_with_urls(self):
        """Testing HostingService unregistration with URLs"""
        register_hosting_service(b'dummy-service', self.DummyServiceWithURLs)
        unregister_hosting_service(b'dummy-service')
        with self.assertRaises(NoReverseMatch):
            (
             local_site_reverse(b'dummy-service-post-commit-hook', kwargs={b'repository_id': 1, 
                b'hosting_service_id': b'dummy-service'}),)
        with self.assertRaises(ItemLookupError):
            unregister_hosting_service(b'dummy-service')