# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/betsee/util/io/log/guiloghandle.py
# Compiled at: 2019-08-22 01:06:39
# Size of source mod 2**32: 3174 bytes
"""
Low-level :mod:`PySide2`-specific logging handler subclasses.
"""
from PySide2.QtCore import Signal
from betse.util.type.types import type_check
from logging import Handler

class LogHandlerSignal(Handler):
    __doc__ = '\n    :class:`Signal`-based handler, redirecting each log record sent to this\n    handler to each slot connected to the signal with which this handler was\n    initialized.\n\n    Parameters\n    ----------\n    _signal : SignalOrNoneTypes\n        Either:\n\n        * If the :meth:`close` method has yet to be called, the signal to\n          forward log records to.\n        * Else (i.e., if the :meth:`close` method has already been called),\n          ``None``.\n    '

    @type_check
    def __init__(self, signal, *args, **kwargs):
        """
        Initialize this handler to log with the passed signal.

        Parameters
        ----------
        signal : Signal
            Signal to forward log records to.

        All remaining parameters are passed as is to our superclass method.
        """
        (super().__init__)(*args, **kwargs)
        self._signal = signal

    def emit(self, record) -> None:
        record_message = self.format(record)
        if self._signal is not None:
            self._signal.emit(record_message)

    def close(self):
        super().close()
        self._signal = None