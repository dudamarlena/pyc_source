# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/hostingsvcs/versionone.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import unicode_literals
from django import forms
from django.utils.translation import ugettext_lazy as _
from reviewboard.admin.validation import validate_bug_tracker_base_hosting_url
from reviewboard.hostingsvcs.forms import HostingServiceForm
from reviewboard.hostingsvcs.service import HostingService

class VersionOneForm(HostingServiceForm):
    versionone_url = forms.CharField(label=_(b'VersionOne URL'), max_length=64, required=True, widget=forms.TextInput(attrs={b'size': b'60'}), validators=[
     validate_bug_tracker_base_hosting_url])


class VersionOne(HostingService):
    name = b'VersionOne'
    form = VersionOneForm
    bug_tracker_field = b'%(versionone_url)s/assetdetail.v1?Number=%%s'
    supports_bug_trackers = True