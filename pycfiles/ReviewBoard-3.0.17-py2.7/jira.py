# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/hostingsvcs/jira.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import unicode_literals, absolute_import
import logging
from django import forms
from django.utils.translation import ugettext_lazy as _
try:
    from jira.client import JIRA as JIRAClient
    from jira.exceptions import JIRAError
    has_jira = True
except ImportError:
    has_jira = False

from reviewboard.admin.validation import validate_bug_tracker_base_hosting_url
from reviewboard.hostingsvcs.bugtracker import BugTracker
from reviewboard.hostingsvcs.forms import HostingServiceForm
from reviewboard.hostingsvcs.service import HostingService

class JIRAForm(HostingServiceForm):
    jira_url = forms.CharField(label=_(b'JIRA URL'), max_length=64, required=True, widget=forms.TextInput(attrs={b'size': b'60'}), validators=[
     validate_bug_tracker_base_hosting_url])

    def clean_jira_url(self):
        return self.cleaned_data[b'jira_url'].rstrip(b'/ ')


class JIRA(HostingService, BugTracker):
    name = b'JIRA'
    form = JIRAForm
    bug_tracker_field = b'%(jira_url)s/browse/%%s'
    supports_bug_trackers = True

    def __init__(self, account):
        super(JIRA, self).__init__(account)
        self.jira_client = None
        return

    def get_bug_info_uncached(self, repository, bug_id):
        """Get the bug info from the server."""
        result = {b'summary': b'', 
           b'description': b'', 
           b'status': b''}
        if has_jira:
            if not self.jira_client:
                try:
                    self.jira_client = JIRAClient(options={b'server': repository.extra_data[b'bug_tracker-jira_url']})
                except ValueError as e:
                    logging.warning(b'Unable to initialize JIRAClient for server %s: %s' % (
                     repository.extra_data[b'bug_tracker-jira_url'], e))
                    return result

            try:
                jira_issue = self.jira_client.issue(bug_id)
                result = {b'description': jira_issue.fields.description, 
                   b'summary': jira_issue.fields.summary, 
                   b'status': jira_issue.fields.status}
            except JIRAError as e:
                logging.warning(b'Unable to fetch JIRA data for issue %s: %s', bug_id, e, exc_info=1)

        return result