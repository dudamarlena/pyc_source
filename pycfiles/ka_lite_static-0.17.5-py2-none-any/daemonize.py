# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/utils/daemonize.py
# Compiled at: 2018-07-11 18:15:30
import os, sys
if os.name == 'posix':

    def become_daemon(our_home_dir='.', out_log='/dev/null', err_log='/dev/null', umask=18):
        """Robustly turn into a UNIX daemon, running in our_home_dir."""
        try:
            if os.fork() > 0:
                sys.exit(0)
        except OSError as e:
            sys.stderr.write('fork #1 failed: (%d) %s\n' % (e.errno, e.strerror))
            sys.exit(1)

        os.setsid()
        os.chdir(our_home_dir)
        os.umask(umask)
        try:
            if os.fork() > 0:
                os._exit(0)
        except OSError as e:
            sys.stderr.write('fork #2 failed: (%d) %s\n' % (e.errno, e.strerror))
            os._exit(1)

        si = open('/dev/null', 'r')
        so = open(out_log, 'a+', 0)
        se = open(err_log, 'a+', 0)
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())
        sys.stdout, sys.stderr = so, se


else:

    def become_daemon(our_home_dir='.', out_log=None, err_log=None, umask=18):
        """
        If we're not running under a POSIX system, just simulate the daemon
        mode by doing redirections and directory changing.
        """
        os.chdir(our_home_dir)
        os.umask(umask)
        sys.stdin.close()
        sys.stdout.close()
        sys.stderr.close()
        if err_log:
            sys.stderr = open(err_log, 'a', 0)
        else:
            sys.stderr = NullDevice()
        if out_log:
            sys.stdout = open(out_log, 'a', 0)
        else:
            sys.stdout = NullDevice()


    class NullDevice:
        """A writeable object that writes to nowhere -- like /dev/null."""

        def write(self, s):
            pass