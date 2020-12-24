# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/synctools/stacks/processingstack.py
# Compiled at: 2020-03-06 02:01:31
# Size of source mod 2**32: 3971 bytes
"""Define some processing stack"""
__authors__ = [
 'H.Payno']
__license__ = 'MIT'
__date__ = '08/01/2020'
from queue import Queue
from silx.gui import qt

class ProcessingThread(qt.QThread):
    __doc__ = 'Class for running some processing'
    sigComputationStarted = qt.Signal()


class FIFO(Queue):
    __doc__ = 'Processing Queue with a First In, First Out behavior'
    sigComputationStarted = qt.Signal()
    sigComputationEnded = qt.Signal()

    def __init__(self):
        Queue.__init__(self)
        self._computationThread = self._create_processing_thread()
        assert isinstance(self._computationThread, ProcessingThread)
        self._computationThread = self._create_processing_thread()
        self._computationThread.sigComputationStarted.connect(self._start_threaded_computation)
        self._scan_currently_computed = None

    def add(self, scan):
        """"""
        Queue.put(self, scan)
        if self.can_process_next():
            self._process_next()

    def _process(self, scan):
        raise NotImplementedError('Virtual class')

    def _process_next(self):
        if Queue.empty(self):
            return
        scan = Queue.get(self)
        self._process(scan)

    def can_process_next(self):
        """
        :return: True if the computation thread is ready to compute
        a new axis position
        :rtype: bool
        """
        return not self._computationThread.isRunning()

    def _end_computation(self, scan):
        """
        callback when the computation thread is finished

        :param scan: pass if no call to '_computationThread is made'
        """
        self.sigComputationEnded.emit()
        if self.can_process_next():
            self._process_next()

    def _create_processing_thread(self) -> ProcessingThread:
        raise NotImplementedError('Virtual class')

    def is_computing(self):
        """Return True if processing thread is running (mean that computation
        is on going)"""
        return self._computationThread.isRunning()

    def wait_computation_finished(self):
        """
        Wait until the computation is finished
        """
        if self._computationThread.isRunning():
            self._computationThread.wait()

    def _start_threaded_computation(self, *args, **kwargs):
        self.sigComputationStarted.emit()

    def _end_threaded_computation(self):
        self._end_computation(scan=(self._scan_currently_computed))