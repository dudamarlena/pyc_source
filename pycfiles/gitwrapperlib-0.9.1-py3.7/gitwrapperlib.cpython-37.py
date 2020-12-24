# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/gitwrapperlib/gitwrapperlib.py
# Compiled at: 2019-01-18 03:11:30
# Size of source mod 2**32: 6022 bytes
"""
Main code for gitwrapperlib

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""
import logging, sys, re
try:
    import sh
except ImportError:
    import pbs

    class Sh(object):
        __doc__ = '\n        Overloading pbs to look like sh\n\n        https://stackoverflow.com/questions/28618906/porting-sh-1-11-based-code-to-windows\n        '

        def __getattr__(self, attr):
            return pbs.Command(attr)


    sh = Sh()

from .gitwrapperlibexceptions import ExecutableNotFound
__author__ = 'Costas Tyfoxylos <costas.tyf@gmail.com>'
__docformat__ = 'google'
__date__ = '2018-01-02'
__copyright__ = 'Copyright 2018, Costas Tyfoxylos'
__credits__ = ['Costas Tyfoxylos']
__license__ = 'MIT'
__maintainer__ = 'Costas Tyfoxylos'
__email__ = '<costas.tyf@gmail.com>'
__status__ = 'Development'
LOGGER_BASENAME = 'gitwrapperlib'
LOGGER = logging.getLogger(LOGGER_BASENAME)
LOGGER.addHandler(logging.NullHandler())

class Git(object):
    __doc__ = 'Models the git command and contstructs some extra helper methods'
    passthrough_methods = ('init', 'pull')
    argument_methods = ('add', 'clone', 'push')

    def __init__(self):
        logger_name = '{base}.{suffix}'.format(base=LOGGER_BASENAME, suffix=(self.__class__.__name__))
        self._logger = logging.getLogger(logger_name)
        self._git = self._get_command()

    @staticmethod
    def _get_command():
        if sys.platform in ('win32', 'cygwin'):
            try:
                sh.git()
            except WindowsError:
                raise ExecutableNotFound
            except pbs.ErrorReturnCode_1:
                git = sh.git

        else:
            try:
                git = sh.Command('git')
            except sh.CommandNotFound:
                raise ExecutableNotFound

            return git

    def __getattr__(self, name):
        if name in self.passthrough_methods:
            return getattr(self._git, name)
        if name in self.argument_methods:

            def wrapper(*args, **kwargs):
                return (getattr(self._git, name))(*args, **kwargs)

            return wrapper

    def remove(self, path):
        """Removes a path with force"""
        self._git.rm('-rf', path)

    def add_forced(self, path):
        """Adds a path with force"""
        self._git.add('-f', path)

    def commit(self, message, *args):
        """Commits"""
        (self._git.commit)('-m', message, *args)

    def add_remote_origin(self, url):
        """Adds the remote origin"""
        self._git.remote('add', 'origin', url)

    def push_master(self):
        """Pushes to master"""
        self._git.push('origin', 'master')

    def push_force_master(self):
        """Pushes to master"""
        self._git.push('origin', 'master', '--force')

    def push_force_branch(self, branch):
        """Pushes to master"""
        self._git.push('origin', branch, '--force')

    def branch_upstream_to_master(self):
        """Branches upstream to master"""
        self._git.branch('-u', 'origin/master')

    def get_branches(self):
        """Returns a list of the branches"""
        return [self._sanitize(branch) for branch in self._git.branch(color='never').splitlines()]

    @staticmethod
    def _sanitize(value):
        if value.startswith('*'):
            value = value.split()[1]
        ansi_escape = re.compile('\\x1B\\[[0-?]*[ -/]*[@-~]')
        value = ansi_escape.sub('', value.strip())
        return value

    def get_current_branch(self):
        """Returns the currently active branch"""
        return next((self._sanitize(branch) for branch in self._git.branch(color='never').splitlines() if branch.startswith('*')), None)

    def create_branch(self, name):
        """Creates a branch"""
        self._git.branch(name)

    def remove_branch(self, name):
        """Removes a branch"""
        self._git.branch('-d', name)

    def switch_branch(self, name):
        """Switches to a branch"""
        self._git.checkout(name)

    def list_tags(self):
        """Lists existing tags"""
        return self._git.tag()

    def add_tag(self, value):
        """Tag with provided value"""
        self._git.tag(value)

    def delete_tag(self, value):
        """Delete the tag provided"""
        self._git.tag('-d', value)

    def create_patch(self, from_tag, to_tag):
        """Create a patch between tags"""
        return str(self._git.diff(('{}..{}'.format(from_tag, to_tag)), _tty_out=False))