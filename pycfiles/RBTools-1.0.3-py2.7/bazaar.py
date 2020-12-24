# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/rbtools/clients/bazaar.py
# Compiled at: 2020-04-14 20:27:46
"""A client for Bazaar."""
from __future__ import unicode_literals
import logging, os, re
from rbtools.clients import SCMClient, RepositoryInfo
from rbtools.clients.errors import TooManyRevisionsError
from rbtools.utils.checks import check_install
from rbtools.utils.diffs import filter_diff, normalize_patterns
from rbtools.utils.process import execute
USING_PARENT_PREFIX = b'Using parent branch '

class BazaarClient(SCMClient):
    """A client for Bazaar.

    This is a wrapper that fetches repository information and generates
    compatible diffs.
    """
    name = b'Bazaar'
    supports_diff_exclude_patterns = True
    can_branch = True
    INDEX_FILE_RE = re.compile(b"===.+'(.+?)'\n")
    BRANCH_REGEX = b'\\w*(repository branch|branch root|checkout root|checkout of branch): (?P<branch_path>.+)$'
    REVISION_SEPARATOR_REGEX = re.compile(b'\\.\\.(?![\\\\/])')

    def get_repository_info(self):
        """Return repository information for the current working tree.

        Returns:
            rbtools.clients.RepositoryInfo:
            The repository info structure.
        """
        if not check_install([b'bzr', b'help']):
            logging.debug(b'Unable to execute "bzr help": skipping Bazaar')
            return
        else:
            bzr_info = execute([b'bzr', b'info'], ignore_errors=True)
            if b'ERROR: Not a branch:' in bzr_info:
                repository_info = None
            else:
                branch_match = re.search(self.BRANCH_REGEX, bzr_info, re.MULTILINE)
                path = branch_match.group(b'branch_path')
                if path == b'.':
                    path = os.getcwd()
                repository_info = RepositoryInfo(path=path, base_path=b'/', local_path=path, supports_parent_diffs=True)
            return repository_info

    def parse_revision_spec(self, revisions=[]):
        """Parse the given revision spec.

        Args:
            revisions (list of unicode, optional):
                A list of revisions as specified by the user. Items in the
                list do not necessarily represent a single revision, since the
                user can use SCM-native syntaxes such as ``r1..r2`` or
                ``r1:r2``. SCMTool-specific overrides of this method are
                expected to deal with such syntaxes.

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

            ``parent_base`` (:py:class:`unicode`, optional):
                The revision to use as the base of a parent diff.

            These will be used to generate the diffs to upload to Review Board
            (or print). The diff for review will include the changes in (base,
            tip], and the parent diff (if necessary) will include (parent,
            base].

            If a single revision is passed in, this will return the parent of
            that revision for "base" and the passed-in revision for "tip".

            If zero revisions are passed in, this will return the current HEAD
            as 'tip', and the upstream branch as 'base', taking into account
            parent branches explicitly specified via --parent.
        """
        n_revs = len(revisions)
        result = {}
        if n_revs == 0:
            result[b'tip'] = self._get_revno()
            result[b'base'] = self._get_revno(b'ancestor:')
        elif n_revs == 1 or n_revs == 2:
            if n_revs == 1:
                revisions = self.REVISION_SEPARATOR_REGEX.split(revisions[0])
                n_revs = len(revisions)
            if n_revs == 1:
                result[b'base'] = self._get_revno(b'before:' + revisions[0])
                result[b'tip'] = self._get_revno(revisions[0])
            elif n_revs == 2:
                result[b'base'] = self._get_revno(revisions[0])
                result[b'tip'] = self._get_revno(revisions[1])
            else:
                raise TooManyRevisionsError
        else:
            raise TooManyRevisionsError
        if self.options.parent_branch:
            result[b'parent_base'] = result[b'base']
            result[b'base'] = self._get_revno(b'ancestor:%s' % self.options.parent_branch)
        return result

    def _get_revno(self, revision_spec=None):
        """Convert a revision spec to a revision number.

        Args:
            revision_spec (unicode, optional):
                The revision spec to convert.

        Returns:
            unicode:
            A new revision spec that contains a revision number instead of a
            symbolic revision.
        """
        command = [
         b'bzr', b'revno']
        if revision_spec:
            command += [b'-r', revision_spec]
        result = execute(command).strip().split(b'\n')
        if len(result) == 1:
            return b'revno:' + result[0]
        if len(result) == 2 and result[0].startswith(USING_PARENT_PREFIX):
            branch = result[0][len(USING_PARENT_PREFIX):]
            return b'revno:%s:%s' % (result[1], branch)

    def diff(self, revisions, include_files=[], exclude_patterns=[], no_renames=False, extra_args=[]):
        """Perform a diff using the given revisions.

        If the revision spec is empty, this returns the diff of the current
        branch with respect to its parent. If a single revision is passed in,
        this returns the diff of the change introduced in that revision. If two
        revisions are passed in, this will do a diff between those two
        revisions.

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
                Unused for Bazaar.

        Returns:
            dict:
            A dictionary containing the following keys:

            ``diff`` (:py:class:`bytes`):
                The contents of the diff to upload.

            ``parent_diff`` (:py:class:`bytes`, optional):
                The contents of the parent diff, if available.
        """
        exclude_patterns = normalize_patterns(exclude_patterns, self.get_repository_info().path)
        diff = self._get_range_diff(revisions[b'base'], revisions[b'tip'], include_files, exclude_patterns)
        if b'parent_base' in revisions:
            parent_diff = self._get_range_diff(revisions[b'parent_base'], revisions[b'base'], include_files, exclude_patterns)
        else:
            parent_diff = None
        return {b'diff': diff, 
           b'parent_diff': parent_diff}

    def _get_range_diff(self, base, tip, include_files, exclude_patterns=[]):
        """Return the diff between 'base' and 'tip'.

        Args:
            base (unicode):
                The name of the base revision.

            tip (unicode):
                The name of the tip revision.

            include_files (list of unicode):
                A list of files to whitelist during the diff generation.

            exclude_patterns (list of unicode, optional):
                A list of shell-style glob patterns to blacklist during diff
                generation.

        Returns:
            bytes:
            The generated diff contents.
        """
        diff_cmd = [
         b'bzr', b'diff', b'-q', b'-r',
         b'%s..%s' % (base, tip)] + include_files
        diff = execute(diff_cmd, ignore_errors=True, log_output_on_error=False, split_lines=True, results_unicode=False)
        if diff:
            if exclude_patterns:
                diff = filter_diff(diff, self.INDEX_FILE_RE, exclude_patterns, base_dir=self.get_repository_info().path)
            return (b'').join(diff)
        else:
            return
            return

    def get_raw_commit_message(self, revisions):
        """Extract the commit message based on the provided revision range.

        Args:
            revisions (dict):
                A dictionary containing ``base`` and ``tip`` keys.

        Returns:
            unicode:
            The commit messages of all commits between (base, tip].
        """
        log_cmd = [
         b'bzr', b'log', b'-r',
         b'%s..%s' % (revisions[b'base'], revisions[b'tip'])]
        lines = execute(log_cmd + [b'--line'], ignore_errors=True, split_lines=True)
        n_revs = len(lines) - 1
        lines = execute(log_cmd + [b'--gnu-changelog', b'-l', str(n_revs)], ignore_errors=True, split_lines=True)
        message = []
        for line in lines:
            if line.startswith(b'\t'):
                message.append(line[1:])
            elif not line.strip():
                message.append(line)

        return (b'').join(message).strip()

    def get_current_branch(self):
        """Return the name of the current branch.

        Returns:
            unicode:
            A string with the name of the current branch.
        """
        return execute([b'bzr', b'nick'], ignore_errors=True).strip()