# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/multiprocess/processes.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 20692 bytes
import subprocess, atexit, os, sys, time, random, socket, signal, multiprocessing.connection
try:
    import cPickle as pickle
except ImportError:
    import pickle

from .remoteproxy import RemoteEventHandler, ClosedError, NoResultError, LocalObjectProxy, ObjectProxy
from ..Qt import USE_PYSIDE
from ..util import cprint
__all__ = [
 'Process', 'QtProcess', 'ForkedProcess', 'ClosedError', 'NoResultError']

class Process(RemoteEventHandler):
    __doc__ = "\n    Bases: RemoteEventHandler\n    \n    This class is used to spawn and control a new python interpreter.\n    It uses subprocess.Popen to start the new process and communicates with it\n    using multiprocessing.Connection objects over a network socket.\n    \n    By default, the remote process will immediately enter an event-processing\n    loop that carries out requests send from the parent process.\n    \n    Remote control works mainly through proxy objects::\n    \n        proc = Process()              ## starts process, returns handle\n        rsys = proc._import('sys')    ## asks remote process to import 'sys', returns\n                                      ## a proxy which references the imported module\n        rsys.stdout.write('hello\n')  ## This message will be printed from the remote \n                                      ## process. Proxy objects can usually be used\n                                      ## exactly as regular objects are.\n        proc.close()                  ## Request the remote process shut down\n    \n    Requests made via proxy objects may be synchronous or asynchronous and may\n    return objects either by proxy or by value (if they are picklable). See\n    ProxyObject for more information.\n    "
    _process_count = 1

    def __init__(self, name=None, target=None, executable=None, copySysPath=True, debug=False, timeout=20, wrapStdout=None):
        """
        ==============  =============================================================
        **Arguments:**
        name            Optional name for this process used when printing messages
                        from the remote process.
        target          Optional function to call after starting remote process.
                        By default, this is startEventLoop(), which causes the remote
                        process to process requests from the parent process until it
                        is asked to quit. If you wish to specify a different target,
                        it must be picklable (bound methods are not).
        copySysPath     If True, copy the contents of sys.path to the remote process
        debug           If True, print detailed information about communication
                        with the child process.
        wrapStdout      If True (default on windows) then stdout and stderr from the
                        child process will be caught by the parent process and
                        forwarded to its stdout/stderr. This provides a workaround
                        for a python bug: http://bugs.python.org/issue3905
                        but has the side effect that child output is significantly
                        delayed relative to the parent output.
        ==============  =============================================================
        """
        if target is None:
            target = startEventLoop
        else:
            if name is None:
                name = str(self)
            else:
                if executable is None:
                    executable = sys.executable
                self.debug = 7 if debug is True else False
                authkey = os.urandom(20)
                if sys.platform.startswith('win'):
                    authkey = None
                l = multiprocessing.connection.Listener(('localhost', 0), authkey=authkey)
                port = l.address[1]
                sysPath = sys.path if copySysPath else None
                bootstrap = os.path.abspath(os.path.join(os.path.dirname(__file__), 'bootstrap.py'))
                self.debugMsg('Starting child process (%s %s)' % (executable, bootstrap))
                if debug:
                    procDebug = Process._process_count % 6 + 1
                    Process._process_count += 1
                else:
                    procDebug = False
            if wrapStdout is None:
                wrapStdout = sys.platform.startswith('win')
            if wrapStdout:
                stdout = subprocess.PIPE
                stderr = subprocess.PIPE
                self.proc = subprocess.Popen((executable, bootstrap), stdin=(subprocess.PIPE), stdout=stdout, stderr=stderr)
                self._stdoutForwarder = FileForwarder(self.proc.stdout, 'stdout', procDebug)
                self._stderrForwarder = FileForwarder(self.proc.stderr, 'stderr', procDebug)
            else:
                self.proc = subprocess.Popen((executable, bootstrap), stdin=(subprocess.PIPE))
        targetStr = pickle.dumps(target)
        pid = os.getpid()
        data = dict(name=(name + '_child'),
          port=port,
          authkey=authkey,
          ppid=pid,
          targetStr=targetStr,
          path=sysPath,
          pyside=USE_PYSIDE,
          debug=procDebug)
        pickle.dump(data, self.proc.stdin)
        self.proc.stdin.close()
        self.debugMsg('Listening for child process on port %d, authkey=%s..' % (port, repr(authkey)))
        while True:
            try:
                conn = l.accept()
                break
            except IOError as err:
                try:
                    if err.errno == 4:
                        continue
                    else:
                        raise
                finally:
                    err = None
                    del err

        RemoteEventHandler.__init__(self, conn, (name + '_parent'), pid=(self.proc.pid), debug=(self.debug))
        self.debugMsg('Connected to child process.')
        atexit.register(self.join)

    def join(self, timeout=10):
        self.debugMsg('Joining child process..')
        if self.proc.poll() is None:
            self.close()
            start = time.time()
            while self.proc.poll() is None:
                if timeout is not None:
                    if time.time() - start > timeout:
                        raise Exception('Timed out waiting for remote process to end.')
                time.sleep(0.05)

        self.debugMsg('Child process exited. (%d)' % self.proc.returncode)

    def debugMsg(self, msg):
        if hasattr(self, '_stdoutForwarder'):
            with self._stdoutForwarder.lock:
                with self._stderrForwarder.lock:
                    RemoteEventHandler.debugMsg(self, msg)
        else:
            RemoteEventHandler.debugMsg(self, msg)


def startEventLoop(name, port, authkey, ppid, debug=False):
    global HANDLER
    if debug:
        import os
        cprint.cout(debug, '[%d] connecting to server at port localhost:%d, authkey=%s..\n' % (
         os.getpid(), port, repr(authkey)), -1)
    conn = multiprocessing.connection.Client(('localhost', int(port)), authkey=authkey)
    if debug:
        cprint.cout(debug, '[%d] connected; starting remote proxy.\n' % os.getpid(), -1)
    HANDLER = RemoteEventHandler(conn, name, ppid, debug=debug)
    while True:
        try:
            HANDLER.processRequests()
            time.sleep(0.01)
        except ClosedError:
            break


class ForkedProcess(RemoteEventHandler):
    __doc__ = '\n    ForkedProcess is a substitute for Process that uses os.fork() to generate a new process.\n    This is much faster than starting a completely new interpreter and child processes\n    automatically have a copy of the entire program state from before the fork. This\n    makes it an appealing approach when parallelizing expensive computations. (see\n    also Parallelizer)\n    \n    However, fork() comes with some caveats and limitations:\n\n    - fork() is not available on Windows.\n    - It is not possible to have a QApplication in both parent and child process\n      (unless both QApplications are created _after_ the call to fork())\n      Attempts by the forked process to access Qt GUI elements created by the parent\n      will most likely cause the child to crash.\n    - Likewise, database connections are unlikely to function correctly in a forked child.\n    - Threads are not copied by fork(); the new process \n      will have only one thread that starts wherever fork() was called in the parent process.\n    - Forked processes are unceremoniously terminated when join() is called; they are not \n      given any opportunity to clean up. (This prevents them calling any cleanup code that\n      was only intended to be used by the parent process)\n    - Normally when fork()ing, open file handles are shared with the parent process, \n      which is potentially dangerous. ForkedProcess is careful to close all file handles \n      that are not explicitly needed--stdout, stderr, and a single pipe to the parent \n      process.\n      \n    '

    def __init__(self, name=None, target=0, preProxy=None, randomReseed=True):
        """
        When initializing, an optional target may be given. 
        If no target is specified, self.eventLoop will be used.
        If None is given, no target will be called (and it will be up 
        to the caller to properly shut down the forked process)
        
        preProxy may be a dict of values that will appear as ObjectProxy
        in the remote process (but do not need to be sent explicitly since 
        they are available immediately before the call to fork().
        Proxies will be availabe as self.proxies[name].
        
        If randomReseed is True, the built-in random and numpy.random generators
        will be reseeded in the child process.
        """
        self.hasJoined = False
        if target == 0:
            target = self.eventLoop
        elif name is None:
            name = str(self)
        else:
            conn, remoteConn = multiprocessing.Pipe()
            proxyIDs = {}
            if preProxy is not None:
                for k, v in preProxy.iteritems():
                    proxyId = LocalObjectProxy.registerObject(v)
                    proxyIDs[k] = proxyId

            ppid = os.getpid()
            pid = os.fork()
            if pid == 0:
                self.isParent = False
                os.setpgrp()
                conn.close()
                sys.stdin.close()
                fid = remoteConn.fileno()
                os.closerange(3, fid)
                os.closerange(fid + 1, 4096)

                def excepthook(*args):
                    import traceback
                    (traceback.print_exception)(*args)

                sys.excepthook = excepthook
                for qtlib in ('PyQt4', 'PySide', 'PyQt5'):
                    if qtlib in sys.modules:
                        sys.modules[(qtlib + '.QtGui')].QApplication = None
                        sys.modules.pop(qtlib + '.QtGui', None)
                        sys.modules.pop(qtlib + '.QtCore', None)

                atexit._exithandlers = []
                atexit.register(lambda : os._exit(0))
                if randomReseed:
                    if 'numpy.random' in sys.modules:
                        sys.modules['numpy.random'].seed(os.getpid() ^ int(time.time() * 10000 % 10000))
                    if 'random' in sys.modules:
                        sys.modules['random'].seed(os.getpid() ^ int(time.time() * 10000 % 10000))
                RemoteEventHandler.__init__(self, remoteConn, (name + '_child'), pid=ppid)
                self.forkedProxies = {}
                for name, proxyId in proxyIDs.iteritems():
                    self.forkedProxies[name] = ObjectProxy(ppid, proxyId=proxyId, typeStr=(repr(preProxy[name])))

                if target is not None:
                    target()
            else:
                self.isParent = True
                self.childPid = pid
                remoteConn.close()
                RemoteEventHandler.handlers = {}
                RemoteEventHandler.__init__(self, conn, (name + '_parent'), pid=pid)
                atexit.register(self.join)

    def eventLoop(self):
        while True:
            try:
                self.processRequests()
                time.sleep(0.01)
            except ClosedError:
                break
            except:
                print('Error occurred in forked event loop:')
                (sys.excepthook)(*sys.exc_info())

        sys.exit(0)

    def join(self, timeout=10):
        if self.hasJoined:
            return
        try:
            self.close(callSync='sync', timeout=timeout, noCleanup=True)
            os.waitpid(self.childPid, 0)
        except IOError:
            pass

        self.hasJoined = True

    def kill(self):
        """Immediately kill the forked remote process. 
        This is generally safe because forked processes are already
        expected to _avoid_ any cleanup at exit."""
        os.kill(self.childPid, signal.SIGKILL)
        self.hasJoined = True


class RemoteQtEventHandler(RemoteEventHandler):

    def __init__(self, *args, **kwds):
        (RemoteEventHandler.__init__)(self, *args, **kwds)

    def startEventTimer(self):
        from ..Qt import QtGui, QtCore
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.processRequests)
        self.timer.start(10)

    def processRequests(self):
        try:
            RemoteEventHandler.processRequests(self)
        except ClosedError:
            from ..Qt import QtGui, QtCore
            QtGui.QApplication.instance().quit()
            self.timer.stop()


class QtProcess(Process):
    __doc__ = "\n    QtProcess is essentially the same as Process, with two major differences:\n    \n    - The remote process starts by running startQtEventLoop() which creates a \n      QApplication in the remote process and uses a QTimer to trigger\n      remote event processing. This allows the remote process to have its own \n      GUI.\n    - A QTimer is also started on the parent process which polls for requests\n      from the child process. This allows Qt signals emitted within the child \n      process to invoke slots on the parent process and vice-versa. This can \n      be disabled using processRequests=False in the constructor.\n      \n    Example::\n    \n        proc = QtProcess()            \n        rQtGui = proc._import('PyQt4.QtGui')\n        btn = rQtGui.QPushButton('button on child process')\n        btn.show()\n        \n        def slot():\n            print('slot invoked on parent process')\n        btn.clicked.connect(proxy(slot))   # be sure to send a proxy of the slot\n    "

    def __init__(self, **kwds):
        if 'target' not in kwds:
            kwds['target'] = startQtEventLoop
        from ..Qt import QtGui
        self._processRequests = kwds.pop('processRequests', True)
        if self._processRequests:
            if QtGui.QApplication.instance() is None:
                raise Exception('Must create QApplication before starting QtProcess, or use QtProcess(processRequests=False)')
        (Process.__init__)(self, **kwds)
        self.startEventTimer()

    def startEventTimer(self):
        from ..Qt import QtCore
        self.timer = QtCore.QTimer()
        if self._processRequests:
            self.startRequestProcessing()

    def startRequestProcessing(self, interval=0.01):
        """Start listening for requests coming from the child process.
        This allows signals to be connected from the child process to the parent.
        """
        self.timer.timeout.connect(self.processRequests)
        self.timer.start(interval * 1000)

    def stopRequestProcessing(self):
        self.timer.stop()

    def processRequests(self):
        try:
            Process.processRequests(self)
        except ClosedError:
            self.timer.stop()


def startQtEventLoop(name, port, authkey, ppid, debug=False):
    global HANDLER
    if debug:
        import os
        cprint.cout(debug, '[%d] connecting to server at port localhost:%d, authkey=%s..\n' % (os.getpid(), port, repr(authkey)), -1)
    conn = multiprocessing.connection.Client(('localhost', int(port)), authkey=authkey)
    if debug:
        cprint.cout(debug, '[%d] connected; starting remote proxy.\n' % os.getpid(), -1)
    from ..Qt import QtGui, QtCore
    app = QtGui.QApplication.instance()
    if app is None:
        app = QtGui.QApplication([])
        app.setQuitOnLastWindowClosed(False)
    HANDLER = RemoteQtEventHandler(conn, name, ppid, debug=debug)
    HANDLER.startEventTimer()
    app.exec_()


import threading

class FileForwarder(threading.Thread):
    __doc__ = "\n    Background thread that forwards data from one pipe to another. \n    This is used to catch data from stdout/stderr of the child process\n    and print it back out to stdout/stderr. We need this because this\n    bug: http://bugs.python.org/issue3905  _requires_ us to catch\n    stdout/stderr.\n\n    *output* may be a file or 'stdout' or 'stderr'. In the latter cases,\n    sys.stdout/stderr are retrieved once for every line that is output,\n    which ensures that the correct behavior is achieved even if \n    sys.stdout/stderr are replaced at runtime.\n    "

    def __init__(self, input, output, color):
        threading.Thread.__init__(self)
        self.input = input
        self.output = output
        self.lock = threading.Lock()
        self.daemon = True
        self.color = color
        self.start()

    def run(self):
        if self.output == 'stdout':
            while True:
                line = self.input.readline()
                with self.lock:
                    cprint.cout(self.color, line, -1)

        else:
            if self.output == 'stderr':
                while True:
                    line = self.input.readline()
                    with self.lock:
                        cprint.cerr(self.color, line, -1)

            else:
                while True:
                    line = self.input.readline()
                    with self.lock:
                        self.output.write(line)