# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/sflib/daemonize.py
# Compiled at: 2009-03-04 04:23:29
"""daemonize python library

Configurable daemon behaviors:

   1.) The current working directory set to the "/" directory.
   2.) The current file creation mode mask set to 0.
   3.) Close all open files (1024). 
   4.) Redirect standard I/O streams to "/dev/null".

A failed call to fork() now raises an exception.

References:
   1) Advanced Programming in the Unix Environment: W. Richard Stevens
   2) Unix Programming Frequently Asked Questions:
         http://www.erlenstar.demon.co.uk/unix/faq_toc.html

@see: http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/278731
@see: http://www.noah.org/wiki/Daemonize_Python
@see: http://xhtml.net/documents/scripts/djangocerise-1.2.zip
@see: http://xhtml.net/scripts/Django-CherryPy-server-DjangoCerise
@see: http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/66012
@see: http://homepage.hispeed.ch/py430/python/daemon.py

@author: Chad J. Schroeder
@copyright: Copyright (C) 2005 Chad J. Schroeder
"""
__author__ = 'Chad J. Schroeder'
__copyright__ = 'Copyright (C) 2005 Chad J. Schroeder'
__revision__ = '$Id$'
__version__ = '0.2'
__contributors__ = [
 'Marco Pantaleoni <panta@elasticworld.org>']
import os, sys, pwd
from sflib import lockfile as lfile
UMASK = 0
WORKDIR = '/'
MAXFD = 1024
if hasattr(os, 'devnull'):
    REDIRECT_TO = os.devnull
else:
    REDIRECT_TO = '/dev/null'

def change_uid_gid(uid, gid=None):
    """Try to change UID and GID to the provided values.
    UID and GID are given as names like 'nobody' not integer.

    Src: http://mail.mems-exchange.org/durusmail/quixote-users/4940/1/
    """
    if not uid:
        return
    if not (os.geteuid() == 0 or os.getuid() == 0):
        return
    (uid, gid) = get_uid_gid(uid, gid)
    os.setgid(gid)
    os.setuid(uid)


def get_uid_gid(uid, gid=None):
    """Try to get the UID and GID numeric values corresponding to
    the provided symbolic ones.

    Src: http://mail.mems-exchange.org/durusmail/quixote-users/4940/1/
    """
    import pwd, grp
    default_grp = None
    if uid:
        (uid, default_grp) = pwd.getpwnam(uid)[2:4]
    if not gid:
        gid = default_grp
    else:
        assert gid is not None
        assert gid != ''
        try:
            gid = grp.getgrnam(gid)[2]
        except KeyError:
            gid = default_grp

    return (
     uid, gid)


def chown_files(filenames, uid, gid=None):
    if not (os.geteuid() == 0 or os.getuid() == 0):
        return
    (uid, gid) = get_uid_gid(uid, gid)
    if uid or gid:
        for filename in filenames:
            if os.path.exists(filename):
                os.chown(filename, uid, gid)


def log_info(log, msg):
    if log is not None:
        log.info(msg)
    return


def log_debug(log, msg):
    if log is not None:
        log.debug(msg)
    return


class RedirectedFileStub(object):
    """
    A file-like duck-typed class, used to replace sys.stderr and sys.stdout,
    making them point to a logging object.
    """
    __module__ = __name__

    def __init__(self, log):
        self.log = log

    def flush(self):
        pass

    def close(self):
        pass

    def write(self, text):
        if text and text[(-1)] == '\n':
            text = text[:-1]
        self.log.debug(text)


def daemonize(pidfile=None, lockfile=None, run_as_user=None, run_as_group=None, workdir=WORKDIR, umask=UMASK, redirect_to=REDIRECT_TO, maxfd=MAXFD, files_for_child=[], log=None, loggers=None, stdout_log=None, stderr_log=None):
    """
    Detach a process from the controlling terminal and run it in the
    background as a daemon.
    """
    log_info(log, 'Daemonizing...')
    if os.getppid() == 1:
        log_debug(log, 'already a daemon. Returning.')
        return True
    locked = False
    if lockfile:
        locked = lfile.get_lock(lockfile)
        if not locked:
            sys.stderr.write("can't obtain a lock ('%s' exists).\n" % lockfile)
            sys.exit(1)
            return False
    try:
        pid = os.fork()
    except OSError, e:
        raise Exception, '%s [%d]' % (e.strerror, e.errno)

    if pid > 0:
        assert pid != 0
        os._exit(0)
    assert pid == 0
    os.setsid()
    try:
        pid = os.fork()
    except OSError, e:
        raise Exception, '%s [%d]' % (e.strerror, e.errno)

    if pid > 0:
        assert pid > 0
        if locked:
            fh = open(lockfile, 'w')
            fh.write('%d\n' % pid)
            fh.close()
        fh = open(pidfile, 'w')
        fh.write('%d\n' % pid)
        fh.close()
        if run_as_user or run_as_group:
            chown_files([pidfile, lockfile] + list(files_for_child), run_as_user, run_as_group)
        os._exit(0)
    assert pid == 0
    os.chdir(workdir)
    os.umask(umask)
    import resource
    l_maxfd = resource.getrlimit(resource.RLIMIT_NOFILE)[1]
    if l_maxfd == resource.RLIM_INFINITY:
        l_maxfd = maxfd
    log_fds = []
    for logger in loggers:
        _log = logger
        while _log is not None:
            import logging
            assert isinstance(_log, logging.Logger)
            for hdlr in _log.handlers:
                if isinstance(hdlr, logging.StreamHandler):
                    assert isinstance(hdlr, logging.StreamHandler)
                    fd = hdlr.stream.fileno()
                    if fd not in log_fds:
                        log_fds.append(fd)

            _log = _log.parent

    if stdout_log is not None:
        sys.stdout = RedirectedFileStub(stdout_log)
    if stderr_log is not None:
        sys.stderr = RedirectedFileStub(stderr_log)
    for fd in range(0, l_maxfd):
        try:
            if fd not in log_fds:
                os.close(fd)
            else:
                log_debug(log, 'skipping close(%s)' % fd)
        except OSError:
            pass

    os.open(redirect_to, os.O_RDWR)
    os.dup2(0, 1)
    os.dup2(0, 2)
    if run_as_user or run_as_group:
        change_uid_gid(run_as_user, run_as_group)
    return True


if __name__ == '__main__':
    if not daemonize():
        sys.exit(1)
    procParams = '\n               return code = %s\n               process ID = %s\n               parent process ID = %s\n               process group ID = %s\n               session ID = %s\n               user ID = %s\n               effective user ID = %s\n               real group ID = %s\n               effective group ID = %s\n               ' % (retCode, os.getpid(), os.getppid(), os.getpgrp(), os.getsid(0), os.getuid(), os.geteuid(), os.getgid(), os.getegid())
    open('daemonize.log', 'w').write(procParams + '\n')
    sys.exit(retCode)