# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/rbtools/clients/svn.py
# Compiled at: 2020-04-14 20:27:46
"""A client for Subversion."""
from __future__ import unicode_literals
import logging, os, posixpath, re, sys
from xml.etree import ElementTree
import six
from six.moves import map
from six.moves.urllib.parse import unquote
from rbtools.api.errors import APIError
from rbtools.clients import PatchResult, RepositoryInfo, SCMClient
from rbtools.clients.errors import AuthenticationError, InvalidRevisionSpecError, MinimumVersionError, OptionsCheckError, SCMError, TooManyRevisionsError
from rbtools.utils.checks import check_gnu_diff, check_install, is_valid_version
from rbtools.utils.console import get_pass
from rbtools.utils.diffs import filename_match_any_patterns, filter_diff, normalize_patterns
from rbtools.utils.filesystem import make_empty_files, make_tempfile, walk_parents
from rbtools.utils.process import execute
_fs_encoding = sys.getfilesystemencoding()

class SVNClient(SCMClient):
    """A client for Subversion.

    This is a wrapper around the svn executable that fetches repository
    information and generates compatible diffs.
    """
    name = b'Subversion'
    supports_diff_exclude_patterns = True
    supports_patch_revert = True
    INDEX_SEP = b'=' * 67
    INDEX_FILE_RE = re.compile(b'^Index: (.+?)(?:\t\\((added|deleted)\\))?\n$')
    DIFF_ORIG_FILE_LINE_RE = re.compile(b'^---\\s+.*\\s+\\(.*\\)')
    DIFF_NEW_FILE_LINE_RE = re.compile(b'^\\+\\+\\+\\s+.*\\s+\\(.*\\)')
    DIFF_COMPLETE_REMOVAL_RE = re.compile(b'^@@ -1,\\d+ \\+0,0 @@$')
    ADDED_FILES_RE = re.compile(b'^Index:\\s+(\\S+)\\t\\(added\\)$', re.M)
    DELETED_FILES_RE = re.compile(b'^Index:\\s+(\\S+)\\t\\(deleted\\)$', re.M)
    REVISION_WORKING_COPY = b'--rbtools-working-copy'
    REVISION_CHANGELIST_PREFIX = b'--rbtools-changelist:'
    VERSION_NUMBER_RE = re.compile(b'(\\d+)\\.(\\d+)\\.(\\d+)')
    SHOW_COPIES_AS_ADDS_MIN_VERSION = (1, 7, 0)
    PATCH_MIN_VERSION = (1, 7, 0)

    def __init__(self, **kwargs):
        """Initialize the client.

        Args:
            **kwargs (dict):
                Keyword arguments to pass through to the superclass.
        """
        super(SVNClient, self).__init__(**kwargs)
        self._svn_info_cache = {}
        self._svn_repository_info_cache = None
        return

    def get_repository_info(self):
        """Return repository information for the current SVN working tree.

        Returns:
            rbtools.clients.RepositoryInfo:
            The repository info structure.
        """
        if self._svn_repository_info_cache:
            return self._svn_repository_info_cache
        else:
            if not check_install([b'svn', b'help']):
                logging.debug(b'Unable to execute "svn help": skipping SVN')
                return
            svn_info_params = [
             b'info']
            if getattr(self.options, b'repository_url', None):
                svn_info_params.append(self.options.repository_url)
            data = self._run_svn(svn_info_params, ignore_errors=True, log_output_on_error=False)
            m = re.search(b'^Repository Root: (.+)$', data, re.M)
            if not m:
                return
            path = m.group(1)
            m = re.search(b'^Working Copy Root Path: (.+)$', data, re.M)
            if m:
                local_path = m.group(1)
            else:
                local_path = None
            m = re.search(b'^URL: (.+)$', data, re.M)
            if not m:
                return
            base_path = m.group(1)[len(path):] or b'/'
            m = re.search(b'^Repository UUID: (.+)$', data, re.M)
            if not m:
                return
            uuid = m.group(1)
            check_gnu_diff()
            ver_string = self._run_svn([b'--version', b'-q'], ignore_errors=True)
            m = self.VERSION_NUMBER_RE.match(ver_string)
            if not m:
                logging.warn(b'Unable to parse SVN client version triple from "%s". Assuming version 0.0.0.', ver_string.strip())
                self.subversion_client_version = (0, 0, 0)
            else:
                self.subversion_client_version = tuple(map(int, m.groups()))
            self._svn_repository_info_cache = SVNRepositoryInfo(path=path, base_path=base_path, local_path=local_path, uuid=uuid)
            return self._svn_repository_info_cache

    def parse_revision_spec(self, revisions=[]):
        """Parse the given revision spec.

        Args:
            revisions (list of unicode, optional):
                A list of revisions as specified by the user. Items in the list
                do not necessarily represent a single revision, since the user
                can use SCM-native syntaxes such as ``r1..r2`` or ``r1:r2``.
                SCMTool-specific overrides of this method are expected to deal
                with such syntaxes.

        Raises:
            rbtools.clients.errors.InvalidRevisionSpecError:
                The given revisions could not be parsed.

            rbtools.clients.errors.TooManyRevisionsError:
                The specified revisions list contained too many revisions.

        Returns:
            dict:
            A dictionary with the following keys:

            ``base`` (:py:class:`unicode`):
                A revision to use as the base of the resulting diff.

            ``tip`` (:py:class:`unicode`):
                A revision to use as the tip of the resulting diff.

            These will be used to generate the diffs to upload to Review Board
            (or print). The diff for review will include the changes in (base,
            tip].

            If a single revision is passed in, this will return the parent of
            that revision for "base" and the passed-in revision for "tip".

            If zero revisions are passed in, this will return the most recently
            checked-out revision for 'base' and a special string indicating the
            working copy for "tip".

            The SVN SCMClient never fills in the 'parent_base' key. Users who
            are using other patch-stack tools who want to use parent diffs with
            SVN will have to generate their diffs by hand.
        """
        n_revisions = len(revisions)
        if n_revisions == 1 and b':' in revisions[0]:
            revisions = revisions[0].split(b':')
            n_revisions = len(revisions)
        if n_revisions == 0:
            return {b'base': b'BASE', 
               b'tip': self.REVISION_WORKING_COPY}
        else:
            if n_revisions == 1:
                revision = revisions[0]
                try:
                    revision = self._convert_symbolic_revision(revision)
                    return {b'base': revision - 1, 
                       b'tip': revision}
                except ValueError:
                    if not self.options.repository_url:
                        status = self._run_svn([
                         b'status', b'--cl', six.text_type(revision),
                         b'--ignore-externals', b'--xml'], results_unicode=False)
                        cl = ElementTree.fromstring(status).find(b'changelist')
                        if cl is not None:
                            return {b'base': b'BASE', 
                               b'tip': self.REVISION_CHANGELIST_PREFIX + revision}
                    raise InvalidRevisionSpecError(b'"%s" does not appear to be a valid revision or changelist name' % revision)

            elif n_revisions == 2:
                try:
                    return {b'base': self._convert_symbolic_revision(revisions[0]), b'tip': self._convert_symbolic_revision(revisions[1])}
                except ValueError:
                    raise InvalidRevisionSpecError(b'Could not parse specified revisions: %s' % revisions)

            else:
                raise TooManyRevisionsError
            return

    def _convert_symbolic_revision(self, revision):
        """Convert a symbolic revision to a numbered revision.

        Args:
            revision (unicode):
                The name of a symbolic revision.

        Raises:
            ValueError:
                The given revision could not be converted.

        Returns:
            int:
            The revision number.
        """
        command = [
         b'-r', six.text_type(revision), b'-l', b'1']
        if getattr(self.options, b'repository_url', None):
            command.append(self.options.repository_url)
        log = self.svn_log_xml(command)
        if log is not None:
            try:
                root = ElementTree.fromstring(log)
            except ValueError as e:
                raise SCMError(b'Failed to parse svn log - %s.' % e)

            logentry = root.find(b'logentry')
            if logentry is not None:
                return int(logentry.attrib[b'revision'])
        raise ValueError
        return

    def scan_for_server(self, repository_info):
        """Find the Review Board server matching this repository.

        Args:
            repository_info (rbtools.clients.RepositoryInfo):
                The repository information structure.

        Returns:
            unicode:
            The Review Board server URL, if available.
        """
        server_url = super(SVNClient, self).scan_for_server(repository_info)
        if server_url:
            return server_url
        return self.scan_for_server_property(repository_info)

    def scan_for_server_property(self, repository_info):
        """Scan for the reviewboard:url property in the repository.

        This method looks for the reviewboard:url property, which is an
        alternate (legacy) way of configuring the Review Board server URL
        inside a subversion repository.

        Args:
            repository_info (rbtools.clients.RepositoryInfo):
                The repository information structure.

        Returns:
            unicode:
            The Review Board server URL, if available.
        """

        def get_url_prop(path):
            url = self._run_svn([b'propget', b'reviewboard:url', path], with_errors=False, extra_ignore_errors=(1, )).strip()
            return url or None

        for path in walk_parents(os.getcwd()):
            if not os.path.exists(os.path.join(path, b'.svn')):
                break
            prop = get_url_prop(path)
            if prop:
                return prop

        return get_url_prop(repository_info.path)

    def get_raw_commit_message(self, revisions):
        """Return the raw commit message(s) for the given revisions.

        Args:
            revisions (dict):
                Revisions to get the commit messages for. This will contain
                ``tip`` and ``base`` keys.

        Returns:
            unicode:
            The commit messages for all the requested revisions.
        """
        base = six.text_type(revisions[b'base'])
        tip = six.text_type(revisions[b'tip'])
        if tip == SVNClient.REVISION_WORKING_COPY or tip.startswith(SVNClient.REVISION_CHANGELIST_PREFIX):
            return b''
        command = [b'-r', b'%s:%s' % (base, tip)]
        if getattr(self.options, b'repository_url', None):
            command.append(self.options.repository_url)
        log = self.svn_log_xml(command)
        try:
            root = ElementTree.fromstring(log)
        except ValueError as e:
            raise SCMError(b'Failed to parse svn log: %s' % e)

        messages = root.findall(b'.//msg')[1:]
        return (b'\n\n').join(message.text for message in messages)

    def diff(self, revisions, include_files=[], exclude_patterns=[], no_renames=False, extra_args=[]):
        """Perform a diff in a Subversion repository.

        If the given revision spec is empty, this will do a diff of the
        modified files in the working directory. If the spec is a changelist,
        it will do a diff of the modified files in that changelist. If the spec
        is a single revision, it will show the changes in that revision. If the
        spec is two revisions, this will do a diff between the two revisions.

        SVN repositories do not support branches of branches in a way that
        makes parent diffs possible, so we never return a parent diff.

        Args:
            revisions (dict):
                A dictionary of revisions, as returned by
                :py:meth:`parse_revision_spec`.

            include_files (list of unicode, optional):
                A list of files to whitelist during the diff generation.

            exclude_patterns (list of unicode, optional):
                A list of shell-style glob patterns to blacklist during diff
                generation.

            extra_args (list, unused):
                Additional arguments to be passed to the diff generation.
                Unused for SVN.

        Returns:
            dict:
            A dictionary containing the following keys:

            ``diff`` (:py:class:`bytes`):
                The contents of the diff to upload.
        """
        repository_info = self.get_repository_info()
        exclude_patterns = normalize_patterns(exclude_patterns, b'/', repository_info.base_path)
        empty_files_revisions = {b'base': None, 
           b'tip': None}
        base = six.text_type(revisions[b'base'])
        tip = six.text_type(revisions[b'tip'])
        diff_cmd = [
         b'diff', b'--diff-cmd=diff', b'--notice-ancestry']
        changelist = None
        if tip == self.REVISION_WORKING_COPY:
            diff_cmd.extend([b'-r', base])
        elif tip.startswith(self.REVISION_CHANGELIST_PREFIX):
            changelist = tip[len(self.REVISION_CHANGELIST_PREFIX):]
            diff_cmd.extend([b'--changelist', changelist])
        elif self.options.repository_url:
            if len(include_files) == 1:
                repository_info.set_base_path(include_files[0])
                include_files = []
            new_url = repository_info.path + repository_info.base_path + b'@' + tip
            if base == b'0':
                old_url = repository_info.path + b'@' + base
            else:
                old_url = repository_info.path + repository_info.base_path + b'@' + base
            diff_cmd.extend([old_url, new_url])
            empty_files_revisions[b'base'] = b'(revision %s)' % base
            empty_files_revisions[b'tip'] = b'(revision %s)' % tip
        else:
            diff_cmd.extend([b'-r', b'%s:%s' % (base, tip)])
            empty_files_revisions[b'base'] = b'(revision %s)' % base
            empty_files_revisions[b'tip'] = b'(revision %s)' % tip
        diff_cmd.extend(include_files)
        if (tip == self.REVISION_WORKING_COPY or changelist) and is_valid_version(self.subversion_client_version, self.SHOW_COPIES_AS_ADDS_MIN_VERSION):
            svn_show_copies_as_adds = getattr(self.options, b'svn_show_copies_as_adds', None)
            if svn_show_copies_as_adds is None:
                if self.history_scheduled_with_commit(changelist, include_files, exclude_patterns):
                    sys.stderr.write(b'One or more files in your changeset has history scheduled with commit. Please try again with "--svn-show-copies-as-adds=y/n".\n')
                    sys.exit(1)
            elif svn_show_copies_as_adds in b'Yy':
                diff_cmd.append(b'--show-copies-as-adds')
        diff = self._run_svn(diff_cmd, split_lines=True, results_unicode=False, log_output_on_error=False)
        diff = self.handle_renames(diff)
        if self.supports_empty_files():
            diff = self._handle_empty_files(diff, diff_cmd, empty_files_revisions)
        diff = self.convert_to_absolute_paths(diff, repository_info)
        if exclude_patterns:
            diff = filter_diff(diff, self.INDEX_FILE_RE, exclude_patterns)
        return {b'diff': (b'').join(diff)}

    def history_scheduled_with_commit(self, changelist, include_files, exclude_patterns):
        """Return whether any files have history scheduled.

        Args:
            changelist (unicode):
                The changelist name, if specified.

            include_files (list of unicode):
                A list of files to whitelist during the diff generation.

            exclude_patterns (list of unicode):
                A list of shell-style glob patterns to blacklist during diff
                generation.

        Returns:
            bool:
            ``True`` if any new files have been scheduled including their
            history.
        """
        status_cmd = [
         b'status', b'-q', b'--ignore-externals']
        if changelist:
            status_cmd.extend([b'--changelist', changelist])
        if include_files:
            status_cmd.extend(include_files)
        for p in self._run_svn(status_cmd, split_lines=True, results_unicode=False):
            try:
                if p[3:4] == b'+':
                    if exclude_patterns:
                        filename = p[8:].rstrip().decode(_fs_encoding)
                        should_exclude = filename_match_any_patterns(filename, exclude_patterns, self.get_repository_info().base_path)
                        if not should_exclude:
                            return True
                    else:
                        return True
            except IndexError:
                pass

        return False

    def find_copyfrom(self, path):
        """Find the source filename for copied files.

        The output of 'svn info' reports the "Copied From" header when invoked
        on the exact path that was copied. If the current file was copied as a
        part of a parent or any further ancestor directory, 'svn info' will not
        report the origin. Thus it is needed to ascend from the path until
        either a copied path is found or there are no more path components to
        try.

        Args:
            path (unicode):
                The filename of the copied file.

        Returns:
            unicode:
            The filename of the source of the copy.
        """

        def smart_join(p1, p2):
            if p2:
                return os.path.join(p1, p2)
            else:
                return p1

        path1 = path
        path2 = None
        while path1:
            info = self.svn_info(path1, ignore_errors=True) or {}
            url = info.get(b'Copied From URL', None)
            if url:
                root = info[b'Repository Root']
                from_path1 = unquote(url[len(root):])
                return smart_join(from_path1, path2)
            if info.get(b'Schedule', None) != b'normal':
                return
            path1, tmp = os.path.split(path1)
            if path1 == b'' or path1 == b'/':
                path1 = None
            else:
                path2 = smart_join(tmp, path2)

        return

    def handle_renames(self, diff_content):
        """Fix up diff headers to properly show renames.

        The output of :command:`svn diff` is incorrect when the file in
        question came into being via svn mv/cp. Although the patch for these
        files are relative to its parent, the diff header doesn't reflect this.
        This function fixes the relevant section headers of the patch to
        portray this relationship.

        Args:
            diff_content (bytes):
                The content of the diffs.

        Returns:
            bytes:
            The processed diff.
        """
        if self.options.repository_url:
            return diff_content
        else:
            result = []
            num_lines = len(diff_content)
            i = 0
            while i < num_lines:
                if i + 4 < num_lines and self.INDEX_FILE_RE.match(diff_content[i]) and diff_content[(i + 1)][:-1] == self.INDEX_SEP and self.DIFF_ORIG_FILE_LINE_RE.match(diff_content[(i + 2)]) and self.DIFF_NEW_FILE_LINE_RE.match(diff_content[(i + 3)]):
                    from_line = diff_content[(i + 2)]
                    to_line = diff_content[(i + 3)]
                    if self.DIFF_COMPLETE_REMOVAL_RE.match(diff_content[(i + 4)]):
                        result.extend(diff_content[i:i + 5])
                    else:
                        to_file, _ = self.parse_filename_header(to_line[4:])
                        copied_from = self.find_copyfrom(to_file)
                        result.append(diff_content[i])
                        result.append(diff_content[(i + 1)])
                        if copied_from is not None:
                            result.append(from_line.replace(to_file.encode(_fs_encoding), copied_from.encode(_fs_encoding)))
                        else:
                            result.append(from_line)
                        result.append(to_line)
                        result.append(diff_content[(i + 4)])
                    i += 5
                else:
                    result.append(diff_content[i])
                    i += 1

            return result

    def _handle_empty_files(self, diff_content, diff_cmd, revisions):
        r"""Handle added and deleted 0-length files in the diff output.

        Since the diff output from :command:`svn diff` does not give enough
        context for 0-length files, we add extra information to the patch.

        For example, the original diff output of an added 0-length file is::

            Index: foo\n
            ===================================================================\n

        The modified diff of an added 0-length file will be::

            Index: foo\t(added)\n
            ===================================================================\n
            --- foo\t(<base_revision>)\n
            +++ foo\t(<tip_revision>)\n

        Args:
            diff_content (list of bytes):
                The content of the diff, split into lines.

            diff_cmd (list of unicode):
                A partial command line to run :command:`svn diff`.

            revisions (dict):
                A dictionary of revisions, as returned by
                :py:meth:`parse_revision_spec`.

        Returns:
            list of bytes:
            The processed diff lines.
        """
        diff_cmd.append(b'--no-diff-deleted')
        diff_with_deleted = self._run_svn(diff_cmd, ignore_errors=True, none_on_ignored_error=True, results_unicode=False)
        if not diff_with_deleted:
            return diff_content
        deleted_files = re.findall(b'^Index:\\s+(\\S+)\\s+\\(deleted\\)$', diff_with_deleted, re.M)
        result = []
        i = 0
        num_lines = len(diff_content)
        while i < num_lines:
            line = diff_content[i]
            if line.startswith(b'Index: ') and (i + 2 == num_lines or i + 2 < num_lines and diff_content[(i + 2)].startswith(b'Index: ')):
                index_line = line.strip()
                filename = index_line.split(b' ', 1)[1].strip()
                if filename in deleted_files:
                    result.append(b'%s\t(deleted)\n' % index_line)
                    if not revisions[b'base'] and not revisions[b'tip']:
                        tip = b'(working copy)'
                        info = self.svn_info(filename, ignore_errors=True)
                        if info and b'Revision' in info:
                            base = b'(revision %s)' % info[b'Revision']
                        else:
                            continue
                    else:
                        base = revisions[b'base']
                        tip = revisions[b'tip']
                else:
                    result.append(b'%s\t(added)\n' % index_line)
                    if not revisions[b'base'] and not revisions[b'tip']:
                        base = tip = b'(revision 0)'
                    else:
                        base = revisions[b'base']
                        tip = revisions[b'tip']
                result.append(b'%s\n' % self.INDEX_SEP)
                result.append(b'--- %s\t%s\n' % (filename.encode(_fs_encoding),
                 base.encode(b'utf-8')))
                result.append(b'+++ %s\t%s\n' % (filename.encode(_fs_encoding),
                 tip.encode(b'utf-8')))
                i += 2
            else:
                result.append(line)
                i += 1

        return result

    def convert_to_absolute_paths(self, diff_content, repository_info):
        """Convert relative paths in a diff output to absolute paths.

        This handles paths that have been svn switched to other parts of the
        repository.

        Args:
            diff_content (bytes):
                The content of the diff.

            repository_info (SVNRepositoryInfo):
                The repository info.

        Returns:
            bytes:
            The processed diff.
        """
        result = []
        for line in diff_content:
            front = None
            orig_line = line
            if self.DIFF_NEW_FILE_LINE_RE.match(line) or self.DIFF_ORIG_FILE_LINE_RE.match(line) or line.startswith(b'Index: '):
                front, line = line.split(b' ', 1)
            if front:
                if line.startswith(b'/'):
                    line = front + b' ' + line
                else:
                    file, rest = self.parse_filename_header(line)
                    if self.options.repository_url:
                        path = unquote(posixpath.join(repository_info.base_path, file))
                    else:
                        info = self.svn_info(file, True)
                        if info is None:
                            result.append(orig_line)
                            continue
                        url = info[b'URL']
                        root = info[b'Repository Root']
                        path = unquote(url[len(root):])
                    line = b'%s %s%s' % (front, path.encode(_fs_encoding),
                     rest)
            result.append(line)

        return result

    def svn_info(self, path, ignore_errors=False):
        """Return a dict which is the result of 'svn info' at a given path.

        Args:
            path (unicode):
                The path to the file being accessed.

            ignore_errors (bool, optional):
                Whether to ignore errors returned by ``svn info``.

        Returns:
            dict:
            The parsed ``svn info`` output.
        """
        if b'@' in path and not path[(-1)] == b'@':
            path += b'@'
        if path not in self._svn_info_cache:
            result = self._run_svn([b'info', path], split_lines=True, ignore_errors=ignore_errors, none_on_ignored_error=True)
            if result is None:
                self._svn_info_cache[path] = None
            else:
                svninfo = {}
                for info in result:
                    parts = info.strip().split(b': ', 1)
                    if len(parts) == 2:
                        key, value = parts
                        svninfo[key] = value

                self._svn_info_cache[path] = svninfo
        return self._svn_info_cache[path]

    def parse_filename_header(self, diff_line):
        """Parse the filename header from a diff.

        Args:
            diff_line (bytes):
                The line of the diff being parsed.

        Returns:
            tuple of (unicode, bytes):
            The parsed header line. The filename will be decoded using the
            system filesystem encoding.
        """
        parts = None
        if b'\t' in diff_line:
            parts = diff_line.split(b'\t', 1)
        if b'  ' in diff_line:
            parts = re.split(b'  +', diff_line, 1)
        if parts:
            return (parts[0].decode(_fs_encoding),
             b'\t' + parts[1])
        else:
            return (
             diff_line.split(b'\n')[0].decode(_fs_encoding),
             b'\n')

    def _get_p_number(self, base_path, base_dir):
        """Return the argument for --strip in svn patch.

        This determines the number of path components to remove from file paths
        in the diff to be applied.
        """
        if base_path == b'/':
            return 1
        else:
            return base_path.count(b'/') + 1

    def _exclude_files_not_in_tree(self, patch_file, base_path):
        """Process a diff and remove entries not in the current directory.

        Args:
            patch_file (unicode):
                The filename of the patch file to process. This file will be
                overwritten by the processed patch.

            base_path (unicode):
                The relative path between the root of the repository and the
                directory that the patch was created in.

        Returns:
            tuple of bool:
            A tuple with two values, representing whether any files have been
            excluded and whether the resulting diff is empty.
        """
        excluded_files = False
        empty_patch = True
        if not base_path.endswith(b'/'):
            base_path += b'/'
        filtered_patch_name = make_tempfile()
        with open(filtered_patch_name, b'w') as (filtered_patch):
            with open(patch_file, b'r') as (original_patch):
                include_file = True
                for line in original_patch.readlines():
                    m = self.INDEX_FILE_RE.match(line)
                    if m:
                        filename = m.group(1).decode(b'utf-8')
                        include_file = filename.startswith(base_path)
                        if not include_file:
                            excluded_files = True
                        else:
                            empty_patch = False
                    if include_file:
                        filtered_patch.write(line)

        os.rename(filtered_patch_name, patch_file)
        return (
         excluded_files, empty_patch)

    def apply_patch(self, patch_file, base_path, base_dir, p=None, revert=False):
        """Apply the patch and return a PatchResult indicating its success.

        Args:
            patch_file (unicode):
                The name of the patch file to apply.

            base_path (unicode):
                The base path that the diff was generated in.

            base_dir (unicode):
                The path of the current working directory relative to the root
                of the repository.

            p (unicode, optional):
                The prefix level of the diff.

            revert (bool, optional):
                Whether the patch should be reverted rather than applied.

        Returns:
            rbtools.clients.PatchResult:
            The result of the patch operation.
        """
        if not is_valid_version(self.subversion_client_version, self.PATCH_MIN_VERSION):
            raise MinimumVersionError(b'Using "rbt patch" with the SVN backend requires at least svn 1.7.0')
        if base_dir and not base_dir.startswith(base_path):
            excluded, empty = self._exclude_files_not_in_tree(patch_file, base_path)
            if excluded:
                logging.warn(b'This patch was generated in a different directory. To prevent conflicts, all files not under the current directory have been excluded. To apply all files in this patch, apply this patch from the %s directory.', base_dir)
                if empty:
                    logging.warn(b'All files were excluded from the patch.')
        cmd = [
         b'patch']
        p_num = p or self._get_p_number(base_path, base_dir)
        if p_num >= 0:
            cmd.append(b'--strip=%s' % p_num)
        if revert:
            cmd.append(b'--reverse-diff')
        cmd.append(six.text_type(patch_file))
        rc, patch_output = self._run_svn(cmd, return_error_code=True)
        if self.supports_empty_files():
            try:
                with open(patch_file, b'rb') as (f):
                    patch = f.read()
            except IOError as e:
                logging.error(b'Unable to read file %s: %s', patch_file, e)
                return

            self.apply_patch_for_empty_files(patch, p_num, revert=revert)
        return PatchResult(applied=rc == 0, patch_output=patch_output)

    def apply_patch_for_empty_files(self, patch, p_num, revert=False):
        """Return whether any empty files in the patch are applied.

        Args:
            patch (bytes):
                The contents of the patch.

            p_num (unicode):
                The prefix level of the diff.

            revert (bool, optional):
                Whether the patch should be reverted rather than applied.

        Returns:
            ``True`` if there are empty files in the patch. ``False`` if there
            were no empty files, or if an error occurred while applying the
            patch.
        """
        patched_empty_files = False
        if revert:
            added_files = self.DELETED_FILES_RE.findall(patch)
            deleted_files = self.ADDED_FILES_RE.findall(patch)
        else:
            added_files = self.ADDED_FILES_RE.findall(patch)
            deleted_files = self.DELETED_FILES_RE.findall(patch)
        if added_files:
            added_files = self._strip_p_num_slashes(added_files, int(p_num))
            make_empty_files(added_files)
            result = self._run_svn([b'add', b'--force'] + added_files, ignore_errors=True, none_on_ignored_error=True)
            if result is None:
                logging.error(b'Unable to execute "svn add" on: %s', (b', ').join(added_files))
            else:
                patched_empty_files = True
        if deleted_files:
            deleted_files = self._strip_p_num_slashes(deleted_files, int(p_num))
            result = self._run_svn([b'delete', b'--force'] + deleted_files, ignore_errors=True, none_on_ignored_error=True)
            if result is None:
                logging.error(b'Unable to execute "svn delete" on: %s', (b', ').join(deleted_files))
            else:
                patched_empty_files = True
        return patched_empty_files

    def supports_empty_files(self):
        """Check if the server supports added/deleted empty files.

        Returns:
            bool:
            Whether the Review Board server supports empty added or deleted
            files.
        """
        return self.capabilities and self.capabilities.has_capability(b'scmtools', b'svn', b'empty_files')

    def _run_svn(self, svn_args, *args, **kwargs):
        """Run the ``svn`` command.

        Args:
            svn_args (list of unicode):
                A list of additional arguments to add to the SVN command line.

            *args (list):
                Additional positional arguments to pass through to
                :py:func:`rbtools.utils.process.execute`.

            **kwargs (dict):
                Additional keyword arguments to pass through to
                :py:func:`rbtools.utils.process.execute`.

        Returns:
            tuple:
            The value returned by :py:func:`rbtools.utils.process.execute`.
        """
        cmdline = [
         b'svn', b'--non-interactive'] + svn_args
        if getattr(self.options, b'svn_username', None):
            cmdline += [b'--username', self.options.svn_username]
        if getattr(self.options, b'svn_prompt_password', None):
            self.options.svn_prompt_password = False
            self.options.svn_password = get_pass(b'SVN Password: ')
        if getattr(self.options, b'svn_password', None):
            cmdline += [b'--password', self.options.svn_password]
        return execute(cmdline, *args, **kwargs)

    def svn_log_xml(self, svn_args, *args, **kwargs):
        """Run SVN log non-interactively and retrieve XML output.

        We cannot run SVN log interactively and retrieve XML output because the
        authentication prompts will be intermixed with the XML output and cause
        XML parsing to fail.

        This function returns None (as if ``none_on_ignored_error`` were
        ``True``) if an error occurs that is not an authentication error.

        Args:
            svn_args (list of unicode):
                A list of additional arguments to add to the SVN command line.

            *args (list):
                Additional positional arguments to pass through to
                :py:func:`rbtools.utils.process.execute`.

            **kwargs (dict):
                Additional keyword arguments to pass through to
                :py:func:`rbtools.utils.process.execute`.

        Returns:
            bytes:
            The resulting log output.

        Raises:
            rbtools.clients.errors.AuthenticationError:
                Authentication to the remote repository failed.
        """
        command = [
         b'log', b'--xml'] + svn_args
        rc, result, errors = self._run_svn(command, return_error_code=True, with_errors=False, return_errors=True, ignore_errors=True, results_unicode=False, *args, **kwargs)
        if rc:
            if errors.startswith(b'svn: E215004'):
                raise AuthenticationError(b'Could not authenticate against remote SVN repository. Please provide the --svn-username and either the --svn-password or --svn-prompt-password command line options.')
            return None
        return result

    def check_options(self):
        """Verify the command line options.

        Raises:
            rbtools.clients.errors.OptionsCheckError:
                The supplied command line options were incorrect. In
                particular, if a file has history scheduled with the commit,
                the user needs to explicitly choose what behavior they want.
        """
        if getattr(self.options, b'svn_show_copies_as_adds', None):
            if len(self.options.svn_show_copies_as_adds) > 1 or self.options.svn_show_copies_as_adds not in b'YyNn':
                raise OptionsCheckError(b"Invalid value '%s' for --svn-show-copies-as-adds option. Valid values are 'y' or 'n'." % self.options.svn_show_copies_as_adds)
        return


class SVNRepositoryInfo(RepositoryInfo):
    """Information on a Subversion repository.

    This stores information on the path and, optionally, UUID of a Subversion
    repository. It can match a local repository against those on a Review Board
    server.

    Attributes:
        repository_id (int):
            ID of the repository in the API. This is used primarily for
            testing purposes, and is not guaranteed to be set.

        uuid (unicode):
            UUID of the Subversion repository.
    """

    def __init__(self, path=None, base_path=None, uuid=None, local_path=None, supports_parent_diffs=False, repository_id=None):
        """Initialize the repository information.

        Args:
            path (unicode):
                Subversion checkout path.

            base_path (unicode):
                Root of the Subversion repository.

            local_path (unicode):
                The local filesystem path for the repository. This can
                sometimes be the same as ``path``, but may not be (since that
                can contain a remote repository path).

            uuid (unicode):
                UUID of the Subversion repository.

            supports_parent_diffs (bool, optional):
                Whether or not the repository supports parent diffs.

            repository_id (int, optional):
                ID of the repository in the API. This is used primarily for
                testing purposes, and is not guaranteed to be set.
        """
        super(SVNRepositoryInfo, self).__init__(path=path, base_path=base_path, local_path=local_path, supports_parent_diffs=supports_parent_diffs)
        self.uuid = uuid
        self.repository_id = repository_id

    def find_server_repository_info(self, server):
        """Return server-side information on the current Subversion repository.

        The point of this function is to find a repository on the server that
        matches self, even if the paths aren't the same. (For example, if self
        uses an 'http' path, but the server uses a 'file' path for the same
        repository.) It does this by comparing repository UUIDs. If the
        repositories use the same path, you'll get back self, otherwise you'll
        get a different SVNRepositoryInfo object (with a different path).

        Args:
            server (rbtools.api.resource.RootResource):
                The root resource for the Review Board server.

        Returns:
            SVNRepositoryInfo:
            The server-side information for this repository.
        """
        repositories = server.get_repositories(tool=b'Subversion').all_items
        cached_repos = []
        for repository in repositories:
            if self.path == repository[b'path'] or b'mirror_path' in repository and self.path == repository[b'mirror_path']:
                self.repository_id = repository.id
                return self
            cached_repos.append(repository)

        for repository in cached_repos:
            try:
                info = repository.get_info()
                if not info or self.uuid != info[b'uuid']:
                    continue
            except APIError:
                continue

            repos_base_path = info[b'url'][len(info[b'root_url']):]
            relpath = self._get_relative_path(self.base_path, repos_base_path)
            if relpath:
                return SVNRepositoryInfo(path=info[b'url'], base_path=relpath, local_path=self.local_path, uuid=self.uuid, repository_id=repository.id)

        return self

    def _get_repository_info(self, server, repository):
        try:
            return server.get_repository_info(repository[b'id'])
        except APIError as e:
            if e.error_code == 210:
                return
            raise e

        return

    def _get_relative_path(self, path, root):
        pathdirs = self._split_on_slash(path)
        rootdirs = self._split_on_slash(root)
        if len(rootdirs) == 0:
            return path
        else:
            if rootdirs != pathdirs[:len(rootdirs)]:
                return
            else:
                if len(pathdirs) == len(rootdirs):
                    return b'/'
                return b'/' + (b'/').join(pathdirs[len(rootdirs):])

            return

    def _split_on_slash(self, path):
        split = re.split(b'/+', path)
        if split[(-1)] == b'':
            split = split[:-1]
        return split