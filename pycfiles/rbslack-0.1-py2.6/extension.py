# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/rbslack/extension.py
# Compiled at: 2016-03-05 05:42:36
from __future__ import unicode_literals
import json, logging
from django.contrib.sites.models import Site
from django.utils.six.moves.urllib.request import Request, urlopen
from djblets.siteconfig.models import SiteConfiguration
from reviewboard.extensions.base import Extension
from reviewboard.extensions.hooks import SignalHook
from reviewboard.reviews.models import BaseComment, ReviewRequest
from reviewboard.reviews.signals import review_request_closed, review_request_published, review_request_reopened, review_published, reply_published
from reviewboard.site.urlresolvers import local_site_reverse

class SlackExtension(Extension):
    """An extension to integrate Review Board with slack.com"""
    metadata = {b'Name': b'Slack Integration', 
       b'Summary': b'Notifies channels on Slack.com for any review request activity.'}
    is_configurable = True
    default_settings = {b'webhook_url': b'', 
       b'channel': b'', 
       b'notify_username': b'Review Board'}

    def initialize(self):
        """Initialize the extension hooks."""
        hooks = [
         (
          review_request_closed, self.on_review_request_closed),
         (
          review_request_published, self.on_review_request_published),
         (
          review_request_reopened, self.on_review_request_reopened),
         (
          review_published, self.on_review_published),
         (
          reply_published, self.on_reply_published)]
        for (signal, handler) in hooks:
            SignalHook(self, signal, handler)

    def notify(self, text, fields):
        """Send a webhook notification to Slack."""
        payload = {b'username': self.settings[b'notify_username'], 
           b'icon_url': b'http://images.reviewboard.org/rbslack/logo.png', 
           b'attachments': [
                          {b'color': b'#efcc96', 
                             b'fallback': text, 
                             b'fields': fields}]}
        channel = self.settings[b'channel']
        if channel:
            payload[b'channel'] = channel
        try:
            urlopen(Request(self.settings[b'webhook_url'], json.dumps(payload)))
        except Exception, e:
            logging.error(b'Failed to send notification to slack.com: %s', e, exc_info=True)

    def format_link(self, path, text):
        """Format the given URL and text to be shown in a Slack message.

        This will combine together the parts of the URL (method, domain, path)
        and format it using Slack's URL syntax.
        """
        siteconfig = SiteConfiguration.objects.get_current()
        site = Site.objects.get_current()
        text = text.replace(b'&', b'&amp;')
        text = text.replace(b'<', b'&lt;')
        text = text.replace(b'>', b'&gt;')
        return b'<%s://%s%s|%s>' % (
         siteconfig.get(b'site_domain_method'),
         site.domain,
         path,
         text)

    def get_user_text_link(self, user, local_site):
        """Get the Slack-formatted link to a user page."""
        if local_site:
            local_site_name = local_site.name
        else:
            local_site_name = None
        user_url = local_site_reverse(b'user', local_site_name=local_site_name, kwargs={b'username': user.username})
        return self.format_link(user_url, user.get_full_name() or user.username)

    def get_review_request_text_link(self, review_request):
        """Get the Slack-formatted link to a review request."""
        return self.format_link(review_request.get_absolute_url(), review_request.summary)

    def on_review_request_closed(self, user, review_request, type, **kwargs):
        """Handler for the review_request_closed signal."""
        if type == ReviewRequest.DISCARDED:
            close_type = b'Discarded'
        elif type == ReviewRequest.SUBMITTED:
            close_type = b'Submitted'
        else:
            logging.error(b'rbslack: Tried to notify on review_request_closed for review request pk=%d with unknown close type "%s"', review_request.pk, type)
            return
        if not user:
            user = review_request.submitter
        review_request_link = self.get_review_request_text_link(review_request)
        user_link = self.get_user_text_link(user, review_request.local_site)
        fields = [
         {b'title': b'Review Request Closed', 
            b'value': review_request_link, 
            b'short': False},
         {b'title': b'By', 
            b'value': user_link, 
            b'short': True},
         {b'title': b'Closed As', 
            b'value': close_type, 
            b'short': True}]
        text = b'Review Request %s: %s' % (close_type, review_request_link)
        logging.debug(b'Notifying slack.com for event review_request_closed: review_request pk=%d', review_request.pk)
        self.notify(text, fields)

    def on_review_request_published(self, user, review_request, changedesc, **kwargs):
        """Handler for the review_request_published signal."""
        review_request_link = self.get_review_request_text_link(review_request)
        user_link = self.get_user_text_link(user, review_request.local_site)
        fields = [
         {b'title': b'Review Request Published', 
            b'value': review_request_link, 
            b'short': False},
         {b'title': b'By', 
            b'value': user_link, 
            b'short': True}]
        text = b'Review Request Published: %s' % review_request_link
        logging.debug(b'Notifying slack.com for event review_request_published: review_request pk=%d', review_request.pk)
        self.notify(text, fields)

    def on_review_request_reopened(self, user, review_request, **kwargs):
        """Handler for the review_request_reopened signal."""
        if not user:
            user = review_request.submitter
        review_request_link = self.get_review_request_text_link(review_request)
        user_link = self.get_user_text_link(user, review_request.local_site)
        fields = [
         {b'title': b'Review Request Reopened', 
            b'value': review_request_link, 
            b'short': False},
         {b'title': b'By', 
            b'value': user_link, 
            b'short': True}]
        text = b'Review Request Reopened: %s' % review_request_link
        logging.debug(b'Notifying slack.com for event review_request_reopened: review_request pk=%d', review_request.pk)
        self.notify(text, fields)

    def notify_review(self, user, review, title, extra_fields=[], extra_text=b''):
        """Helper to do the common part of reviews and replies."""
        review_request = review.review_request
        review_request_link = self.get_review_request_text_link(review_request)
        user_link = self.get_user_text_link(user, review_request.local_site)
        fields = [
         {b'title': title, 
            b'value': review_request_link, 
            b'short': False},
         {b'title': b'By', 
            b'value': user_link, 
            b'short': True}] + extra_fields
        text = b'%s: %s%s' % (title, review_request_link, extra_text)
        self.notify(text, fields)

    def on_review_published(self, user, review, **kwargs):
        """Handler for the review_published signal."""
        logging.debug(b'Notifying slack.com for event review_published: review pk=%d', review.pk)
        open_issues = 0
        for comment in review.get_all_comments():
            if comment.issue_opened and comment.issue_status == BaseComment.OPEN:
                open_issues += 1

        if open_issues == 1:
            issue_text = b'1 issue'
        else:
            issue_text = b'%d issues' % open_issues
        if review.ship_it:
            if open_issues:
                extra_fields = [
                 {b'title': b'Fix it, then Ship it!', b'value': b':warning: %s' % issue_text, 
                    b'short': True}]
                extra_text = b' (Fix it, then Ship it!)'
            else:
                extra_fields = [
                 {b'title': b'Ship it!', 
                    b'value': b':white_check_mark:', 
                    b'short': True}]
                extra_text = b' (Ship it!)'
        elif open_issues:
            extra_fields = [
             {b'title': b'Open Issues', b'value': b':warning: %s' % issue_text, 
                b'short': True}]
            extra_text = b'(%s)' % issue_text
        else:
            extra_fields = []
            extra_text = b''
        self.notify_review(user, review, b'Review Published', extra_fields=extra_fields, extra_text=extra_text)

    def on_reply_published(self, user, reply, **kwargs):
        """Handler for the reply_published signal."""
        logging.debug(b'Notifying slack.com for event reply_published: review pk=%d', reply.pk)
        self.notify_review(user, reply, b'Reply Published')