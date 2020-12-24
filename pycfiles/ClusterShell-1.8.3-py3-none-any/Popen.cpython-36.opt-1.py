# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /ClusterShell/Worker/Popen.py
# Compiled at: 2019-12-07 15:34:33
# Size of source mod 2**32: 4016 bytes
"""
WorkerPopen

ClusterShell worker for executing local commands.

Usage example:
   >>> worker = WorkerPopen("/bin/uname", key="mykernel")
   >>> task.schedule(worker)    # schedule worker
   >>> task.resume()            # run task
   >>> worker.retcode()         # get return code
   0
   >>> worker.read()            # read command output
   'Linux'

"""
from ClusterShell.Worker.Worker import WorkerSimple, StreamClient
from ClusterShell.Worker.Worker import _eh_sigspec_invoke_compat

class PopenClient(StreamClient):

    def __init__(self, worker, key, stderr, timeout, autoclose):
        StreamClient.__init__(self, worker, key, stderr, timeout, autoclose)
        self.popen = None
        self.rc = None
        self.streams.set_writer((worker.SNAME_STDIN), None, retain=False)

    def _start(self):
        """Worker is starting."""
        if not not self.worker.started:
            raise AssertionError
        else:
            assert self.popen is None
            self.popen = self._exec_nonblock((self.worker.command), shell=True)
            task = self.worker.task
            if task.info('debug', False):
                task.info('print_debug')(task, 'POPEN: %s' % self.worker.command)
        self.worker._on_start(self.key)
        return self

    def _close(self, abort, timeout):
        """
        Close client. See EngineClient._close().
        """
        if abort:
            prc = self.popen.poll()
            if prc is None:
                try:
                    self.popen.kill()
                except OSError:
                    pass

        prc = self.popen.wait()
        self.streams.clear()
        self.invalidate()
        if prc >= 0:
            self.rc = prc
            self.worker._on_close(self.key, prc)
        else:
            if timeout:
                assert abort, 'abort flag not set on timeout'
                self.worker._on_timeout(self.key)
            else:
                if not abort:
                    self.rc = 128 + -prc
                    self.worker._on_close(self.key, self.rc)
        if self.worker.eh is not None:
            _eh_sigspec_invoke_compat(self.worker.eh.ev_close, 2, self.worker, timeout)


class WorkerPopen(WorkerSimple):
    __doc__ = '\n    Implements the Popen Worker.\n    '

    def __init__(self, command, key=None, handler=None, stderr=False, timeout=-1, autoclose=False):
        """Initialize Popen worker."""
        WorkerSimple.__init__(self, None, None, None, key, handler, stderr, timeout,
          autoclose, client_class=PopenClient)
        self.command = command
        if not self.command:
            raise ValueError('missing command parameter in WorkerPopen constructor')
        self.key = key

    def retcode(self):
        """Return return code or None if command is still in progress."""
        return self.clients[0].rc


WORKER_CLASS = WorkerPopen