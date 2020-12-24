# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/rbintegrations/extension.py
# Compiled at: 2020-01-07 04:31:42
from __future__ import unicode_literals
from django.conf.urls import include, url
from django.utils.translation import ugettext_lazy as _
from reviewboard.extensions.base import Extension
from reviewboard.extensions.hooks import IntegrationHook, URLHook
from reviewboard.urls import reviewable_url_names, review_request_url_names
from rbintegrations.asana.integration import AsanaIntegration
from rbintegrations.circleci.integration import CircleCIIntegration
from rbintegrations.idonethis.integration import IDoneThisIntegration
from rbintegrations.mattermost.integration import MattermostIntegration
from rbintegrations.slack.integration import SlackIntegration
from rbintegrations.travisci.integration import TravisCIIntegration
from rbintegrations.trello.integration import TrelloIntegration

class RBIntegrationsExtension(Extension):
    """Extends Review Board with support for many common integrations."""
    metadata = {b'Name': _(b'Review Board Integrations'), 
       b'Summary': _(b'A set of third-party service integrations for Review Board.')}
    integrations = [
     AsanaIntegration,
     CircleCIIntegration,
     IDoneThisIntegration,
     MattermostIntegration,
     SlackIntegration,
     TravisCIIntegration,
     TrelloIntegration]
    css_bundles = {b'fields': {b'source_filenames': [
                                       b'css/asana/asana.less',
                                       b'css/trello/trello.less'], 
                   b'apply_to': reviewable_url_names + review_request_url_names}, 
       b'asana-integration-config': {b'source_filenames': [
                                                         b'css/asana/integration-config.less']}, 
       b'travis-ci-integration-config': {b'source_filenames': [
                                                             b'css/travisci/integration-config.less']}}
    js_bundles = {b'fields': {b'source_filenames': [
                                       b'js/asana/asanaFieldView.es6.js',
                                       b'js/trello/trelloFieldView.es6.js'], 
                   b'apply_to': reviewable_url_names + review_request_url_names}, 
       b'asana-integration-config': {b'source_filenames': [
                                                         b'js/asana/integrationConfig.es6.js']}, 
       b'travis-ci-integration-config': {b'source_filenames': [
                                                             b'js/travisci/integrationConfig.es6.js']}}

    def initialize(self):
        """Initialize the extension."""
        for integration_cls in self.integrations:
            IntegrationHook(self, integration_cls)

        URLHook(self, [
         url(b'^rbintegrations/asana/', include(b'rbintegrations.asana.urls')),
         url(b'^rbintegrations/circle-ci/', include(b'rbintegrations.circleci.urls')),
         url(b'^rbintegrations/travis-ci/', include(b'rbintegrations.travisci.urls')),
         url(b'^rbintegrations/trello/', include(b'rbintegrations.trello.urls'))])