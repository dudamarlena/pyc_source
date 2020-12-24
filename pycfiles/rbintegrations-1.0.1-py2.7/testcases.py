# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/rbintegrations/testing/testcases.py
# Compiled at: 2020-01-07 04:31:42
"""Base test cases for rbintegrations."""
from __future__ import unicode_literals
from kgb import SpyAgency
from reviewboard.extensions.testing import ExtensionTestCase
from reviewboard.integrations.base import get_integration_manager
from rbintegrations.extension import RBIntegrationsExtension

class RBIntegrationsExtensionTestCase(SpyAgency, ExtensionTestCase):
    """Base class for unit tests for rbintegrations."""
    extension_class = RBIntegrationsExtension


class IntegrationTestCase(RBIntegrationsExtensionTestCase):
    """Base class for unit tests for individual integrations."""
    integration_cls = None

    def setUp(self):
        super(IntegrationTestCase, self).setUp()
        integration_mgr = get_integration_manager()
        self.integration = integration_mgr.get_integration(self.integration_cls.integration_id)
        integration_mgr.clear_all_configs_cache()