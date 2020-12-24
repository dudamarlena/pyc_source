# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/mvc/support/observables/signal.py
# Compiled at: 2020-03-07 03:51:49
# Size of source mod 2**32: 3814 bytes
import threading
from .observable import Observable

class Signal(Observable):
    __doc__ = "\n        A Signal that can either:\n         - be 'held' from firing until a code block has finished, e.g. to\n           prevent numerous events from firing, when one final event would\n           be enough\n         - be stopped from firing altogether, even after the code block has\n           finished \n        \n        Holding signals back:\n         ...\n         object.hold_signal = HoldableSignal()\n         ...\n         with object.hold_signal.hold():\n             # this code block can call emit() on the hold_signal but it will not\n             # actually emit the signal until the 'with' block is left\n         ...\n         \n        Ignoring signals:\n         ...\n         object.hold_signal =  HoldableSignal()\n         ...\n         with object.hold_signal.ignore():\n             # this code block can call emit() on the hold_signal but it will not\n             # actually emit the signal, even after leaving the 'with' block\n    "
    clock = threading.RLock()

    def __init__(self, *args, **kwargs):
        (super(Signal, self).__init__)(*args, **kwargs)
        self._counter = 0
        self._emissions_pending = False
        self._ignore_levels = []

    def __enter__(self):
        with self.clock:
            self._counter += 1

    def __exit__(self, *args):
        with self.clock:
            self._counter -= 1
            if self._counter < 0:
                raise RuntimeError('Negative counter in CounterLock object! Did you call __exit__ too many times?')
            if len(self._ignore_levels) > 0:
                if self._counter == self._ignore_levels[(-1)]:
                    self._ignore_levels.pop()
            if self._counter == 0:
                if self._emissions_pending:
                    self.emit()

    def hold(self):
        return self

    def ignore(self):
        self._ignore_levels.append(self._counter)
        return self

    def hold_and_emit(self):
        self._emit_pending()
        return self

    def emit(self, arg=None):
        if self._counter == 0:
            self._emissions_pending = False
            for model, name in self.__get_models__():
                model.notify_signal_emit(name, arg)

        else:
            self._emit_pending()

    def _emit_pending(self):
        if not self._emissions_pending:
            self._emissions_pending = bool(len(self._ignore_levels) == 0)