# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-sin1koo5/pip/pip/_internal/vcs/bazaar.py
# Compiled at: 2019-07-30 18:46:55
# Size of source mod 2**32: 3182 bytes
from __future__ import absolute_import
import logging, os
from pip._vendor.six.moves.urllib import parse as urllib_parse
from pip._internal.utils.misc import display_path, path_to_url, rmtree
from pip._internal.vcs.versioncontrol import VersionControl, vcs
logger = logging.getLogger(__name__)

class Bazaar(VersionControl):
    name = 'bzr'
    dirname = '.bzr'
    repo_name = 'branch'
    schemes = ('bzr', 'bzr+http', 'bzr+https', 'bzr+ssh', 'bzr+sftp', 'bzr+ftp', 'bzr+lp')

    def __init__(self, *args, **kwargs):
        (super(Bazaar, self).__init__)(*args, **kwargs)
        if getattr(urllib_parse, 'uses_fragment', None):
            urllib_parse.uses_fragment.extend(['lp'])

    @staticmethod
    def get_base_rev_args(rev):
        return ['-r', rev]

    def export(self, location, url):
        """
        Export the Bazaar repository at the url to the destination location
        """
        if os.path.exists(location):
            rmtree(location)
        url, rev_options = self.get_url_rev_options(url)
        self.run_command(([
         'export', location, url] + rev_options.to_args()),
          show_stdout=False)

    def fetch_new(self, dest, url, rev_options):
        rev_display = rev_options.to_display()
        logger.info('Checking out %s%s to %s', url, rev_display, display_path(dest))
        cmd_args = [
         'branch', '-q'] + rev_options.to_args() + [url, dest]
        self.run_command(cmd_args)

    def switch(self, dest, url, rev_options):
        self.run_command(['switch', url], cwd=dest)

    def update(self, dest, url, rev_options):
        cmd_args = [
         'pull', '-q'] + rev_options.to_args()
        self.run_command(cmd_args, cwd=dest)

    @classmethod
    def get_url_rev_and_auth(cls, url):
        url, rev, user_pass = super(Bazaar, cls).get_url_rev_and_auth(url)
        if url.startswith('ssh://'):
            url = 'bzr+' + url
        return (
         url, rev, user_pass)

    @classmethod
    def get_remote_url(cls, location):
        urls = cls.run_command(['info'], show_stdout=False, cwd=location)
        for line in urls.splitlines():
            line = line.strip()
            for x in ('checkout of branch: ', 'parent branch: '):
                if line.startswith(x):
                    repo = line.split(x)[1]
                    if cls._is_local_repository(repo):
                        return path_to_url(repo)
                    else:
                        return repo

    @classmethod
    def get_revision(cls, location):
        revision = cls.run_command([
         'revno'],
          show_stdout=False, cwd=location)
        return revision.splitlines()[(-1)]

    @classmethod
    def is_commit_id_equal(cls, dest, name):
        """Always assume the versions don't match"""
        return False


vcs.register(Bazaar)