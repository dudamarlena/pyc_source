# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/hostingsvcs/kiln.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import unicode_literals
import json
from django import forms
from django.utils import six
from django.utils.six.moves.urllib.error import HTTPError, URLError
from django.utils.translation import ugettext, ugettext_lazy as _
from reviewboard.hostingsvcs.errors import AuthorizationError, HostingServiceError, RepositoryError
from reviewboard.hostingsvcs.forms import HostingServiceForm
from reviewboard.hostingsvcs.service import HostingService, HostingServiceClient
from reviewboard.scmtools.errors import FileNotFoundError

class KilnForm(HostingServiceForm):
    kiln_account_domain = forms.CharField(label=_(b'Account domain'), max_length=64, required=True, help_text=_(b'The domain used for your Kiln site, as in https://&lt;domain&gt;.kilnhg.com/'), widget=forms.TextInput(attrs={b'size': b'60'}))
    kiln_project_name = forms.CharField(label=_(b'Project name'), initial=b'Repositories', max_length=64, required=True, help_text=_(b'The Kiln project name. Defaults to "Repositories".'), widget=forms.TextInput(attrs={b'size': b'60'}))
    kiln_group_name = forms.CharField(label=_(b'Group name'), initial=b'Group', max_length=64, required=True, help_text=_(b'The Kiln group name. Defaults to "Group".'), widget=forms.TextInput(attrs={b'size': b'60'}))
    kiln_repo_name = forms.CharField(label=_(b'Repository name'), max_length=64, required=True, widget=forms.TextInput(attrs={b'size': b'60'}))


class KilnAPIError(HostingServiceError):
    """Represents one or more errors from a Kiln API request.

    Kiln API responses can contain multiple errors, containing both
    string-based error codes and error text. KilnAPIError stores a
    mapping of provided error codes to error text as an 'errors'
    attribute.

    All error text is joined together with '; ' when displaying the error.
    """

    def __init__(self, errors):
        super(KilnAPIError, self).__init__((b'; ').join([ error[b'sError'] for error in errors
                                                        ]))
        self.errors = dict([ (error[b'codeError'], error[b'sError']) for error in errors
                           ])


class KilnClient(HostingServiceClient):
    """Interfaces with the Kiln 1.0 API."""

    def __init__(self, hosting_service):
        super(KilnClient, self).__init__(hosting_service)
        self.account = hosting_service.account

    def get_base_api_url(self):
        return b'https://%s.kilnhg.com/Api/1.0/' % self.account.data[b'kiln_account_domain']

    def login(self, username, password):
        return self.api_post(b'Auth/Login', fields={b'sUser': username, 
           b'sPassword': password})

    def get_projects(self):
        return self.api_get(b'Project')

    def get_raw_file(self, repository_id, path, revision):
        return self.api_get(b'Repo/%s/Raw/File/%s?rev=%s' % (
         repository_id, self._hex_encode(path),
         revision), raw_content=True).encode(b'utf-8')

    def api_delete(self, url, *args, **kwargs):
        try:
            data = self.json_delete(self._build_api_url(url), *args, **kwargs)[0]
            self._check_api_error(data)
            return data
        except (URLError, HTTPError) as e:
            self._check_api_error_from_exception(e)

    def api_get(self, url, raw_content=False, *args, **kwargs):
        try:
            data = self.http_get(self._build_api_url(url), *args, **kwargs)[0]
            if not raw_content:
                data = json.loads(data)
            self._check_api_error(data, raw_content=raw_content)
            return data
        except (URLError, HTTPError) as e:
            self._check_api_error_from_exception(e)

    def api_post(self, url, *args, **kwargs):
        try:
            data = self.json_post(self._build_api_url(url), *args, **kwargs)[0]
            self._check_api_error(data)
            return data
        except (URLError, HTTPError) as e:
            self._check_api_error_from_exception(e)

    def _build_api_url(self, path):
        url = b'%s%s' % (self.get_base_api_url(), path)
        if b'auth_token' in self.account.data:
            if b'?' in path:
                url += b'&'
            else:
                url += b'?'
            url += b'token=%s' % self.account.data[b'auth_token']
        return url

    def _hex_encode(self, s):
        return (b'').join(b'%02X' % ord(x) for x in bytes(s))

    def _check_api_error_from_exception(self, e):
        self._check_api_error(e.read(), raw_content=True)
        raise HostingServiceError(six.text_type(e))

    def _check_api_error(self, rsp, raw_content=False):
        if raw_content:
            try:
                rsp = json.loads(rsp)
            except:
                rsp = None

        if rsp and b'errors' in rsp:
            for error_info in rsp[b'errors']:
                if error_info[b'codeError'] in ('BadAuthentication', 'InvalidToken'):
                    raise AuthorizationError(error_info[b'sError'])

            raise KilnAPIError(rsp[b'errors'])
        return


class Kiln(HostingService):
    """Hosting service support for Kiln On Demand.

    Kiln On Demand supports Git and Mercurial repositories, accessible
    over its API.

    Bug tracker integration is not provided by Kiln. FogBugz is used for
    that purpose instead.
    """
    name = _(b'Kiln On Demand')
    needs_authorization = True
    supports_repositories = True
    supported_scmtools = [b'Git', b'Mercurial']
    form = KilnForm
    client_class = KilnClient
    repository_fields = {b'Git': {b'path': b'https://%(kiln_account_domain)s.kilnhg.com/Code/%(kiln_project_name)s/%(kiln_group_name)s/%(kiln_repo_name)s.git', 
                b'mirror_path': b'ssh://%(kiln_account_domain)s@%(kiln_account_domain)s.kilnhg.com/%(kiln_project_name)s/%(kiln_group_name)s/%(kiln_repo_name)s'}, 
       b'Mercurial': {b'path': b'https://%(kiln_account_domain)s.kilnhg.com/Code/%(kiln_project_name)s/%(kiln_group_name)s/%(kiln_repo_name)s', 
                      b'mirror_path': b'ssh://%(kiln_account_domain)s@%(kiln_account_domain)s.kilnhg.com/%(kiln_project_name)s/%(kiln_group_name)s/%(kiln_repo_name)s'}}

    def check_repository(self, kiln_account_domain=None, kiln_project_name=None, kiln_group_name=None, kiln_repo_name=None, *args, **kwargs):
        """Checks the validity of a repository.

        This will check to see if there's a repository accessible to the
        user matching the provided information. This will throw an exception
        if the repository was not found, and return cleanly if it was found.
        """
        repo_info = self._find_repository_info(kiln_project_name, kiln_group_name, kiln_repo_name)
        if not repo_info:
            raise RepositoryError(ugettext(b'The repository with this project, group, and name was not found. Please verify that the information exactly matches the configuration on Kiln.'))

    def authorize(self, username, password, kiln_account_domain, *args, **kwargs):
        """Authorizes the Kiln repository.

        Kiln requires an authentication request against a login URL,
        and will return an API token on success. This token is stored
        along with the account data. The username and password are not
        stored.
        """
        self.account.data[b'kiln_account_domain'] = kiln_account_domain
        token = self.client.login(username, password)
        self.account.data[b'auth_token'] = token

    def is_authorized(self):
        """Determines if the account is authorized.

        This just checks if there's a token stored on the account.
        """
        return b'auth_token' in self.account.data

    def get_file(self, repository, path, revision, *args, **kwargs):
        """Fetches a file from the repository.

        This will perform an API request to fetch the contents of a file.
        """
        try:
            return self.client.get_raw_file(self._get_repository_id(repository), path, revision)
        except KilnAPIError as e:
            if b'FileNotFound' in e.errors:
                raise FileNotFoundError(path, revision)
            raise

    def get_file_exists(self, *args, **kwargs):
        """Determines if a file exists.

        This will attempt to fetch the file. This will return whether or not
        that was successful.
        """
        try:
            self.get_file(*args, **kwargs)
            return True
        except FileNotFoundError:
            return False

    def _get_repository_id(self, repository):
        """Returns the Kiln repository ID for a repository.

        Kiln requires usage of a repository ID, instead of using the
        provided name. If the ID hasn't already been fetched, this will
        query for the whole project hierarchy and look for the repository.
        If found, the ID will be recorded for future lookup, avoiding
        any expensive checks in the future.
        """
        key = b'kiln_repo_ix'
        if key not in repository.extra_data:
            repo_info = self._find_repository_info(repository.extra_data[b'kiln_project_name'], repository.extra_data[b'kiln_group_name'], repository.extra_data[b'kiln_repo_name'])
            if repo_info:
                repo_id = repo_info[b'ixRepo']
            else:
                repo_id = None
            repository.extra_data[key] = repo_id
            repository.save(update_fields=[b'extra_data'])
        return repository.extra_data[key]

    def _find_repository_info(self, project_name, group_name, repo_name):
        """Finds information on a repository.

        This will query the list of projects and look for a repository
        matching the provided project name, group name, and repository
        name.
        """
        projects = self.client.get_projects()
        for project in projects:
            if project[b'sSlug'] == project_name:
                for group in project[b'repoGroups']:
                    if group[b'sSlug'] == group_name:
                        for repo in group[b'repos']:
                            if repo[b'sSlug'] == repo_name:
                                return repo

        return