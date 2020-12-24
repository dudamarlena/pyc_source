# uncompyle6 version 3.7.4
# PyPy Python bytecode 2.7 (62218)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/greg/Dropbox/code/dealertrack/flake8-diff/flake8diff/vcs/git.py
# Compiled at: 2015-07-06 16:58:51
from __future__ import unicode_literals, print_function
import logging, subprocess
from ..utils import _execute
from .base import VCSBase
logger = logging.getLogger(__name__)

class GitVCS(VCSBase):
    """
    Git support implementation
    """
    name = b'git'

    def get_vcs(self):
        """
        Get git binary executable path
        """
        return _execute(b'which git', strict=True).strip()

    def is_used(self):
        """
        Determines if this VCS should be used
        """
        try:
            self._is_git_repository()
        except subprocess.CalledProcessError:
            return False

        return True

    def changed_lines(self, filename):
        """
        Get a list of all lines changed by this set of commits.
        """
        diff_command = [
         b'diff',
         b'--new-line-format="%dn "',
         b'--unchanged-line-format=""',
         b'--changed-group-format="%>"']
        difftool_command = [
         self.vcs,
         b'difftool',
         b'-y',
         b'-x',
         (b"'{0}'").format((b' ').join(diff_command))]
        cmd = filter(None, difftool_command + self.commits + [
         b'--',
         filename])
        return _execute((b' ').join(cmd)).split()

    def changed_files(self):
        """
        Return a list of all changed files.
        """
        command = filter(None, [
         self.vcs,
         b'diff',
         b'--name-only'] + self.commits)
        return filter(self.filter_file, iter(_execute((b' ').join(command)).splitlines()))

    def _is_git_repository(self):
        return _execute((b'{vcs} status').format(vcs=self.vcs), strict=True, log_errors=False)