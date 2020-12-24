# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/betsee/util/thread/pool/guipoolwork.py
# Compiled at: 2019-08-01 01:03:54
# Size of source mod 2**32: 57410 bytes
"""
Low-level **pooled worker** (i.e., thread-safe object implementing generically
startable, pausable, resumable, and stoppable business logic isolated to a
dedicated thread by a parent :class:`QThreadPool` container) classes.
"""
from PySide2.QtCore import QMutex, QMutexLocker, QRunnable, QWaitCondition
from betse.exceptions import BetseMethodUnimplementedException
from betse.util.py import pyref
from betse.util.type.types import type_check, CallableTypes, CallableOrNoneTypes, MappingOrNoneTypes, SequenceOrNoneTypes
from betsee.guiexception import BetseePySideThreadWorkerException, BetseePySideThreadWorkerStopException
from betsee.util.thread import guithread
from betsee.util.thread.guithreadenum import ThreadWorkerState
from betsee.util.thread.pool.guipoolworksig import QBetseeThreadPoolWorkerSignals
from betsee.util.type.guitype import QBetseeProgressBarOrNoneTypes, QLabelOrNoneTypes
_worker_id_next = 0
_worker_id_lock = QMutex()

class QBetseeThreadPoolWorker(QRunnable):
    __doc__ = '\n    Low-level **pooled worker** (i.e., thread-safe object implementing\n    generically startable, pausable, resumable, and stoppable business logic\n    isolated to a dedicated thread by a parent :class:`QThreadPool` container).\n\n    Lifecycle\n    ----------\n    The caller remains responsible for the lifecycle of this worker, an\n    intentional design decision with several notable implications:\n\n    * The caller *must* preserve a reference to this worker for the duration of\n      the work performed by this worker (i.e., the :meth:`run` method), ideally\n      as an instance variable of the class calling the\n      :func:`guipoolthread.start_worker` function directing this work.\n      Conversely, a local variable fails to satisfy this requirement. Lastly,\n      note that preserving a reference to this reference is effectively\n      mandatory for other unrelated reasons: notably, pausing, resuming, and\n      stopping work by calling those methods on the reference to this worker.\n    * If this is a **one-shot worker** (i.e., run only once by a single thread)\n      rather than **recyclable worker** (i.e., run multiple times by multiple\n      threads), the caller should connect the :attr:`signals.finished` signal\n      of this worker to a slot nullifying the aforementioned reference to this\n      worker. Failure to do so will result in a minor memory leak.\n\n    By Qt default, workers are implicitly deleted by their parent\n    :class:`QThreadPool` container immediately on returning from the\n    :meth:`run` method. Although a sensible default for C++-based workers for\n    whom lifecycle management is a non-trivial concern, Python-based workers\n    suffer no such constraints and introduces numerous issues; in particular,\n    allowing Qt to implicitly delete workers on worker completion:\n\n    * Prevents callers from optionally recycling otherwise recyclable workers.\n    * Introduces race conditions between the continued usage of these workers\n      from Python callables from differing threads (e.g., slots, event\n      handlers) and the deletion of these workers by Qt itself from the worker\n      thread. As :class:`QRunnable` instances, workers provide *no* equivalent\n      to the :attr:`QObject.destroyed` signal for deterministically responding\n      to worker deletion. The closest equivalents are:\n\n      * The custom :attr:`signals.finished` signal, which typically (but *not*\n        necessarily) coincides with worker deletion.\n      * The optional Python **finalizer** (i.e., special ``__del__()`` method)\n        and corresponding optional ``callback`` parameter performing similar\n        finalization accepted by the standard :func:`weakref.ref` function,\n        which approximately but *not* exactly coincide with worker deletion and\n        which impose unreasonable constraints on implementation -- notably, the\n        inability to propagate or handle exceptions raised by these callables:\n\n            Exceptions raised by the callback will be noted on the standard\n            error output, but cannot be propagated; they are handled in exactly\n            the same way as exceptions raised from an object’s ``__del__()``\n            method.\n\n        Exception propagation and logging is central to sane and deterministic\n        application behaviour. Any small benefit gained from handling worker\n        deletion via such a callback would surely be dwarfed by the grosser\n        detriment of being unable to properly handle exceptions.\n\n      In either case, there would exist a slice of time in which Qt has\n      implicitly deleted a worker but Python has yet to be notified of that\n      implicit deletion and hence continue to operate under the inappropriate\n      assumption of that worker\'s continued existence. Race conditions ensue.\n      Technically, these conditions could be obviated by:\n\n      * Explicitly creating weak rather than strong references to workers.\n      * Wrapping each access to such a weak reference in a\n        ``try: ... except ReferenceError: ...`` block handling this race.\n\n      In practice, however, the maintenance burden of doing so substantially\n      exceeds the negligible benefit of permitting Qt to delete workers.\n\n    Thread Affinity\n    ----------\n    All attributes of instances of this class reside in the original thread in\n    which this worker was instantiated *except* the following, which reside in\n    a dedicated thread of a parent :class:`QThreadPool` container and hence are\n    guaranteed to be thread-safe by definition:\n\n    * The :meth:`run` method.\n    * All local objects instantiated by the :meth:`run` method.\n\n    All other attributes should be assumed to *not* be thread-safe. These\n    attributes may nonetheless be rendered thread-safe by either:\n\n    * Locking access to these attributes behind Qt-specific mutual exclusion\n      primitives and context managers (e.g., :class:`QMutexLocker`).\n    * Defining these attributes to be Qt-specific atomic types (e.g.,\n      :class:`QAtomicInt`). Since no Python-based Qt framework (including\n      PySide2) exposes these types, this approach applies *only* to C++-based\n      Qt applications. Ergo, atomic types are currently inapplicable. See below\n      for further details.\n\n    Signal-slot Connections\n    ----------\n    This class subclasses the :class:`QRunnable` interface rather than the\n    standard :class:`QObject` base class. This has various real-world\n    implications. In particular, subclasses of this class *cannot* directly\n    participate in standard queued signal-slot connections and hence should\n    define neither signals nor slots.\n\n    Instead, to emit signals from this worker to slots on objects residing in\n    other threads:\n\n    * Declare a separate :class:`QObject` subclass defining these signals.\n    * Instantiate an instance of this subclass in the parent thread in which\n      this worker is instantiated.\n    * Pass this instance to this worker\'s :meth:`__init__` method.\n\n    By definition, this worker *cannot* receive any signals emitted from any\n    objects residing in other threads as conventional slots. Instead:\n\n    * Define each such slot as a simple method of this subclass. Since this\n      method will be run from the other thread in which the object calling this\n      method resides rather than the pooled thread in which this worker\n      resides, this method\'s body *must* protectively guard access to instance\n      variables via Qt-specific mutual exclusion primitives. While numerous\n      primitives exist, the following maximize thread-safety in common edge\n      cases (e.g., exceptions) and hence are strongly preferred:\n\n      * :class:`QReadLocker` and :class:`QWriteLocker`, context managers\n        suitable for general-purpose use in guarding access to variables\n        safely:\n\n        * Readable from multiple concurrent threads.\n        * Writable from only a single thread at a time.\n\n      * :class:`QMutexLocker`, a context manager suitable for general-purpose\n        use in guarding access to variables safely readable *and* writable from\n        only a single thread at a time.\n\n    Lastly, note that Qt defines numerous atomic types publicly accessible to\n    C++ but *not* Python applications (e.g., :class:`QtCore::QAtomicInt`). In\n    theory, these types could be leveraged as an efficient alternative to the\n    primitives listed above. In practice, these types have yet to be exposed\n    via any Python Qt framework (PyQt5, PySide2, or otherwise) and hence remain\n    a pipe dream at best.\n\n    Versus QtConcurrent\n    ----------\n    The API published by this superclass bears a mildly passing resemblance to\n    the API published by the QtConcurrent framework -- notably, the\n    :class:`PySide2.QtCore.QFuture` class. Unfortunately, the latter imposes\n    extreme constraints *not* imposed by this superclass.\n\n    The QtConcurrent framework only provides a single means of multithreading\n    arbitrary long-running tasks: :func:`PySide2.QtConcurrent.run`. The\n    official documentation publicly admits the uselessness of this function:\n\n        Note that the :class:`PySide2.QtCore.QFuture` returned by\n        :func:`PySide2.QtConcurrent.run` does not support canceling, pausing,\n        or progress reporting. The :class:`PySide2.QtCore.QFuture` returned can\n        only be used to query for the running/finished status and the return\n        value of the function.\n\n    One enterprising StackOverflower `circumvented this constraint`_ by\n    defining a robust C++ :class:`PySide2.QtCore.QFuture` analogue supporting\n    canceling, pausing, and progress reporting. Sadly, this analogue requires\n    C++-specific facilities unavailable under Python, including:\n\n    * **Templating.** Since the :class:`PySide2.QtCore.QFuture` API is\n      templated, all analogues of that API are also necessarily templated.\n    * Private, undocumented Qt APIs (e.g., ``QFutureInterface``,\n      ``QFutureInterfaceBase``).\n\n    Ergo, the QtConcurrent framework is largely inapplicable in Python and\n    certainly inapplicable for multithreading arbitrary long-running tasks.\n\n    .. _circumvented this constraint:\n       https://stackoverflow.com/a/16729619/2809027\n\n    Versus QThread + QObject\n    ----------\n    The API published by this superclass also bears a passing resemblance to\n    various third-party APIs duplicating the common worker-thread Qt model.\n    These models typically:\n\n    * Define one or more application-specific **worker types** (i.e.,\n      :class:`QObject` subclasses performing long-running tasks to be\n      multithreaded).\n    * Instantiate these subclasses as local worker objects.\n    * Instantiate a local :class:`QThread` object.\n    * Move these workers into this thread via the :class:`QObject.moveToThread`\n      method.\n    * Start this thread by calling the :class:`QThread.start` method.\n    * Start, pause, resume, cancel, and restart these workers thread by\n      emitting signals connected to slots defined on these workers.\n\n    As with the aforementioned QtConcurrent framework, this approach\n    fundamentally works in C++ but fails in Python. For unknown reasons, the\n    :class:`QObject.moveToThread` method silently fails to properly move worker\n    objects in entirety from the main thread into the worker thread. Slots\n    defined on workers claim to run from within their worker thread but instead\n    run from within the main thread, as trivially observed with logging.\n\n    Ergo, the worker-thread Qt model is also largely inapplicable in Python and\n    certainly inapplicable for multithreading arbitrary long-running tasks.\n\n    Attributes (Public)\n    ----------\n    signals : QBetseeThreadPoolWorkerSignals\n        Low-level collection of all public signals thread-safely emittable by\n        the :meth:`run` method from within an arbitrary pooled thread possibly\n        running *no* Qt event loop.\n\n    Attributes (Private)\n    ----------\n    _thread : WeakRefType\n        Weak reference to the :class:`QThread` instance wrapping the thread in\n        which the :meth:`run` method is currently running if that method is\n        currently running *or* ``None`` otherwise (i.e., if this worker either\n        has yet to be started *or* has already finished).\n    _worker_id : int\n        0-based integer uniquely identifying this worker. This worker is\n        guaranteed to be the *only* instance of this class assigned this\n        integer for the lifetime of the current process. For disambiguity with\n        the :func:`id` builtin, this variable is *not* named ``_id``.\n\n    Attributes (Private: State)\n    ----------\n    _state : ThreadWorkerState\n        Non-thread-safe current execution state of this worker. This state is\n        non-thread-safe and hence should *only* be accessed by instantiating an\n        exception-safe :class:QMutexLocker` context manager nonce passed the\n        :attr:`_state_lock` primitive as the target of a ``with`` context.\n    _state_lock : QMutex\n        Non-exception-safe mutual exclusion primitive rendering the\n        :meth:`state` property thread-safe. This primitive is\n        non-exception-safe and hence should *never* be accessed directly. Each\n        access to this primitive should be encapsulated by instantiating an\n        exception-safe :class:QMutexLocker` context manager nonce as the\n        target of a ``with`` context. Note that the context provided by the\n        :class:QMutexLocker` class is *not* safely reusable and hence *must* be\n        re-instantiated in each ``with`` context.\n    _state_unpaused : QWaitCondition\n        Thread synchronization primitive, permitting this worker when paused in\n        its parent thread to indefinitely block until an object in another\n        thread (e.g., the main thread) requests this worker be unpaused by\n        waking up this primitive and hence this worker.\n\n    See Also\n    ----------\n    https://martinfitzpatrick.name/article/multithreading-pyqt-applications-with-qthreadpool\n        Prominent blog article entitled "Multithreading PyQt applications with\n        QThreadPool," strongly inspiring this implementation.\n    https://stackoverflow.com/a/34302791/2809027\n        StackOverflow answer strongly inspiring this implementation.\n    '

    @type_check
    def __init__(self):
        """
        Initialize this pooled worker.
        """
        super().__init__()
        self.setAutoDelete(False)
        self._worker_id = _get_worker_id_next()
        self._state_lock = QMutex()
        self._state_unpaused = QWaitCondition()
        self._state = ThreadWorkerState.IDLE
        self._thread = None
        self.signals = self._make_signals()

    @type_check
    def init(self, progress_bar: QBetseeProgressBarOrNoneTypes=None, progress_label: QLabelOrNoneTypes=None, handler_failed: CallableOrNoneTypes=None, handler_finished: CallableOrNoneTypes=None) -> None:
        """
        Finalize this pooled worker's initialization with the passed widgets.

        To avoid circular references, this method is guaranteed to *not* retain
        references to this main window on returning. References to child
        widgets (e.g., actions) of this window may be retained, however.

        Parameters
        ----------
        progress_bar : QBetseeProgressBarOrNoneTypes
            Progress bar to connect to numeric progress signals emitted by this
            worker. Defaults to ``None``, in which case the caller is expected
            to manually connect these signals to appropriate widget slots.
        progress_label : QLabelOrNoneTypes
            Label to connect to the
            :attr:`QBetseeThreadPoolWorkerSignals.progress_stated` signal
            emitted by this worker. Defaults to ``None``, in which case the
            caller is expected to manually connect this signal to appropriate
            widget slots.
        handler_failed : CallableOrNoneTypes
            Slot to connect to the
            :attr:`QBetseeThreadPoolWorkerSignals.failed` signal emitted by
            this worker. Defaults to ``None``, in which case the caller is
            expected to manually connect this signal to appropriate slots.
        handler_finished : CallableOrNoneTypes
            Slot to connect to the
            :attr:`QBetseeThreadPoolWorkerSignals.finished` signal emitted by
            this worker. Defaults to ``None``, in which case the caller is
            expected to manually connect this signal to appropriate slots.
        """
        if progress_bar is not None:
            self.signals.progress_ranged.connect(progress_bar.set_range_and_value_minimum)
            self.signals.progressed.connect(progress_bar.setValue)
        else:
            if progress_label is not None:
                self.signals.progress_stated.connect(progress_label.setText)
            if handler_failed is not None:
                self.signals.failed.connect(handler_failed)
            if handler_finished is not None:
                self.signals.finished.connect(handler_finished)

    @property
    def _is_running(self) -> bool:
        """
        ``True`` only if this worker is **running** (i.e., performing
        subclass-specific business logic, typically long-running).

        Caveats
        ----------
        **This private property is non-thread-safe.** The caller *must*
        explicitly embed each access of this property within a context manager
        of the form ``with QMutexLocker(self._state_lock):``.
        """
        return self._state is ThreadWorkerState.RUNNING

    def run(self):
        """
        Thread-safe psuedo-slot (i.e., non-slot method mimicking the
        thread-safe, push-based action of a genuine method) performing *all*
        subclass-specific business logic for this worker.

        This method works in a thread-safe manner safely pausable, resumable,
        and stoppable at any time from any object in any thread by directly
        calling the equally thread-safe :meth:`pause`, :meth:`resume`, and
        :meth :meth:`stop` methods.

        States
        ----------
        If this worker is in the :attr:`ThreadWorkerState.IDLE` state, this
        method changes to the :attr:`ThreadWorkerState.RUNNING` state and calls
        the subclass :meth:`_work` method.

        If this worker is in the :attr:`ThreadWorkerState.PAUSED` state, this
        method interprets this signal as a request to resume the work
        presumably previously performed by this worker by a prior signalling of
        this method.  To avoid reentrancy issues, this method changes to the
        :attr:`ThreadWorkerState.RUNNING` state and immediately returns.
        Assuming that a prior call to this method is still executing, that call
        will internally detect this change and resume working as expected.

        If this worker is in the :attr:`ThreadWorkerState.RUNNING` state, this
        method interprets this signal as an accidental attempt by an external
        caller to re-perform the work concurrently being performed by a prior
        call to this method. In that case, this method safely logs a non-fatal
        warning and immediately returns.

        See the :meth:`pause` method for commentary on these design decisions.

        Signals
        ----------
        This method emits the following signals (in order):

        * :attr:`signals.started` immediately *before* this method performs any
          subclass work.
        * :attr:`signals.failed` immediately *after* this method erroneously
          raises an unexpected exception while performing subclass work but
          *before* the :attr:`signals.finished` signal is emitted.
        * :attr:`signals.succeeded` immediately *after* all subclass work
          performed by this method successfully returns but *before* the
          :attr:`signals.finished` signal is emitted.
        * :attr:`signals.finished` immediately *after* this method performs all
          subclass work, regardless of whether that work succeeded or failed.

        Caveats
        ----------
        This method is *not* intended to be called directly. Only the parent
        thread pool of this worker is intended to call this method. External
        callers are advised to call the :func:`guipoolthread.start_worker`
        function instead.

        Subclasses should override the :meth:`_work` method rather than this
        method to perform subclass-specific business logic. This method is
        neither intended nor designed to be redefined by subclasses.
        """
        is_success = False
        try:
            try:
                guithread.log_debug_thread_current('Starting pooled thread worker "%d"...', self._worker_id)
                guithread.die_if_thread_current_main()
                self._thread = pyref.refer_weak(guithread.get_thread_current())
                with QMutexLocker(self._state_lock):
                    if self._state is not ThreadWorkerState.IDLE:
                        raise BetseePySideThreadWorkerException('Non-reentrant thread "{}" worker "{}" run() method called reentrantly (i.e., multiple times).'.format(guithread.get_thread_current_id(), self._worker_id))
                    self._state = ThreadWorkerState.RUNNING
                self.signals.started.emit()
                self._halt_work_if_requested()
                return_value = self._work()
            except BetseePySideThreadWorkerStopException:
                guithread.log_debug_thread_current('Stopping pooled thread worker "%d"...', self._worker_id)
            except Exception as exception:
                guithread.log_debug_thread_current('Emitting pooled thread worker "%d" exception "%r"...', self._worker_id, exception)
                self.signals.failed.emit(exception)
            else:
                is_success = True
                guithread.log_debug_thread_current('Returning pooled thread worker "%d" value "%r"...', self._worker_id, return_value)
                self.signals.succeeded.emit(return_value)
        finally:
            guithread.log_debug_thread_current('Finishing pooled thread worker "%d" with exit status "%r"...', self._worker_id, is_success)
            with QMutexLocker(self._state_lock):
                if self._is_running:
                    self._state = ThreadWorkerState.IDLE
            self.signals.finished.emit(is_success)
            self._thread = None

    def pause(self) -> None:
        """
        Thread-safe psuedo-slot (i.e., non-slot method mimicking the
        thread-safe push-based action of a genuine slot) pausing all work
        performed by this worker.

        This slot temporarily halts this work in a thread-safe manner safely
        resumable at any time by calling the :meth:`resume` method.

        States
        ----------
        If this worker is in the :attr:`ThreadWorkerState.RUNNING` state,
        this method pauses work by changing this state to
        :attr:`ThreadWorkerState.PAUSED`. The :meth:`_halt_work_if_requested`
        method in the thread running this worker then detects this state change
        and responds by indefinitely blocking on this synchronization primitive
        until subsequently awoken by a call to the :meth:`resume` method.

        If this worker is in any other state, this method silently reduces to a
        noop and hence preserves the existing state.
        """
        guithread.log_debug_thread_current('Requesting pooled thread worker "%d" to pause...', self._worker_id)
        with QMutexLocker(self._state_lock):
            if self._state is not ThreadWorkerState.RUNNING:
                guithread.log_debug_thread_current('Ignoring attempt to pause idle or already paused pooled thread worker "%d".', self._worker_id)
                return
            self._state = ThreadWorkerState.PAUSED

    def resume(self) -> None:
        """
        Thread-safe psuedo-slot (i.e., non-slot method mimicking the
        thread-safe push-based action of a genuine slot) unpausing this worker.

        This method resumes work in a thread-safe manner safely re-pausable at
        any time by re-calling the :meth:`pause` method.

        States
        ----------
        If this worker is in the :attr:`ThreadWorkerState.PAUSED` state,
        this method resumes work by changing this state to
        :attr:`ThreadWorkerState.RUNNING` and waking up the currently blocked
        synchronization primitive if any. The :meth:`_halt_work_if_requested`
        method in the thread running this worker then detects this state change
        and responds by unblocking from this primitive and returning to the
        subclass-specific :meth:`_work` method.

        If this worker is in any other state, this method silently reduces to a
        noop and hence preserves the existing state.
        """
        guithread.log_debug_thread_current('Requesting pooled thread worker "%d" to resume...', self._worker_id)
        with QMutexLocker(self._state_lock):
            try:
                if self._state is not ThreadWorkerState.PAUSED:
                    guithread.log_debug_thread_current('Ignoring attempt to resume idle or already working pooled thread worker "%d".', self._worker_id)
                    return
                self._state = ThreadWorkerState.RUNNING
            finally:
                self._unblock_work()

    def stop(self) -> None:
        """
        Thread-safe psuedo-slot (i.e., non-slot method mimicking the
        thread-safe push-based action of a genuine slot) gracefully and
        permanently halting all work performed by this worker.

        As a necessary side effect, this pseudo-slot also resumes this worker
        if currently paused *before* halting this worker, thus unblocking the
        parent thread of this worker if currently blocked.

        Caveats
        ----------
        By :class:`QRunnable` design, this worker is *not* safely restartable
        after halting -- whether by this method being called, the :meth:`_work`
        method either raising an exception or returning successfully without
        doing so, the parent thread running this worker being terminated, or
        otherwise. Ergo, completion is permanent.

        States
        ----------
        Regardless of the current state of this worker, this method halts work
        by changing this state to :attr:`ThreadWorkerState.IDLE`. The
        :meth:`_halt_work_if_requested` method in the thread running this
        worker then detects this state change and responds by raising an
        exception internally caught by the parent :meth:`run` method.
        """
        guithread.log_debug_thread_current('Requesting pooled thread worker "%d" to stop...', self._worker_id)
        with QMutexLocker(self._state_lock):
            try:
                self._state = ThreadWorkerState.IDLE
            finally:
                self._unblock_work()

    def delete_later(self) -> None:
        """
        Thread-safe psuedo-slot (i.e., non-slot method mimicking the
        thread-safe push-based action of a genuine slot) gracefully stopping
        this worker if needed *and* scheduling all :class:`QObject` instances
        owned by this worker for immediate deletion.

        Specifically, this method schedules all signals owned by this worker
        for immediate deletion and hence disconnection from all slots they are
        currently connected to. (Note that doing so is technically unnecessary
        in most cases. In theory, the subsequent nullification of this worker
        by the call should suffice to schedule this deletion. As doing so has
        no harmful side effects, however, this method exists.)
        """
        guithread.log_debug_thread_current('Scheduling pooled thread worker "%d" for deletion...', self._worker_id)
        with QMutexLocker(self._state_lock):
            if self._is_running:
                self.stop()
            if self.signals is not None:
                self.signals.deleteLater()
                self.signals = None
            self._state = ThreadWorkerState.DELETED

    def halt(self) -> None:
        """
        Thread-safe psuedo-slot (i.e., non-slot method mimicking the
        thread-safe push-based action of a genuine slot) attempting to first
        gracefully and then non-gracefully terminate both this worker and the
        pooled thread running this worker... **by any means necessary.**

        Specifically, this method (in order):

        #. Politely requests this pooled thread to gracefully terminate.
        #. Blocks the calling thread (e.g., the main thread) for a negligible
           span of time (e.g., 100ms) while waiting for this pooled thread to
           gracefully terminate. Since the :func:`guipoolthread.halt_workers`
           function calling this pseudo-slot already blocked for a lengthy span
           of time without success for this worker to gracefully terminate,
           this pseudo-slot effectively performs *no* blocking.
        #. If this pooled thread is still running and hence failed to
           gracefully terminate, this thread is immediately terminated
           non-gracefully. (Note that doing so may induce catastrophic damage.
           See the "Caveats" below.)

        Caveats
        ----------
        This pseudo-slot may induce data loss or corruption in edge cases in
        which this worker fails to gracefully terminate itself within a
        reasonable span of time. This implies that this method should *only* be
        called when absolutely necessary (e.g., at application shutdown).
        """
        WAIT_MAX_MILLISECONDS = 100
        guithread.log_debug_thread_current('Terminating pooled thread worker "%d" shortly...', self._worker_id)
        with QMutexLocker(self._state_lock):
            if self._is_running:
                self.stop()
        thread = self._thread()
        if thread is None:
            guithread.log_debug_thread_current('Terminated pooled thread worker "%d" gracefully...', self._worker_id)
        else:
            guithread.log_debug_thread_current('Terminating pooled thread worker "%d" possibly non-gracefully...', self._worker_id)
            thread.quit()
            thread.wait(WAIT_MAX_MILLISECONDS)
            if thread.isRunning():
                guithread.log_warning_thread_current('Terminating pooled thread worker "%d" non-gracefully!', self._worker_id)
                thread.terminate()
            else:
                guithread.log_debug_thread_current('Terminating pooled thread worker "%d" gracefully after all...', self._worker_id)

    def _make_signals(self) -> QBetseeThreadPoolWorkerSignals:
        """
        Low-level collection of all public signals thread-safely emittable by
        the :meth:`run` method from within an arbitrary pooled thread possibly
        running *no* Qt event loop.

        Design
        ----------
        Subclasses may optionally expose subclass-specific signals by trivially
        redefining this method to return a subclass-specific
        :class:`QBetseeThreadPoolWorkerSignals` instance.
        """
        return QBetseeThreadPoolWorkerSignals(halt_work_if_requested=(pyref.refer_weak(self._halt_work_if_requested)))

    def _work(self) -> None:
        """
        Perform *all* subclass-specific business logic for this worker.

        The superclass :meth:`start` slot internally calls this method in a
        thread-safe manner safely pausable *and* stoppable at any time (e.g.,
        by emitting a signal connected to the :meth:`pause` or :meth:`stop`
        slots).

        Design
        ----------
        Subclasses are required to redefine this method to perform this logic
        in an iterative manner periodically calling the
        :meth:`_halt_work_if_requested` method.

        If either:

        * This worker has been externally signalled to stop (e.g., by emitting
          a signal connected to the :meth:`stop` slot).
        * The thread of execution currently running this worker has been
          externally requested to stop (e.g., by calling the
          :func:`guithread.halt_thread_work` function).

        Then the next such call to the :meth:`_halt_work_if_requested` method
        will raise an exception caught by the parent :meth:`start` slot,
        signalling that slot to immediately terminate this worker. Ergo, that
        method should be called *only* when the subclass is in an
        **interruptible state** (i.e., a self-consistent internal state in
        which this subclass is fully prepared to be immediately terminated).
        """
        raise BetseMethodUnimplementedException()

    def _halt_work_if_requested(self) -> None:
        """
        Thread-safely either temporarily or permanently halt all
        subclass-specific business logic when requested to do so by external
        callers residing in other threads.

        This function is intended to be periodically called by the subclass
        :meth:`_work` function. Specifically, this method:

        * Raises an exception (expected to be caught by the :meth:`run` method
          calling the :meth:`_work` function) if either:

          * This worker has been externally signalled to stop (e.g., by an
            external call to the the :meth:`stop` method).
          * The thread of execution currently running this worker has been
            externally requested to stop (e.g., by calling the
            :func:`guithread.halt_thread_work` function).

        * Pauses this worker if this worker has been externally signalled to
          pause (e.g., by an external call to the the :meth:`pause` method).

        Caveats
        ----------
        This method imposes minor computational overhead and hence should be
        called intermittently (rather than overly frequently). Notably, each
        call to this method processes *all* pending events currently queued
        with this worker's thread -- including those queued for all other
        workers currently running in this thread.

        Raises
        ----------
        BetseePySideThreadWorkerStopException
            If this worker or this worker's thread of execution has been
            signalled or requested to be stopped.
        """
        with QMutexLocker(self._state_lock):
            if self._state is ThreadWorkerState.IDLE or guithread.should_halt_thread_work():
                self._stop_work()
            if self._state is ThreadWorkerState.PAUSED:
                self._block_work()

    def _stop_work(self) -> None:
        """
        Thread-safely gracefully terminate all subclass-specific business logic
        performed by this worker.

        This method raises an internal exception expected to be caught *only*
        by the parent :meth:`run` method, as a crude form of coordinating
        signalling between this and that method.
        """
        guithread.log_debug_thread_current('Stopping pooled thread worker "%d"...', self._worker_id)
        raise BetseePySideThreadWorkerStopException('So say we all.')

    def _block_work(self) -> None:
        """
        Non-thread-safely indefinitely block all subclass-specific business
        logic performed by this worker.

        This method waits for an external call from another thread to a worker
        pseudo-slot (e.g., the :meth:`resume` method), all of which internally
        call the :meth:`_unblock_work` method to safely resume work.

        Caveats
        ----------
        **This private method is non-thread-safe.** The caller *must*
        explicitly embed each call to this method within a context manager of
        the form ``with QMutexLocker(self._state_lock):``.
        """
        guithread.log_debug_thread_current('Pausing pooled thread worker "%d"...', self._worker_id)
        self.signals.paused.emit()
        self._state_unpaused.wait(self._state_lock)
        self.signals.resumed.emit()

    def _unblock_work(self) -> None:
        """
        Non-thread-safely unblock all subclass-specific business logic
        performed by this worker.

        This method wakes up the parent thread of this worker and hence this
        worker *after* the :meth:`_halt_work_if_requested` previously called
        the :meth:`_block_work` method to indefinitely block that thread.
        Moreover, this method is typically called by an external call in
        another thread to a worker pseudo-slot (e.g., the :meth:`resume`
        method), all of which internally call this method to request that this
        worker safely resume work.

        If the parent thread of this worker is *NOT* currently blocked, this
        method silently reduces to a noop.

        Caveats
        ----------
        **This private method is non-thread-safe.** The caller *must*
        explicitly embed each call to this method within a context manager of
        the form ``with QMutexLocker(self._state_lock):``.
        """
        guithread.log_debug_thread_current('Resuming pooled thread worker "%d"...', self._worker_id)
        self._state_unpaused.wakeOne()


class QBetseeThreadPoolWorkerCallable(QBetseeThreadPoolWorker):
    __doc__ = '\n    Low-level **callable-defined pooled worker** (i.e., pooled worker whose\n    business logic is encapsulated by a caller-defined callable at worker\n    initialization time).\n\n    This superclass is a convenience wrapper for the\n    :class:`QBetseeThreadPoolWorker` superclass, simplifying usage in the\n    common case of business logic definable by a single callable. Under the\n    more general-purpose :class:`QBetseeThreadPoolWorker` API, each novel type\n    of business logic must be implemented as a distinct subclass overriding the\n    :meth:`_work` method to perform that specific logic. Under the less\n    general-purpose API provided by this superclass, each such type of business\n    logic is instead implemented as a simple callable (e.g., function, lambda)\n    performing that specific logic; no new subclasses need be defined.\n\n    Attributes\n    ----------\n    _func : CallableTypes\n        Callable to be subsequently called by the :meth:`start` method,\n        performing all business logic isolated to this worker within its parent\n        thread.\n    _func_args : SequenceTypes\n        Sequence of all positional arguments to be passed to the :func:`func`\n        callable when subsequently called.\n    _func_kwargs : MappingType\n        Mapping of all keyword arguments to be passed to the :func:`func`\n        callable when subsequently called.\n    '

    @type_check
    def __init__(self, func, func_args, func_kwargs):
        """
        Initialize this callable-defined pooled worker with the passed callable
        and positional and keyword arguments to be passed to that callable when
        subsequently called by the :meth:`start` method.

        Parameters
        ----------
        func : CallableTypes
            Callable to be subsequently called by the :meth:`start` method,
            performing all business logic isolated to this worker within its
            parent thread.
        func_args : SequenceOrNoneTypes
            Sequence of all positional arguments to be passed to the
            :func:`func` callable when subsequently called. Defaults to
            ``None``, in which case this sequence defaults to the empty tuple.
        func_kwargs : MappingOrNoneTypes
            Mapping of all keyword arguments to be passed to the :func:`func`
            callable when subsequently called. Defaults to ``None``, in which
            case this mapping defaults to the empty dictionary.
        """
        super().__init__()
        if func_args is None:
            func_args = ()
        if func_kwargs is None:
            func_kwargs = {}
        self._func = func
        self._func_args = func_args
        self._func_kwargs = func_kwargs

    def _work(self) -> object:
        return (self._func)(*self._func_args, **self._func_kwargs)


def _get_worker_id_next() -> int:
    """
    Thread-safe 0-based integer uniquely identifying the next **pooled worker**
    (i.e., instance of the :class:`QBetseeThreadPoolWorker` superclass).

    This function internally increments this integer in a thread-safe manner,
    ensuring each of several concurrently instantiated workers to be assigned a
    unique 0-based integer.
    """
    global _worker_id_next
    with QMutexLocker(_worker_id_lock):
        worker_id_next = _worker_id_next
        _worker_id_next += 1
        return worker_id_next