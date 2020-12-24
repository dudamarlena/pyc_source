# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/hostingsvcs/gitorious.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import unicode_literals
from django import forms
from django.utils.translation import ugettext_lazy as _
from reviewboard.hostingsvcs.forms import HostingServiceForm
from reviewboard.hostingsvcs.service import HostingService

class GitoriousForm(HostingServiceForm):
    gitorious_project_name = forms.CharField(label=_(b'Project name'), max_length=64, required=True, widget=forms.TextInput(attrs={b'size': b'60'}))
    gitorious_repo_name = forms.CharField(label=_(b'Repository name'), max_length=64, required=True, widget=forms.TextInput(attrs={b'size': b'60'}))


class Gitorious(HostingService):
    name = b'Gitorious'
    form = GitoriousForm
    supported_scmtools = [b'Git']
    supports_repositories = True
    self_hosted = True
    repository_fields = {b'Git': {b'path': b'git://%(hosting_domain)s/%(gitorious_project_name)s/%(gitorious_repo_name)s.git', 
                b'mirror_path': b'%(hosting_url)s/%(gitorious_project_name)s/%(gitorious_repo_name)s.git', 
                b'raw_file_url': b'%(hosting_url)s/%(gitorious_project_name)s/%(gitorious_repo_name)s/blobs/raw/<revision>'}}