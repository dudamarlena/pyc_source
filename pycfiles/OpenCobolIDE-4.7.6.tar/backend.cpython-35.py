# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/colin/Projects/pyqode.core/pyqode/core/managers/backend.py
# Compiled at: 2016-12-29 05:31:31
# Size of source mod 2**32: 8564 bytes
"""
This module contains the backend controller
"""
import logging, socket, sys
from pyqode.qt import QtCore
from pyqode.core.api.client import JsonTcpClient, BackendProcess
from pyqode.core.api.manager import Manager
from pyqode.core.backend import NotRunning, echo_worker

def _logger():
    return logging.getLogger(__name__)


COMM = 1

def comm(msg, *args):
    _logger().log(COMM, msg, *args)


class BackendManager(Manager):
    __doc__ = '\n    The backend controller takes care of controlling the client-server\n    architecture.\n\n    It is responsible of starting the backend process and the client socket and\n    exposes an API to easily control the backend:\n\n        - start\n        - stop\n        - send_request\n\n    '
    LAST_PORT = None
    LAST_PROCESS = None
    SHARE_COUNT = 0

    def __init__(self, editor):
        super(BackendManager, self).__init__(editor)
        self._process = None
        self._sockets = []
        self.server_script = None
        self.interpreter = None
        self.args = None
        self._shared = False
        self._heartbeat_timer = QtCore.QTimer()
        self._heartbeat_timer.setInterval(1000)
        self._heartbeat_timer.timeout.connect(self._send_heartbeat)
        self._heartbeat_timer.start()

    @staticmethod
    def pick_free_port():
        """ Picks a free port """
        test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        test_socket.bind(('127.0.0.1', 0))
        free_port = int(test_socket.getsockname()[1])
        test_socket.close()
        return free_port

    def start(self, script, interpreter=sys.executable, args=None, error_callback=None, reuse=False):
        """
        Starts the backend process.

        The backend is a python script that starts a
        :class:`pyqode.core.backend.JsonServer`. You must write the backend
        script so that you can apply your own backend configuration.

        The script can be run with a custom interpreter. The default is to use
        sys.executable.

        .. note:: This restart the backend process if it was previously
                  running.

        :param script: Path to the backend script.
        :param interpreter: The python interpreter to use to run the backend
            script. If None, sys.executable is used unless we are in a frozen
            application (frozen backends do not require an interpreter).
        :param args: list of additional command line args to use to start
            the backend process.
        :param reuse: True to reuse an existing backend process. WARNING: to
            use this, your application must have one single server script. If
            you're creating an app which supports multiple programming
            languages you will need to merge all backend scripts into one
            single script, otherwise the wrong script might be picked up).
        """
        self._shared = reuse
        if reuse and BackendManager.SHARE_COUNT:
            self._port = BackendManager.LAST_PORT
            self._process = BackendManager.LAST_PROCESS
            BackendManager.SHARE_COUNT += 1
        else:
            if self.running:
                self.stop()
            self.server_script = script
            self.interpreter = interpreter
            self.args = args
            backend_script = script.replace('.pyc', '.py')
            self._port = self.pick_free_port()
            if hasattr(sys, 'frozen') and not backend_script.endswith('.py'):
                program = backend_script
                pgm_args = [str(self._port)]
            else:
                program = interpreter
                pgm_args = [backend_script, str(self._port)]
            if args:
                pgm_args += args
            self._process = BackendProcess(self.editor)
            if error_callback:
                self._process.error.connect(error_callback)
            self._process.start(program, pgm_args)
            if reuse:
                BackendManager.LAST_PROCESS = self._process
                BackendManager.LAST_PORT = self._port
                BackendManager.SHARE_COUNT += 1
            comm('starting backend process: %s %s', program, ' '.join(pgm_args))
            self._heartbeat_timer.start()

    def stop(self):
        """
        Stops the backend process.
        """
        if self._process is None:
            return
        if self._shared:
            BackendManager.SHARE_COUNT -= 1
            if BackendManager.SHARE_COUNT:
                pass
            return
        comm('stopping backend process')
        for s in self._sockets:
            s._callback = None
            s.close()

        self._sockets[:] = []
        self._process._prevent_logs = True
        while self._process.state() != self._process.NotRunning:
            self._process.waitForFinished(1)
            if sys.platform == 'win32':
                self._process.kill()
            else:
                self._process.terminate()

        self._process._prevent_logs = False
        self._heartbeat_timer.stop()
        comm('backend process terminated')

    def send_request(self, worker_class_or_function, args, on_receive=None):
        """
        Requests some work to be done by the backend. You can get notified of
        the work results by passing a callback (on_receive).

        :param worker_class_or_function: Worker class or function
        :param args: worker args, any Json serializable objects
        :param on_receive: an optional callback executed when we receive the
            worker's results. The callback will be called with one arguments:
            the results of the worker (object)

        :raise: backend.NotRunning if the backend process is not running.
        """
        if not self.running:
            try:
                try:
                    self.start(self.server_script, interpreter=self.interpreter, args=self.args)
                except AttributeError:
                    pass

            finally:
                raise NotRunning()

        else:
            comm('sending request, worker=%r' % worker_class_or_function)
            socket = JsonTcpClient(self.editor, self._port, worker_class_or_function, args, on_receive=on_receive)
            socket.finished.connect(self._rm_socket)
            self._sockets.append(socket)
            self._heartbeat_timer.start()

    def _send_heartbeat(self):
        try:
            self.send_request(echo_worker, {'heartbeat': True})
        except NotRunning:
            self._heartbeat_timer.stop()

    def _rm_socket(self, socket):
        try:
            socket.close()
            self._sockets.remove(socket)
            socket.deleteLater()
        except ValueError:
            pass

    @property
    def running(self):
        """
        Tells whether the backend process is running.

        :return: True if the process is running, otherwise False
        """
        try:
            return self._process is not None and self._process.state() != self._process.NotRunning
        except RuntimeError:
            return False

    @property
    def connected(self):
        """
        Checks if the client socket is connected to the backend.

        .. deprecated: Since v2.3, a socket is created per request. Checking
            for global connection status does not make any sense anymore. This
            property now returns ``running``. This will be removed in v2.5
        """
        return self.running

    @property
    def exit_code(self):
        """
        Returns the backend process exit status or None if the
        process is till running.

        """
        if self.running:
            return
        else:
            return self._process.exitCode()