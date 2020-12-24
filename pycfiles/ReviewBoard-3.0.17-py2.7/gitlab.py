# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/hostingsvcs/gitlab.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import unicode_literals
import json, logging, re
from django import forms
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.template.loader import render_to_string
from django.utils.six.moves.urllib.error import HTTPError, URLError
from django.utils.six.moves.urllib.parse import quote, quote_plus, urlparse
from django.utils.translation import ugettext_lazy as _, ugettext
from djblets.cache.backend import cache_memoize
from reviewboard.hostingsvcs.errors import AuthorizationError, HostingServiceError, InvalidPlanError, RepositoryError
from reviewboard.hostingsvcs.forms import HostingServiceAuthForm, HostingServiceForm
from reviewboard.hostingsvcs.service import HostingService
from reviewboard.scmtools.crypto_utils import decrypt_password, encrypt_password
from reviewboard.scmtools.errors import FileNotFoundError
from reviewboard.scmtools.core import Branch, Commit

class GitLabAPIVersionError(HostingServiceError):
    """Raised if we cannot determine the API version."""

    def __init__(self, message, causes):
        """Initialize the GitLabAPIVersionError.

        Args:
            message (unicode):
                The exception message.

            causes (list of Exception):
                The underlying exceptions.
        """
        super(GitLabAPIVersionError, self).__init__(message)
        self.causes = causes

    def __repr__(self):
        """Return a representation of the exception.

        Returns:
            unicode:
            A representation of the exception.
        """
        return b'<GitLabAPIVersionError(message=%r, causes=%r)>' % (
         self.message, self.causes)


class GitLabHostingURLWidget(forms.Widget):
    """A custom input widget for selecting a GitLab host.

    The user can choose between gitlab.com-hosted and self-hosted instances of
    GitLab.
    """
    GITLAB = b'https://gitlab.com'
    CUSTOM = b'custom'
    CHOICES = (
     (
      GITLAB, _(b'gitlab.com')),
     (
      CUSTOM, _(b'Custom')))

    def value_from_datadict(self, data, files, name):
        """Extract the value from the form data.

        Args:
            data (dict):
                The form data.

            files (dict):
                The files.

            name (unicode):
                The name of the form field.

        Returns:
            unicode:
            The form value.
        """
        if data:
            return data.get(name)
        return self.GITLAB

    def render(self, name, value, attrs=None):
        """Render the widget.

        Args:
            name (unicode):
                The name of the widget.

            value (unicode):
                The value of the widget.

            attrs (dict, optional):
                Additional attributes to pass to the widget.

        Returns:
            django.util.safestring.SafeText:
            The rendered widget.
        """
        attrs = self.build_attrs(attrs)
        return render_to_string(b'hostingsvcs/gitlab/url_widget.html', {b'attrs': attrs, 
           b'id': attrs.pop(b'id'), 
           b'is_custom': value and value != self.GITLAB, 
           b'name': name, 
           b'value': value or b''})


class GitLabAuthForm(HostingServiceAuthForm):
    """An authentication form for the GitLab hosting service.

    This form allows user to select between gitlab.com and self-hosted
    instances of GitLab.
    """
    hosting_url = forms.CharField(label=_(b'Service URL'), required=True, widget=GitLabHostingURLWidget(attrs={b'size': 30}))
    private_token = forms.CharField(label=_(b'API Token'), required=True, help_text=_(b'Your GitLab API token. In newer versions of GitLab, you can create one under <code>Settings &gt; Access Tokens &gt; Personal Access</code>. This token will need the <code>api</code> scope. In older versions of GitLab, you can find this under <code>Profile Settings &gt; Account &gt; Private Token</code>.'))

    def __init__(self, *args, **kwargs):
        """Initialize the GitLabAuthForm.

        Args:
            *args (tuple):
                Positional arguments to pass to the base class constructor.

            **kwargs (dict):
                Keyword arguments to pass to the base class constructor.
        """
        super(GitLabAuthForm, self).__init__(*args, **kwargs)
        del self.fields[b'hosting_account_password']

    def clean_hosting_url(self):
        """Clean the hosting_url field.

        This method ensures that the URL has a scheme.

        Returns:
            unicode: The URL.

        Raises:
            django.core.exceptions.ValidationError:
                The URL was missing a scheme.
        """
        hosting_url = self.cleaned_data[b'hosting_url']
        result = urlparse(hosting_url)
        if not result.scheme:
            raise ValidationError(_(b'Invalid hosting URL "%(url)s": missing scheme (e.g., HTTP or HTTPS)') % {b'url': hosting_url})
        return hosting_url

    def get_credentials(self):
        """Return the credentials for the form.

        Returns:
            dict:
            A dict containing the values of the ``username`` and
            ``private_token`` fields.
        """
        credentials = {b'username': self.cleaned_data[b'hosting_account_username'], 
           b'private_token': self.cleaned_data[b'private_token']}
        two_factor_auth_code = self.cleaned_data.get(b'hosting_account_two_factor_auth_code')
        if two_factor_auth_code:
            credentials[b'two_factor_auth_code'] = two_factor_auth_code
        return credentials


class GitLabPersonalForm(HostingServiceForm):
    gitlab_personal_repo_name = forms.CharField(label=_(b'Repository name'), max_length=64, required=True, widget=forms.TextInput(attrs={b'size': b'60'}))


class GitLabGroupForm(HostingServiceForm):
    gitlab_group_name = forms.CharField(label=_(b'GitLab group name'), max_length=64, required=True, widget=forms.TextInput(attrs={b'size': b'60'}))
    gitlab_group_repo_name = forms.CharField(label=_(b'Repository name'), max_length=64, required=True, widget=forms.TextInput(attrs={b'size': b'60'}))


class GitLab(HostingService):
    """Hosting service support for GitLab.

    GitLab is a self-installed source hosting service that supports Git
    repositories. It's available at https://gitlab.org/.
    """
    name = b'GitLab'
    COMMITS_PER_PAGE = 20
    self_hosted = True
    needs_authorization = True
    supports_bug_trackers = True
    supports_post_commit = True
    supports_repositories = True
    supported_scmtools = [b'Git']
    LINK_HEADER_RE = re.compile(b'\\<(?P<url>[^\\>]+)\\>; rel="next"')
    auth_form = GitLabAuthForm
    plans = [
     (
      b'personal',
      {b'name': _(b'Personal'), 
         b'form': GitLabPersonalForm, 
         b'repository_fields': {b'Git': {b'path': b'git@%(hosting_domain)s:%(hosting_account_username)s/%(gitlab_personal_repo_name)s.git', 
                                         b'mirror_path': b'%(hosting_url)s/%(hosting_account_username)s/%(gitlab_personal_repo_name)s.git'}}, 
         b'bug_tracker_field': b'%(hosting_url)s/%(hosting_account_username)s/%(gitlab_personal_repo_name)s/issues/%%s'}),
     (
      b'group',
      {b'name': _(b'Group'), 
         b'form': GitLabGroupForm, 
         b'repository_fields': {b'Git': {b'path': b'git@%(hosting_domain)s:%(gitlab_group_name)s/%(gitlab_group_repo_name)s.git', 
                                         b'mirror_path': b'%(hosting_url)s/%(gitlab_group_name)s/%(gitlab_group_repo_name)s.git'}}, 
         b'bug_tracker_field': b'%(hosting_url)s/%(gitlab_group_name)s/%(gitlab_group_repo_name)s/issues/%%s'})]

    def check_repository(self, plan=None, *args, **kwargs):
        """Checks the validity of a repository.

        This will perform an API request against GitLab to get
        information on the repository. This will throw an exception if
        the repository was not found, and return cleanly if it was found.
        """
        self._find_repository_id(plan, self._get_repository_owner(plan, kwargs), self._get_repository_name(plan, kwargs))

    def authorize(self, username, credentials, hosting_url, *args, **kwargs):
        """Authorize the GitLab repository.

        GitLab uses HTTP Basic Auth for the API, so this will store the
        provided password, encrypted, for use in later API requests.

        Args:
            username (unicode):
                The username of the account being linked.

            credentials (dict):
                Authentication credentials.

            hosting_url (unicode):
                The URL of the GitLab server.

            *args (tuple, unused):
                Ignored positional arguments.

            **kwargs (dict, unused):
                Ignored keyword arguments.

        Raises:
            reviewboard.hostingsvcs.errors.AuthorizationError:
                Authorization could not be completed successfully.

            reviewboard.hostingsvcs.errors.HostingServiceError:
                An HTTP or other unexpected error occurred.
        """
        try:
            self._try_api_versions(hosting_url, path=b'/projects?per_page=1', headers={b'PRIVATE-TOKEN': credentials[b'private_token'].encode(b'utf-8')})
        except (AuthorizationError, GitLabAPIVersionError):
            raise
        except HTTPError as e:
            if e.code == 404:
                raise HostingServiceError(ugettext(b'A GitLab server was not found at the provided URL.'))
            else:
                logging.exception(b'Unexpected HTTP error when linking GitLab account for %s: %s', username, e)
                raise HostingServiceError(ugettext(b'Unexpected HTTP error %s.') % e.code)
        except Exception as e:
            logging.exception(b'Unexpected error when linking GitLab account for %s: %s', username, e)
            raise HostingServiceError(ugettext(b'Unexpected error "%s"') % e)

        self.account.data[b'private_token'] = encrypt_password(credentials[b'private_token'])
        self.account.save()

    def is_authorized(self):
        """Determine if the account has supported authorization tokens.

        This checks if we have previously stored a private token for the
        account. It does not validate that the token still works.

        Returns:
            bool:
            Whether or not the account is authorized with GitLab.
        """
        return b'private_token' in self.account.data

    def get_file(self, repository, path, revision, base_commit_id=None, *args, **kwargs):
        """Fetch a file from GitLab.

        This will perform an API request to fetch the contents of a file.

        Args:
            repository (reviewboard.scmtools.models.Repository):
                The repository to fetch the file from.

            path (unicode):
                The file path.

            revision (unicode):
                The SHA1 of the file blob.

            base_commit_id (unicode, optional):
                An optional commit SHA1.

            *args (tuple, unused):
                Ignored positional arguments.

            **kwargs (dict, unused):
                Ignored keyword arguments.

        Returns:
            bytes:
            The file data at the requested revision.

        Raises:
            reviewboard.scmtools.errors.FileNotFoundError:
                The file could not be retrieved.
        """
        try:
            data, headers = self._api_get(repository.hosting_account.hosting_url, self._get_blob_url(repository, path, revision, base_commit_id), raw_content=True)
            return data
        except (HTTPError, URLError):
            raise FileNotFoundError(path, revision)

    def get_file_exists(self, repository, path, revision, base_commit_id=None, *args, **kwargs):
        """Determine if a file exists.

        This will perform an API request to fetch the metadata for a file.

        Args:
            repository (reviewboard.scmtools.models.Repository):
                The repository to fetch the file from.

            path (unicode):
                The file path.

            revision (unicode):
                The SHA1 of the file blob.

            base_commit_id (unicode, optional):
                An optional commit SHA1.

            *args (tuple, unused):
                Ignored positional arguments.

            **kwargs (dict, unused):
                Ignored keyword arguments.

        Returns:
            bool:
            Whether or not the file exists.

        Raises:
            reviewboard.scmtools.errors.AuthorizationError:
                There was an issue with the authorization credentials.

            reviewboard.scmtools.errors.FileNotFoundError:
                The file could not be retrieved.
        """
        try:
            self._api_get(repository.hosting_account.hosting_url, self._get_blob_url(repository, path, revision, base_commit_id), raw_content=True)
            return True
        except (HTTPError, URLError):
            return False

    def get_branches(self, repository):
        """Return a list of branches.

        This will perform an API request to fetch a list of branches.

        Args:
            repository (reviewboard.scmtools.models.Repository):
                The repository to get branches from.

        Returns:
            list of reviewboard.scmtools.core.Branch:
            The branches available.

        Raises:
            reviewboard.scmtools.errors.AuthorizationError:
                There was an issue with the authorization credentials.

            urllib2.HTTPError:
                There was an error communicating with the server.
        """
        repo_api_url = b'%s/repository/branches' % self._get_repo_api_url(repository)
        refs = self._api_get(repository.hosting_account.hosting_url, repo_api_url)[0]
        results = []
        for ref in refs:
            if b'name' in ref:
                name = ref[b'name']
                results.append(Branch(id=name, commit=ref[b'commit'][b'id'], default=name == b'master'))

        return results

    def get_commits(self, repository, branch=None, start=None):
        """Return a list of commits

        This will perform an API request to fetch a list of commits.

        Args:
            repository (reviewboard.scmtools.models.Repository):
                The repository to fetch commits from.

            branch (unicode, optional):
                The branch to fetch commits from. If not provided, the default
                branch will be used.

            start (unicode, optional):
                The commit to start fetching form.

                If provided, this argument will override ``branch``. Otherwise,
                if neither are provided, the default branch will be used.

        Returns:
            list of reviewboard.scmtools.core.Commit:
            The commits from the API.

        Raises:
            reviewboard.scmtools.errors.AuthorizationError:
                There was an issue with the authorization credentials.

            urllib2.HTTPError:
                There was an error communicating with the server.
        """
        page_size = self.COMMITS_PER_PAGE + 1
        repo_api_url = b'%s/repository/commits?per_page=%s' % (
         self._get_repo_api_url(repository),
         page_size)
        if start:
            repo_api_url += b'&ref_name=%s' % start
        else:
            if branch:
                repo_api_url += b'&ref_name=%s' % branch
            commits = self._api_get(repository.hosting_account.hosting_url, repo_api_url)[0]
            results = []
            for idx, item in enumerate(commits):
                commit = self._parse_commit(item)
                if idx > 0:
                    results[(idx - 1)].parent = commit.id
                results.append(commit)

        if len(commits) == page_size:
            results.pop()
        return results

    def get_change(self, repository, revision):
        """Fetch a single commit from GitLab.

        Args:
            repository (reviewboard.scmtools.models.Repository):
                The repository in question.

            revision (unicode):
                The SHA1 hash of the commit to fetch.

        Returns:
            reviewboard.scmtools.core.Commit:
            The commit in question.

        Raises:
            reviewboard.scmtools.errors.AuthorizationError:
                There was an issue with the authorization credentials.

            urllib2.HTTPError:
                There was an error communicating with the server.
        """
        repo_api_url = self._get_repo_api_url(repository)
        private_token = self._get_private_token()
        commit = cache.get(repository.get_commit_cache_key(revision))
        if commit is None:
            commit_api_url = b'%s/repository/commits/%s' % (
             repo_api_url, revision)
            commit_data = self._api_get(repository.hosting_account.hosting_url, commit_api_url)[0]
            commit = self._parse_commit(commit_data)
            commit.parent = commit_data[b'parent_ids'][0]
        hosting_url = self.account.hosting_url
        if not hosting_url.endswith(b'/'):
            hosting_url += b'/'
        path_api_url = b'%s?private_token=%s' % (
         repo_api_url, private_token)
        project = self._api_get(repository.hosting_account.hosting_url, path_api_url)[0]
        path_with_namespace = project[b'path_with_namespace']
        diff_url = b'%s%s/commit/%s.diff?private_token=%s' % (
         hosting_url, path_with_namespace, revision,
         private_token)
        diff, headers = self.client.http_get(diff_url, headers={b'Accept': b'text/plain'})
        diff = diff.rsplit(b'--\nlibgit', 2)[0]
        if not diff.endswith(b'\n'):
            diff += b'\n'
        commit.diff = diff
        return commit

    def _find_repository_id(self, plan, owner, repo_name):
        """Find the ID of a repository matching the given name and owner.

        If the repository could not be found, an appropriate error will be
        raised.

        Args:
            plan (unicode):
                The plan name.

            owner (unicode):
                The name of the owning group or user.

            repo_name (unicode):
                The name of the repository.

        Returns:
            int:
            The ID of the repository.

        Raises:
            reviewboard.scmtools.errors.AuthorizationError:
                There was an issue with the authorization credentials.

            reviewboard.scmtools.errors.RepositoryError:
                The repository could be found or accessed.

            urllib2.HTTPError:
                There was an error communicating with the server.
        """
        if self._get_api_version(self.account.hosting_url) == b'3':
            return self._find_repository_id_v3(plan, owner, repo_name)
        else:
            return self._find_repository_id_v4(plan, owner, repo_name)

    def _find_repository_id_v4(self, plan, owner, repo_name):
        """Find the ID of a repository matching the given name and owner.

        If the repository could not be found, an appropriate error will be
        raised.

        Args:
            plan (unicode):
                The plan name.

            owner (unicode):
                The name of the owning group or user.

            repo_name (unicode):
                The name of the repository.

        Returns:
            int:
            The ID of the repository.

        Raises:
            reviewboard.scmtools.errors.AuthorizationError:
                There was an issue with the authorization credentials.

            reviewboard.scmtools.errors.RepositoryError:
                The repository could be found or accessed.

            urllib2.HTTPError:
                There was an error communicating with the server.
        """
        project = b'%s/%s' % (owner, repo_name)
        try:
            data, headers = self._api_get(self.account.hosting_url, b'projects/%s' % quote_plus(project))
            return data[b'id']
        except HTTPError as e:
            if e.code == 404:
                raise RepositoryError(ugettext(b'A repository with this name was not found, or your user may not own it.'))
            raise

    def _find_repository_id_v3(self, plan, owner, repo_name):
        """Find the ID of a repository matching the given name and owner.

        If the repository could not be found, an appropriate error will be
        raised.

        Args:
            plan (unicode):
                The plan name.

            owner (unicode):
                The name of the owning group or user.

            repo_name (unicode):
                The name of the repository.

        Returns:
            int:
            The ID of the repository.

        Raises:
            reviewboard.scmtools.errors.AuthorizationError:
                There was an issue with the authorization credentials.

            reviewboard.scmtools.errors.RepositoryError:
                The repository could be found or accessed.

            urllib2.HTTPError:
                There was an error communicating with the server.
        """
        if plan == b'personal':
            repositories = self._api_get_repositories()
            for repository_entry in repositories:
                namespace = repository_entry[b'namespace']
                if namespace[b'path'] == owner and repository_entry[b'path'] == repo_name:
                    return repository_entry[b'id']

            raise RepositoryError(ugettext(b'A repository with this name was not found, or your user may not own it.'))
        elif plan == b'group':
            groups = self._api_get_groups()
            for group_entry in groups:
                group_name = group_entry.get(b'full_path', group_entry[b'name'])
                if group_name == owner:
                    group_id = group_entry[b'id']
                    group_data = self._api_get_group(group_id)
                    repositories = group_data[b'projects']
                    for repository_entry in repositories:
                        if repository_entry[b'name'] == repo_name:
                            return repository_entry[b'id']

                    raise RepositoryError(ugettext(b'A repository with this name was not found on this group, or your user may not have access to it.'))

            raise RepositoryError(ugettext(b'A group with this name was not found, or your user may not have access to it.'))
        else:
            raise InvalidPlanError(plan)

    def _api_get_group(self, group_id):
        """Return information about a given group.

        Args:
            group_id (int):
                The ID of the group to fetch repositories for.

        Returns:
            dict:
            Information about the requested group.

        Raises:
            reviewboard.scmtools.errors.AuthorizationError:
                There was an issue with the authorization credentials.

            urllib2.HTTPError:
                There was an error communicating with the server.
        """
        return self._api_get(self.account.hosting_url, b'groups/%s' % group_id)[0]

    def _api_get_groups(self):
        """Return a list of groups the user has access to.

        This will fetch up to 100 groups from GitLab. These are all groups the
        user has any form of access to.

        Returns:
            list of dict:
            The list of group information.

        Raises:
            reviewboard.scmtools.errors.AuthorizationError:
                There was an issue with the authorization credentials.

            urllib2.HTTPError:
                There was an error communicating with the server.
        """
        return self._api_get(self.account.hosting_url, b'groups?per_page=100')[0]

    def _api_get_repositories(self):
        """Return a list of repositories the user has access to.

        These are all repositories the user has any form of access to.

        Returns:
            list of dict:
            A list of the parsed JSON responses.

        Raises:
            reviewboard.scmtools.errors.AuthorizationError:
                There was an issue with the authorization credentials.

            urllib2.HTTPError:
                There was an error communicating with the server.
        """
        return self._api_get_list(self.account.hosting_url, b'projects?per_page=100')

    def _build_api_url(self, hosting_url, path, api_version=None):
        """Build an API URL.

        Args:
            hosting_url (unicode):
                The URL of the GitLab server.

            path (unicode):
                The API path (not including :samp:`/api/v{version}/`) to build
                the URL for.

            api_version (int, optional):
                The version of the API (3 or 4) to build the URL for.

                If not provided, it will be determined via the cache or, if
                uncached, from the server itself.

        Returns:
            unicode:
            The URL.
        """
        if api_version is None:
            api_version = self._get_api_version(hosting_url)
        return b'%s/api/v%s/%s' % (hosting_url.rstrip(b'/'), api_version,
         path.lstrip(b'/'))

    def _get_blob_url(self, repository, path, revision, base_commit_id=None):
        """Return the URL for accessing the contents of a file.

        Args:
            repository (reviewboard.scmtools.models.Repository):
                The repository.

            path (unicode):
                The path to the file.

            revision (unicode):
                The SHA1 of the blob.

            base_commit_id (unicode, optional):
                The SHA1 of the commit to fetch the file at.

                If provided, this will use their standard blob API, which takes
                a commit ID and a file path.

                If not provided, it will try the newer API for accessing based
                on a blob SHA1. This requires a new enough version of GitLab,
                which we unfortunately cannot detect through their API.

        Returns:
            unicode:
            The blob URL.
        """
        repo_api_url = self._get_repo_api_url(repository)
        api_version = self._get_api_version(self.account.hosting_url)
        if api_version == b'3':
            if base_commit_id:
                return b'%s/repository/blobs/%s?filepath=%s' % (
                 repo_api_url, base_commit_id, quote(path))
            else:
                return b'%s/repository/raw_blobs/%s' % (
                 repo_api_url, revision)

        else:
            return b'%s/repository/blobs/%s/raw' % (
             repo_api_url, revision)

    def _get_repo_api_url(self, repository):
        """Return the base URL for a repository's API.

        The first time this is called, it will look up the repository ID
        through the API. This may take time, but only has to be done once
        per repository.

        Args:
            repository (reviewboard.scmtools.models.Repository):
                The repository.

        Returns:
            unicode:
            The URL of the repository.
        """
        return b'projects/%s' % self._get_repository_id(repository)

    def _get_repository_id(self, repository):
        """Return the ID of a repository.

        If the ID is unknown, this will attempt to look up the ID in the
        list of repositories the user has access to. It will then store the
        ID for later requests, to prevent further lookups.

        Args:
            repository (reviewboard.scmtools.models.Repository):
                The repository.

        Returns:
            int:
            The ID of the repository in GitLab.
        """
        key = b'gitlab_project_id'
        if key not in repository.extra_data:
            plan = repository.extra_data[b'repository_plan']
            repository.extra_data[key] = self._find_repository_id(plan, self._get_repository_owner(plan, repository.extra_data), self._get_repository_name(plan, repository.extra_data))
            repository.save()
        return repository.extra_data[key]

    def _get_repository_owner(self, plan, extra_data):
        """Return the owner of a repository.

        Args:
            plan (unicode):
                The plan name. This should be one of either ``'personal'`` or
                ``'group'``.

            extra_data (dict):
                The
                :py:attr:`~reviewboard.scmtools.models.Repository.extra_data`
                attribute.

        Returns:
            unicode:
            The owner of the repository.

            If this is a personal repository, the owner will be the user who
            has linked their account to GitLab.

            If this is a group repository, the owner will be the group name.

        Raises:
              reviewboard.hostingsvcs.errors.InvalidPlanError:
                  Raised when the plan is not a valid choice.
        """
        if plan == b'personal':
            return self.account.username
        if plan == b'group':
            return extra_data[b'gitlab_group_name']
        raise InvalidPlanError(plan)

    def _get_repository_name(self, plan, extra_data):
        """Return the name of the repository.

        Args:
            plan (unicode):
                The repository plan.

            extra_data (dict):
                The ``extra_data`` attribute of the corresponding
                :py:class:`reviewboard.scmtools.models.Repository`.

        Returns:
            unicode:
            The name of the plan.

        Raises:
            reviewboard.hostingsvcs.errors.InvalidPlanError:
                An invalid plan was given.
        """
        if plan == b'personal':
            return extra_data[b'gitlab_personal_repo_name']
        if plan == b'group':
            return extra_data[b'gitlab_group_repo_name']
        raise InvalidPlanError(plan)

    def _get_private_token(self):
        """Return the private token used for authentication.

        Returns:
            unicode:
            The API token.
        """
        return decrypt_password(self.account.data[b'private_token'])

    def _api_get(self, hosting_url=None, path=None, url=None, raw_content=False):
        """Make a request to the GitLab API and return the result.

        If ``hosting_url`` and ``path`` are provided, the API version will be
        deduced from the server. Otherwise, the full URL given in ``url`` will
        be used.

        Args:
            hosting_url (unicode, optional):
                The host of the repository.

            path (unicode, optional):
                The path after :samp:`/api/v{version}`.

            url (unicode, optional):
                If provided, the full URL to retrieve. Passing ``hosting_url``
                and ``path`` should be preferred over this argument.

            raw_content (bool, optional):
                Whether or not to return the raw content (if ``True``) or to
                parse it as JSON (if ``False``).

                Defaults to ``False``.

        Returns:
            object:
            The response.

        Raises:
            reviewboard.scmtools.errors.AuthorizationError:
                There was an issue with the authorization credentials.

            urllib2.HTTPError:
                There was an error communicating with the server.
        """
        if url:
            assert not hosting_url
            if not not path:
                raise AssertionError
            else:
                url = self._build_api_url(hosting_url, path)
            headers = {b'PRIVATE-TOKEN': self._get_private_token()}
            headers[b'Accept'] = raw_content or b'application/json'
        try:
            data, headers = self.client.http_get(url, headers)
            if raw_content:
                return (data, headers)
            return (json.loads(data), headers)
        except HTTPError as e:
            if e.code == 401:
                raise AuthorizationError(ugettext(b'The login or password is incorrect.'))
            raise

    def _api_get_list(self, hosting_url, path):
        """Make a request to a GitLab list API and return the full list.

        If the server provides a "next" link in the headers (GitLab 6.8.0+),
        this will follow that link and fetch all the results. Otherwise, this
        will provide only the first page of results.

        Args:
            hosting_url (unicode):
                The GitLab server URL.

            path (unicode):
                The path to list resource to fetch.

        Returns:
            list of dict:
            The list of all objects retrieved from the path and its subsequent
            pages.

        Raises:
            reviewboard.scmtools.errors.AuthorizationError:
                There was an issue with the authorization credentials.

            urllib2.HTTPError:
                There was an error communicating with the server.
        """
        all_data = []
        url = self._build_api_url(hosting_url, path)
        while url:
            data, headers = self._api_get(url=url)
            all_data += data
            url = None
            for link in headers.get(b'link', b'').split(b', '):
                m = self.LINK_HEADER_RE.match(link)
                if m:
                    url = m.group(b'url')
                    break

        return all_data

    def _get_api_version(self, hosting_url):
        """Return the version of the API supported by the given server.

        This method will cache the result.

        Args:
            hosting_url (unicode):
                The URL of the GitLab server.

        Returns:
            unicode:
            The version of the API as a string.

            It is returned as a string because
            :py:func:`djblets.cache.backend.cache_memoize` does not work on
            integer results.
        """
        headers = {}
        if self.account.data and b'private_token' in self.account.data:
            headers[b'PRIVATE-TOKEN'] = decrypt_password(self.account.data[b'private_token'])
        return cache_memoize(b'gitlab-api-version:%s' % hosting_url, expiration=3600, lookup_callable=lambda : self._try_api_versions(hosting_url, headers=headers, path=b'/projects?per_page=1')[0])

    def _try_api_versions(self, hosting_url, path, http_method=b'get', use_json=False, **request_kwargs):
        """Try different API versions and return the first valid response.

        Args:
            hosting_url (unicode):
                The URL of the GitLab server.

            path (unicode):
                The API path to retrieve, not including
                :samp:`/api/v{version}`.

            http_method (unicode, optional):
                The method to use. Defaults to ``GET``.

            use_json (bool, optional):
                Whether or not to interpret the results as JSON.

            **request_kwargs (dict):
                Additional keyword arguments to pass to the request method.

        Returns:
            tuple:
            A 3-tuple of:

            * The API version (:py:class:`unicode`).
            * The response body (:py:class:`bytes` or :py:class:`dict`).
            * The response headers (:py:class:`dict`).

        Raises:
            reviewboard.scmtools.errors.AuthorizationError:
                There was an issue with the authorization credentials.

            GitLabAPIVersionError:
                The API version could be determined.
        """
        http_method = http_method.lower()
        if use_json:
            method = getattr(self.client, b'json_%s' % http_method)
        else:
            method = getattr(self.client, b'http_%s' % http_method)
        errors = []
        for api_version in ('4', '3'):
            url = self._build_api_url(hosting_url, path, api_version=api_version)
            try:
                rsp, headers = method(url, **request_kwargs)
            except HTTPError as e:
                if e.code == 401:
                    raise AuthorizationError(b'The API token is invalid.')
                errors.append(e)
            except Exception as e:
                errors.append(e)
            else:
                return (
                 api_version, rsp, headers)

        raise GitLabAPIVersionError(ugettext(b'Could not determine the GitLab API version for %(url)s due to an unexpected error (%(errors)s). Check to make sure the URL can be resolved from this server and that any SSL certificates are valid and trusted.') % {b'url': hosting_url, 
           b'errors': errors[0]}, causes=errors)

    def _parse_commit(self, commit_data):
        """Return a Commit object based on data return from the API.

        Args:
            commit_data (dict):
                The data returned from the GitLab API.

        Returns
            reviewboard.scmtools.core.Commit:
            The parsed commit.
        """
        return Commit(author_name=commit_data[b'author_name'], id=commit_data[b'id'], date=commit_data[b'created_at'], message=commit_data.get(b'message', commit_data.get(b'title', b'')))