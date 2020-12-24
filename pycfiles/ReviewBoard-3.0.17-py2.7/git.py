# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/scmtools/git.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import unicode_literals
import logging, os, platform, re, stat
from django.utils import six
from django.utils.six.moves import cStringIO as StringIO
from django.utils.six.moves.urllib.parse import quote as urlquote, urlsplit, urlunsplit
from django.utils.translation import ugettext_lazy as _
from djblets.util.filesystem import is_exe_in_path
from reviewboard.diffviewer.parser import DiffParser, DiffParserError, ParsedDiffFile
from reviewboard.scmtools.core import SCMClient, SCMTool, HEAD, PRE_CREATION
from reviewboard.scmtools.errors import FileNotFoundError, InvalidRevisionFormatError, RepositoryNotFoundError, SCMError
from reviewboard.ssh import utils as sshutils
GIT_DIFF_EMPTY_CHANGESET_SIZE = 3
try:
    import urlparse
    uses_netloc = urlparse.uses_netloc
    urllib_urlparse = urlparse.urlparse
except ImportError:
    import urllib.parse
    uses_netloc = urllib.parse.uses_netloc
    urllib_urlparse = urllib.parse.urlparse

uses_netloc.append(b'git')
sshutils.register_rbssh(b'GIT_SSH')

class ShortSHA1Error(InvalidRevisionFormatError):

    def __init__(self, path, revision, *args, **kwargs):
        InvalidRevisionFormatError.__init__(self, path=path, revision=revision, detail=six.text_type(_(b'The SHA1 is too short. Make sure the diff is generated with `git diff --full-index`.')), *args, **kwargs)


class GitTool(SCMTool):
    """
    You can only use this tool with a locally available git repository.
    The repository path should be to the .git directory (important if
    you do not have a bare repositry).
    """
    scmtool_id = b'git'
    name = b'Git'
    diffs_use_absolute_paths = True
    supports_raw_file_urls = True
    field_help_text = {b'path': _(b'For local Git repositories, this should be the path to a .git directory that Review Board can read from. For remote Git repositories, it should be the clone URL.')}
    dependencies = {b'executables': [
                      b'git']}

    def __init__(self, repository):
        super(GitTool, self).__init__(repository)
        local_site_name = None
        if repository.local_site:
            local_site_name = repository.local_site.name
        credentials = repository.get_credentials()
        self.client = GitClient(repository.path, repository.raw_file_url, credentials[b'username'], credentials[b'password'], repository.encoding, local_site_name)
        return

    def get_file(self, path, revision=HEAD, **kwargs):
        if revision == PRE_CREATION:
            return b''
        return self.client.get_file(path, revision)

    def file_exists(self, path, revision=HEAD, **kwargs):
        if revision == PRE_CREATION:
            return False
        try:
            return self.client.get_file_exists(path, revision)
        except (FileNotFoundError, InvalidRevisionFormatError):
            return False

    def normalize_patch(self, patch, filename, revision):
        """Normalize the provided patch file.

        This will make new, changed, and deleted symlinks look like
        regular files.

        Otherwise patch fails to apply the diff, complaining about the
        file not being a symlink.

        Args:
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
        m = GitDiffParser.FILE_MODE_RE.search(patch)
        if m:
            mode = int(m.group(b'mode'), 8)
            if stat.S_ISLNK(mode):
                mode = stat.S_IFREG | stat.S_IMODE(mode)
                patch = b'%s%o%s' % (patch[:m.start(b'mode')], mode,
                 patch[m.end(b'mode'):])
        return patch

    def parse_diff_revision(self, file_str, revision_str, moved=False, copied=False, *args, **kwargs):
        revision = revision_str
        if file_str == b'/dev/null':
            revision = PRE_CREATION
        elif revision != PRE_CREATION and (not (moved or copied) or revision != b''):
            self.client.validate_sha1_format(file_str, revision)
        return (file_str, revision)

    def get_parser(self, data):
        return GitDiffParser(data)

    @classmethod
    def check_repository(cls, path, username=None, password=None, local_site_name=None):
        """
        Performs checks on a repository to test its validity.

        This should check if a repository exists and can be connected to.
        This will also check if the repository requires an HTTPS certificate.

        The result is returned as an exception. The exception may contain
        extra information, such as a human-readable description of the problem.
        If the repository is valid and can be connected to, no exception
        will be thrown.
        """
        client = GitClient(path, local_site_name=local_site_name, username=username, password=password)
        super(GitTool, cls).check_repository(client.path, username, password, local_site_name)
        if not client.is_valid_repository():
            raise RepositoryNotFoundError()


class GitDiffParser(DiffParser):
    """
    This class is able to parse diffs created with Git
    """
    pre_creation_regexp = re.compile(b'^0+$')
    FILE_MODE_RE = re.compile(b'^(?:(?:new|deleted) file mode|index \\w+\\.\\.\\w+) (?P<mode>\\d+)$', re.M)
    DIFF_GIT_LINE_RES = [
     re.compile(b'^diff --git (?P<aq>")?a/(?P<orig_filename>[^"]+)(?(aq)") (?P<bq>")?b/(?P<new_filename>[^"]+)(?(bq)")$'),
     re.compile(b'^diff --git (?P<aq>")?(?!a/)(?P<orig_filename>(?(aq)[^"]|[^ ])+)(?(aq)") (?P<bq>")?(?!b/)(?P<new_filename>(?(bq)[^"]|[^ ])+)(?(bq)")$'),
     re.compile(b'^diff --git (?!")(?!a/)(?P<orig_filename>[^"]+)(?!") (?!")(?!b/)(?P<new_filename>(?P=orig_filename))(?!")$')]
    EXTENDED_HEADERS_KEYS = set([
     b'old mode',
     b'new mode',
     b'deleted file mode',
     b'new file mode',
     b'copy from',
     b'copy to',
     b'rename from',
     b'rename to',
     b'similarity index',
     b'dissimilarity index',
     b'index'])

    def _parse_extended_headers(self, linenum):
        """Parse an extended headers section.

        A dictionary with keys being the header name and values
        being a tuple of (header value, complete header line) will
        be returned. The complete header lines will have a trailing
        new line added for convenience.
        """
        headers = {}
        while linenum < len(self.lines):
            line = self.lines[linenum]
            for key in self.EXTENDED_HEADERS_KEYS:
                if line.startswith(key):
                    headers[key] = (
                     line[len(key) + 1:], line + b'\n')
                    break
            else:
                break

            linenum += 1

        return (headers, linenum)

    def parse(self):
        """
        Parses the diff, returning a list of File objects representing each
        file in the diff.
        """
        self.files = []
        i = 0
        preamble = StringIO()
        while i < len(self.lines):
            next_i, file_info, new_diff = self._parse_diff(i)
            if file_info:
                if self.files:
                    self.files[(-1)].finalize()
                self._ensure_file_has_required_fields(file_info)
                file_info.prepend_data(preamble.getvalue())
                preamble.close()
                preamble = StringIO()
                self.files.append(file_info)
            elif new_diff:
                preamble.close()
                preamble = StringIO()
            else:
                preamble.write(self.lines[i])
                preamble.write(b'\n')
            i = next_i

        try:
            if self.files:
                self.files[(-1)].finalize()
            elif preamble.getvalue().strip() != b'':
                raise DiffParserError(b'This does not appear to be a git diff', 0)
        finally:
            preamble.close()

        return self.files

    def _parse_diff(self, linenum):
        """Parses out one file from a Git diff

        This will return a tuple of the next line number, the file info
        (if any), and whether or not we've found a file (even if we decided
        not to record it).
        """
        if self.lines[linenum].startswith(b'diff --git'):
            line, info = self._parse_git_diff(linenum)
            return (
             line, info, True)
        else:
            return (
             linenum + 1, None, False)
            return

    def _parse_git_diff(self, linenum):
        start_linenum = linenum
        diff_git_line = self.lines[linenum]
        file_info = ParsedDiffFile()
        file_info.append_data(diff_git_line)
        file_info.append_data(b'\n')
        file_info.binary = False
        linenum += 1
        if linenum >= len(self.lines):
            return (linenum, None)
        else:
            file_info.origInfo = self.base_commit_id
            file_info.newInfo = self.new_commit_id
            headers, linenum = self._parse_extended_headers(linenum)
            for line in self.lines[start_linenum:linenum]:
                m = GitDiffParser.FILE_MODE_RE.search(line)
                if m:
                    mode = int(m.group(b'mode'), 8)
                    if stat.S_ISLNK(mode):
                        file_info.is_symlink = True
                        break

            if self._is_new_file(headers):
                file_info.append_data(headers[b'new file mode'][1])
                file_info.origInfo = PRE_CREATION
            elif self._is_deleted_file(headers):
                file_info.append_data(headers[b'deleted file mode'][1])
                file_info.deleted = True
            elif self._is_mode_change(headers):
                file_info.append_data(headers[b'old mode'][1])
                file_info.append_data(headers[b'new mode'][1])
            if self._is_moved_file(headers):
                file_info.origFile = headers[b'rename from'][0]
                file_info.newFile = headers[b'rename to'][0]
                file_info.moved = True
                if b'similarity index' in headers:
                    file_info.append_data(headers[b'similarity index'][1])
                file_info.append_data(headers[b'rename from'][1])
                file_info.append_data(headers[b'rename to'][1])
            else:
                if self._is_copied_file(headers):
                    file_info.origFile = headers[b'copy from'][0]
                    file_info.newFile = headers[b'copy to'][0]
                    file_info.copied = True
                    if b'similarity index' in headers:
                        file_info.append_data(headers[b'similarity index'][1])
                    file_info.append_data(headers[b'copy from'][1])
                    file_info.append_data(headers[b'copy to'][1])
                empty_change = True
                if b'index' in headers:
                    index_range = headers[b'index'][0].split()[0]
                    if b'..' in index_range:
                        file_info.origInfo, file_info.newInfo = index_range.split(b'..')
                    if self.pre_creation_regexp.match(file_info.origInfo):
                        file_info.origInfo = PRE_CREATION
                    file_info.append_data(headers[b'index'][1])
                while linenum < len(self.lines):
                    if self._is_git_diff(linenum):
                        break
                    elif self._is_binary_patch(linenum):
                        file_info.binary = True
                        file_info.append_data(self.lines[linenum])
                        file_info.append_data(b'\n')
                        empty_change = False
                        linenum += 1
                        break
                    elif self._is_diff_fromfile_line(linenum):
                        orig_line = self.lines[linenum]
                        new_line = self.lines[(linenum + 1)]
                        orig_filename = orig_line[len(b'--- '):]
                        new_filename = new_line[len(b'+++ '):]
                        if orig_filename.endswith(b'\t'):
                            orig_filename = orig_filename[:-1]
                        if new_filename.endswith(b'\t'):
                            new_filename = new_filename[:-1]
                        if orig_filename.startswith(b'a/'):
                            orig_filename = orig_filename[2:]
                        if new_filename.startswith(b'b/'):
                            new_filename = new_filename[2:]
                        if orig_filename == b'/dev/null':
                            file_info.origInfo = PRE_CREATION
                            file_info.origFile = new_filename
                        else:
                            file_info.origFile = orig_filename
                        if new_filename == b'/dev/null':
                            file_info.newFile = orig_filename
                        else:
                            file_info.newFile = new_filename
                        file_info.append_data(orig_line)
                        file_info.append_data(b'\n')
                        file_info.append_data(new_line)
                        file_info.append_data(b'\n')
                        linenum += 2
                    else:
                        empty_change = False
                        linenum = self.parse_diff_line(linenum, file_info)

            if not (file_info.origFile or not file_info.newFile):
                raise AssertionError
                self._parse_diff_git_line(diff_git_line, file_info, linenum)
            if isinstance(file_info.origFile, six.binary_type):
                file_info.origFile = file_info.origFile.decode(b'utf-8')
            if isinstance(file_info.newFile, six.binary_type):
                file_info.newFile = file_info.newFile.decode(b'utf-8')
            if empty_change and file_info.origInfo != PRE_CREATION and not (file_info.moved or file_info.copied or file_info.deleted):
                file_info = None
            return (linenum, file_info)

    def _parse_diff_git_line(self, diff_git_line, file_info, linenum):
        """Parses the "diff --git" line for filename information.

        Not all diffs have "---" and "+++" lines we can parse for the
        filenames. Git leaves these out if there aren't any changes made
        to the file.

        This function attempts to extract this information from the
        "diff --git" lines in the diff. It supports the following:

        * All filenames with quotes.
        * All filenames with a/ and b/ prefixes.
        * Filenames without quotes, prefixes, or spaces.
        * Filenames without quotes or prefixes, where the original and
          modified filenames are identical.
        """
        for regex in self.DIFF_GIT_LINE_RES:
            m = regex.match(diff_git_line)
            if m:
                file_info.origFile = m.group(b'orig_filename')
                file_info.newFile = m.group(b'new_filename')
                return

        raise DiffParserError(b'Unable to parse the "diff --git" line for this file, due to the use of filenames with spaces or --no-prefix, --src-prefix, or --dst-prefix options.', linenum)

    def _is_new_file(self, headers):
        return b'new file mode' in headers

    def _is_deleted_file(self, headers):
        return b'deleted file mode' in headers

    def _is_mode_change(self, headers):
        return b'old mode' in headers and b'new mode' in headers

    def _is_copied_file(self, headers):
        return b'copy from' in headers and b'copy to' in headers

    def _is_moved_file(self, headers):
        return b'rename from' in headers and b'rename to' in headers

    def _is_git_diff(self, linenum):
        return self.lines[linenum].startswith(b'diff --git')

    def _is_binary_patch(self, linenum):
        line = self.lines[linenum]
        return line.startswith(b'Binary file') or line.startswith(b'GIT binary patch')

    def _is_diff_fromfile_line(self, linenum):
        return linenum + 1 < len(self.lines) and self.lines[linenum].startswith(b'--- ') and self.lines[(linenum + 1)].startswith(b'+++ ')

    def _ensure_file_has_required_fields(self, file_info):
        """Make sure that the file object has all expected fields.

        This is needed so that there aren't explosions higher up the chain when
        the web layer is expecting a string object.
        """
        for attr in ('origInfo', 'newInfo'):
            if getattr(file_info, attr) is None:
                setattr(file_info, attr, b'')

        return


class GitClient(SCMClient):
    FULL_SHA1_LENGTH = 40
    schemeless_url_re = re.compile(b'^(?P<username>[A-Za-z0-9_\\.-]+@)?(?P<hostname>[A-Za-z0-9_\\.-]+):(?P<path>.*)')

    def __init__(self, path, raw_file_url=None, username=None, password=None, encoding=b'', local_site_name=None):
        super(GitClient, self).__init__(self._normalize_git_url(path), username=username, password=password)
        if not is_exe_in_path(b'git'):
            raise ImportError
        self.raw_file_url = raw_file_url
        self.encoding = encoding
        self.local_site_name = local_site_name
        self.git_dir = None
        url_parts = urllib_urlparse(self.path)
        if url_parts[0] == b'file':
            if platform.system() == b'Windows':
                self.git_dir = url_parts[1] + url_parts[2]
            else:
                self.git_dir = url_parts[2]
            p = self._run_git([b'--git-dir=%s' % self.git_dir, b'config',
             b'core.repositoryformatversion'])
            failure = p.wait()
            if failure:
                if not os.access(self.git_dir, os.R_OK):
                    raise SCMError(_(b"Permission denied accessing the local Git repository '%s'") % self.git_dir)
                else:
                    raise SCMError(_(b'Unable to retrieve information from local Git repository'))
        return

    def is_valid_repository(self):
        """Checks if this is a valid Git repository."""
        url_parts = urlsplit(self.path)
        if url_parts.scheme.lower() in ('http', 'https') and url_parts.username is None and self.username:
            new_netloc = urlquote(self.username, safe=b'')
            if self.password:
                new_netloc += b':' + urlquote(self.password, safe=b'')
            new_netloc += b'@' + url_parts.netloc
            path = urlunsplit((url_parts[0], new_netloc, url_parts[2],
             url_parts[3], url_parts[4]))
        else:
            path = self.path
        p = self._run_git([b'ls-remote', path, b'HEAD'])
        errmsg = p.stderr.read()
        failure = p.wait()
        if failure:
            logging.error(b'Git: Failed to find valid repository %s: %s' % (
             self.path, errmsg))
            return False
        else:
            return True

    def get_file(self, path, revision):
        if self.raw_file_url:
            self.validate_sha1_format(path, revision)
            return self.get_file_http(self._build_raw_url(path, revision), path, revision)
        else:
            return self._cat_file(path, revision, b'blob')

    def get_file_exists(self, path, revision):
        if self.raw_file_url:
            try:
                self.get_file(path, revision)
                return True
            except Exception:
                return False

        else:
            contents = self._cat_file(path, revision, b'-t')
            return contents and contents.strip() == b'blob'

    def validate_sha1_format(self, path, sha1):
        """Validates that a SHA1 is of the right length for this repository."""
        if self.raw_file_url and len(sha1) != self.FULL_SHA1_LENGTH:
            raise ShortSHA1Error(path, sha1)

    def _run_git(self, args):
        """Runs a git command, returning a subprocess.Popen."""
        return SCMTool.popen([b'git'] + args, local_site_name=self.local_site_name)

    def _build_raw_url(self, path, revision):
        url = self.raw_file_url
        url = url.replace(b'<revision>', revision)
        url = url.replace(b'<filename>', urlquote(path))
        return url

    def _cat_file(self, path, revision, option):
        """
        Call git-cat-file(1) to get content or type information for a
        repository object.

        If called with just "commit", gets the content of a blob (or
        raises an exception if the commit is not a blob).

        Otherwise, "option" can be used to pass a switch to git-cat-file,
        e.g. to test or existence or get the type of "commit".
        """
        commit = self._resolve_head(revision, path)
        p = self._run_git([b'--git-dir=%s' % self.git_dir, b'cat-file',
         option, commit])
        contents = p.stdout.read()
        errmsg = six.text_type(p.stderr.read())
        failure = p.wait()
        if failure:
            if errmsg.startswith(b'fatal: Not a valid object name'):
                raise FileNotFoundError(path, revision=commit)
            else:
                raise SCMError(errmsg)
        return contents

    def _resolve_head(self, revision, path):
        if revision == HEAD:
            if path == b'':
                raise SCMError(b'path must be supplied if revision is %s' % HEAD)
            return b'HEAD:%s' % path
        else:
            return six.text_type(revision)

    def _normalize_git_url(self, path):
        if path.startswith(b'file://'):
            return path
        url_parts = urllib_urlparse(path)
        scheme = url_parts[0]
        netloc = url_parts[1]
        if scheme and netloc:
            return path
        m = self.schemeless_url_re.match(path)
        if m:
            path = m.group(b'path')
            if not path.startswith(b'/'):
                path = b'/' + path
            return b'ssh://%s%s%s' % (m.group(b'username') or b'',
             m.group(b'hostname'),
             path)
        return b'file://' + path