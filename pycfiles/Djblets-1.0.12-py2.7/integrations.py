# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/integrations/templatetags/integrations.py
# Compiled at: 2019-06-12 01:17:17
"""Integrations template tags."""
from __future__ import unicode_literals
import warnings
from django import template
from djblets.deprecation import RemovedInDjblets20Warning
register = template.Library()

@register.simple_tag
def render_integration_config_status(integration, config):
    """Render the integration configuration's status.

    This is deprecated and no longer returns anything.

    Deprecated:
        1.0.11:
        This method no longer serves any purpose, due to major UI
        changes. It now returns an empty string.

    Args:
        integration (djblets.integrations.integrations.Integration, unused):
            The integration to which the config belongs.

        config (djblets.integrations.models.IntegrationConfig, unused):
            The configuration whose status is to be rendered.

    Returns:
        unicode:
        An empty string.
    """
    warnings.warn(b'{% render_integration_config_status %} is deprecated and should no longer be called.', RemovedInDjblets20Warning)
    return integration.render_config_status(config)