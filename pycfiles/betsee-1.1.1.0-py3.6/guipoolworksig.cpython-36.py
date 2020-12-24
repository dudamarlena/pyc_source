# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/betsee/util/thread/pool/guipoolworksig.py
# Compiled at: 2019-08-01 01:03:54
# Size of source mod 2**32: 13259 bytes
"""
Low-level **pooled worker signals** (i.e., collection of all :class:`Signal`
instances thread-safely emittable by the :meth:`QBetseeThreadPoolWorker.run`
method from an arbitrary pooled thread possibly running *no* Qt event loop)
classes.
"""
from PySide2.QtCore import QObject, Signal
from betse.util.type.types import type_check, WeakRefBoundMethodType

class QBetseeThreadPoolWorkerSignals(QObject):
    __doc__ = '\n    Low-level **pooled worker signals** (i.e., collection of all\n    :class:`Signal` instances thread-safely emittable by the\n    :meth:`QBetseeThreadPoolWorker.run` method from an arbitrary pooled thread\n    possibly running *no* Qt event loop).\n\n    Each instance of this class is owned by a pooled worker (i.e.,\n    :class:`QBetseeThreadPoolWorker` instance), whose :meth:`run` method emits\n    signals defined by this class typically connected to slots defined by\n    objects residing in the original thread in which this worker was\n    instantiated (e.g., the main event thread).\n\n    Signal Emission\n    ----------\n    External callers attempting to emit signals defined by this collection\n    should typically prefer to call the higher-level wrapper methods whose\n    names are prefixed by ``emit_`` (e.g., :meth:`emit_progress_range`) in\n    lieu of the associate lower-level signals (e.g., :attr:`progress_ranged`).\n    The former wrap the latter with essential multithreading handling,\n    including guaranteeably calling the vital :meth:`halt_work_if_requested`\n    method *after* emitting each such signal. Nonetheless, to permit these\n    signals to be trivially connected to, these signals necessarily remain\n    public rather than private variables.\n\n    Thread Affinity\n    ----------\n    Each instance of this class resides in the original thread in which this\n    worker was instantiated and resides. Hence, neither this class nor any\n    subclass of this class should define slots. Why? Qt would execute these\n    slots in that original thread rather than the thread running this worker.\n\n    Attributes\n    ----------\n    _halt_work_if_requested : WeakRefBoundMethodType\n        Weak reference to a bound method either temporarily or permanently\n        halting all business logic performed by the parent worker that owns\n        this collection when requested to do so by external callers residing in\n        other threads.\n    '
    started = Signal()
    progress_ranged = Signal(int, int)
    progress_stated = Signal(str)
    progressed = Signal(int)
    paused = Signal()
    resumed = Signal()
    finished = Signal(bool)
    failed = Signal(Exception)
    succeeded = Signal(object)

    @type_check
    def __init__(self, halt_work_if_requested):
        """
        Initialize this pooled worker signals collection.

        Parameters
        ----------
        halt_work_if_requested : WeakRefBoundMethodType
            Weak reference to a bound method either temporarily or permanently
            halting all business logic performed by the parent worker that owns
            this collection when requested to do so by external callers
            residing in other threads.  For convenience, this is typically the
            :meth:`guipoolwork.QBetseeThreadPoolWorker._halt_work_if_requested`
            method bound to this parent worker. Accepting a reference to this
            method rather than this parent worker avoids circular object
            references between this parent worker and this child collection.
        """
        super().__init__()
        self._halt_work_if_requested = halt_work_if_requested

    @type_check
    def emit_progress_range(self, progress_min: int, progress_max: int) -> None:
        """
        Emit the :attr:`progress_ranged` signal with the passed range of all
        possible **progress values** (i.e., integers subsequently emitted by
        the :attr:`emit_progress` signal method) for the parent worker.

        Parameters
        ----------
        progress_min : int
            Minimum progress value emitted by :attr:`emit_progress`.
        progress_max : int
            Maximum progress value emitted by :attr:`emit_progress`.

        See Also
        ----------
        :attr:`progress_ranged`
            Further details.
        """
        self.progress_ranged.emit(progress_min, progress_max)
        self._halt_work_if_requested()()

    @type_check
    def emit_progress_state(self, status: str) -> None:
        """
        Emit the :attr:`progress_stated` signal with the passed **progress
        status** (i.e., string subsequently emitted by the
        :attr:`emit_progress_state` signal method) for the parent worker.

        Parameters
        ----------
        status : str
            Human-readable string signifying the progress of work completed.

        See Also
        ----------
        :attr:`progress_stated`
            Further details.
        """
        self.progress_stated.emit(status)
        self._halt_work_if_requested()()

    @type_check
    def emit_progress(self, progress: int) -> None:
        """
        Emit the :attr:`progressed` signal with the passed **progress value**
        (i.e., integer signifying the progress of work completed) for the
        parent worker.

        Parameters
        ----------
        progress : int
            Integer signifying the progress of work completed.

        See Also
        ----------
        :attr:`progressed`
            Further details.
        """
        self.progressed.emit(progress)
        self._halt_work_if_requested()()