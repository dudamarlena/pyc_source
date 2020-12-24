# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/asfpy/daemon.py
# Compiled at: 2020-03-10 09:07:33
# Size of source mod 2**32: 4606 bytes
"""
This is the standardized daemon library.
Usage example:
    import asfpy.daemon
    def main():
        print("hello world...")
    myprog = asfpy.daemon.Daemon(main, pidfile = '/var/run/myprog.pid')
    myprog.start()
"""
import os, sys, threading, random, atexit, signal, inspect, time

class Daemon:

    def __init__(self, main, pidfile=None, quiet=True):
        self.main = main
        if not pidfile:
            pidfile = sys.argv[0] if len(sys.argv) > 0 else 'generic_py'
            pidfile = '/var/run/%s.pid' % pidfile
        self.pidfile = pidfile
        self.quiet = quiet

    def daemonize(self):
        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError as err:
            try:
                sys.stderr.write('fork #1 failed: {0}\n'.format(err))
                sys.exit(1)
            finally:
                err = None
                del err

        else:
            os.chdir('/')
            os.setsid()
            os.umask(0)
            try:
                pid = os.fork()
                if pid > 0:
                    sys.exit(0)
            except OSError as err:
                try:
                    sys.stderr.write('fork #2 failed: {0}\n'.format(err))
                    sys.exit(1)
                finally:
                    err = None
                    del err

            else:
                if self.quiet:
                    sys.stdout.flush()
                    sys.stderr.flush()
                    si = open(os.devnull, 'r')
                    so = open(os.devnull, 'a+')
                    se = open(os.devnull, 'a+')
                    os.dup2(si.fileno(), sys.stdin.fileno())
                    os.dup2(so.fileno(), sys.stdout.fileno())
                    os.dup2(se.fileno(), sys.stderr.fileno())
                atexit.register(self.delpid)
                pid = str(os.getpid())
                with open(self.pidfile, 'w+') as (f):
                    f.write(pid + '\n')

    def delpid(self):
        os.remove(self.pidfile)

    def start(self, args=None):
        """Start the daemon."""
        try:
            with open(self.pidfile, 'r') as (pf):
                pid = int(pf.read().strip())
        except IOError:
            pid = None
        else:
            if pid:
                message = 'pidfile {0} already exist. Daemon already running?\n'
                sys.stderr.write(message.format(self.pidfile))
                sys.exit(1)
            self.daemonize()
            self.run(args)

    def stop(self):
        """Stop the daemon."""
        try:
            with open(self.pidfile, 'r') as (pf):
                pid = int(pf.read().strip())
        except IOError:
            pid = None
        else:
            if not pid:
                message = 'pidfile {0} does not exist. Daemon not running?\n'
                sys.stderr.write(message.format(self.pidfile))
                return None
            print('Trying to kill')
            try:
                while True:
                    os.kill(pid, signal.SIGTERM)
                    time.sleep(0.1)

            except OSError as err:
                try:
                    e = str(err.args)
                    if e.find('No such process') > 0:
                        if os.path.exists(self.pidfile):
                            os.remove(self.pidfile)
                    else:
                        print(str(err.args))
                        print('boo')
                        sys.exit(1)
                finally:
                    err = None
                    del err

            else:
                print('killed')

    def restart(self):
        """Restart the daemon."""
        self.stop()
        self.start()

    def run(self, args=None):
        if args:
            self.main(args)
        else:
            self.main()