# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/plone/recipe/cluster/daemon.py
# Compiled at: 2008-08-11 05:37:05
__doc__ = '\nCopyright (c) 2006-2007 by:\n    Blue Dynamics Alliance Klein & Partner KEG, Austria\n    Squarewave Computing Robert Niederreiter, Austria\n\nPermission to use, copy, modify, and distribute this software and its \ndocumentation for any purpose and without fee is hereby granted, provided that \nthe above copyright notice appear in all copies and that both that copyright \nnotice and this permission notice appear in supporting documentation, and that \nthe name of Stichting Mathematisch Centrum or CWI not be used in advertising \nor publicity pertaining to distribution of the software without specific, \nwritten prior permission.\n\nSTICHTING MATHEMATISCH CENTRUM DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS \nSOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS, IN \nNO EVENT SHALL STICHTING MATHEMATISCH CENTRUM BE LIABLE FOR ANY SPECIAL, \nINDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS \nOF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER \nTORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF \nTHIS SOFTWARE.\n\nReferences:\n    http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/66012\n\nHistory:\n    2001/07/10 by Juergen Hermann\n    2002/08/28 by Noah Spurrier\n    2003/02/24 by Clark Evans\n    2006/01/25 by Robert Niederreiter\n\nClass Daemon is used to run any routine in the background on unix environments\nas daemon.\n\nThere are several things to consider:\n    \n*The instance object given to the constructor MUST provide a run method with \nrepresents the main routine of the daemon\n\n*The instance object MUST provide global file descriptors for (and named as):\n    -stdin\n    -stdout\n    -stderr\n\n*The instance object MUST provide a global (and named as) pidfile.\n\n\nAdapted for plone.recipe.cluster by Tarek Ziadé:\n  - added a before_stop hook\n  - made stdin, stdout, stderr compatible with sys ones\n  - added some stderr outputs when the daemon is stopped.\n  - a lot of refactoring\n  - added child subprocess managment\n  - added the status\n'
__author__ = 'Robert Niederreiter <office@squarewave.at>'
__version__ = 0.1
__docformat__ = 'plaintext'
import os, sys, time
from signal import SIGTERM

class Daemon(object):
    __module__ = __name__
    UMASK = 0
    WORKDIR = '.'
    instance = None
    startmsg = 'Started with pid %s'
    stopmsg = 'stopped pid %s'

    def __init__(self, instance):
        self.instance = instance

    def daemonize(self, child_pids):
        """Fork the process into the background.
        """
        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError, e:
            sys.stderr.write('fork #1 failed: (%d) %s\n' % (e.errno, e.strerror))
            sys.exit(1)

        os.chdir(self.WORKDIR)
        os.umask(self.UMASK)
        os.setsid()
        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError, e:
            sys.stderr.write('fork #2 failed: (%d) %s\n' % (e.errno, e.strerror))
            sys.exit(1)

        if not self.instance.stderr:
            self.instance.stderr = self.instance.stdout
        if isinstance(self.instance.stdin, str):
            si = file(self.instance.stdin, 'r')
        else:
            si = self.instance.stdin
        if isinstance(self.instance.stdout, str):
            so = file(self.instance.stdout, 'a+')
        else:
            so = self.instance.stdout
        if isinstance(self.instance.stderr, str):
            se = file(self.instance.stderr, 'a+', 0)
        else:
            se = self.instance.stderr
        pid = str(os.getpid())
        sys.stderr.write('%s\n' % self.startmsg % pid)
        sys.stderr.flush()
        if self.instance.pidfile:
            pid_list = (':').join([pid] + [ str(p) for p in child_pids ])
            file(self.instance.pidfile, 'w+').write('%s\n' % pid_list)
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())
        self.instance.run()

    def _kill(self, pid):
        sys.stderr.write('Stopping PID %d\n' % pid)
        try:
            while 1:
                os.kill(pid, SIGTERM)
                time.sleep(1)

            sys.stderr.write('\n%s\n' % self.stopmsg % pid)
            sys.stderr.flush()
        except OSError, err:
            err = str(err)
            if not err.find('No such process') > 0:
                sys.stderr.write('%s\n' % err)
                sys.stderr.flush()
                return False

        return True

    def _stop(self, pid, child_pids):
        """stopping"""
        if not pid:
            mess = "Could not stop, pid file '%s' missing.\n"
            sys.stderr.write(mess % self.instance.pidfile)
            sys.exit(1)
        for child_pid in child_pids:
            self._kill(child_pid)

        if hasattr(self.instance, 'before_stop'):
            pids = self.instance.before_stop()
            self._display_pids(pids)
            for subpid in pids:
                try:
                    os.waitpid(subpid, 0)
                except OSError:
                    pass

        if self._kill(pid):
            os.remove(self.instance.pidfile)
            sys.exit(0)
        else:
            sys.exit(1)

    def _display_pids(self, pids):
        pids = [ str(p) for p in pids ]
        sys.stderr.write('Child PIDs: %s\n' % (', ').join(pids))

    def _start(self, pid):
        """Starts the daemon"""
        if pid:
            mess = "Start aborded since pid file '%s' exists.\n"
            sys.stderr.write(mess % self.instance.pidfile)
            sys.exit(1)
        if hasattr(self.instance, 'before_start'):
            child_pids = self.instance.before_start()
            self._display_pids(child_pids)
        else:
            child_pids = []
        self.daemonize(child_pids)

    def _restart(self, pid, child_pids):
        """Restarts the daemon"""
        if not pid:
            mess = "Could not stop, pid file '%s' missing.\n"
            sys.stderr.write(mess % self.instance.pidfile)
            sys.exit(1)
        for child_pid in child_pids:
            self._kill(pid)

        if self._kill(pid):
            os.remove(self.instance.pidfile)
        if hasattr(self.instance, 'before_restart'):
            child_pids = self.instance.before_restart()
            self._display_pids(child_pids)
        self.daemonize(child_pids)

    def _status(self, pid, pids):
        if not pid:
            sys.stderr.write('Not running.\n')
        else:
            sys.stderr.write('Running.\n')

    def startstop(self, action):
        """Start/stop/restart behaviour.
        """
        try:
            pf = file(self.instance.pidfile, 'r')
            pids = [ int(pid) for pid in pf.read().strip().split(':') ]
            pid = pids[0]
            child_pids = pids[1:]
            pf.close()
        except IOError:
            pid = None
            child_pids = []

        if action == 'stop':
            self._stop(pid, child_pids)
        elif action == 'start':
            self._start(pid)
        elif action == 'restart':
            self._restart(pid, child_pids)
        elif action == 'status':
            self._status(pid, child_pids)
        else:
            print 'usage: %s start|stop|restart' % sys.argv[0]
            sys.exit(2)
        return