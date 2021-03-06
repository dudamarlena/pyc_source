# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-hbx1i2h0/pip/pip/_internal/vcs/subversion.py
# Compiled at: 2020-04-16 14:32:34
# Size of source mod 2**32: 12292 bytes
from __future__ import absolute_import
import logging, os, re
from pip._internal.utils.logging import indent_log
from pip._internal.utils.misc import display_path, is_console_interactive, rmtree, split_auth_from_netloc
from pip._internal.utils.subprocess import make_command
from pip._internal.utils.typing import MYPY_CHECK_RUNNING
from pip._internal.vcs.versioncontrol import VersionControl, vcs
_svn_xml_url_re = re.compile('url="([^"]+)"')
_svn_rev_re = re.compile('committed-rev="(\\d+)"')
_svn_info_xml_rev_re = re.compile('\\s*revision="(\\d+)"')
_svn_info_xml_url_re = re.compile('<url>(.*)</url>')
if MYPY_CHECK_RUNNING:
    from typing import Optional, Tuple
    from pip._internal.utils.subprocess import CommandArgs
    from pip._internal.utils.misc import HiddenText
    from pip._internal.vcs.versioncontrol import AuthInfo, RevOptions
logger = logging.getLogger(__name__)

class Subversion(VersionControl):
    name = 'svn'
    dirname = '.svn'
    repo_name = 'checkout'
    schemes = ('svn', 'svn+ssh', 'svn+http', 'svn+https', 'svn+svn')

    @classmethod
    def should_add_vcs_url_prefix(cls, remote_url):
        return True

    @staticmethod
    def get_base_rev_args(rev):
        return ['-r', rev]

    @classmethod
    def get_revision(cls, location):
        """
        Return the maximum revision for all files under a given location
        """
        revision = 0
        for base, dirs, files in os.walk(location):
            if cls.dirname not in dirs:
                dirs[:] = []
                continue
            else:
                dirs.remove(cls.dirname)
                entries_fn = os.path.join(base, cls.dirname, 'entries')
                if not os.path.exists(entries_fn):
                    continue
                dirurl, localrev = cls._get_svn_url_rev(base)
                if base == location:
                    base = dirurl + '/'
                else:
                    dirs[:] = dirurl and dirurl.startswith(base) or []
                    continue
            revision = max(revision, localrev)

        return revision

    @classmethod
    def get_netloc_and_auth(cls, netloc, scheme):
        if scheme == 'ssh':
            return super(Subversion, cls).get_netloc_and_auth(netloc, scheme)
        return split_auth_from_netloc(netloc)

    @classmethod
    def get_url_rev_and_auth(cls, url):
        url, rev, user_pass = super(Subversion, cls).get_url_rev_and_auth(url)
        if url.startswith('ssh://'):
            url = 'svn+' + url
        return (
         url, rev, user_pass)

    @staticmethod
    def make_rev_args(username, password):
        extra_args = []
        if username:
            extra_args += ['--username', username]
        if password:
            extra_args += ['--password', password]
        return extra_args

    @classmethod
    def get_remote_url(cls, location):
        orig_location = location
        while not os.path.exists(os.path.join(location, 'setup.py')):
            last_location = location
            location = os.path.dirname(location)
            if location == last_location:
                logger.warning('Could not find setup.py for directory %s (tried all parent directories)', orig_location)
                return

        return cls._get_svn_url_rev(location)[0]

    @classmethod
    def _get_svn_url_rev(cls, location):
        from pip._internal.exceptions import InstallationError
        entries_path = os.path.join(location, cls.dirname, 'entries')
        if os.path.exists(entries_path):
            with open(entries_path) as (f):
                data = f.read()
        else:
            data = ''
        if not data.startswith('8'):
            if data.startswith('9') or data.startswith('10'):
                data = list(map(str.splitlines, data.split('\n\x0c\n')))
                del data[0][0]
                url = data[0][3]
                revs = [int(d[9]) for d in data if len(d) > 9 if d[9]] + [0]
        elif data.startswith('<?xml'):
            match = _svn_xml_url_re.search(data)
            if not match:
                raise ValueError('Badly formatted data: %r' % data)
            url = match.group(1)
            revs = [int(m.group(1)) for m in _svn_rev_re.finditer(data)] + [0]
        else:
            try:
                xml = cls.run_command([
                 'info', '--xml', location],
                  show_stdout=False)
                url = _svn_info_xml_url_re.search(xml).group(1)
                revs = [int(m.group(1)) for m in _svn_info_xml_rev_re.finditer(xml)]
            except InstallationError:
                url, revs = None, []

            if revs:
                rev = max(revs)
            else:
                rev = 0
        return (
         url, rev)

    @classmethod
    def is_commit_id_equal(cls, dest, name):
        """Always assume the versions don't match"""
        return False

    def __init__(self, use_interactive=None):
        if use_interactive is None:
            use_interactive = is_console_interactive()
        self.use_interactive = use_interactive
        self._vcs_version = None
        super(Subversion, self).__init__()

    def call_vcs_version(self):
        """Query the version of the currently installed Subversion client.

        :return: A tuple containing the parts of the version information or
            ``()`` if the version returned from ``svn`` could not be parsed.
        :raises: BadCommand: If ``svn`` is not installed.
        """
        version_prefix = 'svn, version '
        version = self.run_command(['--version'], show_stdout=False)
        if not version.startswith(version_prefix):
            return ()
        version = version[len(version_prefix):].split()[0]
        version_list = version.split('.')
        try:
            parsed_version = tuple(map(int, version_list))
        except ValueError:
            return ()
        else:
            return parsed_version

    def get_vcs_version(self):
        """Return the version of the currently installed Subversion client.

        If the version of the Subversion client has already been queried,
        a cached value will be used.

        :return: A tuple containing the parts of the version information or
            ``()`` if the version returned from ``svn`` could not be parsed.
        :raises: BadCommand: If ``svn`` is not installed.
        """
        if self._vcs_version is not None:
            return self._vcs_version
        vcs_version = self.call_vcs_version()
        self._vcs_version = vcs_version
        return vcs_version

    def get_remote_call_options(self):
        """Return options to be used on calls to Subversion that contact the server.

        These options are applicable for the following ``svn`` subcommands used
        in this class.

            - checkout
            - export
            - switch
            - update

        :return: A list of command line arguments to pass to ``svn``.
        """
        if not self.use_interactive:
            return [
             '--non-interactive']
        svn_version = self.get_vcs_version()
        if svn_version >= (1, 8):
            return [
             '--force-interactive']
        return []

    def export(self, location, url):
        """Export the svn repository at the url to the destination location"""
        url, rev_options = self.get_url_rev_options(url)
        logger.info('Exporting svn repository %s to %s', url, location)
        with indent_log():
            if os.path.exists(location):
                rmtree(location)
            cmd_args = make_command('export', self.get_remote_call_options(), rev_options.to_args(), url, location)
            self.run_command(cmd_args, show_stdout=False)

    def fetch_new(self, dest, url, rev_options):
        rev_display = rev_options.to_display()
        logger.info('Checking out %s%s to %s', url, rev_display, display_path(dest))
        cmd_args = make_command('checkout', '-q', self.get_remote_call_options(), rev_options.to_args(), url, dest)
        self.run_command(cmd_args)

    def switch(self, dest, url, rev_options):
        cmd_args = make_command('switch', self.get_remote_call_options(), rev_options.to_args(), url, dest)
        self.run_command(cmd_args)

    def update(self, dest, url, rev_options):
        cmd_args = make_command('update', self.get_remote_call_options(), rev_options.to_args(), dest)
        self.run_command(cmd_args)


vcs.register(Subversion)