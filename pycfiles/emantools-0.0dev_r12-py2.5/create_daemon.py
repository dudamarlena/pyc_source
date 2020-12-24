# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/emantools/create_daemon.py
# Compiled at: 2008-04-06 23:55:06
"""Disk And Execution MONitor (Daemon)

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
"""
__author__ = 'Chad J. Schroeder'
__copyright__ = 'Copyright (C) 2005 Chad J. Schroeder'
__revision__ = '$Id$'
__version__ = '0.2'
import os, sys
UMASK = 0
WORKDIR = '/'
MAXFD = 1024
if hasattr(os, 'devnull'):
    REDIRECT_TO = os.devnull
else:
    REDIRECT_TO = '/dev/null'

def createDaemon():
    """Detach a process from the controlling terminal and run it in the
   background as a daemon.
   """
    try:
        pid = os.fork()
    except OSError, e:
        raise Exception, '%s [%d]' % (e.strerror, e.errno)

    if pid == 0:
        os.setsid()
        try:
            pid = os.fork()
        except OSError, e:
            raise Exception, '%s [%d]' % (e.strerror, e.errno)
        else:
            if pid == 0:
                os.chdir(WORKDIR)
                os.umask(UMASK)
            else:
                os._exit(0)
    else:
        os._exit(0)
    import resource
    maxfd = resource.getrlimit(resource.RLIMIT_NOFILE)[1]
    if maxfd == resource.RLIM_INFINITY:
        maxfd = MAXFD
    for fd in range(0, maxfd):
        try:
            os.close(fd)
        except OSError:
            pass

    os.open(REDIRECT_TO, os.O_RDWR)
    os.dup2(0, 1)
    os.dup2(0, 2)
    return 0


if __name__ == '__main__':
    retCode = createDaemon()
    procParams = '\n   return code = %s\n   process ID = %s\n   parent process ID = %s\n   process group ID = %s\n   session ID = %s\n   user ID = %s\n   effective user ID = %s\n   real group ID = %s\n   effective group ID = %s\n   ' % (retCode, os.getpid(), os.getppid(), os.getpgrp(), os.getsid(0),
     os.getuid(), os.geteuid(), os.getgid(), os.getegid())
    open('createDaemon.log', 'w').write(procParams + '\n')
    sys.exit(retCode)