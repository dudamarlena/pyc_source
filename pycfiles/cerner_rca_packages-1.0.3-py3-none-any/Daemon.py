# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/lib/Daemon.py
# Compiled at: 2012-04-20 03:47:25
import sys, os, time, atexit, errno
from signal import SIGTERM

class Daemon:
    """
    A generic daemon class.
   
    Usage: subclass the Daemon class and override the run() method
    """

    def __init__(self, pidfile, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.pidfile = pidfile

    def daemonize(self):
        """
        do the UNIX double-fork magic, see Stevens' "Advanced
        Programming in the UNIX Environment" for details (ISBN 0201563177)
        http://www.erlenstar.demon.co.uk/unix/faq_2.html#SEC16
        """
        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError as e:
            sys.stderr.write('fork #1 failed: %d (%s)\n' % (e.errno, e.strerror))
            sys.exit(1)

        os.chdir('/')
        os.setsid()
        os.umask(0)
        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError as e:
            sys.stderr.write('fork #2 failed: %d (%s)\n' % (e.errno, e.strerror))
            sys.exit(1)

        sys.stdout.flush()
        sys.stderr.flush()
        si = file(self.stdin, 'r')
        so = file(self.stdout, 'a+')
        se = file(self.stderr, 'a+', 0)
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())
        atexit.register(self.delpid)
        pid = str(os.getpid())
        file(self.pidfile, 'w+').write('%s\n' % pid)

    def delpid(self):
        os.remove(self.pidfile)

    def start(self):
        """
        Start the daemon
        """
        try:
            pf = file(self.pidfile, 'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None

        if pid:
            if self.running():
                message = 'pidfile %s already exist. Daemon already running?\n'
                sys.stderr.write(message % self.pidfile)
                sys.exit(1)
            else:
                self.delpid()
        self.daemonize()
        self.run()
        return

    def stop(self, restart=False):
        """
        Stop the daemon
        """
        try:
            pf = file(self.pidfile, 'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None

        if not pid:
            if restart:
                message = 'pidfile %s does not exist. Daemon not running?\nProceeding to start the Daemon now.\n'
            else:
                message = 'pidfile %s does not exist. Daemon not running?\n'
            sys.stderr.write(message % self.pidfile)
            return
        else:
            try:
                while 1:
                    os.kill(pid, SIGTERM)
                    time.sleep(0.1)

            except OSError as err:
                err = str(err)
                if err.find('No such process') > 0:
                    if os.path.exists(self.pidfile):
                        os.remove(self.pidfile)
                else:
                    print str(err)
                    sys.exit(1)

            return

    def running(self):
        """Checks if the daemon is running based on its pid
        """
        try:
            os.kill(int(open(self.pidfile).read().strip()), 0)
            return True
        except IOError:
            return False
        except OSError as err:
            if err.errno == errno.ESRCH:
                return False
            if err.errno == errno.EPERM:
                print 'No permission to signal this process!'
            else:
                print 'Unknown error'

    def restart(self):
        """
        Restart the daemon
        """
        self.stop(restart=True)
        self.start()

    def run(self):
        """
        You should override this method when you subclass Daemon. It will be called after the process has been
        daemonized by start() or restart().
        """
        pass