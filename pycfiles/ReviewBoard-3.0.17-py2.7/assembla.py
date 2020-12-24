# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/hostingsvcs/assembla.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import unicode_literals
from django import forms
from django.utils.translation import ugettext_lazy as _
from reviewboard.admin.server import get_hostname
from reviewboard.hostingsvcs.forms import HostingServiceForm
from reviewboard.hostingsvcs.service import HostingService
from reviewboard.scmtools.crypto_utils import decrypt_password, encrypt_password

class AssemblaForm(HostingServiceForm):
    assembla_project_id = forms.CharField(label=_(b'Project ID'), max_length=64, required=True, widget=forms.TextInput(attrs={b'size': b'60'}), help_text=_(b"The project ID, as shown in the URL (https://www.assembla.com/spaces/<b>&lt;project_id&gt;</b>), or your Perforce repository's Depot Host."))

    def save(self, repository):
        """Save the Assembla repository form.

        This will force the Perforce host and ticket authentication settings
        to values required for Assembla.

        Args:
            repository (reviewboard.scmtools.models.Repository):
                The repository being saved.
        """
        super(AssemblaForm, self).save(repository)
        if repository.get_scmtool().name == b'Perforce':
            project_id = self.cleaned_data[b'assembla_project_id']
            client_name = Assembla.make_p4_client_name(project_id)
            repository.extra_data.update({b'use_ticket_auth': True, 
               b'p4_host': project_id, 
               b'p4_client': client_name})


class Assembla(HostingService):
    """Hosting service support for Assembla.com.

    Assembla is a hosting service that offers, amongst other features,
    Perforce, Subversion, and Git repository support.

    They do not have much of an API that we can take advantage of, so it's
    impossible for us to support Git. However, Perforce and Subversion work.
    """
    name = b'Assembla'
    needs_authorization = True
    supports_bug_trackers = True
    supports_repositories = True
    supported_scmtools = [b'Perforce', b'Subversion']
    form = AssemblaForm
    repository_fields = {b'Perforce': {b'path': b'perforce.assembla.com:1666'}, 
       b'Subversion': {b'path': b'https://subversion.assembla.com/svn/%(assembla_project_id)s/'}}
    bug_tracker_field = b'https://www.assembla.com/spaces/%(assembla_project_id)s/tickets/%%s'

    @classmethod
    def make_p4_client_name(cls, project_id):
        """Return a new P4CLIENT value from the hostname and project ID.

        The client name will consist of the Review Board server's hostname
        and a sanitized version of the project ID.

        Args:
            project_id (unicode):
                The project ID provided by Assembla. This is equivalent to the
                P4HOST value for Perforce.

        Returns:
            unicode:
            A new Perforce client name.
        """
        return b'%s-%s' % (get_hostname(), project_id.replace(b'/', b'-'))

    def check_repository(self, path, username, password, scmtool_class, local_site_name, assembla_project_id=None, *args, **kwargs):
        """Check the validity of a repository hosted on Assembla.

        Perforce repositories are handled specially. The Assembla project ID
        will be used as the Perforce host, which is needed to tell Assembla
        which repository on the server to use.

        Args:
            path (unicode):
                The repository path.

            username (unicode):
                The username used for authenticating.

            password (unicode):
                The password used for authenticating.

            scmtool_class (type):
                The SCMTool for the repository.

            local_site_name (unicode):
                The name of the Local Site, if any.

            assembla_project_id (unicode):
                The project ID for the Assembla team.

            *args (tuple):
                Additional arguments to pass to the superclass.

            **kwargs (dict):
                Additional keyword arguments to pass to the superclass.
        """
        username = self.account.username
        password = self.get_password()
        if scmtool_class.name == b'Perforce':
            scmtool_class.check_repository(path=path, username=username, password=password, local_site_name=local_site_name, p4_host=assembla_project_id, p4_client=self.make_p4_client_name(assembla_project_id))
        else:
            super(Assembla, self).check_repository(path=path, username=username, password=password, local_site_name=local_site_name, scmtool_class=scmtool_class, **kwargs)

    def authorize(self, username, password, *args, **kwargs):
        """Authorize the Assembla account.

        For Assembla, we simply use the native SCMTool support, as there's
        no useful API available. We just store the password encrypted, which
        will be used by the SCMTool.

        Args:
            username (unicode):
                The username for authentication.

            password (unicode):
                The password for authentication.

            *args (tuple):
                Additional arguments.

            **kwargs (dict):
                Additional keyword arguments.
        """
        self.account.data[b'password'] = encrypt_password(password)
        self.account.save()

    def is_authorized(self):
        """Return if the account has a password set.

        Returns:
            bool:
            ``True`` if a password is set, or ``False`` if one has not yet
            been set.
        """
        return self.account.data.get(b'password') is not None

    def get_password(self):
        """Return the password for this account.

        This is needed for Perforce and Subversion.

        Returns:
            unicode:
            The stored password for the account.
        """
        return decrypt_password(self.account.data[b'password'])

    @classmethod
    def get_repository_fields(cls, tool_name=None, *args, **kwargs):
        """Return values for the fields in the repository form.

        This forces the encoding value to "utf8" on Perforce, which is needed
        by Assembla.

        Args:
            tool_name (unicode):
                The name of the SCMTool for the repository.

            *args (tuple):
                Additional arguments.

            **kwargs (dict):
                Additional keyword arguments.

        Returns:
            dict:
            The resulting repository field values.
        """
        data = super(Assembla, cls).get_repository_fields(tool_name=tool_name, *args, **kwargs)
        if tool_name == b'Perforce':
            data[b'encoding'] = b'utf8'
        return data