# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /rbpowerpack/scmtools/tfs_git.py
# Compiled at: 2019-06-17 15:11:31
from __future__ import unicode_literals
import logging, os, posixpath, tempfile
from django.core.cache import cache
from django.utils.translation import ugettext_lazy as _
from django.utils.six.moves.urllib.error import HTTPError
from django.utils.six.moves.urllib.parse import unquote, urlparse
from djblets.cache.backend import make_cache_key
from reviewboard.scmtools.core import Branch, Commit, SCMTool, PRE_CREATION
from reviewboard.scmtools.errors import AuthenticationError, FileNotFoundError, RepositoryNotFoundError, SCMError
from reviewboard.scmtools.git import GitDiffParser, ShortSHA1Error
from rbpowerpack.scmtools.base import PowerPackSCMToolMetaClass
from rbpowerpack.scmtools.tfs import TFSClient
from rbpowerpack.utils.extension import get_powerpack_extension

class TFSGitClient(TFSClient):
    """Client for Team Foundation Server git repositories.

    This uses the REST API (available in Visual Studio 2013 and Visual Studio
    Team Services) to communicate with Team Foundation Server git repositories.
    """
    FULL_SHA1_LENGTH = 40

    def __init__(self, path, repo_id=None, username=None, password=None, api_path=None, *args, **kwargs):
        """Initialize the client."""
        if b'_git/' not in path:
            raise SCMError(_(b'The given path does not appear to be a TFS Git clone URL.'))
        self.clone_path = path
        self.repo_id = repo_id
        self.username = username
        self.password = password
        self.collection_path = path.split(b'_git/', 1)[0]
        super(TFSGitClient, self).__init__(self.collection_path, username=username, password=password, *args, **kwargs)
        self.path = api_path
        if not self.use_basic_auth and api_path:
            self.password_manager.add_password(None, api_path, self.username, self.password)
        return

    def check_repository(self):
        """Check the repository to see if it is valid."""
        if self.repo_id is None:
            self._find_repo_id()
            if self.repo_id is None:
                raise RepositoryNotFoundError()
        headers, data = self._api_request(b'git/repositories/%s' % self.repo_id)
        if data[b'id'] != self.repo_id:
            raise SCMError(b'Repository ID did not match')
        return

    def get_file(self, path, revision, **kwargs):
        """Get the contents of a file."""
        try:
            query = {b'$format': b'octetstream'}
            headers, data = self._api_request(b'git/repositories/%s/blobs/%s' % (self.repo_id, revision), query, decode_json=False)
            return data
        except HTTPError as e:
            if e.code == 404:
                raise FileNotFoundError(path, revision)
            else:
                raise e

    def get_branches(self):
        """Return a list of data on branches in the repository.

        This will perform an API lookup for the list of branches, returning
        data entries for each one that's found.

        Returns:
            list of dict:
            The list of data on branches in the repository.

        Raises:
            reviewboard.scmtools.errors.SCMError:
                There was a failure in fetching data from this API.
        """
        try:
            data = self._api_request(b'git/repositories/%s/refs/heads' % self.repo_id)[1]
            return data[b'value']
        except Exception as e:
            logging.exception(b'Unexpected error when fetching TFS-Git branches for repository path "%s": %s', self.clone_path, e)
            raise SCMError(e)

    def get_commits(self, page_size, branch=None, start=None):
        """Return a page of data about commits in the repository.

        This will perform an API lookup for a page of commits for the
        given branch and optional starting point, returning entries for
        each one that's found. Each page will return a certain number of
        commits. The ``start`` parameter is used to retrieve subsequent
        pages of commits.

        Args:
            page_size (int):
                The maximum number of commits to fetch per page.

            branch (unicode):
                The starting branch for the commits.

            start (unicode):
                The ID of the commit to start from. This takes precedence over
                ``branch`` (as TFS-Git only allows one or the other).

        Returns:
            list of dict:
            A page of data about commits in the repository.

        Raises:
            reviewboard.scmtools.errors.SCMError:
                There was a failure in fetching data from this API.
        """
        query = {b'top': page_size}
        if start:
            query[b'commit'] = start
        else:
            if branch:
                query[b'branch'] = branch
            try:
                data = self._api_request(b'git/repositories/%s/commits' % self.repo_id, query)[1]
                return data[b'value']
            except Exception as e:
                logging.exception(b'Unexpected error when fetching TFS-Git commits for repository path "%s": %s', self.clone_path, e)
                raise SCMError(e)

    def get_commit(self, sha):
        """Return information on a commit with the given SHA.

        This will perform an API lookup for a commit with the given SHA,
        returning the raw data.

        Args:
            shsa (unicode):
                The full SHA of the commit.

        Returns:
            dict:
            Information on the SHA of the commit.

        Raises:
            reviewboard.scmtools.errors.SCMError:
                There was a failure in fetching data from this API.
        """
        try:
            return self._api_request(b'git/repositories/%s/commits/%s' % (self.repo_id, sha))[1]
        except Exception as e:
            logging.exception(b'Unexpected error when fetching TFS-Git commits for repository path "%s": %s', self.clone_path, e)
            raise SCMError(e)

    def get_commit_diff_list(self, base_version, target_version):
        """Return information on the differences between two commits.

        This API returns high-level metadata on the changes between two
        commits. Mainly, that consists of the file list, and some information
        on the types of changes (adds, edits, renames, deletes, etc.). It
        does not provide any information on the actual diffed content.

        Args:
            base_version (unicode):
                The SHA for the original commit.

            target_version (unicode)
                The SHA for the modified commit.

        Returns:
            list of dict:
            A list of changes/differences between the commits.
        """
        try:
            rsp = self._api_request(b'git/repositories/%s/diffs/commits' % self.repo_id, {b'baseVersionType': b'commit', 
               b'baseVersion': base_version, 
               b'targetVersionType': b'commit', 
               b'targetVersion': target_version, 
               b'$top': 1000})[1]
            return rsp[b'changes']
        except Exception as e:
            logging.exception(b'Unexpected error when fetching TFS-Git diff list for repository path "%s", commit %s: %s', self.clone_path, target_version, e)
            raise SCMError(e)

    def validate_sha1_format(self, path, sha1):
        """Validate that a SHA1 is of the right length for this repository.

        Args:
            path (unicode):
                The path for the file accompanying the SHA. This will be used
                in the exception, if raised.

            sha1 (unicode):
                The SHA1 to validate.

        Raises:
            reviewboard.scmtools.git.ShortSHA1Error:
                The provided SHA1 wasn't a full-length SHA.
        """
        if len(sha1) != self.FULL_SHA1_LENGTH:
            raise ShortSHA1Error(path, sha1)

    def _api_request(self, *args, **kwargs):
        """Perform an API request to the server.

        This differs from :py:meth:`TFSClient._api_request
        <rbpowerpack.scmtools.tfs.TFSClient._api_request>` in that it will
        locate the API path first if not already found. This is done lazily
        here rather than when constructing the tool in order to save on
        unnecessary API lookups in the New Review Request page (and others).

        Args:
            *args (tuple):
                Positional arguments to pass to the parent method.

            **kwargs (dict):
                Keyword arguments to pass to the parent method.

        Returns:
            object:
            The resulting deserialized object from the API response payload.
        """
        if self.path is None:
            self._find_api_path()
        if self.repo_id is None:
            self._find_repo_id()
        return super(TFSGitClient, self)._api_request(*args, **kwargs)

    def _find_api_path(self):
        """Find the API path based on the clone URL.

        This will attempt to use the clone URL as a starting point, looking
        for the URL used as the base for API calls.
        """
        cache_key = make_cache_key(b'tfs-git-api-path:%s' % self.clone_path)
        api_path = cache.get(cache_key)
        if api_path is not None:
            self.path = api_path
            if not self.use_basic_auth:
                self.password_manager.add_password(None, self.path, self.username, self.password)
        else:
            self.path = self.collection_path
            url_parts = list(urlparse(self.path))
            while True:
                try:
                    self._api_request(b'git/repositories')
                    logging.info(b'Detected TFS-git API path at %s', self.path)
                    cache.set(cache_key, self.path)
                    break
                except HTTPError:
                    if url_parts[2].endswith(b'/'):
                        new_dir = posixpath.dirname(url_parts[2][:-1])
                    else:
                        new_dir = posixpath.dirname(url_parts[2])
                    if not new_dir.endswith(b'/'):
                        new_dir += b'/'
                    if new_dir == url_parts[2]:
                        raise SCMError(b'Could not find the API URL for clone path %s' % self.clone_path)
                    url_parts[2] = new_dir
                    self.path = b'%s://%s%s' % tuple(url_parts[:3])
                    if not self.use_basic_auth:
                        self.password_manager.add_password(None, self.path, self.username, self.password)

        return

    def _find_repo_id(self):
        """Look up and return the ID of a git repository based on the name.

        This will fetch the 'repositories' API endpoint and search for the
        path in the results. If the repository is found, this returns the ID (a
        GUID). If not, this returns None.
        """
        self.repo_id = b''
        try:
            headers, data = self._api_request(b'git/repositories')
            path_quoted = self.clone_path.lower()
            path_unquoted = unquote(path_quoted)
            for repository in data[b'value']:
                if repository[b'remoteUrl'].lower() in (path_quoted,
                 path_unquoted):
                    self.repo_id = repository[b'id']
                    if self.repository:
                        self.repository.extra_data[b'repo_id'] = self.repo_id
                        self.repository.save(update_fields=[b'extra_data'])
                    return

            raise RepositoryNotFoundError()
        except Exception as e:
            logging.exception(b'Unexpected error when trying to find a TFS Git repository matching clone URL %s: %s', self.clone_path, e)
            raise


class TFSGitTool(SCMTool):
    """SCMTool for Team Foundation Server git repositories."""
    __metaclass__ = PowerPackSCMToolMetaClass
    name = b'Team Foundation Server (git)'
    supports_post_commit = True
    policy_func_name = b'is_tfs_enabled'
    field_help_text = {b'path': _(b'The fully-qualified clone path for the repository (i.e. http://tfs:8080/tfs/DefaultCollection/_git/git-project). This should match the "Clone Repository" path in the team explorer.')}
    COMMITS_PER_PAGE = 20
    EMPTY_SHA = b'000000000000000000000000000000000000000'

    def __init__(self, repository):
        """Initialize the tool."""
        super(TFSGitTool, self).__init__(repository)
        credentials = repository.get_credentials()
        encodings = []
        for e in repository.encoding.split(b','):
            e = e.strip()
            if e:
                encodings.append(e)

        if get_powerpack_extension() is not None:
            self.client = TFSGitClient(repository.path, repo_id=repository.extra_data.get(b'repo_id'), username=credentials[b'username'], password=credentials[b'password'], encodings=encodings or [b'iso-8859-15'], use_basic_auth=repository.extra_data.get(b'tfs_use_basic_auth', False), api_path=repository.extra_data.get(b'tfs_api_path'), repository=repository)
        else:
            self.client = None
        return

    def get_file(self, path, revision=None, **kwargs):
        """Get the contents of a file at the given revision."""
        return self.client.get_file(path, revision)

    def get_diffs_use_absolute_paths(self):
        """Get whether or not diffs contain absolute paths."""
        return True

    def get_parser(self, data):
        """Construct and return a DiffParser for the given diff data."""
        return GitDiffParser(data)

    def parse_diff_revision(self, file_str, revision_str, moved=False, copied=False, *args, **kwargs):
        """Parse the given file and revision strings.

        This implementation is the same as reviewboard.scmtools.git.GitTool.
        """
        revision = revision_str
        if file_str == b'/dev/null':
            revision = PRE_CREATION
        elif revision != PRE_CREATION and (not (moved or copied) or revision != b''):
            self.client.validate_sha1_format(file_str, revision)
        return (file_str, revision)

    @classmethod
    def check_repository(cls, path, username=None, password=None, local_site_name=None, use_basic_auth=False, tfs_api_path=None):
        """Perform checks on a repository to test its validity.
        This should check if a repository exists and can be connected to.

        The result is returned as an exception. The exception may contain
        extra information, such as a human-readable description of the problem.
        If the repository is valid and can be connected to, no exception
        will be thrown.
        """
        try:
            client = TFSGitClient(path, username=username, password=password, use_basic_auth=use_basic_auth, api_path=tfs_api_path)
            client.check_repository()
        except HTTPError as e:
            if e.code == 403 or e.code == 401:
                raise AuthenticationError([b'password'], e.reason)
            elif e.code == 404:
                raise RepositoryNotFoundError()
            else:
                raise SCMError(e)
        except RepositoryNotFoundError:
            raise
        except Exception as e:
            raise SCMError(e)

    def get_branches(self):
        """Return a list of all branches in the repository.

        This returns a list of Branch objects. One (and only one) of those
        objects should have the "default" field set to True.

        Returns:
            list of reviewboard.scmtools.core.Branch:
            The list of branches in the repository.

        Raises:
            reviewboard.scmtools.errors.SCMError:
                There was a failure in fetching the list of branches.
        """
        branches_data = self.client.get_branches()
        results = []
        for item in branches_data:
            name = item[b'name'][len(b'refs/heads/'):]
            results.append(Branch(id=name, commit=item[b'objectId'], default=name == b'master'))

        return results

    def get_commits(self, branch=None, start=None):
        """Return a list of all branches in the repository.

        This returns a list of Branch objects. One (and only one) of those
        objects should have the "default" field set to True.

        Args:
            branch (unicode):
                The starting branch for the commits.

            start (unicode):
                The ID of the commit to start from. This takes precedence over
                ``branch`` (as TFS-Git only allows one or the other).

        Returns:
            list of reviewboard.scmtools.core.Branch:
            The list of branches in the repository.

        Raises:
            reviewboard.scmtools.errors.SCMError:
                There was a failure in fetching the list of commits.
        """
        page_size = self.COMMITS_PER_PAGE + 1
        commits_data = self.client.get_commits(page_size=page_size, branch=branch, start=start)
        results = []
        for item in commits_data:
            commit = Commit(id=item[b'commitId'], author_name=item[b'author'][b'name'], date=item[b'committer'][b'date'], message=item[b'comment'])
            if results:
                results[(-1)].parent = commit.id
            results.append(commit)

        if len(results) == page_size:
            results.pop()
        return results

    def get_change(self, revision):
        """Return information on a commit in the repository.

        Args:
            revision (unicode):
                The SHA of the commit.

        Returns:
            reviewboard.scmtools.core.Commit:
            The commit message, if found.

        Raises:
            reviewboard.scmtools.errors.SCMError:
                There was a failure in fetching the commit, or the
                commit was not found.
        """
        commit = cache.get(self.repository.get_commit_cache_key(revision))
        if commit:
            author_name = commit.author_name
            date = commit.date
            parent_revision = commit.parent
            message = commit.message
        else:
            commits_data = self.client.get_commits(page_size=2, start=revision)
            commit_data = commits_data[0]
            author_name = commit_data[b'author'][b'name']
            date = commit_data[b'committer'][b'date']
            message = commit_data[b'comment']
            parent_revision = commits_data[1][b'commitId']
        diff_list = self.client.get_commit_diff_list(base_version=parent_revision, target_version=revision)
        new_changes = []
        diff = []
        renames = {}
        for change in diff_list:
            item = change[b'item']
            if item[b'gitObjectType'] != b'blob':
                continue
            change_types = change[b'changeType'].split(b', ')
            rename_source_path = change.get(b'sourceServerItem')
            path = item.get(b'path').lstrip(b'/')
            if rename_source_path:
                rename_source_path = rename_source_path.lstrip(b'/')
            new_change = {b'types': change_types, 
               b'old_sha': item.get(b'originalObjectId') or self.EMPTY_SHA, 
               b'new_sha': item.get(b'objectId') or self.EMPTY_SHA, 
               b'path': path, 
               b'rename_source_path': rename_source_path}
            new_changes.append(new_change)
            if b'sourceRename' in change_types:
                if path in renames:
                    assert renames[path][b'source'] is None
                    renames[path][b'source'] = new_change
                else:
                    renames[path] = {b'source': new_change, 
                       b'dest': None}
            elif b'rename' in change_types:
                if rename_source_path in renames:
                    assert renames[rename_source_path][b'dest'] is None
                    renames[rename_source_path][b'dest'] = new_change
                else:
                    renames[rename_source_path] = {b'source': None, 
                       b'dest': new_change}

        for change in new_changes:
            change_types = change[b'types']
            old_sha = change[b'old_sha']
            new_sha = change[b'new_sha']
            path = change[b'path']
            rename_source_path = change[b'rename_source_path']
            old_path = None
            new_path = None
            old_contents = None
            new_contents = None
            metadata_lines = []
            needs_contents = True
            if b'rename' in change_types:
                continue
            elif b'edit' in change_types:
                old_path = path
                new_path = path
            elif change_types == [b'add']:
                assert old_sha == self.EMPTY_SHA
                old_path = None
                new_path = path
            elif b'delete' in change_types:
                old_path = path
                if b'sourceRename' in change_types:
                    dest_rename_info = renames[old_path][b'dest']
                    new_path = dest_rename_info[b'path']
                    new_sha = dest_rename_info[b'new_sha']
                    metadata_lines = [
                     b'rename from %s' % old_path,
                     b'rename to %s' % new_path]
                    if b'edit' not in dest_rename_info[b'types']:
                        needs_contents = False
                else:
                    assert new_sha == self.EMPTY_SHA
                    metadata_lines = [
                     b'deleted file mode 100644']
            else:
                logging.warning((b'Unhandled change type "%s" in TFS-Git commit %s on repository ID=%s, ').join(change_types), revision, self.repository.pk)
                continue
            if needs_contents:
                if old_path and old_sha != self.EMPTY_SHA:
                    try:
                        old_contents = self.repository.get_file(old_path, old_sha)
                    except FileNotFoundError as e:
                        raise SCMError(b'Unable to fetch original file "%s" (%s) for TFS-Git commit %s on repository ID=%s: %s' % (
                         old_path, revision, old_sha,
                         self.repository.pk, e))

                if new_path and new_sha != self.EMPTY_SHA:
                    try:
                        new_contents = self.repository.get_file(new_path, new_sha)
                    except FileNotFoundError as e:
                        raise SCMError(b'Unable to fetch modified file "%s" (%s) for TFS-Git commit %s on repository ID=%s: %s' % (
                         old_path, revision, old_sha,
                         self.repository.pk, e))

            if old_path:
                old_path = old_path.encode(b'utf-8')
            if new_path:
                new_path = new_path.encode(b'utf-8')
            diff += [
             b'diff --git a/%s b/%s\n' % (
              old_path or new_path, new_path or old_path)] + [ b'%s\n' % metadata_line.encode(b'utf-8') for metadata_line in metadata_lines
                                                             ]
            if old_contents or new_contents:
                diff += [
                 b'index %s..%s\n' % (old_sha.encode(b'utf-8'),
                  new_sha.encode(b'utf-8')),
                 b'--- %s\n' % (old_path or b'/dev/null'),
                 b'+++ %s\n' % (new_path or b'/dev/null')]
                old_tmp = tempfile.NamedTemporaryFile(delete=False)
                old_tmp.write(old_contents or b'')
                old_tmp.close()
                new_tmp = tempfile.NamedTemporaryFile(delete=False)
                new_tmp.write(new_contents or b'')
                new_tmp.close()
                p = SCMTool.popen([b'diff', b'-u', old_tmp.name, new_tmp.name])
                unified_diff = p.stdout.read()
                errmsg = p.stderr.read()
                rc = p.wait()
                os.unlink(old_tmp.name)
                os.unlink(new_tmp.name)
                if rc == 2:
                    logging.error(b'Failed to create unified diff between %r and %r for commit %s on repository ID=%s: %s', old_path, new_path, revision, self.repository.pk, errmsg)
                continue
            if not unified_diff.startswith(b'---'):
                raise AssertionError
                diff += unified_diff.splitlines(True)[2:]

        return Commit(id=revision, author_name=author_name, date=date, message=message, parent=parent_revision, diff=(b'').join(diff))