# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/hostingsvcs/splat.py
# Compiled at: 2020-02-11 04:03:56
"""Support for Splat as a bug tracker."""
from __future__ import unicode_literals
import logging
from django import forms
from django.utils.translation import ugettext_lazy as _
from reviewboard.hostingsvcs.bugtracker import BugTracker
from reviewboard.hostingsvcs.forms import HostingServiceForm
from reviewboard.hostingsvcs.service import HostingService

class SplatForm(HostingServiceForm):
    """The Splat bug tracker configuration form."""
    splat_org_name = forms.SlugField(label=_(b'Splat Organization Name'), max_length=64, required=True, widget=forms.TextInput(attrs={b'size': 60}))


class Splat(HostingService, BugTracker):
    """The Splat bug tracker.

    Splat is a SaaS bugtracker hosted at https://hellosplat.com. It is owned
    and run by Beanbag, Inc. and is used as the official bug tracker for
    Review Board.
    """
    name = b'Splat'
    form = SplatForm
    bug_tracker_field = b'https://hellosplat.com/s/%(splat_org_name)s/tickets/%%s/'
    supports_bug_trackers = True

    def get_bug_info_uncached(self, repository, bug_id):
        """Return the bug info from the server.

        Args:
            repository (reviewboard.scmtools.model.Repository):
                The repository that is using Splat as a bug tracker.

            bug_id (unicode):
                The bug identifier.

        Returns:
            dict:
            A dictionary of the bug information.
        """
        result = {b'summary': b'', 
           b'description': b'', 
           b'description_text_format': b'', 
           b'status': b''}
        url = b'https://hellosplat.com/api/orgs/%s/tickets/%s/?only-fields=status,summary,text,text_format' % (
         repository.extra_data[b'bug_tracker-splat_org_name'], bug_id)
        try:
            rsp = self.client.json_get(url)[0]
            ticket = rsp[b'ticket']
        except Exception as e:
            logging.warning(b'Unable to fetch Splat data from %s: %s', url, e, exc_info=True)
        else:
            text = ticket[b'text']
            text_format = {b'plain': b'plain', 
               b'markdown': b'markdown', 
               b'html': b'html'}.get(ticket[b'text_format'], b'plain')
            result = {b'description': text, 
               b'description_text_format': text_format, 
               b'status': ticket[b'status'], 
               b'summary': ticket[b'summary']}

        return result