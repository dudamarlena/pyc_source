# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/integrations/tests/test_hooks.py
# Compiled at: 2019-06-12 01:17:17
from __future__ import unicode_literals
from django.utils import six
from djblets.extensions.hooks import ExtensionHookPoint
from djblets.integrations.hooks import BaseIntegrationHook
from djblets.integrations.integration import Integration
from djblets.integrations.manager import IntegrationManager
from djblets.integrations.tests.models import IntegrationConfig
from djblets.integrations.tests.testcases import IntegrationsTestCase

@six.add_metaclass(ExtensionHookPoint)
class DummyIntegrationHook(BaseIntegrationHook):

    def __init__(self, manager, *args, **kwargs):
        self.manager = manager
        super(DummyIntegrationHook, self).__init__(*args, **kwargs)

    def get_integration_manager(self):
        return self.manager


class DummyIntegration(Integration):

    def initialize(self):
        pass


class IntegrationHookTests(IntegrationsTestCase):
    """Unit tests for djblets.integrations.hooks.BaseIntegrationHook."""

    def setUp(self):
        super(IntegrationHookTests, self).setUp()
        self.manager = IntegrationManager(IntegrationConfig)
        self.hooks = set()
        self.hook = DummyIntegrationHook(self.manager, self, DummyIntegration)

    def test_initialize(self):
        """Testing BaseIntegrationHook.initialize"""
        self.assertIn(DummyIntegration.integration_id, self.manager._integration_classes)

    def test_shutdown(self):
        """Testing BaseIntegrationHook.initialize"""
        self.hook.disable_hook()
        self.assertNotIn(DummyIntegration.integration_id, self.manager._integration_classes)