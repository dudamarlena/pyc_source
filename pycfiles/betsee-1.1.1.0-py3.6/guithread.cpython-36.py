# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/betsee/util/thread/guithread.py
# Compiled at: 2019-08-01 01:03:54
# Size of source mod 2**32: 21311 bytes
"""
Low-level **multithreading** (i.e., platform-portable, pure-Qt,
:class:`QThread`-based parallelization implemented external to Python and hence
Python's restrictive Global Interpreter Lock (GIL)) facilities.
"""
from PySide2.QtCore import QCoreApplication, QEventLoop, QThread
from betse.util.io.log import logs
from betse.util.py import pythread
from betse.util.type.types import type_check
from betsee.guiexception import BetseePySideThreadException
from betsee.util.type.guitype import QThreadOrNoneTypes
_THREAD_MAIN_ID = None

def die_if_thread_current_main() -> None:
    """
    Raise an exception if the current thread is the main thread in the active
    Python interpreter.

    This function should typically be called for safety by callers attempting
    to subsequently block the current thread (e.g., by calling the
    :func:`wait_for_events_if_none` function). The main thread administers the
    Qt-specific GUI event loop and hence should *never* be blocked for any
    duration of time whatsoever.

    Raises
    ----------
    BetseePySideThreadException
        If this function is called from the main thread.

    See Also
    ----------
    :func:`is_thread_current_main`
        Further details.
    """
    if is_thread_current_main():
        raise BetseePySideThreadException(QCoreApplication.translate('die_if_thread_current_main', 'Operation prohibited in main thread.'))


def _die_unless_thread_main_id() -> None:
    """
    Raise an exception unless a prior call to the :func:`init` function has
    defined the :data:`_THREAD_MAIN_ID` global.

    Raises
    ----------
    BetseePySideThreadException
        If the :func:`init` function has yet to be called.
    """
    global _THREAD_MAIN_ID
    if _THREAD_MAIN_ID is None:
        raise BetseePySideThreadException(QCoreApplication.translate('_die_unless_thread_main_id', '"_THREAD_MAIN_ID" undefined (e.g., due to the init() function having yet to be called).'))


@type_check
def is_thread_current_main() -> bool:
    """
    ``True`` only if the current thread is the main thread in the active Python
    interpreter.
    """
    global get_thread_current_id
    _die_unless_thread_main_id()
    return get_thread_current_id() == _THREAD_MAIN_ID


@type_check
def should_halt_thread_work(thread: QThreadOrNoneTypes=None) -> bool:
    """
    ``True`` only if some object has requested that the passed thread of
    execution voluntarily halt *all* tasks (e.g., overriden :meth:`QThread.run`
    method) and workers (e.g., subclassed :class:`QBetseeThreadWorkerABC`
    object) currently running in this thread.

    This function is intended to be voluntarily called by tasks and workers.

    Caveats
    ----------
    One parent thread may run an arbitrary number of child workers. However,
    the request to halt tested by this function is a low-level condition
    applying to a single thread rather than a single worker. Hence, if this
    function returns ``False``, *all* tasks and workers currently running in
    this thread are expected to gracefully halt all work being performed and
    then terminate.

    For fine-grained control over worker lifecycles, external callers are
    strongly advised to signal each such worker to gracefully halt (e.g., by
    emitting a signal connected to the :meth:`QBetseeThreadWorkerABC.stop`
    slot) rather than requesting that the thread running those workers halt
    (e.g., by calling the :meth:`QThread.requestInterruption` method).
    Nonetheless, workers are expected to respect both types of requests.

    For convenience, note that the
    :meth:`QBetseeThreadWorkerABC._halt_work_if_requested` method implicitly
    respects both types of requests. Ergo, :class:`QBetseeThreadWorkerABC`
    subclasses need *not* and should *not* explicitly call this function.

    Parameters
    ----------
    thread : QThreadOrNoneTypes
        Thread to request to be halted. Defaults to ``None``, in which case the
        current thread of execution is requested to be halted.

    Returns
    ----------
    bool
        ``True`` only if some object has requested this thread to voluntarily
        halt *all* tasks and workers currently running in this thread.

    See Also
    ----------
    :func:`halt_thread_work`
        Companion function requesting this thread to voluntarily halt these
        tasks and workers.
    """
    if thread is None:
        thread = get_thread_current()
    return thread.isInterruptionRequested()


def get_thread_current() -> QThread:
    """
    Wrapper encapsulating the **current thread** (i.e., Qt-specific thread of
    execution responsible for the call to this function).
    """
    return QThread.currentThread()


def get_thread_current_id() -> int:
    pass


def get_thread_current_process_name() -> str:
    """
    Name of the low-level kernel-level process associated with the current
    thread, equivalent to the Qt-specific name of this object.

    See Also
    ----------
    :meth:`betsee.util.thread.guithreadcls.QBetseeWorkerThread.process_name`
        Further details.
    """
    thread = get_thread_current()
    return thread.objectName()


def get_thread_event_dispatcher_current() -> tuple:
    """
    2-tuple ``(thread, event_dispatcher)`` encapsulating both the thread *and*
    event dispatcher for the current thread of execution if this thread has an
    event dispatcher *or* raise an exception otherwise (i.e., if this thread
    has no event dispatcher).

    Design
    ----------
    This getter intentionally returns both the thread *and* event dispatcher
    for the current thread of execution rather than merely the latter. Why?
    Because it appears infeasible to pass around arbitrary instances of the
    :class:`QAbstractEventDispatcher` superclass. For unknown reasons, some
    combination of Python and/or Qt aggressively collect an event dispatcher in
    the absence of a strong reference to the thread of that event dispatcher.
    Ergo, the two *must* be passed around as a single, cohesive unit.

    Returns
    ----------
    (QThread, QAbstractEventDispatcher)
        2-tuple ``(thread, event_dispatcher)``, where:

        * ``thread`` is the Qt-based wrapper encapsulating the current thread.
        * ``event_dispatcher`` is the Qt-based wrapper for the event dispatcher
          of the current thread.

    Raises
    ----------
    BetseePySideThreadException
        If this thread has *no* event dispatcher.
    """
    thread = QThread.currentThread()
    event_dispatcher = thread.eventDispatcher()
    if not event_dispatcher:
        raise BetseePySideThreadException(QCoreApplication.translate('get_thread_event_dispatcher_current', 'No event dispatcher running for thread "{}".'.format(thread.objectName())))
    return (
     thread, event_dispatcher)


@type_check
def log_debug_thread_current(message: str, *args) -> None:
    """
    Log the passed debug message from any arbitrary thread with the root
    logger, formatted with the passed ``%``-style positional arguments.

    Parameters
    ----------
    message : str
        Human-readable message to be logged.

    All remaining positional parameters are conditionally interpolated as
    ``%``-style format specifiers into this message by logging facilities.

    See Also
    ----------
    :func:`log_debug_thread_main`
        Faster analogue intended to be called *only* when the current thread is
        the main thread.
    """
    (logs.log_debug)(message + ' <from thread "%d">', *args, *(get_thread_current_id(),))


@type_check
def log_warning_thread_current(message: str, *args) -> None:
    """
    Log the passed warning message from any arbitrary thread with the root
    logger, formatted with the passed ``%``-style positional arguments.

    Parameters
    ----------
    message : str
        Human-readable message to be logged.

    All remaining positional parameters are conditionally interpolated as
    ``%``-style format specifiers into this message by logging facilities.
    """
    (logs.log_warning)(message + ' <from thread "%d">', *args, *(get_thread_current_id(),))


@type_check
def log_debug_thread_main(message: str, *args) -> None:
    """
    Log the passed debug message from the main thread with the root logger,
    formatted with the passed ``%``-style positional arguments.

    Caveats
    ----------
    This function is intended to be called *only* from the main thread. For
    efficiency, this function does *not* validate this to be the case.

    Parameters
    ----------
    message : str
        Human-readable message to be logged.

    All remaining positional parameters are conditionally interpolated as
    ``%``-style format specifiers into this message by logging facilities.

    See Also
    ----------
    :func:`log_debug_thread_current`
        Slower analogue intended to be called from *any* thread.
    """
    (logs.log_debug)(message + ' <from main thread "%d">', *args, *(_THREAD_MAIN_ID,))


@type_check
def halt_thread_work(thread: QThreadOrNoneTypes=None) -> bool:
    """
    Requested that the passed thread of execution voluntarily halt *all* tasks
    (e.g., overriden :meth:`QThread.run` method) and workers (e.g., subclassed
    :class:`QBetseeThreadWorkerABC` object) currently running in this thread.

    This function is intended to be called from objects in other threads.

    Caveats
    ----------
    After this function is called, this request will be unconditionally
    preserved in this thread until this thread is manually halted and restarted
    (e.g., by calling the :meth:`QBetseeWorkerThread.halt` and
    :meth:`QBetseeWorkerThread.start` methods in that order). Sadly, doing so:

    * Terminates all tasks and workers currently running in this thread,
      typically in a non-graceful manner resulting in in-memory or on-disk data
      corruption.
    * Discards all pending events currently queued with this thread --
      including both outgoing signals emitted by *and* incoming slots signalled
      on any workers still running in this thread.

    Hence, due to long-standing deficiencies in the Qt API, this request
    *cannot* be gracefully "undone." Attempting to do so *always* runs a risk
    of non-gracefully terminating running and pending work. The only
    alternative to this extremely concerning caveat is to signal each such
    worker to gracefully halt (e.g., by emitting a signal connected to the
    :meth:`QBetseeThreadWorkerABC.stop` slot) rather than calling this method.

    **You have been warned.** There be vicious vipers scuttling about here.

    Parameters
    ----------
    thread : QThreadOrNoneTypes
        Thread to request to be halted. Defaults to ``None``, in which case the
        current thread of execution is requested to be halted.

    See Also
    ----------
    :func:`should_halt_thread_work`
        Further details.
    https://forum.qt.io/topic/43067/qthread-requestinterruption-cannot-be-undone
        Prominent Qt forum discussion on this lamentable topic.
    """
    if thread is None:
        thread = get_thread_current()
    return thread.requestInterruption()


@type_check
def process_thread_current_events() -> None:
    """
    Process all pending events queued with the current thread.

    This function unconditionally processes *all* such events, including both
    outgoing signals emitted by *and* incoming slots signalled on all workers
    currently running in this thread.

    Caveats
    ----------
    Avoid manually calling the static :func:`QCoreApplication.processEvents`
    function to process events for the current thread of execution. If this
    thread has *no* event dispatcher, that function silently and hence unsafely
    ignores all pending :class:`DeferredDelete` events currently queued for
    this thread. Since numerous standard widgets (e.g., :class:`QToolTip`)
    require these events to be processed in a timely manner, ignoring these
    events fundamentally disrupts widget sanity.
    """
    thread, event_dispatcher = get_thread_event_dispatcher_current()
    event_dispatcher.processEvents(QEventLoop.AllEvents)


@type_check
def wait_for_thread_current_event_if_none() -> None:
    """
    Indefinitely block the current thread until *another* thread posts a new
    event to the current thread if *no* pending events are queued with the
    current thread *or* safely return immediately otherwise (i.e., if one or
    more pending events are currently queued with this thread).

    This function is intended to be called *only* from the slots of workers
    currently running in the thread of execution associated with the passed
    event dispatcher. In this case, this function call gracefully returns when
    another object in another thread of execution emits a signal connected to a
    slot of such a worker.

    Caveats
    ----------
    **Never call this function from an object owned by the main event-handling
    thread.** Doing so effectively blocks the application GUI managed by this
    thread. Instead, only call this function from a worker guaranteed to be
    running in this thread.
    """
    die_if_thread_current_main()
    thread, event_dispatcher = get_thread_event_dispatcher_current()
    event_dispatcher.processEvents(QEventLoop.WaitForMoreEvents)


def init() -> None:
    """
    Initialize this submodule.

    Caveats
    ----------
    **This function is intended to be called from the main thread.** If this is
    *not* the case, the :data:`_THREAD_MAIN_ID` global will be improperly
    initialized.

    Raises
    ----------
    BetsePyException
        If the active Python interpreter does *not* support multithreading.
    """
    global _THREAD_MAIN_ID
    global get_thread_current_id
    logs.log_debug('Initializing multithreading facilities...')
    pythread.die_unless_threadable()
    try:
        QThread.currentThreadId
    except AttributeError:
        logs.log_warning('QThread.currentThreadId() undefined; falling back to thread wrapper ID.')

        def get_thread_current_id() -> int:
            return id(get_thread_current())

    else:

        def get_thread_current_id() -> int:
            return QThread.currentThreadId()

    get_thread_current_id.__doc__ = "\n    Arbitrary Qt-specific integer uniquely identifying the current thread in\n    the active Python interpreter if the currently installed version of PySide2\n    exposes the :meth:`QThread.currentThreadId` method yielding this integer\n    *or* the Python-specific ID of this thread's object wrapper instead.\n\n    Caveats\n    ----------\n    This integer is non-portable and hence should *only* be embedded in\n    low-level debugging messages.\n\n    Note that there exists no general-purpose :func:`get_thread_id` getter\n    returning the unique identifier for an arbitrary thread, as Qt defines no\n    corresponding functionality for doing so.\n\n    See Also\n    ----------\n    :func:`get_thread_current`\n        Further details.\n    "
    _THREAD_MAIN_ID = get_thread_current_id()