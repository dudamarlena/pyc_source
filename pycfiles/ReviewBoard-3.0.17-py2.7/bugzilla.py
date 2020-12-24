# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/hostingsvcs/bugzilla.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import unicode_literals
import logging
from django import forms
from django.utils import six
from django.utils.translation import ugettext_lazy as _
from reviewboard.hostingsvcs.bugtracker import BugTracker
from reviewboard.hostingsvcs.forms import HostingServiceForm
from reviewboard.hostingsvcs.service import HostingService
from reviewboard.admin.validation import validate_bug_tracker_base_hosting_url

class BugzillaForm(HostingServiceForm):
    bugzilla_url = forms.CharField(label=_(b'Bugzilla URL'), max_length=64, required=True, widget=forms.TextInput(attrs={b'size': b'60'}), validators=[
     validate_bug_tracker_base_hosting_url])

    def clean_bugzilla_url(self):
        return self.cleaned_data[b'bugzilla_url'].rstrip(b'/')


class Bugzilla(HostingService, BugTracker):
    name = b'Bugzilla'
    form = BugzillaForm
    bug_tracker_field = b'%(bugzilla_url)s/show_bug.cgi?id=%%s'
    supports_bug_trackers = True

    def get_bug_info_uncached(self, repository, bug_id):
        """Get the bug info from the server."""
        bug_id = six.text_type(bug_id)
        result = {b'summary': b'', 
           b'description': b'', 
           b'status': b''}
        try:
            url = b'%s/rest/bug/%s' % (
             repository.extra_data[b'bug_tracker-bugzilla_url'],
             bug_id)
            rsp, headers = self.client.json_get(b'%s?include_fields=summary,status' % url)
            result[b'summary'] = rsp[b'bugs'][0][b'summary']
            result[b'status'] = rsp[b'bugs'][0][b'status']
        except Exception as e:
            logging.warning(b'Unable to fetch bugzilla data from %s: %s', url, e, exc_info=1)

        try:
            url += b'/comment'
            rsp, headers = self.client.json_get(url)
            result[b'description'] = rsp[b'bugs'][bug_id][b'comments'][0][b'text']
        except Exception as e:
            logging.warning(b'Unable to fetch bugzilla data from %s: %s', url, e, exc_info=1)

        return result