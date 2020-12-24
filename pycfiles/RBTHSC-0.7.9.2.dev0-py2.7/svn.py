# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\rbtools\clients\svn.py
# Compiled at: 2017-04-19 05:14:02
from __future__ import unicode_literals
import getpass, logging, os, posixpath, re, sys
from xml.etree import ElementTree
import six
from six.moves.urllib.parse import unquote
from rbtools.api.errors import APIError
from rbtools.clients import PatchResult, RepositoryInfo, SCMClient
from rbtools.clients.errors import AuthenticationError, InvalidRevisionSpecError, MinimumVersionError, OptionsCheckError, SCMError, TooManyRevisionsError
from rbtools.utils.checks import check_gnu_diff, check_install, is_valid_version
from rbtools.utils.diffs import filename_match_any_patterns, filter_diff, normalize_patterns
from rbtools.utils.filesystem import make_empty_files, make_tempfile, walk_parents
from rbtools.utils.process import execute

class SVNClient(SCMClient):
    """
    A wrapper around the svn Subversion tool that fetches repository
    information and generates compatible diffs.
    """
    name = b'Subversion'
    INDEX_SEP = b'=' * 67
    INDEX_FILE_RE = re.compile(b'^Index: (.+?)(?:\t\\((added|deleted)\\))?\n$')
    supports_diff_exclude_patterns = True
    supports_patch_revert = True
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
        super(SVNClient, self).__init__(**kwargs)

    def get_repository_info(self):
        if not check_install([b'svn', b'help']):
            logging.debug(b'Unable to execute "svn help": skipping SVN')
            return
        else:
            svn_info_params = [
             b'info']
            if getattr(self.options, b'repository_url', None):
                svn_info_params.append(self.options.repository_url)
            data = self._run_svn(svn_info_params, ignore_errors=True, results_unicode=False)
            m = re.search(b'^Repository Root: (.+)$', data, re.M)
            if not m:
                return
            path = m.group(1)
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
                logging.warn(b'Unable to parse SVN client version triple from "%s". Assuming version 0.0.0.' % ver_string.strip())
                self.subversion_client_version = (0, 0, 0)
            else:
                self.subversion_client_version = tuple(map(int, m.groups()))
            return SVNRepositoryInfo(path, base_path, uuid)

    def parse_revision_spec(self, revisions=[]):
        """Parses the given revision spec.

        The 'revisions' argument is a list of revisions as specified by the
        user. Items in the list do not necessarily represent a single revision,
        since the user can use SCM-native syntaxes such as "r1..r2" or "r1:r2".
        SCMTool-specific overrides of this method are expected to deal with
        such syntaxes.

        This will return a dictionary with the following keys:
            'base':        A revision to use as the base of the resulting diff.
            'tip':         A revision to use as the tip of the resulting diff.

        These will be used to generate the diffs to upload to Review Board (or
        print). The diff for review will include the changes in (base, tip].

        If a single revision is passed in, this will return the parent of that
        revision for 'base' and the passed-in revision for 'tip'.

        If zero revisions are passed in, this will return the most recently
        checked-out revision for 'base' and a special string indicating the
        working copy for 'tip'.

        The SVN SCMClient never fills in the 'parent_base' key. Users who are
        using other patch-stack tools who want to use parent diffs with SVN
        will have to generate their diffs by hand.
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
                        status = self._run_svn([b'status', b'--cl', str(revision),
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
        server_url = super(SVNClient, self).scan_for_server(repository_info)
        if server_url:
            return server_url
        return self.scan_for_server_property(repository_info)

    def scan_for_server_property(self, repository_info):

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

    def diff(self, revisions, include_files=[], exclude_patterns=[], extra_args=[]):
        """
        Performs a diff in a Subversion repository.

        If the given revision spec is empty, this will do a diff of the
        modified files in the working directory. If the spec is a changelist,
        it will do a diff of the modified files in that changelist. If the spec
        is a single revision, it will show the changes in that revision. If the
        spec is two revisions, this will do a diff between the two revisions.

        SVN repositories do not support branches of branches in a way that
        makes parent diffs possible, so we never return a parent diff.
        """
        repository_info = self.get_repository_info()
        exclude_patterns = normalize_patterns(exclude_patterns, b'/', repository_info.base_path)
        empty_files_revisions = {b'base': None, 
           b'tip': None}
        base = str(revisions[b'base'])
        tip = str(revisions[b'tip'])
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
                    sys.stderr.write(b"One or more files in your changeset has history scheduled with commit. Please try again with '--svn-show-copies-as-adds=y/n'.\n")
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
        """ Method to find if any file status has '+' in 4th column"""
        status_cmd = [
         b'status', b'-q', b'--ignore-externals']
        if changelist:
            status_cmd.extend([b'--changelist', changelist])
        if include_files:
            status_cmd.extend(include_files)
        for p in self._run_svn(status_cmd, split_lines=True, results_unicode=False):
            try:
                if p[3] == b'+':
                    if exclude_patterns:
                        filename = p[8:].rstrip()
                        should_exclude = filename_match_any_patterns(filename, exclude_patterns, self.get_repository_info().base_path)
                        if not should_exclude:
                            return True
                    else:
                        return True
            except IndexError:
                pass

        return False

    def find_copyfrom(self, path):
        """
        A helper function for handle_renames

        The output of 'svn info' reports the "Copied From" header when invoked
        on the exact path that was copied. If the current file was copied as a
        part of a parent or any further ancestor directory, 'svn info' will not
        report the origin. Thus it is needed to ascend from the path until
        either a copied path is found or there are no more path components to
        try.
        """

        def smart_join(p1, p2):
            if p2:
                return os.path.join(p1, p2)
            return p1

        path1 = path
        path2 = None
        while path1:
            info = self.svn_info(path1, ignore_errors=True) or {}
            url = info.get(b'Copied From URL', None)
            if url:
                root = info[b'Repository Root']
                from_path1 = unquote(url[len(root):]).encode(b'utf-8')
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
        """
        The output of svn diff is incorrect when the file in question came
        into being via svn mv/cp. Although the patch for these files are
        relative to its parent, the diff header doesn't reflect this.
        This function fixes the relevant section headers of the patch to
        portray this relationship.
        """
        if self.options.repository_url:
            return diff_content
        else:
            result = []
            from_line = to_line = None
            for line in diff_content:
                if self.DIFF_ORIG_FILE_LINE_RE.match(line):
                    from_line = line
                    continue
                if self.DIFF_NEW_FILE_LINE_RE.match(line):
                    to_line = line
                    continue
                if from_line and to_line:
                    if self.DIFF_COMPLETE_REMOVAL_RE.match(line):
                        result.append(from_line)
                        result.append(to_line)
                    else:
                        to_file, _ = self.parse_filename_header(to_line[4:])
                        copied_from = self.find_copyfrom(to_file)
                        if copied_from is not None:
                            result.append(from_line.replace(to_file, copied_from))
                        else:
                            result.append(from_line)
                        result.append(to_line)
                    from_line = to_line = None
                result.append(line)

            return result

    def _handle_empty_files(self, diff_content, diff_cmd, revisions):
        """Handles added and deleted 0-length files in the diff output.

        Since the diff output from svn diff does not give enough context for
        0-length files, we add extra information to the patch.

        For example, the original diff output of an added 0-length file is:
        Index: foo

        ===================================================================

        The modified diff of an added 0-length file will be:
        Index: foo      (added)

        ===================================================================

        --- foo (<base_revision>)

        +++ foo (<tip_revision>)

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
                if isinstance(base, six.text_type):
                    base = base.encode(b'utf-8')
                if isinstance(tip, six.text_type):
                    tip = tip.encode(b'utf-8')
                result.append(b'%s\n' % self.INDEX_SEP)
                result.append(b'--- %s\t%s\n' % (filename, base))
                result.append(b'+++ %s\t%s\n' % (filename, tip))
                i += 2
            else:
                result.append(line)
                i += 1

        return result

    def convert_to_absolute_paths(self, diff_content, repository_info):
        """
        Converts relative paths in a diff output to absolute paths.
        This handles paths that have been svn switched to other parts of the
        repository.
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
                    line = b'%s %s%s' % (front, path, rest)
            result.append(line)

        return result

    def svn_info(self, path, ignore_errors=False):
        """Return a dict which is the result of 'svn info' at a given path."""
        svninfo = {}
        if b'@' in path and not path[(-1)] == b'@':
            path += b'@'
        result = self._run_svn([b'info', path], split_lines=True, ignore_errors=ignore_errors, none_on_ignored_error=True, results_unicode=False)
        if result is None:
            return
        else:
            for info in result:
                parts = info.strip().split(b': ', 1)
                if len(parts) == 2:
                    key, value = parts
                    svninfo[key] = value

            return svninfo

    def parse_filename_header(self, s):
        parts = None
        if b'\t' in s:
            parts = s.split(b'\t', 1)
        if b'  ' in s:
            parts = re.split(b'  +', s)
        if parts:
            parts[1] = b'\t' + parts[1]
            return parts
        else:
            return [
             s.split(b'\n')[0], b'\n']

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

        The file at the location patch_file will be overwritten by the new
        patch.

        This function returns a tuple of two booleans. The first boolean
        indicates if any files have been excluded. The second boolean indicates
        if the resulting diff patch file is empty.
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
        """Apply the patch and return a PatchResult indicating its success."""
        if not is_valid_version(self.subversion_client_version, self.PATCH_MIN_VERSION):
            raise MinimumVersionError(b'Using "rbt patch" with the SVN backend requires at least svn 1.7.0')
        if base_dir and not base_dir.startswith(base_path):
            excluded, empty = self._exclude_files_not_in_tree(patch_file, base_path)
            if excluded:
                logging.warn(b'This patch was generated in a different directory. To prevent conflicts, all files not under the current directory have been excluded. To apply all files in this patch, apply this patch from the %s directory.' % base_dir)
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
        """Returns True if any empty files in the patch are applied.

        If there are no empty files in the patch or if an error occurs while
        applying the patch, we return False.
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
        """Checks if the RB server supports added/deleted empty files."""
        return self.capabilities and self.capabilities.has_capability(b'scmtools', b'svn', b'empty_files')

    def _run_svn(self, svn_args, *args, **kwargs):
        cmdline = [
         b'svn', b'--non-interactive'] + svn_args
        if getattr(self.options, b'svn_username', None):
            cmdline += [b'--username', self.options.svn_username]
        if getattr(self.options, b'svn_prompt_password', None):
            self.options.svn_prompt_password = False
            self.options.svn_password = getpass.getpass(b'SVN Password:')
        if getattr(self.options, b'svn_password', None):
            cmdline += [b'--password', self.options.svn_password]
        return execute(cmdline, *args, **kwargs)

    def svn_log_xml(self, svn_args, *args, **kwargs):
        """Run SVN log non-interactively and retrieve XML output.

        We cannot run SVN log interactively and retrieve XML output because the
        authentication prompts will be intermixed with the XML output and cause
        XML parsing to fail.

        This function returns None (as if none_on_ignored_error where True) if
        an error occurs that is not an authentication error.
        """
        command = [
         b'log', b'--xml'] + svn_args
        rc, result, errors = self._run_svn(command, return_error_code=True, with_errors=False, return_errors=True, ignore_errors=True, results_unicode=False, *args, **kwargs)
        if rc:
            if errors.startswith(b'svn: E215004'):
                raise AuthenticationError(b'Could not authenticate against remote SVN repository. Please provide the --svn-username and either the --svn-password or --svn-prompt-password command-line options.')
            return None
        return result

    def check_options(self):
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

    def __init__(self, path, base_path, uuid, repository_id=None):
        """Initialize the repository information.

        Args:
            path (unicode):
                Subversion checkout path.

            base_path (unicode):
                Root of the Subversion repository.

            uuid (unicode):
                UUID of the Subversion repository.

            repository_id (int, optional):
                ID of the repository in the API. This is used primarily for
                testing purposes, and is not guaranteed to be set.
        """
        super(SVNRepositoryInfo, self).__init__(path, base_path)
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
                return SVNRepositoryInfo(info[b'url'], relpath, self.uuid, repository_id=repository.id)

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
        split = re.split(b'/*', path)
        if split[(-1)] == b'':
            split = split[0:-1]
        return split