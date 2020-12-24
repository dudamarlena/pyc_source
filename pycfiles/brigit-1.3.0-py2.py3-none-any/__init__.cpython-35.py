# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/zero/github/kozea/brigit/build/lib/brigit/__init__.py
# Compiled at: 2016-06-20 09:23:13
# Size of source mod 2**32: 4013 bytes
"""
briGit - Very simple git wrapper module

"""
import logging
from logging import getLogger
import os
from subprocess import Popen, PIPE
from datetime import datetime
handler = None
try:
    from log_colorizer import make_colored_stream_handler
    handler = make_colored_stream_handler()
except ImportError:
    handler = logging.StreamHandler()

class NullHandler(logging.Handler):
    __doc__ = 'Handler that do nothing'

    def emit(self, record):
        """Do nothing"""
        pass


class GitException(Exception):
    __doc__ = 'Exception raised when something went wrong for git'

    def __init__(self, message):
        super(GitException, self).__init__(message)


class RawGit(object):
    __doc__ = 'Git command wrapper'

    def __init__(self, git_path, encoding='utf-8'):
        """Init a Git wrapper with an instance"""
        self.path = git_path
        self.encoding = encoding

    def __call__(self, command, *args, **kwargs):
        """Run a command with args as arguments."""
        full_command = (
         'git', command) + tuple(('--%s=%s' % (key, value) if len(key) > 1 else '-%s %s' % (key, value)) for key, value in list(kwargs.items())) + args
        self.logger.info('> %s' % ' '.join(full_command))
        process = Popen(full_command, stdout=PIPE, stderr=PIPE, cwd=self.path)
        out, err = process.communicate()
        out = out.decode(self.encoding)
        err = err.decode(self.encoding)
        self.logger.debug('%s' % out)
        retcode = process.poll()
        if retcode:
            if err:
                self.logger.error('%s' % err)
            raise GitException('%s has returned %d - error was %s' % (
             ' '.join(full_command), retcode, err))
        return out

    def __getattr__(self, name):
        """Any method not implemented will be executed as is."""
        return lambda *args**args: self(name, *args, **kwargs)


class Git(RawGit):
    __doc__ = 'Utility class overloading most used functions'

    def __init__(self, git_path, remote=None, quiet=True, bare=False):
        """Init the repo or clone the remote if remote is not None."""
        if '~' in git_path:
            git_path = os.path.expanduser(git_path)
        super(Git, self).__init__(git_path)
        dirpath = os.path.dirname(self.path)
        basename = os.path.basename(self.path)
        self.logger = getLogger('brigit')
        if not quiet:
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.addHandler(NullHandler())
        if not os.path.exists(self.path):
            if remote:
                if not os.path.exists(dirpath):
                    os.makedirs(dirpath)
                self.path = dirpath
                self.clone(remote, basename, '--recursive')
                self.path = git_path
        else:
            os.makedirs(self.path)
            if bare:
                self.init('--bare')
            else:
                self.init()
        self.remote_path = remote

    def pretty_log(self, *args, **kwargs):
        """Return the log as a list of dict"""
        kwargs['pretty'] = 'format:%H;;%an;;%ae;;%at;;%s'
        for line in self.log(*args, **kwargs).split('\n'):
            fields = line.split(';;')
            yield {'hash': fields[0], 
             'author': {'name': fields[1], 
                        'email': fields[2]}, 
             
             'datetime': datetime.fromtimestamp(float(fields[3])), 
             'message': fields[4]}