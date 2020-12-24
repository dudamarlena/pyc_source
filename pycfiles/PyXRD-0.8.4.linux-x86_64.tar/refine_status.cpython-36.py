# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyxrd/refinement/refine_status.py
# Compiled at: 2020-03-07 03:51:50
# Size of source mod 2**32: 4049 bytes
import time

class RefineStatus(object):
    __doc__ = '\n    A status object for a refinement. This should provide some hints\n    for the UI to keep track of the status of the refinement.\n    \n    The error, running and finished flags are mutually exclusive but can be\n    False together. When the cancelled flag is set, the user cancelled the\n    refinement (the stop signal was set). When the error flag is true, an error\n    was encountered during the refinement. When the finished flag is true the \n    refinement has finished successfully. When the running flag is true the \n    refinement is still running. When all three flags are False, the refinement \n    has not started yet.\n    \n    The status message should be a textual description of these three flags,\n    but can be set to any value.\n    \n    The current error is retrieved from the RefinementHistory instance passed\n    in the constructor (it is the residual of the last solution registered).\n    \n    The best way to use the status object is with a context, like this:\n    \n     with RefineHistory() as history:\n         with RefineStatus(history) as status:\n             run_refinement()\n             \n    '
    _error = False

    @property
    def error(self):
        return self._error

    @error.setter
    def error(self, value):
        self._error = bool(value)
        if self._error:
            self.running = False
            self.cancelled = False
            self.finished = False

    _cancelled = False

    @property
    def cancelled(self):
        return self._cancelled

    @cancelled.setter
    def cancelled(self, value):
        self._cancelled = bool(value)
        if self._cancelled:
            self.running = False
            self.error = False
            self.finished = False

    _running = False

    @property
    def running(self):
        return self._running

    @running.setter
    def running(self, value):
        self._running = bool(value)
        if self._running:
            self.error = False
            self.cancelled = False
            self.finished = False

    _finished = False

    @property
    def finished(self):
        return self._finished

    @finished.setter
    def finished(self, value):
        self._finished = bool(value)
        if self._finished:
            self.error = False
            self.cancelled = False
            self.running = False

    message = 'Not initialized.'

    @property
    def current_error(self):
        return self.history.last_solution[self.history.RESIDUAL_INDEX]

    def __init__(self, history, stop_signal=None):
        assert history is not None, 'The RefinementStatus needs a RefinementHistory instance!'
        self.history = history
        self.stop_signal = stop_signal
        self.message = 'Initialized.'
        self.start_time = -1
        self.end_time = -1

    def __enter__(self):
        self.running = True
        self.message = 'Running...'
        self.start_time = time.time()
        return self

    def __exit__(self, tp, value, traceback):
        self.start_time = -1
        if tp is not None:
            self.message = 'Refinement error!'
            self.error = True
        elif self.stop_signal is not None:
            if self.stop_signal.is_set():
                self.message = 'Refinement cancelled!'
                self.cancelled = True
        else:
            self.message = 'Refinement finished!'
            self.finished = True

    def get_total_time(self):
        """ Gets the total time the refinement has run in ms """
        if self.start_time == -1:
            return 0
        else:
            return (self.end_time - self.start_time) * 1000.0