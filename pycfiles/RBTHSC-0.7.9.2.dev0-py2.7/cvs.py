# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\rbtools\clients\cvs.py
# Compiled at: 2017-04-19 05:14:02
import logging, os, re, socket
from rbtools.clients import SCMClient, RepositoryInfo
from rbtools.clients.errors import InvalidRevisionSpecError, TooManyRevisionsError
from rbtools.utils.checks import check_install
from rbtools.utils.diffs import filter_diff, normalize_patterns
from rbtools.utils.process import execute

class CVSClient(SCMClient):
    """
    A wrapper around the cvs tool that fetches repository
    information and generates compatible diffs.
    """
    name = 'CVS'
    supports_diff_exclude_patterns = True
    supports_patch_revert = True
    INDEX_FILE_RE = re.compile('^Index: (.+)\n$')
    REVISION_WORKING_COPY = '--rbtools-working-copy'

    def __init__(self, **kwargs):
        super(CVSClient, self).__init__(**kwargs)

    def get_repository_info(self):
        if not check_install(['cvs']):
            logging.debug('Unable to execute "cvs": skipping CVS')
            return
        else:
            cvsroot_path = os.path.join('CVS', 'Root')
            if not os.path.exists(cvsroot_path):
                return
            with open(cvsroot_path, 'r') as (fp):
                repository_path = fp.read().strip()
            i = repository_path.find('@')
            if i != -1:
                repository_path = repository_path[i + 1:]
            i = repository_path.rfind(':')
            if i != -1:
                host = repository_path[:i]
                try:
                    canon = socket.getfqdn(host)
                    repository_path = repository_path.replace('%s:' % host, '%s:' % canon)
                except socket.error as msg:
                    logging.error('failed to get fqdn for %s, msg=%s', host, msg)

            return RepositoryInfo(path=repository_path)

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

        If a single revision is passed in, this will raise an exception,
        because CVS doesn't have a repository-wide concept of "revision", so
        selecting an individual "revision" doesn't make sense.

        With two revisions, this will treat those revisions as tags and do a
        diff between those tags.

        If zero revisions are passed in, this will return revisions relevant
        for the "current change". The exact definition of what "current" means
        is specific to each SCMTool backend, and documented in the
        implementation classes.

        The CVS SCMClient never fills in the 'parent_base' key. Users who are
        using other patch-stack tools who want to use parent diffs with CVS
        will have to generate their diffs by hand.

        Because `cvs diff` uses multiple arguments to define multiple tags,
        there's no single-argument/multiple-revision syntax available.
        """
        n_revs = len(revisions)
        if n_revs == 0:
            return {'base': 'BASE', 
               'tip': self.REVISION_WORKING_COPY}
        else:
            if n_revs == 1:
                raise InvalidRevisionSpecError('CVS does not support passing in a single revision.')
            else:
                if n_revs == 2:
                    return {'base': revisions[0], 
                       'tip': revisions[1]}
                raise TooManyRevisionsError
            return {'base': None, 
               'tip': None}

    def diff(self, revisions, include_files=[], exclude_patterns=[], extra_args=[]):
        """Get the diff for the given revisions.

        If revision_spec is empty, this will return the diff for the modified
        files in the working directory. If it's not empty and contains two
        revisions, this will do a diff between those revisions.
        """
        cwd = os.getcwd()
        exclude_patterns = normalize_patterns(exclude_patterns, cwd, cwd)
        include_files = include_files or []
        diff_cmd = [
         'cvs', 'diff', '-uN']
        base = revisions['base']
        tip = revisions['tip']
        if not (base == 'BASE' and tip == self.REVISION_WORKING_COPY):
            diff_cmd.extend(['-r', base, '-r', tip])
        diff = execute(diff_cmd + include_files, extra_ignore_errors=(1, ), log_output_on_error=False, split_lines=True)
        if exclude_patterns:
            diff = filter_diff(diff, self.INDEX_FILE_RE, exclude_patterns, base_dir=cwd)
        return {'diff': ('').join(diff)}