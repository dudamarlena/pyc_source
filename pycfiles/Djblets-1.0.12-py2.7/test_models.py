# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/integrations/tests/test_models.py
# Compiled at: 2019-06-12 01:17:17
from __future__ import unicode_literals
from djblets.integrations.integration import Integration
from djblets.integrations.manager import IntegrationManager
from djblets.integrations.tests.models import IntegrationConfig
from djblets.integrations.tests.testcases import IntegrationsTestCase

class DummyIntegration1(Integration):
    default_settings = {b'foo': b'default-foo'}

    def initialize(self):
        pass


class IntegrationConfigTests(IntegrationsTestCase):
    """Unit tests for djblets.integrations.models.BaseIntegrationConfig."""

    def setUp(self):
        super(IntegrationConfigTests, self).setUp()
        self.manager = IntegrationManager(IntegrationConfig)
        self.integration = self.manager.register_integration_class(DummyIntegration1)
        self.config = self.integration.create_config()
        self.config.manager = self.manager

    def test_integration(self):
        """Testing BaseIntegrationConfig.integration"""
        self.assertEqual(self.config.integration, self.integration)

    def test_get(self):
        """Testing BaseIntegrationConfig.get"""
        self.config.settings[b'foo'] = b'bar'
        self.assertEqual(self.config.get(b'foo'), b'bar')

    def test_get_with_integration_defaults(self):
        """Testing BaseIntegrationConfig.get with integration defaults"""
        self.assertEqual(self.config.get(b'foo'), b'default-foo')

    def test_get_with_default(self):
        """Testing BaseIntegrationConfig.get with default"""
        self.assertEqual(self.config.get(b'new-key', b'my-default'), b'my-default')

    def test_set(self):
        """Testing BaseIntegrationConfig.set"""
        self.config.set(b'my-key', b'my-value')
        self.assertEqual(self.config.settings.get(b'my-key'), b'my-value')