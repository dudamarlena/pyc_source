# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/hostingsvcs/fedorahosted.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import unicode_literals
from django import forms
from django.utils.translation import ugettext_lazy as _
from reviewboard.hostingsvcs.forms import HostingServiceForm
from reviewboard.hostingsvcs.service import HostingService

class FedoraHostedForm(HostingServiceForm):
    fedorahosted_repo_name = forms.CharField(label=_(b'Repository name'), max_length=64, required=True, widget=forms.TextInput(attrs={b'size': b'60'}))


class FedoraHosted(HostingService):
    """Hosting service support for fedorahosted.org.

    This was a hosting service for Git, Mercurial, and Subversion provided
    by Fedora. This service was retired on March 1st, 2017.

    Deprecated:
        3.0.17:
        This service will no longer appear as an option when configuring a
        repository.
    """
    name = b'Fedora Hosted'
    visible = False
    form = FedoraHostedForm
    supports_repositories = True
    supports_bug_trackers = True
    supported_scmtools = [b'Git', b'Mercurial', b'Subversion']
    repository_fields = {b'Git': {b'path': b'git://git.fedorahosted.org/git/%(fedorahosted_repo_name)s.git', 
                b'raw_file_url': b'http://git.fedorahosted.org/cgit/%(fedorahosted_repo_name)s.git/blob/<filename>?id=<revision>'}, 
       b'Mercurial': {b'path': b'http://hg.fedorahosted.org/hg/%(fedorahosted_repo_name)s/', 
                      b'mirror_path': b'https://hg.fedorahosted.org/hg/%(fedorahosted_repo_name)s/'}, 
       b'Subversion': {b'path': b'http://svn.fedorahosted.org/svn/%(fedorahosted_repo_name)s/', 
                       b'mirror_path': b'https://svn.fedorahosted.org/svn/%(fedorahosted_repo_name)s/'}}
    bug_tracker_field = b'https://fedorahosted.org/%(fedorahosted_repo_name)s/ticket/%%s'