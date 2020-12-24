# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/hostingsvcs/beanstalk.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import unicode_literals
import json, logging, os
from collections import defaultdict
from django import forms
from django.conf.urls import url
from django.http import HttpResponse
from django.utils import six
from django.utils.six.moves.urllib.error import HTTPError, URLError
from django.utils.six.moves.urllib.parse import quote
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.http import require_POST
from reviewboard.admin.server import get_server_url
from reviewboard.hostingsvcs.forms import HostingServiceAuthForm, HostingServiceForm
from reviewboard.hostingsvcs.hook_utils import close_all_review_requests, get_review_request_id
from reviewboard.hostingsvcs.service import HostingService
from reviewboard.scmtools.crypto_utils import decrypt_password, encrypt_password
from reviewboard.scmtools.errors import FileNotFoundError
from reviewboard.scmtools.svn.utils import collapse_svn_keywords, has_expanded_svn_keywords

class BeanstalkAuthForm(HostingServiceAuthForm):
    """Authentication form for the Beanstalk hosting service.

    This replaces some of the help text to make setup a bit easier.
    """

    class Meta:
        labels = {b'hosting_account_password': b'Access token'}
        help_texts = {b'hosting_account_username': _(b'Your Beanstalk username. This is case-sensitive and will not be your Beanstalk e-mail address.'), 
           b'hosting_account_password': _(b'A pre-generated access token used to log into your account via an API. You can generate these on Beanstalk by clicking your name in the top-right of any page, clicking "Access Tokens," and then clicking "Generate a token."')}


class BeanstalkForm(HostingServiceForm):
    beanstalk_account_domain = forms.CharField(label=_(b'Beanstalk account domain'), max_length=64, required=True, widget=forms.TextInput(attrs={b'size': b'60'}), help_text=_(b'This is the <tt>domain</tt> part of <tt>domain.beanstalkapp.com</tt>'))
    beanstalk_repo_name = forms.CharField(label=_(b'Repository name'), max_length=64, required=True, widget=forms.TextInput(attrs={b'size': b'60'}))


class BeanstalkHookViews(object):
    """Container class for hook views."""

    @staticmethod
    @require_POST
    def process_post_receive_hook(request, *args, **kwargs):
        """Close review requests as submitted automatically after a push.

        Args:
            request (django.http.HttpRequest):
                The request from the Beanstalk webhook.

        Returns:
            django.http.HttpResponse:
            The HTTP response.
        """
        try:
            server_url = get_server_url(request=request)
            if b'payload' in request.POST:
                payload = json.loads(request.POST[b'payload'])
                BeanstalkHookViews._close_git_review_requests(payload, server_url)
            else:
                payload = json.loads(request.POST[b'commit'])
                BeanstalkHookViews._close_svn_review_request(payload, server_url)
        except KeyError as e:
            logging.error(b'There is no JSON payload in the POST request.: %s', e)
            return HttpResponse(status=415)
        except ValueError as e:
            logging.error(b'The payload is not in JSON format: %s', e)
            return HttpResponse(status=415)

        return HttpResponse()

    @staticmethod
    def _close_git_review_requests(payload, server_url):
        """Close all review requests for the git repository.

        A git payload may contain multiple commits. If a commit's commit
        message does not contain a review request ID, it closes based on
        it's commit id.

        Args:
            payload (dict):
                The decoded webhook payload.

            server_url (unicode):
                The current server URL.
        """
        review_id_to_commits_map = defaultdict(list)
        branch_name = payload.get(b'branch')
        if not branch_name:
            return review_id_to_commits_map
        commits = payload.get(b'commits', [])
        for commit in commits:
            commit_hash = commit.get(b'id')
            commit_message = commit.get(b'message')
            review_request_id = get_review_request_id(commit_message, server_url, commit_hash)
            commit_entry = b'%s (%s)' % (branch_name, commit_hash[:7])
            review_id_to_commits_map[review_request_id].append(commit_entry)

        close_all_review_requests(review_id_to_commits_map)

    @staticmethod
    def _close_svn_review_request(payload, server_url):
        """Close the review request for an SVN repository.

        The SVN payload contains one commit. If the commit's message does not
        contain a review request ID, this will not close any review requests.

        Args:
            payload (dict):
                The decoded webhook payload.

            server_url (unicode):
                The current server URL.
        """
        review_id_to_commits_map = defaultdict(list)
        commit_message = payload.get(b'message')
        branch_name = payload.get(b'changeset_url', b'SVN Repository')
        revision = b'%s %d' % (b'Revision: ', payload.get(b'revision'))
        review_request_id = get_review_request_id(commit_message, server_url, None)
        commit_entry = b'%s (%s)' % (branch_name, revision)
        review_id_to_commits_map[review_request_id].append(commit_entry)
        close_all_review_requests(review_id_to_commits_map)
        return


class Beanstalk(HostingService):
    """Hosting service support for Beanstalk.

    Beanstalk is a source hosting service that supports Git and Subversion
    repositories. It's available at http://beanstalkapp.com/.
    """
    name = b'Beanstalk'
    needs_authorization = True
    supports_bug_trackers = False
    supports_repositories = True
    supported_scmtools = [b'Git', b'Subversion']
    form = BeanstalkForm
    auth_form = BeanstalkAuthForm
    repository_fields = {b'Git': {b'path': b'git@%(beanstalk_account_domain)s.beanstalkapp.com:/%(beanstalk_account_domain)s/%(beanstalk_repo_name)s.git', 
                b'mirror_path': b'https://%(beanstalk_account_domain)s.git.beanstalkapp.com/%(beanstalk_repo_name)s.git'}, 
       b'Subversion': {b'path': b'https://%(beanstalk_account_domain)s.svn.beanstalkapp.com/%(beanstalk_repo_name)s/'}}
    repository_url_patterns = [
     url(b'^hooks/post-receive/$', BeanstalkHookViews.process_post_receive_hook)]

    def check_repository(self, beanstalk_account_domain=None, beanstalk_repo_name=None, *args, **kwargs):
        """Checks the validity of a repository.

        This will perform an API request against Beanstalk to get
        information on the repository. This will throw an exception if
        the repository was not found, and return cleanly if it was found.
        """
        self._api_get_repository(beanstalk_account_domain, beanstalk_repo_name)

    def authorize(self, username, password, hosting_url, local_site_name=None, *args, **kwargs):
        """Authorizes the Beanstalk repository.

        Beanstalk uses HTTP Basic Auth for the API, so this will store the
        provided password, encrypted, for use in later API requests.
        """
        self.account.data[b'password'] = encrypt_password(password)
        self.account.save()

    def is_authorized(self):
        """Determines if the account has supported authorization tokens.

        This just checks if there's a password set on the account.
        """
        return self.account.data.get(b'password', None) is not None

    def get_password(self):
        """Returns the password for this account.

        This is needed for API calls and for Subversion.
        """
        return decrypt_password(self.account.data[b'password'])

    def get_file(self, repository, path, revision, base_commit_id=None, *args, **kwargs):
        """Fetches a file from Beanstalk.

        This will perform an API request to fetch the contents of a file.

        If using Git, this will expect a base commit ID to be provided.
        """
        try:
            contents = self._api_get_node(repository, path, revision, base_commit_id, contents=True)
        except URLError:
            raise FileNotFoundError(path, revision)

        if repository.tool.name == b'Subversion':
            contents = self._normalize_svn_file_content(repository, contents, path, revision)
        return contents

    def get_file_exists(self, repository, path, revision, base_commit_id=None, *args, **kwargs):
        """Determines if a file exists.

        This will perform an API request to fetch the metadata for a file.

        If using Git, this will expect a base commit ID to be provided.
        """
        try:
            self._api_get_node(repository, path, revision, base_commit_id)
            return True
        except (HTTPError, URLError, FileNotFoundError):
            return False

    def normalize_patch(self, repository, patch, filename, revision):
        """Normalize a diff/patch file before it's applied.

        If working with a Subversion repository, then diffs being put up
        for review may have expanded keywords in them. This may occur if
        the file was diffed against a repository that did not (at that time)
        list those keywords in the ``svn:keywords`` property. We need to
        collapse these down.

        For non-Subversion repositories, the default behavior of the
        repository backend is used.

        Args:
            repository (reviewboard.scmtools.models.Repository):
                The repository the patch is meant to apply to.

            patch (bytes):
                The diff/patch file to normalize.

            filename (unicode):
                The name of the file being changed in the diff.

            revision (unicode):
                The revision of the file being changed in the diff.

        Returns:
            bytes:
            The resulting diff/patch file.
        """
        if repository.tool.name == b'Subversion':
            return self._normalize_svn_file_content(repository, patch, filename, revision)
        else:
            return super(Beanstalk, self).normalize_patch(repository, patch, filename, revision)

    def _normalize_svn_file_content(self, repository, contents, path, revision):
        """Post-process a file pertaining to a Subversion repository.

        This is common code that handles collapsing keywords for files fetched
        from or diffed against a Subversion repository.

        Args:
            repository (reviewboard.scmtools.models.Repository):
                The repository the content is for.

            contents (bytes):
                The file content to normalize.

            path (unicode):
                The path to the file.

            revision (unicode):
                The revision of the file.

        Returns:
            bytes:
            The resulting file.
        """
        if has_expanded_svn_keywords(contents):
            try:
                props = self._api_get_svn_props(repository, path, revision)
            except URLError:
                props = None

            if props and b'svn:keywords' in props:
                contents = collapse_svn_keywords(contents, props[b'svn:keywords'].encode(b'utf-8'))
        return contents

    def _api_get_repository(self, account_domain, repository_name):
        url = self._build_api_url(account_domain, b'repositories/%s.json' % repository_name)
        return self._api_get(url)

    def _api_get_node(self, repository, path, revision, base_commit_id, contents=False):
        is_git = repository.tool.name == b'Git'
        if is_git and (contents or not base_commit_id):
            url_path = b'blob?id=%s&name=%s' % (
             quote(revision), quote(os.path.basename(path)))
            raw_content = True
        else:
            if is_git:
                expected_revision = base_commit_id
            else:
                expected_revision = revision
            url_path = b'node.json?path=%s&revision=%s' % (
             quote(path), quote(expected_revision))
            if contents:
                url_path += b'&contents=true'
            raw_content = False
        url = self._build_api_url(self._get_repository_account_domain(repository), b'repositories/%s/%s' % (
         repository.extra_data[b'beanstalk_repo_name'], url_path))
        result = self._api_get(url, raw_content=raw_content)
        if not raw_content and contents:
            result = result[b'contents'].encode(b'utf-8')
        return result

    def _api_get_svn_props(self, repository, path, revision):
        """Return the SVN properties for a file in the repository.

        This will query for all SVN properties set for a particular file,
        returning them as a dictionary mapping property names to values.

        Args:
            repository (reviewboard.scmtools.models.Repository):
                The Subversion repository containing the file.

            path (unicode):
                The path to the file to retrieve properties for.

            revision (unicode):
                The revision of the file.

        Returns:
            dict:
            A mapping of property names to values.
        """
        url = self._build_api_url(self._get_repository_account_domain(repository), b'repositories/%s/props.json?path=%s&revision=%s' % (
         repository.extra_data[b'beanstalk_repo_name'],
         quote(path), quote(revision)))
        result = self._api_get(url)
        return result.get(b'svn_properties', {})

    def _build_api_url(self, account_domain, url):
        return b'https://%s.beanstalkapp.com/api/%s' % (account_domain, url)

    def _get_repository_account_domain(self, repository):
        return repository.extra_data[b'beanstalk_account_domain']

    def _api_get(self, url, raw_content=False):
        try:
            data, headers = self.client.http_get(url, username=self.account.username, password=self.get_password())
            if raw_content:
                return data
            return json.loads(data)
        except HTTPError as e:
            data = e.read()
            try:
                rsp = json.loads(data)
            except:
                rsp = None

            if rsp and b'errors' in rsp:
                raise Exception((b'; ').join(rsp[b'errors']))
            else:
                raise Exception(six.text_type(e))

        return