# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/betsee/util/thread/lone/guiloneworker.py
# Compiled at: 2019-08-01 01:03:54
# Size of source mod 2**32: 24158 bytes
"""
Low-level **non-pooled worker** (i.e., thread-safe object implementing
generically startable, pausable, resumable, and haltable business logic in a
multithreaded manner intended to be moved to the thread encapsulated by a
:class:`QThread` object) classes.
"""
from PySide2.QtCore import QObject, Signal, Slot
from betse.exceptions import BetseMethodUnimplementedException
from betse.util.io.log import logs
from betsee.guiexception import BetseePySideThreadWorkerStopException
from betsee.util.thread import guithread
from betsee.util.thread.guithreadenum import ThreadWorkerState
from betsee.util.widget.mixin.guiwdgmixin import QBetseeObjectMixin

class QBetseeLoneThreadWorkerABC(QBetseeObjectMixin, QObject):
    __doc__ = '\n    Abstract base class of all low-level **non-pooled worker** (i.e.,\n    thread-safe object implementing generically startable, pausable, resumable,\n    and haltable business logic in a multithreaded manner intended to be adopted\n    by the thread encapsulated by a :class:`QBetseeLoneThread` object)\n    subclasses.\n\n    By default, workers are recyclable and hence may be reused (i.e., have their\n    :meth:`start` slots signalled) an arbitrary number of times within any\n    arbitrary thread. Where undesirable, see the\n    :cless:`QBetseeLoneThreadWorkerThrowawayABC` for an alternative superclass\n    constraining workers to be non-recyclable.\n\n    Caveats\n    ----------\n    This obsolete superclass has been superceded by the superior\n    :class:`betse.util.thread.pool.guipoolwork.QBetseeThreadPoolWorker`\n    superclass, whose :class:`QRunnable`-based API requires substantially less\n    boilerplate.\n\n    Attributes\n    ----------\n    _state : ThreadWorkerState\n        Current execution state of this worker. For thread-safety, this state\n        should *not* be externally accessed by objects residing in other\n        threads. Doing so safely would require thread-safe mutual exclusion\n        (e.g., with a dedicated :class:`QMutexLocker` context manager), which\n        currently exceeds the mandate of this superclass.\n\n    See Also\n    ----------\n    https://codereview.stackexchange.com/a/173258/124625\n        StackOverflow answer strongly inspiring this implementation.\n    '

    def __init__(self):
        """
        Initialize this worker.

        Caveats
        ----------
        This method intentionally accepts *no* passed parameters and hence
        cannot be passed a parent `QObject`. So, this worker is **unparented**
        (i.e., has no such parent). Why? Because this worker will be
        subsequently adopted into a different thread than the original thread in
        which this worker was instantiated. However, most candidate `QObject`
        parents of this worker would presumably reside in that original thread.
        Objects in different threads should typically *not* control the
        lifecycle of each other, as the parent of a child `QObject` does;
        doing so typically violates thread-safety. (That's bad.)
        """
        super().__init__()
        self._state = ThreadWorkerState.IDLE
        self.start_signal.connect(self.start)
        self.stop_signal.connect(self.stop)
        self.pause_signal.connect(self.pause)
        self.resume_signal.connect(self.resume)

    start_signal = Signal(str)
    stop_signal = Signal()
    pause_signal = Signal()
    resume_signal = Signal()
    started = Signal()
    finished = Signal(bool)

    @Slot(str)
    def start(self, arbitrary_str: str) -> None:
        """
        Slot performing *all* subclass-specific business logic for this worker.

        This slot works in a thread-safe manner safely pausable and stoppable at
        any time (e.g., by emitting a signal connected to the :meth:`pause` or
        :meth:`stop` slots).

        States
        ----------
        If this worker is in the :attr:`ThreadWorkerState.IDLE` state, this
        slot changes to the :attr:`ThreadWorkerState.WORKING` state and calls
        the subclass :meth:`_work` method.

        If this worker is in the :attr:`ThreadWorkerState.PAUSED` state, this
        slot interprets this signal as a request to resume the work presumably
        previously performed by this worker by a prior signalling of this slot.
        To avoid reentrancy issues, this slot changes to the
        :attr:`ThreadWorkerState.WORKING` state and immediately returns.
        Assuming that a prior call to this slot is still executing, that call
        will internally detect this change and resume working as expected.

        If this worker is in the :attr:`ThreadWorkerState.WORKING` state, this
        slot interprets this signal as an accidental attempt by an external
        caller to re-perform the work concurrently being performed by a prior
        call to this slot. In that case, this slot safely logs a non-fatal
        warning and immediately returns.

        See the :meth:`pause` slot for commentary on these design decisions.

        Signals
        ----------
        This slot emits the following signals:

        * :attr:`started` immediately *before* this slot performs any
          subclass-specific business logic for this worker.
        * :attr:`finished` immediately *after* this slot performs all
          subclass-specific business logic for this worker.

        Caveats
        ----------
        Subclasses must override the :meth:`_work` method rather than this slot
        to perform subclass-specific business logic. This slot is neither
        intended nor designed to be overriden by subclasses.
        """
        is_success = False
        if self._state is ThreadWorkerState.PAUSED:
            logs.log_debug('Resuming thread "%d" worker "%s" via reentrant start() slot...', guithread.get_thread_current_id(), self.obj_name)
            self._state = ThreadWorkerState.WORKING
            return
        if self._state is ThreadWorkerState.WORKING:
            logs.log_warning('Ignoring attempt to reenter thread "%d" worker "%s" start() slot.', guithread.get_thread_current_id(), self.obj_name)
            return
        logs.log_debug('Starting thread "%d" worker "%s"...', guithread.get_thread_current_id(), self.obj_name)
        self._state = ThreadWorkerState.WORKING
        self.started.emit()
        try:
            self._halt_work_if_requested()
            self._work(arbitrary_str)
            is_success = True
            if self._state is ThreadWorkerState.WORKING:
                self._state = ThreadWorkerState.IDLE
        except BetseePySideThreadWorkerStopException:
            pass

        logs.log_debug('Finishing thread "%d" worker "%s" with success status "%r"...', guithread.get_thread_current_id(), self.obj_name, is_success)
        self.finished.emit(is_success)

    @Slot()
    def stop(self) -> None:
        """
        Slot stopping all work performed by this worker.

        This slot prematurely halts this work in a thread-safe manner. Whether
        this work is safely restartable (e.g., by emitting a signal connected to
        the :meth:`start` slot) is a subclass-specific implementation detail.
        Subclasses may voluntarily elect to either prohibit or permit restarts.

        States
        ----------
        If this worker is in the :attr:`ThreadWorkerState.IDLE` state, this
        slot silently reduces to a noop and preserves the existing state. In
        this case, this worker remains idle.

        If this worker is in either the :attr:`ThreadWorkerState.WORKING` or
        :attr:`ThreadWorkerState.PAUSED`, implying this worker to either
        currently be or recently have been working, this slot changes the
        current state to the :attr:`ThreadWorkerState.IDLE` state. In either
        case, this worker ceases working.
        """
        logs.log_debug('Stopping thread "%d" worker "%s"...', guithread.get_thread_current_id(), self.obj_name)
        if self._state is not ThreadWorkerState.IDLE:
            self._state = ThreadWorkerState.IDLE

    @Slot()
    def pause(self) -> None:
        """
        Slot pausing all work performed by this worker.

        This slot temporarily halts this work in a thread-safe manner safely
        resumable at any time (e.g., by emitting a signal connected to the
        :meth:`resume` slot).

        States
        ----------
        If this worker is *not* currently working, this slot silently reduces to
        a noop. While raising a fatal exception in this edge case might
        superficially appear to be reasonable, the queued nature of signal-slot
        connections introduces unavoidable delays in event delivery and hence
        slot execution. In particular, raising an exception would introduce a
        race condition between the time that a user interactively requests a
        working worker to be paused and that worker's completion of its work.
        """
        if self._state is not ThreadWorkerState.WORKING:
            logs.log_debug('Ignoring attempt to pause idle or already paused thread "%d" worker "%s".', guithread.get_thread_current_id(), self.obj_name)
            return
        logs.log_debug('Pausing thread "%d" worker "%s"...', guithread.get_thread_current_id(), self.obj_name)
        self._state = ThreadWorkerState.PAUSED
        while self._state is ThreadWorkerState.PAUSED:
            guithread.wait_for_thread_current_event_if_none()

    @Slot()
    def resume(self) -> None:
        """
        Slot **resuming** (i.e., unpausing) this worker.

        This slot resumes working in a thread-safe manner safely re-pausable at
        any time (e.g., by re-emitting a signal connected to the :meth:`pause`
        slot).

        States
        ----------
        If this worker is in either of the following states, this slot silently
        reduces to a noop and preserves the existing state:

        * :attr:`ThreadWorkerState.IDLE`, implying this worker to *not*
          currently be paused. In this case, this worker remains idle.
        * :attr:`ThreadWorkerState.WORKING`, implying this worker to already
          have been resumed. In this case, this worker remains working.

        See the :meth:`pause` slot for commentary on this design decision.
        """
        logs.log_debug('Resuming thread "%d" worker "%s"...', guithread.get_thread_current_id(), self.obj_name)
        if self._state is ThreadWorkerState.PAUSED:
            self._state = ThreadWorkerState.WORKING

    def _work(self, arbitrary_str: str) -> None:
        """
        Perform *all* subclass-specific business logic for this worker.

        The superclass :meth:`start` slot internally calls this method in a
        thread-safe manner safely pausable *and* stoppable at any time (e.g., by
        emitting a signal connected to the :meth:`pause` or :meth:`stop` slots).

        Design
        ----------
        Subclasses are required to redefine this method to perform this logic in
        an iterative manner periodically calling the
        :meth:`_halt_work_if_requested` method.

        If either:

        * This worker has been externally signalled to stop (e.g., by emitting a
          signal connected to the :meth:`stop` slot).
        * The thread of execution currently running this worker has been
          externally requested to stop (e.g., by calling the
          :func:`guithread.halt_thread_work` function).

        Then the next such call to the :meth:`_halt_work_if_requested` method
        will raise an exception caught by the parent :meth:`start` slot,
        signalling that slot to immediately terminate this worker. Ergo, that
        method should be called *only* when the subclass is in an
        **interruptible state** (i.e., a self-consistent internal state in which
        this subclass is fully prepared to be immediately terminated).
        """
        raise BetseMethodUnimplementedException()

    def _halt_work_if_requested(self) -> None:
        """
        Raise an exception if either:

        * This worker has been externally signalled to stop (e.g., by emitting a
          signal connected to the :meth:`stop` slot).
        * The thread of execution currently running this worker has been
          externally requested to stop (e.g., by calling the
          :func:`guithread.halt_thread_work` function).

        This function is intended to be periodically called by the subclass
        :meth:`_work` function. The exception raised by this function is
        guaranteed to be caught by the :meth:`start` method calling that
        :meth:`_work` function.

        Caveats
        ----------
        This function imposes minor computational overhead and hence should be
        called intermittently (rather than overly frequently). Notably, each
        call to this method processes *all* pending events currently queued with
        this worker's thread -- including those queued for all other workers
        currently running in this thread.

        Raises
        ----------
        BetseePySideThreadWorkerStopException
            If this worker or this worker's thread of execution has been
            signalled or requested to be stopped.
        """
        guithread.process_thread_current_events()
        if self._state is ThreadWorkerState.IDLE or guithread.should_halt_thread_work():
            logs.log_debug('Interrupting thread "%d" worker "%s"...', guithread.get_thread_current_id(), self.obj_name)
            raise BetseePySideThreadWorkerStopException('So say we all.')


class QBetseeLoneThreadWorkerThrowawayABC(QBetseeLoneThreadWorkerABC):
    __doc__ = '\n    Abstract base class of all low-level **throw-away non-pooled worker** (i.e.,\n    non-pooled worker guaranteed to be garbage-collected after completing its\n    work) subclasses.\n\n    Equivalently, this is the superclass of all single-use, one-shot, one-time,\n    non-recyclable non-pooled workers. By default, workers are recyclable and\n    hence may be reused (i.e., have their :meth:`start` slots signalled) an\n    arbitrary number of times within any arbitrary thread. Instances of this\n    superclass are non-recyclable and hence may *not* be reused more than once,\n    however.\n\n    Usage\n    ----------\n    Ideally, the :meth:`start` slot of each instance of this superclass should\n    be signalled at most once. Immediately *after* performing all\n    subclass-specific work via the :meth:`_work` method, this slot (in order):\n\n    #. Emits the :attr:`finished` signal.\n    #. Signals itself to be garbage-collected via the :meth:`deleteLater` slot.\n    #. Returns.\n\n    After returning from the :meth:`start` slot, all external references to this\n    worker are effectively invalidated and hence equivalent to ``None``; no such\n    worker may be safely used for *any* subsequent purposes.\n    '

    def __init__(self, *args, **kwargs):
        (super().__init__)(*args, **kwargs)