# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/hostingsvcs/sourceforge.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import unicode_literals
from django import forms
from django.utils.translation import ugettext_lazy as _
from reviewboard.hostingsvcs.forms import HostingServiceForm
from reviewboard.hostingsvcs.service import HostingService

class SourceForgeForm(HostingServiceForm):
    sourceforge_project_name = forms.CharField(label=_(b'Project name'), max_length=64, required=True, widget=forms.TextInput(attrs={b'size': b'60'}))


class SourceForge(HostingService):
    name = b'SourceForge'
    form = SourceForgeForm
    supports_repositories = True
    supports_bug_trackers = True
    supported_scmtools = [b'Bazaar', b'CVS', b'Mercurial', b'Subversion']
    repository_fields = {b'Bazaar': {b'path': b'bzr://%(sourceforge_project_name)s.bzr.sourceforge.net/bzrroot/%(sourceforge_project_name)s', 
                   b'mirror_path': b'bzr+ssh://%(sourceforge_project_name)s.bzr.sourceforge.net/bzrroot/%(sourceforge_project_name)s'}, 
       b'CVS': {b'path': b':pserver:anonymous@%(sourceforge_project_name)s.cvs.sourceforge.net:/cvsroot/%(sourceforge_project_name)s', 
                b'mirror_path': b'%(sourceforge_project_name)s.cvs.sourceforge.net/cvsroot/%(sourceforge_project_name)s'}, 
       b'Mercurial': {b'path': b'http://%(sourceforge_project_name)s.hg.sourceforge.net:8000/hgroot/%(sourceforge_project_name)s', 
                      b'mirror_path': b'ssh://%(sourceforge_project_name)s.hg.sourceforge.net/hgroot/%(sourceforge_project_name)s'}, 
       b'Subversion': {b'path': b'http://%(sourceforge_project_name)s.svn.sourceforge.net/svnroot/%(sourceforge_project_name)s', 
                       b'mirror_path': b'https://%(sourceforge_project_name)s.svn.sourceforge.net/svnroot/%(sourceforge_project_name)s'}}
    bug_tracker_field = b'http://sourceforge.net/support/tracker.php?aid=%%s'