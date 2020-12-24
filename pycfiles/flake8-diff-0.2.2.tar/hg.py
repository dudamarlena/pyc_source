# uncompyle6 version 3.7.4
# PyPy Python bytecode 2.7 (62218)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/greg/Dropbox/code/dealertrack/flake8-diff/flake8diff/vcs/hg.py
# Compiled at: 2015-07-06 16:58:51
from __future__ import unicode_literals, print_function
import logging, subprocess
from ..utils import _execute
from .base import VCSBase
logger = logging.getLogger(__name__)

class HgVCS(VCSBase):
    """
    Mercurial support implementation
    """
    name = b'hg'

    def get_vcs(self):
        """
        Get git binary executable path
        """
        vcs = _execute(b'which hg', strict=True).strip()
        return vcs

    def is_used(self):
        """
        Determines if this VCS should be used
        """
        try:
            self._is_mercurial_repository()
        except subprocess.CalledProcessError:
            return False

        return True

    def changed_lines(self, filename):
        """
        Get a list of all lines changed by this set of commits.
        """
        commits = [ (b'-r {}').format(c) ]
        command_arguments = [
         b'--program=diff',
         b'\'--option=--new-line-format="%dn "\'',
         b'\'--option=--unchanged-line-format=""\'',
         b'\'--option=--changed-group-format="%>"\'',
         filename]
        command = [
         self.vcs, b'extdiff'] + commits + command_arguments
        result = _execute((b' ').join(command))
        result = result.replace(b'"', b'').strip().split(b' ')
        return result

    def changed_files(self):
        """
        Return a list of all changed files.
        """
        commits = [ (b'-r {}').format(c) ]
        command = [
         self.vcs, b'diff', b'--stat'] + commits
        result = _execute((b' ').join(command))
        lines = result.strip().split(b'\n')[:-1]
        files = [ line.split(b'|')[0].strip() ]
        return filter(self.filter_file, files)

    def check(self):
        try:
            _execute((b'{vcs} extdiff').format(vcs=self.vcs), strict=True, log_errors=False)
        except subprocess.CalledProcessError:
            message = b"Mercurial 'extdiff' extension is disabled.\nPlease add the following lines to your ~/.hgrc\n\n[extensions]\nextdiff = \n"
            print(message)
            raise Exception(b"Please enable 'extdiff' extension")

        return True

    def _is_mercurial_repository(self):
        return _execute((b'{vcs} status').format(vcs=self.vcs), strict=True, log_errors=False)