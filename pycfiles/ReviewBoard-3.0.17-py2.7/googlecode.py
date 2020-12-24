# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/hostingsvcs/googlecode.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import unicode_literals
from django import forms
from django.utils.translation import ugettext_lazy as _
from reviewboard.hostingsvcs.forms import HostingServiceForm
from reviewboard.hostingsvcs.service import HostingService

class GoogleCodeForm(HostingServiceForm):
    googlecode_project_name = forms.CharField(label=_(b'Project name'), max_length=64, required=True, widget=forms.TextInput(attrs={b'size': b'60'}))


class GoogleCode(HostingService):
    """Hosting service support for Google Code.

    This was a hosting service for Mercurial and Subversion provided by
    Google, and the original home of Review Board. This service was retired
    on January 15, 2016.

    Deprecated:
        3.0.17:
        This service will no longer appear as an option when configuring a
        repository.
    """
    name = b'Google Code'
    visible = False
    form = GoogleCodeForm
    supported_scmtools = [b'Mercurial', b'Subversion']
    supports_repositories = True
    supports_bug_trackers = True
    repository_fields = {b'Mercurial': {b'path': b'http://%(googlecode_project_name)s.googlecode.com/hg', 
                      b'mirror_path': b'https://%(googlecode_project_name)s.googlecode.com/hg'}, 
       b'Subversion': {b'path': b'http://%(googlecode_project_name)s.googlecode.com/svn', 
                       b'mirror_path': b'https://%(googlecode_project_name)s.googlecode.com/svn'}}
    bug_tracker_field = b'http://code.google.com/p/%(googlecode_project_name)s/issues/detail?id=%%s'