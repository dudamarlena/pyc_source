# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/hostingsvcs/bitbucket.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import unicode_literals
import json, logging
from collections import defaultdict
from django import forms
from django.conf.urls import url
from django.core.cache import cache
from django.http import HttpResponse, HttpResponseBadRequest
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils import six
from django.utils.six.moves.urllib.error import HTTPError, URLError
from django.utils.six.moves.urllib.parse import quote, urlencode
from django.utils.translation import ugettext_lazy as _, ugettext
from django.views.decorators.http import require_POST
from reviewboard.admin.server import build_server_url, get_server_url
from reviewboard.hostingsvcs.errors import AuthorizationError, HostingServiceAPIError, HostingServiceError, InvalidPlanError, RepositoryError
from reviewboard.hostingsvcs.forms import HostingServiceAuthForm, HostingServiceForm
from reviewboard.hostingsvcs.hook_utils import close_all_review_requests, get_repository_for_hook, get_review_request_id
from reviewboard.hostingsvcs.service import HostingService
from reviewboard.scmtools.core import Branch, Commit
from reviewboard.scmtools.crypto_utils import decrypt_password, encrypt_password
from reviewboard.scmtools.errors import FileNotFoundError
from reviewboard.site.urlresolvers import local_site_reverse

class BitbucketAuthForm(HostingServiceAuthForm):

    class Meta(object):
        help_texts = {b'hosting_account_username': _(b'Your Bitbucket username. This must <em>not</em> be your e-mail address! You can find your username in your <a href="https://bitbucket.org/account/admin/">Bitbucket Account Settings</a>.'), 
           b'hosting_account_password': _(b'The password used for your account, or a <a href="https://bitbucket.org/account/admin/app-passwords">configured app password</a>. <strong>Important:</strong> If using two-factor authentication, you <em>must</em> use an app password configured with read access to repositories, accounts, and projects.')}


class BitbucketPersonalForm(HostingServiceForm):
    bitbucket_repo_name = forms.CharField(label=_(b'Repository name'), max_length=64, required=True, widget=forms.TextInput(attrs={b'size': b'60'}), help_text=_(b'The name of the repository. This is the &lt;repo_name&gt; in https://bitbucket.org/&lt;username&gt;/&lt;repo_name&gt;/'))


class BitbucketOtherUserForm(HostingServiceForm):
    bitbucket_other_user_username = forms.CharField(label=_(b'Username'), max_length=64, required=True, widget=forms.TextInput(attrs={b'size': b'60'}), help_text=_(b'The username of the user who owns the repository. This is the &lt;username&gt; in https://bitbucket.org/&lt;username&gt;/&lt;repo_name&gt;/'))
    bitbucket_other_user_repo_name = forms.CharField(label=_(b'Repository name'), max_length=64, required=True, widget=forms.TextInput(attrs={b'size': b'60'}), help_text=_(b'The name of the repository. This is the &lt;repo_name&gt; in https://bitbucket.org/&lt;username&gt;/&lt;repo_name&gt;/'))


class BitbucketTeamForm(HostingServiceForm):
    bitbucket_team_name = forms.CharField(label=_(b'Team name'), max_length=64, required=True, widget=forms.TextInput(attrs={b'size': b'60'}), help_text=_(b'The name of the team. This is the &lt;team_name&gt; in https://bitbucket.org/&lt;team_name&gt;/&lt;repo_name&gt;/'))
    bitbucket_team_repo_name = forms.CharField(label=_(b'Repository name'), max_length=64, required=True, widget=forms.TextInput(attrs={b'size': b'60'}), help_text=_(b'The name of the repository. This is the &lt;repo_name&gt; in https://bitbucket.org/&lt;team_name&gt;/&lt;repo_name&gt;/'))


class BitbucketHookViews(object):
    """Container class for hook views."""

    @staticmethod
    @require_POST
    def post_receive_hook_close_submitted(request, local_site_name=None, repository_id=None, hosting_service_id=None, hooks_uuid=None):
        """Close review requests as submitted automatically after a push.

        Args:
            request (django.http.HttpRequest):
                The request from the Bitbucket webhook.

            local_site_name (unicode, optional):
                The local site name, if available.

            repository_id (int, optional):
                The pk of the repository, if available.

            hosting_service_id (unicode, optional):
                The name of the hosting service.

            hooks_uuid (unicode, optional):
                The UUID of the configured webhook.

        Returns:
            django.http.HttpResponse:
            A response for the request.
        """
        repository = get_repository_for_hook(repository_id=repository_id, hosting_service_id=hosting_service_id, local_site_name=local_site_name, hooks_uuid=hooks_uuid)
        try:
            payload = json.loads(request.body)
        except ValueError as e:
            logging.error(b'The payload is not in JSON format: %s', e)
            return HttpResponseBadRequest(b'Invalid payload format')

        server_url = get_server_url(request=request)
        review_request_id_to_commits = BitbucketHookViews._get_review_request_id_to_commits_map(payload, server_url, repository)
        if review_request_id_to_commits:
            close_all_review_requests(review_request_id_to_commits, local_site_name, repository, hosting_service_id)
        return HttpResponse()

    @classmethod
    def _get_review_request_id_to_commits_map(cls, payload, server_url, repository):
        """Return a mapping of review request ID to a list of commits.

        If a commit's commit message does not contain a review request ID, we
        append the commit to the key None.

        Args:
            payload (dict):
                The decoded webhook payload.

            server_url (unicode):
                The URL of the Review Board server.

            repository (reviewboard.scmtools.models.Repository):
                The repository object.

        Returns:
            dict:
            A mapping from review request ID to a list of matching commits from
            the payload.
        """
        results = defaultdict(list)
        try:
            changes = payload[b'push'][b'changes']
        except KeyError:
            return results

        seen_commits_urls = set()
        for change in changes:
            change_new = change.get(b'new') or {}
            if change_new and change_new[b'type'] not in ('branch', 'named_branch',
                                                          'bookmark'):
                continue
            truncated = change.get(b'truncated', False)
            commits = change.get(b'commits') or []
            target_name = change_new.get(b'name')
            if not target_name or not commits:
                continue
            if truncated:
                try:
                    commits_url = change[b'links'][b'commits'][b'href']
                except KeyError:
                    commits_url = None

                commits = cls._iter_commits(repository.hosting_service, commits_url, seen_commits_urls=seen_commits_urls)
            for commit in commits:
                commit_hash = commit.get(b'hash')
                commit_message = commit.get(b'message')
                branch_name = commit.get(b'branch')
                review_request_id = get_review_request_id(commit_message=commit_message, server_url=server_url, commit_id=commit_hash, repository=repository)
                if review_request_id is not None:
                    results[review_request_id].append(b'%s (%s)' % (target_name, commit_hash[:7]))

        return results

    @classmethod
    def _iter_commits(cls, hosting_service, commits_url, seen_commits_urls, max_pages=5):
        """Iterate through all pages of commits for a URL.

        This will go through each page of commits corresponding to a Push
        event, yielding each commit for further processing.

        Args:
            hosting_service (Bitbucket):
                The hosting service instance.

            commits_url (unicode):
                The beginning URL to page through.

            seen_commits_urls (set):
                The URLs that have already been seen. If a URL from this set
                is encountered, pagination will stop.

            max_pages (int, optional):
                The maximum number of pages to iterate through.

        Yields:
            dict:
            A payload for an individual commit.
        """
        cur_page = 0
        while commits_url and cur_page < max_pages:
            if commits_url in seen_commits_urls:
                break
            seen_commits_urls.add(commits_url)
            commits_rsp = hosting_service.api_get(commits_url)
            for commit_rsp in commits_rsp.get(b'values', []):
                yield commit_rsp

            commits_url = commits_rsp.get(b'next')
            cur_page += 1


class Bitbucket(HostingService):
    """Hosting service support for Bitbucket.

    Bitbucket is a hosting service that supports Git and Mercurial
    repositories, and provides issue tracker support. It's available
    at https://www.bitbucket.org/.
    """
    name = b'Bitbucket'
    auth_form = BitbucketAuthForm
    needs_authorization = True
    supports_repositories = True
    supports_bug_trackers = True
    supports_post_commit = True
    has_repository_hook_instructions = True
    repository_url_patterns = [
     url(b'^hooks/(?P<hooks_uuid>[a-z0-9]+)/close-submitted/$', BitbucketHookViews.post_receive_hook_close_submitted, name=b'bitbucket-hooks-close-submitted')]
    supported_scmtools = [
     b'Git', b'Mercurial']
    plans = [
     (
      b'personal',
      {b'name': _(b'Personal'), 
         b'form': BitbucketPersonalForm, 
         b'repository_fields': {b'Git': {b'path': b'git@bitbucket.org:%(hosting_account_username)s/%(bitbucket_repo_name)s.git', 
                                         b'mirror_path': b'https://%(hosting_account_username)s@bitbucket.org/%(hosting_account_username)s/%(bitbucket_repo_name)s.git'}, 
                                b'Mercurial': {b'path': b'https://%(hosting_account_username)s@bitbucket.org/%(hosting_account_username)s/%(bitbucket_repo_name)s', 
                                               b'mirror_path': b'ssh://hg@bitbucket.org/%(hosting_account_username)s/%(bitbucket_repo_name)s'}}, 
         b'bug_tracker_field': b'https://bitbucket.org/%(hosting_account_username)s/%(bitbucket_repo_name)s/issue/%%s/'}),
     (
      b'other-user',
      {b'name': _(b'Other User'), 
         b'form': BitbucketOtherUserForm, 
         b'repository_fields': {b'Git': {b'path': b'git@bitbucket.org:%(bitbucket_other_user_username)s/%(bitbucket_other_user_repo_name)s.git', 
                                         b'mirror_path': b'https://%(hosting_account_username)s@bitbucket.org/%(bitbucket_other_user_username)s/%(bitbucket_other_user_repo_name)s.git'}, 
                                b'Mercurial': {b'path': b'https://%(hosting_account_username)s@bitbucket.org/%(bitbucket_other_user_username)s/%(bitbucket_other_user_repo_name)s', 
                                               b'mirror_path': b'ssh://hg@bitbucket.org/%(bitbucket_other_user_username)s/%(bitbucket_other_user_repo_name)s'}}, 
         b'bug_tracker_field': b'https://bitbucket.org/%(bitbucket_other_user_username)s/%(bitbucket_other_user_repo_name)s/issue/%%s/'}),
     (
      b'team',
      {b'name': _(b'Team'), 
         b'form': BitbucketTeamForm, 
         b'repository_fields': {b'Git': {b'path': b'git@bitbucket.org:%(bitbucket_team_name)s/%(bitbucket_team_repo_name)s.git', 
                                         b'mirror_path': b'https://%(hosting_account_username)s@bitbucket.org/%(bitbucket_team_name)s/%(bitbucket_team_repo_name)s.git'}, 
                                b'Mercurial': {b'path': b'https://%(hosting_account_username)s@bitbucket.org/%(bitbucket_team_name)s/%(bitbucket_team_repo_name)s', 
                                               b'mirror_path': b'ssh://hg@bitbucket.org/%(bitbucket_team_name)s/%(bitbucket_team_repo_name)s'}}, 
         b'bug_tracker_field': b'https://bitbucket.org/%(bitbucket_team_name)s/%(bitbucket_team_repo_name)s/issue/%%s/'})]
    DEFAULT_PLAN = b'personal'

    def check_repository(self, plan=DEFAULT_PLAN, tool_name=None, *args, **kwargs):
        """Checks the validity of a repository.

        This will perform an API request against Bitbucket to get
        information on the repository. This will throw an exception if
        the repository was not found, and return cleanly if it was found.
        """
        repo_name = self._get_repository_name_raw(plan, kwargs)
        if b'/' in repo_name:
            raise RepositoryError(ugettext(b'Please specify just the name of the repository, not a path.'))
        if b'.git' in repo_name:
            raise RepositoryError(ugettext(b'Please specify just the name of the repository without ".git".'))
        try:
            rsp = self.api_get(self._build_api_url(b'repositories/%s/%s' % (
             self._get_repository_owner_raw(plan, kwargs),
             self._get_repository_name_raw(plan, kwargs)), query={b'fields': b'scm'}))
        except HostingServiceError as e:
            if six.text_type(e) == b'Resource not found':
                raise RepositoryError(ugettext(b'A repository with this name was not found.'))
            raise

        scm = rsp[b'scm']
        if scm == b'git' and tool_name != b'Git' or scm == b'hg' and tool_name != b'Mercurial':
            raise RepositoryError(ugettext(b'The Bitbucket repository being configured does not match the type of repository you have selected.'))

    def authorize(self, username, password, *args, **kwargs):
        """Authorizes the Bitbucket repository.

        Bitbucket supports HTTP Basic Auth or OAuth for the API. We use
        HTTP Basic Auth for now, and we store provided password,
        encrypted, for use in later API requests.
        """
        self.account.data[b'password'] = encrypt_password(password)
        try:
            self.api_get(self._build_api_url(b'user'))
            self.account.save()
        except HostingServiceError as e:
            del self.account.data[b'password']
            if e.http_code in (401, 403):
                self._raise_auth_error()
            else:
                raise
        except Exception:
            del self.account.data[b'password']
            raise

    def is_authorized(self):
        """Determines if the account has supported authorization tokens.

        This just checks if there's a password set on the account.
        """
        return self.account.data.get(b'password', None) is not None

    def get_file(self, repository, path, revision, base_commit_id=None, *args, **kwargs):
        """Fetches a file from Bitbucket.

        This will perform an API request to fetch the contents of a file.

        If using Git, this will expect a base commit ID to be provided.
        """
        try:
            return self._api_get_src(repository, path, revision, base_commit_id)
        except (URLError, HTTPError):
            raise FileNotFoundError(path, revision)

    def get_file_exists(self, repository, path, revision, base_commit_id=None, *args, **kwargs):
        """Determines if a file exists.

        This will perform an API request to fetch the metadata for a file.

        If using Git, this will expect a base commit ID to be provided.
        """
        try:
            self._api_get_file_meta(repository, path, revision, base_commit_id)
            return True
        except (URLError, HTTPError, FileNotFoundError):
            return False

    def get_repository_hook_instructions(self, request, repository):
        """Returns instructions for setting up incoming webhooks."""
        webhook_endpoint_url = build_server_url(local_site_reverse(b'bitbucket-hooks-close-submitted', local_site=repository.local_site, kwargs={b'repository_id': repository.pk, 
           b'hosting_service_id': repository.hosting_account.service_name, 
           b'hooks_uuid': repository.get_or_create_hooks_uuid()}))
        add_webhook_url = b'https://bitbucket.org/%s/%s/admin/addon/admin/bitbucket-webhooks/bb-webhooks-repo-admin' % (
         self._get_repository_owner(repository),
         self._get_repository_name(repository))
        example_id = 123
        example_url = build_server_url(local_site_reverse(b'review-request-detail', local_site=repository.local_site, kwargs={b'review_request_id': example_id}))
        return render_to_string(b'hostingsvcs/bitbucket/repo_hook_instructions.html', RequestContext(request, {b'example_id': example_id, 
           b'example_url': example_url, 
           b'repository': repository, 
           b'server_url': get_server_url(), 
           b'add_webhook_url': add_webhook_url, 
           b'webhook_endpoint_url': webhook_endpoint_url}))

    def _get_default_branch_name(self, repository):
        """Return the name of the repository's default branch.

        Args:
            repository (reviewboard.scmtools.models.Repository):
                The repository whose default branch is to be looked up.

        Returns:
            unicode: The name of the default branch.
        """
        repository_rsp = self.api_get(self._build_repository_api_url(repository, query={b'fields': b'mainbranch.name'}))
        try:
            return repository_rsp[b'mainbranch'][b'name']
        except KeyError:
            return

        return

    def get_branches(self, repository):
        """Return all upstream branches in the repository.

        This will paginate through all the results, 100 entries at a time,
        returning all branches listed in the repository.

        Args:
            repository (reviewboard.scmtools.models.Repository):
                The repository to retrieve branches from.

        Returns:
            list of reviewboard.scmtools.core.Branch:
            The list of branches found in the repository.
        """
        default_branch_name = self._get_default_branch_name(repository)
        found_default_branch = False
        branches = []
        branches_url = self._build_repository_api_url(repository, b'refs/branches', query={b'pagelen': b'100', 
           b'fields': b'values.name,values.target.hash,next'})
        while branches_url:
            branches_rsp = self.api_get(branches_url)
            for branch_info in branches_rsp[b'values']:
                try:
                    branch_name = branch_info[b'name']
                    is_default = branch_name == default_branch_name
                    if is_default:
                        found_default_branch = True
                    branches.append(Branch(id=branch_name, commit=branch_info[b'target'][b'hash'], default=is_default))
                except KeyError as e:
                    logging.error(b'Missing "%s" key in Bitbucket branch definition %r for repository %s. Skipping branch.', e, branch_info, repository.pk)

            branches_url = branches_rsp.get(b'next')

        if not found_default_branch:
            branches[0].default = True
        return branches

    def get_commits(self, repository, branch=None, start=None):
        """Return a page of commits in the repository.

        This will return 20 commits at a time. The list of commits can start
        on a given branch (for branch filtering) or commit (for pagination).

        Args:
            repository (reviewboard.scmtools.models.Repository):
                The repository to retrieve branches from.

            branch (unicode, optional):
                The branch to retrieve commits from.

            start (unicode, optional):
                The first commit to retrieve in the page, for pagination.

        Returns:
            list of reviewboard.scmtools.core.Commit:
            The list of commits found in the repository.
        """
        path = b'commits'
        start = start or branch
        if start:
            path += b'/%s' % start
        url = self._build_repository_api_url(repository, path, query={b'pagelen': 20, 
           b'fields': self._get_commit_fields_query(b'values.')})
        return [ self._build_commit_from_rsp(commit_rsp) for commit_rsp in self.api_get(url)[b'values']
               ]

    def get_change(self, repository, revision):
        commit = cache.get(repository.get_commit_cache_key(revision))
        if not commit:
            commit_rsp = self.api_get(self._build_repository_api_url(repository, b'commit/%s' % revision, query={b'fields': self._get_commit_fields_query()}))
            commit = self._build_commit_from_rsp(commit_rsp)
        diff_url = self._build_repository_api_url(repository, b'diff/%s' % revision)
        diff = self.api_get(diff_url, raw_content=True)
        if not diff.endswith(b'\n'):
            diff += b'\n'
        return Commit(author_name=commit.author_name, id=commit.id, date=commit.date, message=commit.message, diff=diff, parent=commit.parent)

    def _get_commit_fields_query(self, prefix=b''):
        """Return the fields needed in a query string for commit parsing.

        This is needed by APIs that want to limit the fields in the payload
        and need to parse commits.

        Args:
            prefix (unicode, optional):
                An optional prefix for each field.

        Returns:
            unicode:
            The fields to include in a ``?fields=`` query string.
        """
        return (b',').join(prefix + name for name in ('author.raw', 'hash', 'date',
                                                      'message', 'parents.hash'))

    def _build_commit_from_rsp(self, commit_rsp):
        """Return a Commit from an API reesponse.

        This will parse a response from the API and return a structured
        commit.

        Args:
            commit_rsp (dict):
                The API payload for a commit.

        Returns:
            reviewboard.scmtools.core.Commit:
            A commit based on the payload.
        """
        commit = Commit(author_name=commit_rsp[b'author'][b'raw'], id=commit_rsp[b'hash'], date=commit_rsp[b'date'], message=commit_rsp[b'message'])
        if commit_rsp[b'parents']:
            commit.parent = commit_rsp[b'parents'][0][b'hash']
        return commit

    def _build_repository_api_url(self, repository, path=b'', **kwargs):
        """Build an API URL for the given repository.

        This is a wrapper around :py:meth:`_build_api_url` for
        repository-based APIs.

        Args:
            repository (reviewboard.scmtools.models.Repository):
                The repository.

            path (unicode, optional):
                Optional extra path relative to the resource for this
                repository. If left blank, the repository's resource URL
                will be returned.

            **kwargs (dict):
                Extra positional argument to pass to :py:meth:`_build_api_url`.

        Returns:
            unicode:
            The API URL.
        """
        username = self._get_repository_owner(repository)
        repo_name = self._get_repository_name(repository)
        return self._build_api_url((b'repositories/%s/%s/%s' % (
         quote(username), quote(repo_name), path)), **kwargs)

    def _api_get_src(self, repository, path, revision, base_commit_id):
        """Return the source of a file.

        Args:
            repository (reviewboard.scmtools.models.Repository):
                The repository containing the file.

            path (unicode):
                The path to the file.

            revision (unicode):
                The revision of the file.

            base_commit_id (unicode):
                The SHA1 of the commit to fetch the file at. If provided,
                this will take precedence over ``revision``.

                This is needed by Git.

        Returns:
            bytes:
            The contents of the file.

        Raises:
            reviewboard.scmtools.errors.FileNotFoundError:
                The file could not be found.
        """
        if base_commit_id:
            revision = base_commit_id
        else:
            if repository.tool.name == b'Git':
                raise FileNotFoundError(path, revision, detail=b'The necessary revision information needed to find this file was not provided. Use RBTools 0.5.2 or newer.')
            url = self._build_repository_api_url(repository, b'src/%s/%s' % (quote(revision), quote(path)))
            try:
                return self.api_get(url, raw_content=True)
            except FileNotFoundError:
                raise FileNotFoundError(path, revision=revision, base_commit_id=base_commit_id)

    def _api_get_file_meta(self, repository, path, revision, base_commit_id):
        """Return metadata on a file.

        Args:
            repository (reviewboard.scmtools.models.Repository):
                The repository containing the file.

            path (unicode):
                The path to the file.

            revision (unicode):
                The revision of the file.

            base_commit_id (unicode):
                The SHA1 of the commit to fetch the file at. If provided,
                this will take precedence over ``revision``.

                This is needed by Git.

        Returns:
            dict:
            The metadata on the file.

        Raises:
            reviewboard.scmtools.errors.FileNotFoundError:
                The file could not be found.
        """
        if base_commit_id:
            revision = base_commit_id
        else:
            if repository.tool.name == b'Git':
                raise FileNotFoundError(path, revision, detail=b'The necessary revision information needed to find this file was not provided. Use RBTools 0.5.2 or newer.')
            url = b'%s?format=meta' % self._build_repository_api_url(repository, b'src/%s/%s' % (quote(revision), quote(path)))
            try:
                return self.api_get(url)
            except FileNotFoundError:
                raise FileNotFoundError(path, revision=revision, base_commit_id=base_commit_id)

    def _build_api_url(self, path, query={}, version=None):
        """Return the URL for an API.

        By default, this uses the 2.0 API. The version can be overridden
        if another version is needed.

        Args:
            path (unicode):
                The path relative to the root of the API.

            query (dict, optional):
                Optional query arguments for the request.

            version (unicode, optional):
                The optional custom API version to use. If not specified,
                the 2.0 API will be used.

        Returns:
            unicode:
            The absolute URL for the API.
        """
        url = b'https://bitbucket.org/api/%s/%s' % (version or b'2.0', path)
        if query:
            url += b'?%s' % urlencode(query)
        return url

    def _get_repository_plan(self, repository):
        return repository.extra_data.get(b'repository_plan') or self.DEFAULT_PLAN

    def _get_repository_name(self, repository):
        return self._get_repository_name_raw(self._get_repository_plan(repository), repository.extra_data)

    def _get_repository_name_raw(self, plan, extra_data):
        if plan == b'personal':
            return extra_data[b'bitbucket_repo_name']
        if plan == b'team':
            return extra_data[b'bitbucket_team_repo_name']
        if plan == b'other-user':
            return extra_data[b'bitbucket_other_user_repo_name']
        raise InvalidPlanError(plan)

    def _get_repository_owner(self, repository):
        return self._get_repository_owner_raw(self._get_repository_plan(repository), repository.extra_data)

    def _get_repository_owner_raw(self, plan, extra_data):
        if plan == b'personal':
            return self.account.username
        if plan == b'team':
            return extra_data[b'bitbucket_team_name']
        if plan == b'other-user':
            return extra_data[b'bitbucket_other_user_username']
        raise InvalidPlanError(plan)

    def api_get(self, url, raw_content=False):
        try:
            data, headers = self.client.http_get(url, username=self.account.username, password=decrypt_password(self.account.data[b'password']))
            if raw_content:
                return data
            return json.loads(data)
        except HTTPError as e:
            self._check_api_error(e)

    def _check_api_error(self, e):
        data = e.read()
        try:
            rsp = json.loads(data)
        except:
            rsp = None

        message = data
        if rsp and b'error' in rsp:
            error = rsp[b'error']
            if b'message' in error:
                message = error[b'message']
        if message:
            message = six.text_type(message)
        if e.code == 401:
            self._raise_auth_error(message)
        elif e.code == 404:
            if message.startswith(b'Repository'):
                raise HostingServiceError(message, http_code=e.code)
            raise FileNotFoundError(b'')
        else:
            raise HostingServiceAPIError(message or ugettext(b'Unexpected HTTP %s error when talking to Bitbucket') % e.code, http_code=e.code, rsp=e)
        return

    def _raise_auth_error(self, message=None):
        raise AuthorizationError(message or ugettext(b'Invalid Bitbucket username or password. Make sure you are using your Bitbucket username and not e-mail address, and are using an app password if two-factor authentication is enabled.'))