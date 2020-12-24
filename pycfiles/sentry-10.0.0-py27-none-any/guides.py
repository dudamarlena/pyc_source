# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/assistant/guides.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from django.utils.translation import ugettext_lazy as _
GUIDES = {'issue': {'id': 1, 
             'required_targets': [
                                'issue_title', 'exception'], 
             'steps': [
                     {'title': _('Issue Details'), 
                        'message': _("The issue page contains all the details about an issue. Let's get started."), 
                        'target': 'issue_title'},
                     {'title': _('Stacktrace'), 
                        'message': _('See the sequence of function calls that led to the error, and global/local variables for each stack frame.'), 
                        'target': 'exception'},
                     {'title': _('Breadcrumbs'), 
                        'message': _("Breadcrumbs are a trail of events that happened prior to the error. They're similar to traditional logs but can record more rich structured data. When Sentry is used with web frameworks, breadcrumbs are automatically captured for events like database calls and network requests."), 
                        'target': 'breadcrumbs'},
                     {'title': _('Tags'), 
                        'message': _('Attach arbitrary key-value pairs to each event which you can search and filter on. View a heatmap of all tags for an issue on the right panel. '), 
                        'target': 'tags'},
                     {'title': _('Resolve'), 
                        'message': _('Resolve an issue to remove it from your issue list. Sentry can also <a href="/settings/account/notifications/" target="_blank"> alert you</a> when a new issue occurs or a resolved issue re-occurs.'), 
                        'target': 'resolve'},
                     {'title': _('Delete and Ignore'), 
                        'message': _('Delete an issue to remove it from your issue list until it happens again. Ignore an issue to remove it permanently or until certain conditions are met.'), 
                        'target': 'ignore_delete_discard'},
                     {'title': _('Issue Number'), 
                        'message': _('Include this unique identifier in your commit message to have Sentry automatically resolve the issue when your code is deployed. <a href="https://docs.sentry.io/learn/releases/" target="_blank">Learn more</a>.'), 
                        'target': 'issue_number'},
                     {'title': _('Ownership Rules'), 
                        'message': _('Define users or teams responsible for specific file paths or URLs so that alerts can be routed to the right person. <a href="https://docs.sentry.io/learn/issue-owners/" target="_blank">Learn more</a>.'), 
                        'target': 'owners'}]}, 
   'issue_stream': {'id': 3, 
                    'required_targets': [
                                       'issue_stream'], 
                    'steps': [
                            {'title': _('Issues'), 
                               'message': _('Sentry automatically groups similar events together into an issue. Similarity is determined by stacktrace and other factors. <a href="https://docs.sentry.io/data-management/rollups/" target="_blank">Learn more</a>. '), 
                               'target': 'issue_stream'}]}}