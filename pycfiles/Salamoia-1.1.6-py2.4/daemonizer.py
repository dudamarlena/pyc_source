# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/salamoia/utility/daemonizer.py
# Compiled at: 2007-12-02 16:26:55
import sys, os

class Daemonizer(object):
    """
    The daemonizer object handles the daemonizing under UNIX.

    Just call damonize() and you will be a daemon!

    You will need to use syslog to comunicate with the rest
    of the world.
    """
    __module__ = __name__

    def __init__(self, appname=None):
        """
        The appname will be used for naming the pid file
        """
        self.appname = appname

    def daemonize(self):
        """
        This method does the real job of daemonizing the process.
        Upon return from this method we are running a new process.
        This process is detached from the controlling terminal and session and cd to /
        
        It writes the pid to /var/run/appname.pid
        """
        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError, e:
            print >> sys.stderr, 'fork #1 failed: %d (%s)' % (e.errno, e.strerror)
            sys.exit(1)

        stdin = '/dev/null'
        stdout = '/dev/null'
        stderr = '/dev/null'
        si = file(stdin, 'r')
        so = file(stdout, 'a+')
        se = file(stderr, 'a+', 0)
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())
        os.chdir('/')
        os.setsid()
        os.umask(0)
        try:
            pid = os.fork()
            if pid > 0:
                if self.appname:
                    try:
                        f = open('/var/run/%s.pid' % self.appname, 'w')
                        print >> f, pid
                    except IOError:
                        print 'Daemon PID %d' % pid

                sys.exit(0)
        except OSError, e:
            print >> sys.stderr, 'fork #2 failed: %d (%s)' % (e.errno, e.strerror)
            sys.exit(1)


from salamoia.tests import *
runDocTests()