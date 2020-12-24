# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/rbintegrations/trello/integration.py
# Compiled at: 2020-01-07 04:31:42
"""Integration for associating review requests with Trello cards."""
from __future__ import unicode_literals
from django.utils.functional import cached_property
from reviewboard.extensions.hooks import ReviewRequestFieldsHook
from reviewboard.integrations import Integration
from rbintegrations.trello.fields import TrelloField
from rbintegrations.trello.forms import TrelloIntegrationConfigForm

class TrelloIntegration(Integration):
    """Integrates Review Board with Trello."""
    name = b'Trello'
    description = b'Associate Trello cards with your review requests.'
    config_form_cls = TrelloIntegrationConfigForm

    def initialize(self):
        """Initialize the integration hooks."""
        ReviewRequestFieldsHook(self, b'main', [TrelloField])

    @cached_property
    def icon_static_urls(self):
        """The icons used for the integration."""
        from rbintegrations.extension import RBIntegrationsExtension
        extension = RBIntegrationsExtension.instance
        return {b'1x': extension.get_static_url(b'images/trello/icon.png'), 
           b'2x': extension.get_static_url(b'images/trello/icon@2x.png')}