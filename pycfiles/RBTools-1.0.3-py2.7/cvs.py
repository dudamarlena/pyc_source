# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/rbtools/clients/cvs.py
# Compiled at: 2020-04-14 20:27:46
"""A client for CVS."""
from __future__ import unicode_literals
import logging, os, re, socket
from rbtools.clients import SCMClient, RepositoryInfo
from rbtools.clients.errors import InvalidRevisionSpecError, TooManyRevisionsError
from rbtools.utils.checks import check_install
from rbtools.utils.diffs import filter_diff, normalize_patterns
from rbtools.utils.process import execute

class CVSClient(SCMClient):
    """A client for CVS.

    This is a wrapper around the cvs executable that fetches repository
    information and generates compatible diffs.
    """
    name = b'CVS'
    supports_diff_exclude_patterns = True
    supports_patch_revert = True
    INDEX_FILE_RE = re.compile(b'^Index: (.+)\n$')
    REVISION_WORKING_COPY = b'--rbtools-working-copy'

    def get_repository_info(self):
        """Return repository information for the current working tree.

        Returns:
            rbtools.clients.RepositoryInfo:
            The repository info structure.
        """
        if not check_install([b'cvs']):
            logging.debug(b'Unable to execute "cvs": skipping CVS')
            return
        else:
            cvsroot_path = os.path.join(b'CVS', b'Root')
            if not os.path.exists(cvsroot_path):
                return
            with open(cvsroot_path, b'r') as (fp):
                repository_path = fp.read().strip()
            i = repository_path.find(b'@')
            if i != -1:
                repository_path = repository_path[i + 1:]
            i = repository_path.rfind(b':')
            if i != -1:
                host = repository_path[:i]
                try:
                    canon = socket.getfqdn(host)
                    repository_path = repository_path.replace(b'%s:' % host, b'%s:' % canon)
                except socket.error as msg:
                    logging.error(b'failed to get fqdn for %s, msg=%s', host, msg)

            return RepositoryInfo(path=repository_path, local_path=repository_path)

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

            If a single revision is passed in, this will raise an exception,
            because CVS doesn't have a repository-wide concept of "revision",
            so selecting an individual "revision" doesn't make sense.

            With two revisions, this will treat those revisions as tags and do
            a diff between those tags.

            If zero revisions are passed in, this will return revisions
            relevant for the "current change". The exact definition of what
            "current" means is specific to each SCMTool backend, and documented
            in the implementation classes.

            The CVS SCMClient never fills in the 'parent_base' key. Users who
            are using other patch-stack tools who want to use parent diffs with
            CVS will have to generate their diffs by hand.

            Because :command:`cvs diff` uses multiple arguments to define
            multiple tags, there's no single-argument/multiple-revision syntax
            available.
        """
        n_revs = len(revisions)
        if n_revs == 0:
            return {b'base': b'BASE', 
               b'tip': self.REVISION_WORKING_COPY}
        else:
            if n_revs == 1:
                raise InvalidRevisionSpecError(b'CVS does not support passing in a single revision.')
            else:
                if n_revs == 2:
                    return {b'base': revisions[0], 
                       b'tip': revisions[1]}
                raise TooManyRevisionsError
            return {b'base': None, 
               b'tip': None}

    def diff(self, revisions, include_files=[], exclude_patterns=[], no_renames=False, extra_args=[]):
        """Perform a diff using the given revisions.

        If no revisions are specified, this will return the diff for the
        modified files in the working directory. If it's not empty and contains
        two revisions, this will do a diff between those revisions.

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
                Unused for CVS.

        Returns:
            dict:
            A dictionary containing the following keys:

            ``diff`` (:py:class:`bytes`):
                The contents of the diff to upload.
        """
        cwd = os.getcwd()
        exclude_patterns = normalize_patterns(exclude_patterns, cwd, cwd)
        include_files = include_files or []
        diff_cmd = [
         b'cvs', b'diff', b'-uN']
        base = revisions[b'base']
        tip = revisions[b'tip']
        if not (base == b'BASE' and tip == self.REVISION_WORKING_COPY):
            diff_cmd.extend([b'-r', base, b'-r', tip])
        diff = execute(diff_cmd + include_files, extra_ignore_errors=(1, ), log_output_on_error=False, split_lines=True, results_unicode=False)
        if exclude_patterns:
            diff = filter_diff(diff, self.INDEX_FILE_RE, exclude_patterns, base_dir=cwd)
        return {b'diff': (b'').join(diff)}