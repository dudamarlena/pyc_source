# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /rbpowerpack/hostingsvcs/bitbucket_server.py
# Compiled at: 2019-06-17 15:11:31
"""Hosting service for Bitbucket Server."""
from __future__ import unicode_literals
import json, logging, os, tempfile
from datetime import datetime
from django import forms
from django.utils import six
from django.utils.six.moves.urllib.error import HTTPError, URLError
from django.utils.six.moves.urllib.parse import urlencode
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _, ugettext
from reviewboard.hostingsvcs.errors import AuthorizationError, HostingServiceAPIError, HostingServiceError, InvalidPlanError, RepositoryError
from reviewboard.hostingsvcs.forms import HostingServiceForm
from reviewboard.hostingsvcs.service import HostingService
from reviewboard.scmtools.core import Branch, Commit, SCMTool
from reviewboard.scmtools.crypto_utils import decrypt_password, encrypt_password
from reviewboard.scmtools.errors import FileNotFoundError
from rbpowerpack.utils.extension import get_powerpack_extension

class BitbucketServerPersonalForm(HostingServiceForm):
    """Hosting service form for Bitbucket Server personal repos.

    Provides additional fields on top of the base hosting service form.
    """
    bitbucket_server_personal_repo_owner = forms.CharField(label=_(b'Repository owner username'), max_length=128, required=True, widget=forms.TextInput(attrs={b'size': 60}), help_text=_(b'The username of the user owning the repository.'))
    bitbucket_server_personal_repo_name = forms.CharField(label=_(b'Repository name'), max_length=128, required=True, widget=forms.TextInput(attrs={b'size': 60}))

    def clean_bitbucket_server_personal_repo_owner(self):
        """Clean the repository owner username.

        This translates the inputted username into a slug for use with the API.

        Returns:
            unicode:
            The translated name.
        """
        owner = self.cleaned_data[b'bitbucket_server_personal_repo_owner']
        self.cleaned_data[b'bitbucket_server_personal_repo_owner_slug'] = slugify(owner)
        return owner

    def clean_bitbucket_server_personal_repo_name(self):
        """Clean the repository name.

        This translates the inputted repository name into a slug for use with
        the API.

        Returns:
            unicode:
            The translated name.
        """
        repo_name = self.cleaned_data[b'bitbucket_server_personal_repo_name']
        self.cleaned_data[b'bitbucket_server_personal_repo_name_slug'] = slugify(repo_name)
        return repo_name


class BitbucketServerProjectForm(HostingServiceForm):
    """Hosting service form for Bitbucket Server project repos.

    Provides additional fields on top of the base hosting service form.
    """
    bitbucket_server_project_key = forms.CharField(label=_(b'Project key'), max_length=128, required=True, widget=forms.TextInput(attrs={b'size': 60}), help_text=_(b'The project key as configured in the Bitbucket Server project settings.'))
    bitbucket_server_project_repo_name = forms.CharField(label=_(b'Repository name'), max_length=128, required=True, widget=forms.TextInput(attrs={b'size': 60}))

    def clean_bitbucket_server_project_key(self):
        """Clean the project name.

        This translates the inputted project name into a slug for use with the
        API.

        Returns:
            unicode:
            The translated name.
        """
        project_key = self.cleaned_data[b'bitbucket_server_project_key']
        self.cleaned_data[b'bitbucket_server_project_key_slug'] = slugify(project_key)
        return project_key

    def clean_bitbucket_server_project_repo_name(self):
        """Clean the repository name.

        This translates the inputted repository name into a slug for use with
        the API.

        Returns:
            unicode:
            The translated name.
        """
        repo_name = self.cleaned_data[b'bitbucket_server_project_repo_name']
        self.cleaned_data[b'bitbucket_server_project_repo_name_slug'] = slugify(repo_name)
        return repo_name


class BitbucketServer(HostingService):
    """Hosting service for Bitbucket Server.

    Bitbucket Server is a product which provides some similar features to
    Bitbucket, but with an on-premise installation. It's a completely separate
    product from Bitbucket itself (it was an acquisition of "Stash"), and
    therefore doesn't share any code with the regular Bitbucket hosting
    service.
    """
    name = b'Bitbucket Server'
    needs_authorization = True
    supports_bug_trackers = False
    supports_repositories = True
    supports_post_commit = False
    supported_scmtools = [
     b'Git']
    self_hosted = True
    plans = [
     (
      b'project',
      {b'name': _(b'Project Repository'), 
         b'form': BitbucketServerProjectForm, 
         b'repository_fields': {b'Git': {b'path': b'%(hosting_url)s/scm/%(bitbucket_server_project_key_slug)s/%(bitbucket_server_project_repo_name_slug)s.git'}}}),
     (
      b'personal',
      {b'name': _(b'Personal Repository'), 
         b'form': BitbucketServerPersonalForm, 
         b'repository_fields': {b'Git': {b'path': b'%(hosting_url)s/scm/~%(bitbucket_server_personal_repo_owner_slug)s/%(bitbucket_server_personal_repo_name_slug)s.git'}}})]
    DEFAULT_PLAN = b'project'

    def check_repository(self, username, password, plan=DEFAULT_PLAN, *args, **kwargs):
        """Check the validity of a repository.

        This performs a check against the hosting service to ensure that the
        information provided by the user represents a valid repository.

        Args:
            username (unicode):
                The username to use for authentication.

            password (unicode):
                The password to use for authentication.

            plan (unicode, optional):
                The ID of the selected plan.

            *args (tuple):
                Additional positional arguments passed by the caller.

            **kwargs (dict):
                Additional keyword arguments passed by the caller. This
                includes all field data from the HostingServiceForm.

        Raises:
            reviewboard.hostingsvcs.errors.HostingServiceError:
                An error occurred communicating with the hosting service.

            reviewboard.hostingsvcs.errors.RepositoryError:
                An error occurred when trying to verify the repository.
        """
        url = self._build_api_url(self.account.hosting_url, self._get_repository_api_root_raw(plan, kwargs))
        try:
            self._api_get(url)
        except AuthorizationError as e:
            raise RepositoryError(_(b'The repository exists, but the configured user does not have permission to access it: %s') % e.message)
        except HostingServiceError as e:
            if e.http_code == 404:
                raise RepositoryError(_(b'A repository with this name was not found.'))
            raise
        except Exception as e:
            raise RepositoryError(e)

    def authorize(self, username, password, hosting_url, *args, **kwargs):
        """Authorize an account for the hosting service.

        Args:
            username (unicode):
                The username for the account.

            password (unicode):
                The password for the account.

            hosting_url (unicode):
                The hosting URL for the service, if self-hosted.

            *args (tuple):
                Extra unused positional arguments.

            **kwargs (dict):
                Extra keyword arguments containing values from the
                repository's configuration.

        Raises:
            reviewboard.hostingsvcs.errors.AuthorizationError:
                The credentials provided were not valid.

            reviewboard.hostingsvcs.errors.HostingServiceError:
                An error occurred communicating with the hosting service.
        """
        self.account.data[b'password'] = encrypt_password(password)
        try:
            self._api_get(self._build_api_url(hosting_url, b'application-properties'))
            self.account.save()
        except HostingServiceError as e:
            del self.account.data[b'password']
            if e.http_code in (401, 403):
                self._raise_auth_error()
            else:
                raise
        except Exception as e:
            logging.exception(b'Unexpected error when authorizing Bitbucket Server credentials: %s', e)
            del self.account.data[b'password']
            raise HostingServiceError(e)

    def is_authorized(self):
        """Return whether or not the hosting service account is authorized.

        Returns:
            bool:
            True if the account has been successfully authorized.
        """
        return self.account.data.get(b'password') is not None

    def get_file(self, repository, path, revision, base_commit_id=None, *args, **kwargs):
        """Retrieve a file from the repository.

        Args:
            repository (reviewboard.scmtools.models.Repository):
                The repository.

            path (unicode):
                The file path to fetch.

            revision (unicode):
                The revision of the file to fetch.

            base_commit_id (unicode, optional):
                The ID of the commit corresponding to the file revision.

            *args (tuple):
                Additional positional arguments passed by the caller.

            **kwargs (tuple):
                Additional keyword arguments passed by the caller.

        Returns:
            bytes:
            The contents of the file at the given revision.

        Raises:
            reviewboard.scmtools.errors.FileNotFoundError:
                The file did not exist at the given revision.
        """
        if not base_commit_id:
            raise FileNotFoundError(path, revision, detail=_(b'The necessary revision information needed to find this file was not provided. Use RBTools 0.5.2 or newer.'))
        url = self._build_server_url(self.account.hosting_url, b'%s/raw/%s' % (self._get_repository_api_root(repository), path), {b'at': base_commit_id})
        try:
            return self._api_get(url, raw_content=True)
        except FileNotFoundError:
            raise FileNotFoundError(path, revision=revision, base_commit_id=base_commit_id)

    def get_file_exists(self, repository, path, revision, base_commit_id=None, *args, **kwargs):
        """Return whether or not a file exists at a given revision.

        Args:
            repository (reviewboard.scmtools.models.Repository):
                The repository.

            path (unicode):
                The file path to fetch.

            revision (unicode):
                The revision of the file to fetch.

            base_commit_id (unicode, optional):
                The ID of the commit corresponding to the file revision.

            *args (tuple):
                Additional positional arguments passed by the caller.

            **kwargs (tuple):
                Additional keyword arguments passed by the caller.

        Returns:
            bool:
            True if the file exists at the given revision.
        """
        try:
            self.get_file(repository, path, revision, base_commit_id=base_commit_id, *args, **kwargs)
            return True
        except (URLError, HTTPError, FileNotFoundError):
            return False

    def get_branches(self, repository):
        """Return a list of all branches in the repository.

        Args:
            repository (reviewboard.scmtools.models.Repository):
                The repository to list branches on.

        Returns:
            list of reviewboard.scmtools.core.Branch:
            The list of all branches in the repository. One (and only one) of
            these will have the ``default`` field set to True.
        """
        resource = b'%s/branches' % self._get_repository_api_root(repository)
        return [ Branch(id=item[b'displayId'], commit=item[b'latestCommit'], default=item[b'isDefault']) for item in self._api_get_all_pages(resource)
               ]

    def get_commits(self, repository, branch=None, start=None):
        """Return a list of commits backward in history from a given point.

        This can be called multiple times in succession using the "parent"
        field of the last entry as the start parameter in order to paginate
        through the history of commits in the repository.

        Args:
            repository (reviewboard.scmtools.models.Repository):
                The repository to list commits on.

            branch (unicode, optional):
                The branch to list commits on.

            start (unicode, optional):
                An optional starting commit.
        """
        query = {b'limit': 30}
        if start:
            query[b'until'] = start
        commits = []
        data = self._api_get(self._build_api_url(self.account.hosting_url, b'%s/commits' % self._get_repository_api_root(repository), query))
        for item in data[b'values']:
            date = datetime.fromtimestamp(item[b'authorTimestamp'] / 1000.0)
            commits.append(Commit(id=item[b'id'], author_name=item[b'author'][b'name'], date=date.isoformat(), message=item[b'message'], parent=item[b'parents'][0][b'id']))

        return commits

    def get_change(self, repository, revision):
        """Return an individual change.

        Args:
            repository (reviewboard.scmtools.models.Repository):
                The repository to fetch the change from.

            revision (unicode):
                The revision of the change to fetch.

        Returns:
            tuple:
            A 2-tuple, containing the commit message and diff, both unicode
            objects.
        """
        api_root = self._get_repository_api_root(repository)
        commit_data = self._api_get(self._build_api_url(self.account.hosting_url, b'%s/commits/%s' % (api_root, revision)))
        parent_revision = commit_data[b'parents'][0][b'id']
        change_data = self._api_get_all_pages(b'%s/changes' % api_root, {b'since': parent_revision, 
           b'until': revision})
        diff = []
        for change in change_data:
            if change[b'nodeType'] != b'FILE':
                continue
            change_type = change[b'type']
            binary = False
            copied = False
            new_path = b''
            old_path = b''
            new_file = b''
            old_file = b''
            new_version = change[b'contentId']
            old_version = change[b'fromContentId']
            if change_type == b'MODIFY':
                old_path = new_path = change[b'path'][b'toString']
                old_file = self.get_file(repository, old_path, old_version, base_commit_id=parent_revision)
                new_file = self.get_file(repository, new_path, new_version, base_commit_id=revision)
            elif change_type == b'MOVE':
                old_path = change[b'srcPath'][b'toString']
                new_path = change[b'path'][b'toString']
                old_file = self.get_file(repository, old_path, old_version, base_commit_id=parent_revision)
                new_file = self.get_file(repository, new_path, new_version, base_commit_id=revision)
            elif change_type == b'ADD':
                old_path = new_path = change[b'path'][b'toString']
                new_file = self.get_file(repository, new_path, new_version, base_commit_id=revision)
            elif change_type == b'DELETE':
                old_path = new_path = change[b'path'][b'toString']
                old_file = self.get_file(repository, old_path, old_version, base_commit_id=parent_revision)
            else:
                logging.warning(b'Unhandled change type "%s" in Bitbucket Server commit %s', change_type, revision)
                continue
            old_label = b'%s\t%s' % (old_path, old_version)
            new_label = b'%s\t%s' % (new_path, new_version)
            if not binary:
                if old_path != new_path and old_file == new_file:
                    if copied:
                        diff.append(b'Copied from: %s\n' % old_path)
                    diff.append(b'--- %s\n' % old_label)
                    diff.append(b'+++ %s\n' % new_label)
                else:
                    old_tmp = tempfile.NamedTemporaryFile(delete=False)
                    old_tmp.write(old_file)
                    old_tmp.close()
                    new_tmp = tempfile.NamedTemporaryFile(delete=False)
                    new_tmp.write(new_file)
                    new_tmp.close()
                    p = SCMTool.popen([
                     b'diff', b'-u', b'--label', old_label, b'--label',
                     new_label, old_tmp.name, new_tmp.name])
                    unified_diff = p.stdout.read()
                    errmsg = p.stderr.read()
                    rc = p.wait()
                    if rc == 2:
                        logging.error(b'Failed to create unified diff between %s and %s: %s', old_label, new_label, errmsg)
                        binary = True
                    else:
                        if copied:
                            diff.append(b'Copied from: %s\n' % old_path)
                        diff.append(unified_diff)
                os.unlink(old_tmp.name)
                os.unlink(new_tmp.name)
            if binary:
                diff.append(b'--- %s' % old_label)
                diff.append(b'+++ %s' % new_label)
                diff.append(b'Binary files %s and %s differ\n' % (
                 old_path, new_path))

        diff = (b'').join(diff)
        raise NotImplementedError

    def _build_server_url(self, hosting_url, path, query={}):
        """Return the URL for a path on the remote server.

        Args:
            hosting_url (unicode):
                The URL of the Bitbucket Server instance.

            path (unicode):
                The API path (relative to ``/rest/api/1.0/``).

            query (dict, optional):
                Optional query arguments for the request.

        Returns:
            unicode:
            The absolute URL for the API resource.
        """
        if hosting_url.endswith(b'/'):
            hosting_url = hosting_url[:-1]
        url = b'%s/%s' % (hosting_url, path)
        if query:
            url += b'?%s' % urlencode(query)
        return url

    def _build_api_url(self, hosting_url, path, query={}):
        """Return the URL for an API resource.

        Args:
            hosting_url (unicode):
                The URL of the Bitbucket Server instance.

            path (unicode):
                The API path (relative to ``/rest/api/1.0/``).

            query (dict, optional):
                Optional query arguments for the request.

        Returns:
            unicode:
            The absolute URL for the API resource.
        """
        return self._build_server_url(hosting_url, b'rest/api/1.0/%s' % path, query)

    def _raise_auth_error(self, message=None):
        """Raise an authentication error.

        Args:
            message (unicode, optional):
                An optional message to use instead of the default.

        Raises:
            reviewboard.hostingsvcs.errors.AuthorizationError:
                The error to percolate up to the caller.
        """
        raise AuthorizationError(message or ugettext(b'Invalid Bitbucket Server username or password. Make sure you are using your Bitbucket Server username and not e-mail address.'))

    def _api_get_all_pages(self, resource, query={}):
        """Fetch and return all pages in a paginated API.

        Args:
            resource (unicode):
                The API resource to fetch (relative URL).

            query (dict, optional):
                Query arguments.

        Returns:
            list:
            A list containing all the items returned by the API.
        """
        query[b'limit'] = 1000
        query[b'start'] = 0
        results = []
        for i in range(1000):
            data = self._api_get(self._build_api_url(self.account.hosting_url, resource, query))
            results.extend(data[b'values'])
            if data[b'isLastPage']:
                break
            query[b'start'] = data[b'nextPageStart']

        return results

    def _api_get(self, url, raw_content=False):
        """Make a request to the Bitbucket Server API.

        Args:
            url (unicode):
                The URL to fetch.

            raw_content (bool, optional):
                Whether the API endpoint should be returned in raw form or a
                parsed object.

        Returns:
            object:
            Depending on the value of ``raw_content``, this will either be
            ``bytes``, or the parsed JSON content from the API.
        """
        try:
            data, headers = self.client.http_get(url, username=self.account.username, password=decrypt_password(self.account.data[b'password']))
            if raw_content:
                return data
            return json.loads(data)
        except HTTPError as e:
            self._check_api_error(e)

    def _check_api_error(self, e):
        """Translate an error returned by the API.

        Args:
            e (urllib2.HTTPError):
                The error returned by the Bitbucket Server API.

        Raises:
            reviewboard.hostingsvcs.errors.AuthorizationError:
                The supplied credentials were not correct or the user does not
                have access to the given API resource.

            reviewboard.hostingsvcs.errors.HostingServiceAPIError:
                The API resource returned an error.

            reviewboard.scmtools.errors.FileNotFoundError:
                The file was not found (used when fetching raw file sources).
        """
        data = e.read()
        try:
            rsp = json.loads(data)
        except:
            rsp = None

        message = data
        if rsp and b'errors' in rsp:
            error = rsp[b'errors'][0]
            if b'message' in error:
                message = error[b'message']
        if message:
            message = six.text_type(message)
        if e.code == 401:
            self._raise_auth_error(message)
        elif e.code == 404:
            if rsp:
                raise HostingServiceError(message, http_code=e.code)
            else:
                raise FileNotFoundError(b'')
        else:
            raise HostingServiceAPIError(message or ugettext(b'Unexpected HTTP %s error when talking to Bitbucket Server.') % e.code, http_code=e.code, rsp=e)
        return

    def _get_plan(self, repository):
        """Return the plan ID for the given repository.

        Args:
            repository (reviewboard.scmtools.models.Repository):
                The repository.

        Returns:
            unicode:
            The ID of the plan selected for the repository.
        """
        return repository.extra_data.get(b'repository_plan') or self.DEFAULT_PLAN

    def _get_repository_api_root(self, repository):
        """Return the relative API path for a given repository.

        Args:
            repository (reviewboard.scmtools.models.Repository):
                The repository.

        Returns:
            unicode:
            The relative API path to use for the repository.

        Raises:
            reviewboard.hostingsvcs.errors.InvalidPlanError:
                The repository is configured with an invalid plan ID.
        """
        return self._get_repository_api_root_raw(self._get_plan(repository), repository.extra_data)

    def _get_repository_api_root_raw(self, plan, extra_data):
        """Return the relative API path for a given repository.

        Args:
            plan (unicode):
                The ID of the selected plan.

            extra_data (dict):
                The contents of the repository's ``extra_data`` field.

        Returns:
            unicode:
            The relative API path to use for the repository.

        Raises:
            reviewboard.hostingsvcs.errors.InvalidPlanError:
                The repository is configured with an invalid plan ID.
        """
        if plan == b'personal':
            return b'users/%s/repos/%s' % (
             extra_data[b'bitbucket_server_personal_repo_owner_slug'],
             extra_data[b'bitbucket_server_personal_repo_name_slug'])
        if plan == b'project':
            return b'projects/%s/repos/%s' % (
             extra_data[b'bitbucket_server_project_key_slug'],
             extra_data[b'bitbucket_server_project_repo_name_slug'])
        raise InvalidPlanError(plan)

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
        return extension is not None and extension.policy.is_bitbucket_server_enabled(user, repository)