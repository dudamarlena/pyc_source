# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Benutzer\haschtl\Dokumente\GIT\kellerlogger\RTOC\RTLogger\Daemon.py
# Compiled at: 2019-04-23 10:37:58
# Size of source mod 2**32: 3907 bytes
"""Generic linux daemon base class for python 3.x.

Source: https://web.archive.org/web/20160320091458/http://www.jejik.com/files/examples/daemon3x.py"""
import sys, os, time, atexit, signal, logging as log
log.basicConfig(level=(log.INFO))
logging = log.getLogger(__name__)

class Daemon:
    __doc__ = 'A generic daemon class.\n\n    Usage: subclass the daemon class and override the run() method.'

    def __init__(self, pidfile):
        self.pidfile = pidfile

    def daemonize(self):
        """Deamonize class. UNIX double fork mechanism."""
        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError as err:
            sys.stderr.write('fork #1 failed: {0}\n'.format(err))
            sys.exit(1)

        os.chdir('/')
        os.setsid()
        os.umask(0)
        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError as err:
            sys.stderr.write('fork #2 failed: {0}\n'.format(err))
            sys.exit(1)

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

    def start(self):
        """Start the daemon."""
        logging.info('Starting server...')
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
        logging.info('Stopping server ...')
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
                logging.debug(str(err.args))
                sys.exit(1)

    def restart(self):
        """Restart the daemon."""
        logging.info('Restarting server...')
        self.stop()
        logging.info('Server stopped. Now restarting ...')
        self.start()
        logging.info('Server restarted.')

    def run(self):
        """You should override this method when you subclass Daemon.

        It will be called after the process has been daemonized by
        start() or restart()."""
        pass