# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dr/Documents/code/Python/Projects/ControllProxy/seed/mrpackage/daemon.py
# Compiled at: 2018-05-23 02:09:21
# Size of source mod 2**32: 3983 bytes
"""Generic linux daemon base class for python 3.x."""
import sys, os, time, atexit, signal

class Daemon:
    __doc__ = 'A generic daemon class.\n\n    Usage: subclass the daemon class and override the run() method.'

    def __init__(self, pidfile):
        self.pidfile = pidfile
        self.std = pidfile + '.log'
        self.ste = pidfile + '.err.log'

    def daemonize_mul(self, jobs):
        imTheFather = True
        children = []
        for job in jobs:
            child = os.fork()
            if child:
                children.append(child)
            else:
                imTheFather = False
                job()
                break

        if imTheFather:
            for child in children:
                os.waitpid(child, 0)

    def daemonize(self):
        """Deamonize class. UNIX double fork mechanism."""
        try:
            child = os.fork()
            is_child = False
            if child:
                sys.exit(0)
            else:
                is_child = True
        except OSError as err:
            sys.stderr.write('fork #1 failed: {0}\n'.format(err))
            sys.exit(1)

        os.chdir('/')
        os.setsid()
        os.umask(0)
        try:
            child = os.fork()
            if child:
                sys.exit(0)
        except OSError as err:
            sys.stderr.write('fork #2 failed: {0}\n'.format(err))
            sys.exit(1)

        sys.stdout.flush()
        sys.stderr.flush()
        si = open(os.devnull, 'r')
        so = open(self.ste, 'a+')
        se = open(self.std, 'a+')
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())
        atexit.register(self.delpid)
        pid = str(os.getpid())
        with open(self.pidfile, 'w+') as (f):
            f.write(pid + '\n')

    def delpid(self):
        os.remove(self.pidfile)

    def start(self):
        """Start the daemon."""
        try:
            with open(self.pidfile, 'r') as (pf):
                pid = int(pf.read().strip())
        except IOError:
            pid = None

        if pid:
            message = 'pidfile {0} already exist. ' + 'Daemon already running?\n'
            sys.stderr.write(message.format(self.pidfile))
            sys.exit(1)
        self.daemonize()
        self.run()

    def stop(self):
        """Stop the daemon."""
        try:
            with open(self.pidfile, 'r') as (pf):
                pid = int(pf.read().strip())
        except IOError:
            pid = None

        if not pid:
            message = 'pidfile {0} does not exist. ' + 'Daemon not running?\n'
            sys.stderr.write(message.format(self.pidfile))
            return
        try:
            while True:
                os.kill(pid, signal.SIGTERM)
                time.sleep(0.1)

        except OSError as err:
            e = str(err.args)
            if e.find('No such process') > 0:
                if os.path.exists(self.pidfile):
                    os.remove(self.pidfile)
            else:
                print(str(err.args))
                sys.exit(1)

    def restart(self):
        """Restart the daemon."""
        self.stop()
        self.start()

    def run(self):
        """You should override this method when you subclass Daemon.

        It will be called after the process has been daemonized by
        start() or restart()."""
        pass