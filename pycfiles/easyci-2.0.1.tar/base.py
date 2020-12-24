# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/naphatkrit/Dropbox/Documents/code/easyci/easyci/vcs/base.py
# Compiled at: 2015-09-07 02:44:46
"""
This module is inspired by the open-sourced project Changes:
https://github.com/dropbox/changes
"""
from __future__ import absolute_import
import os, os.path
from contextlib import contextmanager
from subprocess32 import Popen, PIPE, check_call
from easyci.utils import contextmanagers

class CommandError(Exception):

    def __init__(self, cmd, retcode, stdout, stderr):
        self.cmd = cmd
        self.retcode = retcode
        self.stdout = stdout
        self.stderr = stderr

    def __unicode__(self):
        return '%s returned %d:\nSTDOUT: %r\nSTDERR: %r' % (
         self.cmd, self.retcode, self.stdout, self.stderr)

    def __str__(self):
        return self.__unicode__().encode('utf-8')


class Vcs(object):

    def __init__(self, path=None):
        """Initialize a new Vcs object for a repository located at `path`.
        If `path` is `None`, then `get_working_directory` is used to identify
        the path.

        Args:
            path (str) - optional. The path to the repo working directory.
        """
        self.path = None
        if path is None:
            self.path = self.get_working_directory()
        else:
            self.path = path
        assert self.exists()
        return

    def run(self, *args, **kwargs):
        if self.path is not None:
            kwargs.setdefault('cwd', self.path)
        kwargs['env'] = {}
        kwargs['stdout'] = PIPE
        kwargs['stderr'] = PIPE
        proc = Popen(args, **kwargs)
        stdout, stderr = proc.communicate()
        if proc.returncode != 0:
            raise CommandError(args[0], proc.returncode, stdout, stderr)
        return stdout

    def exists(self):
        """Check if the working directory exists

        Returns:
            bool - True if the working directory exists
        """
        return os.path.exists(self.path)

    def get_working_directory(self):
        """Get the working directory for this repo.

        Args:
            cls (class object): The class

        Returns:
            str - the path to the working directory

        Raises:
            CommandError
        """
        raise NotImplementedError

    def install_hook(self, hook_name, hook_content):
        """Install the repository hook for this repo.

        Args:
            hook_name (str)
            hook_content (str)
        """
        raise NotImplementedError

    def remove_ignored_files(self):
        """Remove files ignored by the repository
        """
        raise NotImplementedError

    def remove_unstaged_files(self):
        """Remove all unstaged files. This does NOT remove ignored files.

        TODO this may be specific to git?
        """
        raise NotImplementedError

    def clear(self, target_commit):
        """Resets the repository to the target commit, removing any staged,
        unstaged, and untracked files.

        Args:
            target_commit (str): the commit ID
        Raises:
            CommandError - if the commit does not exist
        """
        raise NotImplementedError

    def private_dir(self):
        """Get the private directory associated with this repo, but untracked
        by the repo.

        Returns:
            str - absolute path
        """
        raise NotImplementedError

    def repository_dir(self):
        """Get the directory used by the VCS to store repository info.

        e.g. .git for git

        Returns:
            str - absolute path
        """
        raise NotImplementedError

    def get_signature(self):
        """Get the signature of the current state of the repository

        Returns:
            str
        """
        raise NotImplementedError

    def ignore_patterns_file(self):
        """The ignore patterns file for this repo type.

        e.g. .gitignore for git

        Returns:
            str - file name
        """
        raise NotImplementedError

    def path_is_ignored(self, path):
        """Given a path, check if the path would be ignored.

        Returns:
            boolean
        """
        raise NotImplementedError

    def get_ignored_files(self):
        """Returns the list of files being ignored in this repository.

        Note that file names, not directories, are returned.

        So, we will get the following:

        a/b.txt
        a/c.txt

        instead of just:

        a/

        Returns:
            List[str] - list of ignored files. The paths are relative to the repo.
        """
        raise NotImplementedError

    @contextmanager
    def temp_copy(self):
        """Yields a new Vcs object that represents a temporary, disposable
        copy of the current repository. The copy is deleted at the end
        of the context.

        The following are not copied:
        - ignored files
        - easyci private directory (.git/eci for git)

        Yields:
            Vcs
        """
        with contextmanagers.temp_dir() as (temp_dir):
            temp_root_path = os.path.join(temp_dir, 'root')
            path = os.path.join(self.path, '')
            check_call(['rsync', '-r', ('--exclude={}').format(self.private_dir()),
             ('--filter=dir-merge,- {}').format(self.ignore_patterns_file()), path, temp_root_path])
            copy = self.__class__(path=temp_root_path)
            yield copy