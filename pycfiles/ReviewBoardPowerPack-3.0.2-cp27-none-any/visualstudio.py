# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /rbpowerpack/hostingsvcs/visualstudio.py
# Compiled at: 2019-06-17 15:11:31
from __future__ import unicode_literals
from django import forms
from django.utils import six
from django.utils.translation import ugettext_lazy as _
from reviewboard.hostingsvcs.errors import AuthorizationError
from reviewboard.hostingsvcs.forms import HostingServiceAuthForm, HostingServiceForm
from reviewboard.hostingsvcs.service import HostingService
from reviewboard.scmtools.crypto_utils import decrypt_password, encrypt_password
from reviewboard.scmtools.errors import AuthenticationError
from reviewboard.scmtools.models import Tool
from rbpowerpack.utils.extension import get_powerpack_extension

class VisualStudioTeamServicesAuthForm(HostingServiceAuthForm):
    """Authentication form for VisualStudio.com."""

    class Meta(object):
        ALT_CREDENTIALS_HELP_URL = b'https://www.reviewboard.org/docs/powerpack/latest/powerpack/manual/visualstudio/#configuring-alternate-authentication-credentials'
        help_texts = {b'hosting_account_username': _(b'The "alternate credentials" username configured for your account. See <a href="%s">Configuring Alternate Authentication Credentials</a>.') % ALT_CREDENTIALS_HELP_URL, 
           b'hosting_account_password': _(b'The "alternate credentials" password configured for your account. See <a href="%s">Configuring Alternate Authentication Credentials</a>.') % ALT_CREDENTIALS_HELP_URL}


class VisualStudioTeamServicesForm(HostingServiceForm):
    """Form for VisualStudio.com hosted repositories."""
    vso_account_name = forms.CharField(label=_(b'VisualStudio.com account name'), max_length=64, required=True, widget=forms.TextInput(attrs={b'size': b'60'}), help_text=_(b'Your account name on VisualStudio.com. This is the &lt;account&gt; part of your Team Services URL: https://&lt;account&gt;.visualstudio.com/'))
    vso_project_name = forms.CharField(label=_(b'VisualStudio.com project name'), max_length=64, required=False, widget=forms.TextInput(attrs={b'size': b'60'}), help_text=_(b'Your project name on VisualStudio.com. This is only required for Git repositories.'))
    vso_repository_name = forms.CharField(label=_(b'VisualStudio.com repository name'), max_length=64, required=False, widget=forms.TextInput(attrs={b'size': b'60'}), help_text=_(b'Your repository name on VisualStudio.com. This is only required for Git repositories.'))

    def save(self, repository):
        """Save the VSO repository.

        Args:
            repository (reviewboard.scmtools.models.Repository):
                The repository being saved.
        """
        super(VisualStudioTeamServicesForm, self).save(repository)
        repository.extra_data[b'tfs_use_basic_auth'] = True
        repository.extra_data[b'tfs_api_path'] = VisualStudioTeamServices.build_api_path(repository.extra_data[b'vso_account_name'])


class VisualStudioTeamServices(HostingService):
    """Hosting Service for VisualStudio.com."""
    name = b'VisualStudio.com'
    needs_authorization = True
    supports_bug_trackers = False
    supports_post_commit = True
    supports_repositories = True
    supported_scmtools = [
     b'Team Foundation Server',
     b'Team Foundation Server (git)']
    form = VisualStudioTeamServicesForm
    auth_form = VisualStudioTeamServicesAuthForm
    repository_fields = {b'Team Foundation Server': {b'path': b'https://%(vso_account_name)s.visualstudio.com/defaultcollection'}, 
       b'Team Foundation Server (git)': {b'path': b'https://%(vso_account_name)s.visualstudio.com/DefaultCollection/%(vso_project_name)s/_git/%(vso_repository_name)s'}}

    @classmethod
    def build_api_path(self, vso_account_name):
        """Return the API path for a VisualStudio.com account.

        Args:
            vso_account_name (unicode):
                The account name.

        Returns:
            unicode:
            The API path.
        """
        return b'https://%s.visualstudio.com/DefaultCollection/' % vso_account_name

    def check_repository(self, path, username, password, scmtool_class, local_site_name, vso_account_name=None, *args, **kwargs):
        """Check the validity of a repository hosted on VSO.

        Args:
            path (six.text_type):
                The repository path.

            username (six.text_type):
                The username used for authenticating.

            password (six.text_type):
                The password used for authenticating.

            scmtool_class (type):
                The SCMTool for the repository.

            local_site_name (six.text_type):
                The name of the local site, if any.

            vso_account_name (unicode):
                The VisualStudio.com account name.

            *args (tuple):
                Additional arguments.

            **kwargs (dict):
                Additional keyword arguments.

        Raises:
            reviewboard.scmtools.errors.AuthenticationError:
                The login credentials are incorrect.

            reviewboard.scmtools.errors.RepositoryNotFoundError:
                The repository was not found with the given path.

            reviewboard.scmtools.errors.SCMError:
                Some other error occurred.
        """
        username = self.account.username
        password = self.get_password()
        scmtool_class.check_repository(path=path, username=username, password=password, local_site_name=local_site_name, use_basic_auth=True, tfs_api_path=self.build_api_path(vso_account_name))

    def authorize(self, username, password, vso_account_name=None, local_site_name=None, *args, **kwargs):
        """Authorize the account.

        Args:
            username (unicode):
                The username for authentication.

            password (unicode):
                The password for authentication.

            vso_account_name (unicode):
                The team account name for VisualStudio.com. This is the
                subdomain.

            local_site_name (unicode, optional):
                The Local Site used for the repository.

            *args (tuple):
                Additional arguments (unused).

            **kwargs (dict):
                Additional keyword arguments (unused).
        """
        try:
            tool_name = b'Team Foundation Server'
            tool = Tool.objects.get(name=tool_name)
            scmtool_class = tool.get_scmtool_class()
            api_path = self.build_api_path(vso_account_name)
            path = self.repository_fields[tool_name][b'path'] % {b'vso_account_name': vso_account_name}
            scmtool_class.check_repository(path=path, username=username, password=password, local_site_name=local_site_name, use_basic_auth=True, tfs_api_path=api_path)
        except AuthenticationError as e:
            raise AuthorizationError(six.text_type(e))

        self.account.data[b'password'] = encrypt_password(password)
        self.account.save()

    def is_authorized(self):
        """Return whether the account has a password set.

        Returns:
            bool:
            ``True`` if a password is set, or ``False`` if one has not yet been
            set.
        """
        return self.account.data.get(b'password') is not None

    def get_password(self):
        """Return the password for this account.

        Returns:
            six.text_type:
            The decrypted password.
        """
        try:
            return decrypt_password(self.account.data[b'password'])
        except KeyError:
            return

        return

    def get_branches(self, repository):
        """Return a list of all branches in the repository.

        Args:
            repository (reviewboard.scmtools.models.Repository):
                The repository.

        Returns:
            list of :py:class:`reviewboard.scmtools.core.Branch`:
            The branches in the repository.
        """
        return repository.get_scmtool().get_branches()

    def get_commits(self, repository, branch=None, start=None):
        """Return a list of commits given a starting point.

        This is basically a log operation. It returns a page of commits going
        backward in time from a given starting point (usually a branch tip).

        Args:
            repository (reviewboard.scmtools.models.Repository):
                The repository.

            branch (unicode):
                The branch name to log, if any.

            start (unicode):
                The ID of the commit to start logging from.

        Returns:
            list of :py:class:`reviewboard.scmtools.core.Commit`:
            A subset of the commits in the repository.
        """
        return repository.get_scmtool().get_commits(branch, start)

    def get_change(self, repository, revision):
        """Return an individual change.

        Args:
            repository (reviewboard.scmtools.models.Repository):
                The repository.

            revision (reviewboard.scmtools.core.Revision):
                The ID of the commit to return.

        Returns:
            reviewboard.scmtools.core.Commit:
            The commit, including the diff.
        """
        return repository.get_scmtool().get_change(revision)

    def can_user_post(self, user, repository):
        """Return whether a user can post against the given repository.

        This will check the extension's policy to ensure that the user
        is permitted to post.

        Args:
            user (django.contrib.auth.models.User):
                The user to check.

            repository (reviewboard.scmtools.models.Repository):
                The repository to check.

        Returns:
            bool:
            ``True`` if the user is allowed to post a change against the given
            repository. ``False``, otherwise.
        """
        extension = get_powerpack_extension()
        return extension is not None and extension.policy.is_visual_studio_team_services_enabled(user, repository)