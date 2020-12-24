# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/hostingsvcs/fogbugz.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import unicode_literals
from django import forms
from django.utils.translation import ugettext_lazy as _
from reviewboard.hostingsvcs.forms import HostingServiceForm
from reviewboard.hostingsvcs.service import HostingService

class FogBugzForm(HostingServiceForm):
    fogbugz_account_domain = forms.CharField(label=_(b'Account domain'), max_length=64, required=True, help_text=_(b'The domain used for your FogBugz site, as in https://&lt;domain&gt;.fogbugz.com/'), widget=forms.TextInput(attrs={b'size': b'60'}))


class FogBugz(HostingService):
    """Bug tracker support for FogBugz.

    FogBugz is a bug tracker service provided by Fog Creek. This integration
    supports linking bug numbers to reports on a FogBugz account.
    """
    name = _(b'FogBugz')
    supports_bug_trackers = True
    form = FogBugzForm
    bug_tracker_field = b'https://%(fogbugz_account_domain)s.fogbugz.com/f/cases/%%s'