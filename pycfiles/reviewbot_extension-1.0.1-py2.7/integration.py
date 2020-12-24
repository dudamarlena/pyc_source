# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/reviewbotext/integration.py
# Compiled at: 2018-07-31 04:09:55
from __future__ import unicode_literals
import json, logging
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _
from djblets.extensions.hooks import SignalHook
from reviewboard.admin.server import get_server_url
from reviewboard.integrations import Integration
from reviewboard.reviews.models import StatusUpdate
from reviewboard.reviews.signals import review_request_published
from reviewbotext.forms import ReviewBotConfigForm
from reviewbotext.models import Tool

class ReviewBotIntegration(Integration):
    """The integration for Review Bot.

    Each integration configuration corresponds to a tool that will be run when
    some conditions match.
    """
    name = b'Review Bot'
    description = _(b'Performs automated analysis and review on code changes.')
    config_form_cls = ReviewBotConfigForm

    def initialize(self):
        """Initialize the integration hooks."""
        SignalHook(self, review_request_published, self._on_review_request_published)

    @cached_property
    def icon_static_urls(self):
        """The icons used for the integration."""
        from reviewbotext.extension import ReviewBotExtension
        extension = ReviewBotExtension.instance
        return {b'1x': extension.get_static_url(b'images/reviewbot.png'), 
           b'2x': extension.get_static_url(b'images/reviewbot@2x.png')}

    def _on_review_request_published(self, sender, review_request, **kwargs):
        """Handle when a review request is published.

        Args:
            sender (object):
                The sender of the signal.

            review_request (reviewboard.reviews.models.ReviewRequest):
                The review request which was published.

            **kwargs (dict):
                Additional keyword arguments.
        """
        review_request_id = review_request.get_display_id()
        diffset = review_request.get_latest_diffset()
        if not diffset:
            return
        else:
            changedesc = kwargs.get(b'changedesc')
            if changedesc is not None:
                fields_changed = changedesc.fields_changed
                if b'diff' not in fields_changed or b'added' not in fields_changed[b'diff']:
                    return
            from reviewbotext.extension import ReviewBotExtension
            extension = ReviewBotExtension.instance
            matching_configs = [ config for config in self.get_configs(review_request.local_site) if config.match_conditions(form_cls=self.config_form_cls, review_request=review_request)
                               ]
            if not matching_configs:
                return
            server_url = get_server_url(local_site=review_request.local_site)
            session = extension.login_user()
            user = extension.user
            for config in matching_configs:
                tool_id = config.settings.get(b'tool')
                try:
                    tool = Tool.objects.get(pk=tool_id)
                except Tool.DoesNotExist:
                    logging.error(b'Skipping Review Bot integration config %s (%d) because Tool with pk=%d does not exist.', config.name, config.pk, tool_id)

                review_settings = {b'max_comments': config.settings.get(b'max_comments', ReviewBotConfigForm.MAX_COMMENTS_DEFAULT), 
                   b'comment_unmodified': config.settings.get(b'comment_on_unmodified_code', ReviewBotConfigForm.COMMENT_ON_UNMODIFIED_CODE_DEFAULT), 
                   b'open_issues': config.settings.get(b'open_issues', ReviewBotConfigForm.OPEN_ISSUES_DEFAULT)}
                try:
                    tool_options = json.loads(config.settings.get(b'tool_options', b'{}'))
                except Exception as e:
                    logging.exception(b'Failed to parse tool_options for Review Bot integration config %s (%d): %s', config.name, config.pk, e)
                    tool_options = {}

                status_update = StatusUpdate.objects.create(service_id=b'reviewbot.%s' % tool.name, summary=tool.name, description=b'starting...', review_request=review_request, change_description=changedesc, state=StatusUpdate.PENDING, timeout=tool.timeout, user=user)
                repository = review_request.repository
                queue = b'%s.%s' % (tool.entry_point, tool.version)
                if tool.working_directory_required:
                    queue = b'%s.%s' % (queue, repository.name)
                extension.celery.send_task(b'reviewbot.tasks.RunTool', kwargs={b'server_url': server_url, 
                   b'session': session, 
                   b'username': user.username, 
                   b'review_request_id': review_request_id, 
                   b'diff_revision': diffset.revision, 
                   b'status_update_id': status_update.pk, 
                   b'review_settings': review_settings, 
                   b'tool_options': tool_options, 
                   b'repository_name': repository.name, 
                   b'base_commit_id': diffset.base_commit_id}, queue=queue)

            return