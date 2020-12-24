# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/integrations/tests/test_views.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import unicode_literals
from django.test import RequestFactory
from reviewboard.integrations.base import Integration, get_integration_manager
from reviewboard.integrations.models import IntegrationConfig
from reviewboard.integrations.views import AdminIntegrationConfigFormView
from reviewboard.site.models import LocalSite
from reviewboard.testing.testcase import TestCase

class MyIntegration(Integration):
    pass


class AdminIntegrationConfigFormViewTests(TestCase):
    """Unit tests for AdminIntegrationConfigFormView."""

    def setUp(self):
        super(AdminIntegrationConfigFormViewTests, self).setUp()
        self.integration = MyIntegration(get_integration_manager())
        self.config = IntegrationConfig()
        self.request = RequestFactory().request()
        self.view = AdminIntegrationConfigFormView(request=self.request, integration=self.integration, config=self.config)

    def test_get_form_kwargs(self):
        """Testing AdminIntegrationConfigFormView.get_form_kwargs"""
        form_kwargs = self.view.get_form_kwargs()
        self.assertIsNone(form_kwargs[b'limit_to_local_site'])

    def test_get_form_kwargs_with_local_site(self):
        """Testing AdminIntegrationConfigFormView.get_form_kwargs with
        LocalSite
        """
        local_site = LocalSite.objects.create(name=b'local-site-1')
        self.request.local_site = local_site
        form_kwargs = self.view.get_form_kwargs()
        self.assertEqual(form_kwargs[b'limit_to_local_site'], local_site)