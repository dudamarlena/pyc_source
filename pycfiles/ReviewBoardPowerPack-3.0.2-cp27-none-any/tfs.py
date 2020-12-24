# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /rbpowerpack/scmtools/tfs.py
# Compiled at: 2019-06-17 15:11:31
from __future__ import unicode_literals
import base64, json, logging, os, pprint, tempfile
from django.utils.six.moves.urllib.error import HTTPError
from django.utils.six.moves.urllib.parse import quote, unquote, urlencode
from django.utils.six.moves.urllib.request import HTTPPasswordMgrWithDefaultRealm, Request, build_opener, urlopen
from django.utils.translation import ugettext_lazy as _
from ntlm import HTTPNtlmAuthHandler
from reviewboard.diffviewer.diffutils import convert_to_unicode
from reviewboard.diffviewer.parser import DiffParser
from reviewboard.hostingsvcs.errors import AuthorizationError
from reviewboard.scmtools.core import Branch, Commit, SCMClient, SCMTool, PRE_CREATION, HEAD
from reviewboard.scmtools.errors import AuthenticationError, FileNotFoundError, RepositoryNotFoundError, SCMError
from rbpowerpack.scmtools.base import PowerPackSCMToolMetaClass

class BinaryFileError(ValueError):
    pass


class TFSClient(SCMClient):
    """Client for Team Foundation Server.

    This uses the REST API (available in Visual Studio 2013 and Visual Studio
    Team Services) to communicate with a Team Foundation Server repository.
    """

    def __init__(self, path, username=None, password=None, encodings=None, use_basic_auth=False, repository=None):
        """Initialize the client.

        The URL (``path``) can be either quoted or unquoted (%-escaped), since
        it's coming from user input. In the case that it needs to be quoted,
        that will happen during init.
        """
        needs_quote = True
        if b'%' in path:
            if unquote(path) != path:
                needs_quote = False
        if needs_quote:
            path = quote(path, b'/:')
        if not path.endswith(b'/'):
            path = path + b'/'
        super(TFSClient, self).__init__(path, username, password)
        self.encodings = encodings
        self.use_basic_auth = use_basic_auth
        self.repository = repository
        if self.use_basic_auth:
            self.basic_credentials = base64.b64encode(b'%s:%s' % (username, password))
            self.password_manager = None
            self.url_opener = None
        else:
            self.password_manager = HTTPPasswordMgrWithDefaultRealm()
            self.password_manager.add_password(None, path, username, password)
            auth_handler = HTTPNtlmAuthHandler.HTTPNtlmAuthHandler(self.password_manager)
            self.url_opener = build_opener(auth_handler)
        return

    def _api_request(self, resource, query=None, decode_json=True, include_api_version=True):
        if query is None:
            query = {}
        if include_api_version:
            query[b'api-version'] = b'1.0'
        url = b'%s_apis/%s?%s' % (self.path,
         quote(resource),
         urlencode(query))
        logging.debug(b'Making request to %s (use_basic_auth=%s)', url, self.use_basic_auth)
        if self.use_basic_auth:
            request = Request(url)
            request.add_header(b'Authorization', b'Basic %s' % self.basic_credentials)
            rsp = urlopen(request)
        else:
            rsp = self.url_opener.open(url)
        if rsp.code != 200:
            if rsp.code == 203 and rsp.headers.get(b'X-Tfs-Location', b'').startswith(b'/_signin'):
                if self.repository and self.repository.hosting_account:
                    try:
                        del self.repository.hosting_account.data[b'password']
                        self.repository.hosting_account.save(update_fields=[
                         b'data'])
                    except KeyError:
                        pass

                raise AuthorizationError(_(b'Your account credentials are no longer valid. Please set new credentials in your repository configuration.'), http_code=rsp.code)
            msg = rsp.read()
            logging.debug(b'Got unexpected response (%d): %s', rsp.code, msg)
            raise HTTPError(url, rsp.code, msg, {}, None)
        data = rsp.read()
        if decode_json:
            return (rsp.headers, json.loads(data))
        else:
            return (
             rsp.headers, data)
            return

    def get_branches(self):
        headers, data = self._api_request(b'tfvc/branches', {b'includeChildren': b'true'})
        return [
         Branch(b'$/', b'$/', default=True)] + [ branch for item in data[b'value'] for branch in self._walk_branch(item)
                                               ]

    def get_commits(self, branch=None, start=None):
        if branch is None:
            branch = b'$/'
        query = {b'searchCriteria.itemPath': branch, 
           b'$top': 30}
        if start is not None:
            query[b'searchCriteria.toId'] = start
        headers, data = self._api_request(b'tfvc/changesets', query)
        commits = []
        for item in data[b'value']:
            changeset_id = int(item[b'changesetId'])
            if changeset_id == 1:
                parent = b''
            else:
                parent = b'%d' % (changeset_id - 1)
            commits.append(Commit(author_name=item[b'author'][b'displayName'], id=b'%d' % changeset_id, date=item[b'createdDate'], message=item.get(b'comment', b''), parent=parent))

        return commits

    def get_change(self, revision):
        headers, data = self._api_request(b'tfvc/changesets/%s' % revision, {b'maxChangeCount': b'100'})
        changeset_id = int(data[b'changesetId'])
        if changeset_id == 1:
            parent = b''
        else:
            parent = b'%d' % (changeset_id - 1)
        diff = []
        for change in data[b'changes']:
            change_types = change[b'changeType'].split(b', ')
            binary = False
            copied = b'branch' in change_types
            new_path = b''
            old_path = b''
            new_file = b''
            old_file = b''
            new_version = b''
            old_version = b''
            if b'add' in change_types and b'edit' in change_types:
                new_path = old_path = change[b'item'][b'path']
                old_version = 0
                new_version = change[b'item'][b'version']
                old_file = b''
                try:
                    new_file = self.get_file(new_path, new_version)
                except BinaryFileError:
                    binary = True

            elif b'edit' in change_types:
                new_path = change[b'item'][b'path']
                if b'rename' in change_types or copied:
                    old_path = change[b'sourceServerItem']
                else:
                    old_path = new_path
                new_version = change[b'item'][b'version']
                old_version = new_version - 1
                try:
                    old_file = self.get_file(old_path, old_version)
                    new_file = self.get_file(new_path, new_version)
                except BinaryFileError:
                    binary = True

            elif b'delete' in change_types and b'sourceRename' not in change_types:
                new_path = old_path = change[b'item'][b'path']
                old_version = change[b'item'][b'version'] - 1
                new_version = b'(deleted)'
                try:
                    old_file = self.get_file(old_path, old_version)
                    new_file = b''
                except BinaryFileError:
                    binary = True

            elif b'rename' in change_types:
                new_path = change[b'item'][b'path']
                old_path = change[b'sourceServerItem']
                new_version = change[b'item'][b'version']
                old_version = new_version - 1
                try:
                    new_file = self.get_file(new_path, new_version)
                    old_file = new_file
                except BinaryFileError:
                    binary = True

            elif copied:
                new_path = change[b'item'][b'path']
                old_path = change[b'sourceServerItem']
                new_version = change[b'item'][b'version']
                old_version = new_version - 1
                try:
                    old_file = self.get_file(old_path, old_version)
                    new_file = self.get_file(new_path, new_version)
                except BinaryFileError:
                    binary = True

            elif b'sourceRename' in change_types:
                pass
            else:
                logging.warning(b'Unhandled change type "%s" in TFS commit %d', (b', ').join(change_types), changeset_id)
                continue
            old_label = b'%s\t%s' % (old_path.encode(b'utf-8'), old_version)
            new_label = b'%s\t%s' % (new_path.encode(b'utf-8'), new_version)
            if not binary:
                if old_path != new_path and old_file == new_file:
                    if copied:
                        diff.append(b'Copied from: %s\n' % old_path.encode(b'utf-8'))
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
                            diff.append(b'Copied from: %s\n' % old_path.encode(b'utf-8'))
                        diff.append(unified_diff)
                    os.unlink(old_tmp.name)
                    os.unlink(new_tmp.name)
            if binary:
                diff.append(b'--- %s\n' % old_label)
                diff.append(b'+++ %s\n' % new_label)
                diff.append(b'Binary files %s and %s differ\n' % (
                 old_path.encode(b'utf-8'),
                 new_path.encode(b'utf-8')))

        try:
            diff = (b'').join(diff)
        except Exception as e:
            logging.error(b'Failed to create diff: %s\n%s', e, pprint.pformat(diff), exc_info=True)
            raise e

        return Commit(author_name=data[b'author'][b'displayName'], id=b'%d' % changeset_id, date=data[b'createdDate'], message=data.get(b'comment', b''), parent=parent, diff=diff)

    def check_repository(self):
        self._api_request(b'projects')

    def get_file(self, path, revision, **kwargs):
        if path.startswith(b'/'):
            path = path[1:]
        query = {b'path': path, 
           b'versionType': b'Changeset', 
           b'version': str(revision)}
        try:
            headers, data = self._api_request(b'tfvc/items', query, decode_json=False, include_api_version=False)
            content_type = headers[b'Content-Type'].split(b';', 1)[0]
            text_mimetypes = [
             b'application/octet-stream',
             b'application/xhtml+xml',
             b'application/xml',
             b'application/x-sh',
             b'application/x-cshapplication/ecmascript',
             b'application/javascript',
             b'application/json',
             b'application/msaccess',
             b'application/x-latex',
             b'application/x-tex']
            if content_type.startswith(b'text/') or content_type in text_mimetypes:
                try:
                    enc, data = convert_to_unicode(data, self.encodings)
                    return data.encode(b'utf-8')
                except Exception:
                    pass

            logging.info(b'Treating file %s:%s (%s) as binary', path, revision, content_type)
            raise BinaryFileError
        except HTTPError as e:
            if e.code == 404:
                raise FileNotFoundError(path, revision)
            else:
                raise e

    def _walk_branch(self, branch_info):
        """Yield Branch objects for a tree of branch data.

        This will walk through a tree of branch information, yielding a
        :py:class:`~reviewboard.scmtools.core.Branch` for each each level
        of the tree. This ensures all children of a branch, grandchildren,
        and so forth will be included.

        Args:
            branch_info (dict):
                Information on a branch from the API.

        Yields:
            reviewboard.scmtools.core.Branch:
            A branch for each level in the tree.
        """
        path = branch_info[b'path']
        yield Branch(id=path, name=path)
        for child_info in branch_info.get(b'children', []):
            for branch in self._walk_branch(child_info):
                yield branch


class TFSTool(SCMTool):
    """SCMTool for Team Foundation Server."""
    __metaclass__ = PowerPackSCMToolMetaClass
    name = b'Team Foundation Server'
    supports_post_commit = True
    field_help_text = {b'path': _(b'The fully-qualified path to the TFS server and collection (i.e. http://tfs:8080/tfs/DefaultCollection). This should match the path listed in the TFS Administration Console or the collection reported when running `tf workfold`.')}
    policy_func_name = b'is_tfs_enabled'

    def __init__(self, repository):
        super(TFSTool, self).__init__(repository)
        credentials = repository.get_credentials()
        encodings = []
        for e in repository.encoding.split(b','):
            e = e.strip()
            if e:
                encodings.append(e)

        use_basic_auth = repository.extra_data.get(b'tfs_use_basic_auth', False)
        self.client = TFSClient(repository.path, username=credentials[b'username'], password=credentials[b'password'], encodings=encodings or [b'iso-8859-15'], use_basic_auth=use_basic_auth, repository=repository)

    def get_file(self, path, revision=None, base_commit_id=None):
        return self.client.get_file(path, revision)

    def file_exists(self, path, revision=HEAD, base_commit_id=None, **kwargs):
        try:
            self.client.get_file(path, revision)
            return True
        except BinaryFileError:
            return True
        except FileNotFoundError:
            return False

    def parse_diff_revision(self, file_str, revision_str, moved=False, copied=False, **kwargs):
        revision = revision_str
        if file_str == b'/dev/null' or revision_str == b'0':
            revision = PRE_CREATION
        return (file_str, revision)

    def get_parser(self, data):
        return TFSDiffParser(data)

    def get_diffs_use_absolute_paths(self):
        return True

    def get_branches(self):
        """Get a list of all branches in the repositories.

        This returns a list of Branch objects. One (and only one) of those
        objects should have the "default" field set to True.
        """
        try:
            return self.client.get_branches()
        except Exception as e:
            raise SCMError(e)

    def get_commits(self, branch=None, start=None):
        """Get a list of commits backward in history from a given point.

        This returns a list of Commit objects (at most 30).

        This can be called multiple times in succession using the "parent"
        field of the last entry as the start parameter in order to paginate
        through the history of commits in the repository.
        """
        try:
            return self.client.get_commits(branch, start)
        except Exception as e:
            raise SCMError(e)

    def get_change(self, revision):
        """Get an individual change.

        This returns a Commit object containing the details of the commit.
        """
        try:
            return self.client.get_change(revision)
        except Exception as e:
            logging.error(b'Failed to get the change from TFS for revision "%s": %s', revision, e, exc_info=True)
            raise SCMError(e)

    @classmethod
    def check_repository(cls, path, username=None, password=None, local_site_name=None, use_basic_auth=False, **kwargs):
        """Performs checks on a repository to test its validity.

        This should check if a repository exists and can be connected to.

        The result is returned as an exception. The exception may contain
        extra information, such as a human-readable description of the problem.
        If the repository is valid and can be connected to, no exception
        will be thrown.
        """
        client = TFSClient(path, username, password, use_basic_auth=use_basic_auth)
        try:
            client.check_repository()
        except HTTPError as e:
            if e.code == 403 or e.code == 401:
                raise AuthenticationError([b'password'], e.msg)
            elif e.code == 404:
                raise RepositoryNotFoundError()
            else:
                raise SCMError(e)
        except Exception as e:
            raise SCMError(e)


class TFSDiffParser(DiffParser):
    """DiffParser for TFS.

    This exists to handle the specifics of added files (revision '0'), moved
    files, and binary files as created by the rbtools TFS diff implementation.
    """

    def parse_special_header(self, linenum, info):
        linenum = super(TFSDiffParser, self).parse_special_header(linenum, info)
        if linenum + 1 < len(self.lines) and self.lines[linenum].startswith(b'Copied from: '):
            info[b'copied'] = True
            linenum += 1
        return linenum

    def parse_diff_header(self, linenum, info):
        linenum = super(TFSDiffParser, self).parse_diff_header(linenum, info)
        deleted = info.get(b'newInfo') == b'(deleted)'
        added = info.get(b'oldFile') == b'/dev/null' or info.get(b'origInfo') == b'0'
        info[b'deleted'] = deleted
        if added:
            info[b'origFile'] = info.get(b'newFile')
        if info.get(b'origFile') != info.get(b'newFile') and not deleted and not added and not info.get(b'copied', False):
            info[b'moved'] = True
        if linenum < len(self.lines) and self.lines[linenum].startswith(b'Binary files'):
            info[b'binary'] = True
            linenum += 1
        return linenum

    def parse(self):
        files = super(TFSDiffParser, self).parse()
        for f in files:
            if f.moved and f.insert_count == 0 and f.delete_count == 0:
                f._data = b''

        self.files = files
        return files