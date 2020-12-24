# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/betsee/gui/simtab/run/guisimrunact.py
# Compiled at: 2019-08-01 01:03:54
# Size of source mod 2**32: 49316 bytes
"""
High-level **simulator proactor** (i.e., :mod:`PySide2`-based object
controlling but *not* displaying the execution of simulation phases)
functionality.
"""
from PySide2.QtCore import QCoreApplication, QObject, Slot
from PySide2.QtWidgets import QProgressBar, QLabel
from betse.exceptions import BetseSimUnstableException
from betse.util.io.log import logs
from betse.util.py import pythread
from betse.util.type import enums
from betse.util.type.obj import objects
from betse.util.type.types import type_check, BoolOrNoneTypes
from betsee.guiexception import BetseeSimmerException, BetseeSimmerBetseException
from betsee.gui.window.guiwindow import QBetseeMainWindow
from betsee.gui.simtab.run.guisimrunenum import SimmerState
from betsee.gui.simtab.run.guisimrunstate import SIMMER_STATES_IDLE, SIMMER_STATES_INTO_FIXED, SIMMER_STATES_FROM_FLUID, SIMMER_STATES_RUNNING, SIMMER_STATES_WORKING, SIMMER_STATES_UNWORKABLE
from betsee.gui.simtab.run.guisimrunabc import QBetseeSimmerStatefulABC
from betsee.gui.simtab.run.phase.guisimrunphase import QBetseeSimmerPhase
from betsee.gui.simtab.run.phase.guisimrunphaser import QBetseeSimmerPhaser
from betsee.gui.simtab.run.work.guisimrunwork import QBetseeSimmerPhaseWorker
from betsee.util.thread import guithread
from betsee.util.thread.pool import guipoolthread
from collections import deque

class QBetseeSimmerProactor(QBetseeSimmerStatefulABC):
    __doc__ = '\n    High-level **simulator proactor** (i.e., :mod:`PySide2`-based object\n    controlling but *not* displaying the execution of simulation phases).\n\n    This proactor maintains all state needed to manage these phases, including:\n\n    * A queue of all simulation subcommands to be interactively run.\n    * Whether or not a simulation subcommand is currently being run.\n    * The state of the currently run simulation subcommand (if any), including:\n\n      * Visualization (typically, Vmem animation) of the most recent step\n        completed for this subcommand.\n      * Textual status describing this step in human-readable language.\n      * Numeric progress as a relative function of the total number of steps\n        required by this subcommand.\n\n    Design\n    ----------\n    This proactor implements the well-known `proactor design pattern`_, whereby\n    each simulation subcommand is asynchronously run by a simulator worker\n    assigned to a pooled thread dedicated to that worker. This pattern is\n    effectively an asynchronous variant of the `reactor design pattern`_.\n\n    For maintainability, this proactor subsumes *all* roles defined by this\n    pattern except the core role of the **asynchronous operation** (e.g., work\n    performed by each worker), including the following roles:\n\n    * **Proactive initiator** (i.e., the highest-level parent object\n      responsible for governing all asynchronous activity).\n    * **Asynchronous operation processor** (i.e., the second-highest-level\n      parent object responsible for starting the asynchronous activity and\n      forwarding responsibility for handling its completion to the completion\n      dispatcher).\n    * **Completion dispatcher** (i.e., the second-lowest-level child object\n      responsible for receiving control from the asynchronous operation\n      processor on the completion of the asynchronous activity and forwarding\n      responsibility for handling its completion to the completion handler).\n    * **Completion handler** (i.e., the lowest-level child object responsible\n      for handling the actual completion of the asynchronous activity).\n\n    .. _proactor design pattern:\n       https://en.wikipedia.org/wiki/Proactor_pattern\n    .. _reactor design pattern:\n       https://en.wikipedia.org/wiki/Reactor_pattern\n\n    Caveats\n    ----------\n    For simplicity, this proactor internally assumes the active Python\n    interpreter to prohibit Python-based multithreading via a Global\n    Interpreter Lock (GIL). Specifically, all worker-centric attributes (e.g.,\n    :attr:`_worker`, :attr:`_workers_queued`) are assumed to be implicitly\n    synchronized despite access to these attributes *not* being explicitly\n    locked behind a Qt-based mutual exclusion primitive.\n\n    GIL-less Python interpreters violate this simplistic assumption. For\n    example, the :meth:`stop_workers` and :meth:`_handle_worker_completion`\n    slots suffer obvious (albeit unlikely) race conditions under GIL-less\n    interpreters due to competitively deleting the same underlying worker in a\n    desynchronized and hence non-deterministic manner.\n\n    Yes, this is assuredly a bad idea. Yes, this is us nonchalantly shrugging.\n\n    Attributes (Public)\n    ----------\n    phaser : QBetseeSimmerPhaser\n        Container containing all simulator phase controllers.\n\n    Attributes (Private)\n    ----------\n    _p : Parameters\n        Simulation configuration singleton.\n\n    Attributes (Private: Thread)\n    ----------\n    _thread : QBetseeWorkerThread\n        Thread controller owning all simulator workers (i.e.,\n        :class:`QBetseeSimmerWorkerABC` instances responsible for running\n        queued simulation subcommands in a multithreaded manner).\n    _workers_queued : {QueueType, NoneType}\n        **Simulator worker queue** (i.e., double-ended queue of each simulator\n        worker to be subsequently run in a multithreaded manner by the parent\n        proactor to run a simulation subcommand whose corresponding checkbox\n        was checked at the time this queue was instantiated) if this simulator\n        has started one or more such workers *or* ``None`` otherwise (i.e., if\n        no such workers have been started).\n\n    Attributes (Private: Widgets)\n    ----------\n    _action_toggle_work : QAction\n        Alias of the :attr:`QBetseeMainWindow.action_sim_run_toggle_work`\n        action.\n    _progress_bar : QProgressBar\n        Alias of the :attr:`QBetseeMainWindow.sim_run_player_progress` widget.\n    _progress_status : QLabel\n        Alias of the :attr:`QBetseeMainWindow.sim_run_player_status` label.\n    _progress_substatus : QLabel\n        Alias of the :attr:`QBetseeMainWindow.sim_run_player_substatus` label.\n    '

    def __init__(self, *args, **kwargs):
        """
        Initialize this simulator.
        """
        (super().__init__)(*args, **kwargs)
        pythread.die_unless_gil()
        self._p = None
        self._action_toggle_work = None
        self._progress_bar = None
        self._progress_status = None
        self._workers_queued = None
        self.phaser = QBetseeSimmerPhaser(self)

    @type_check
    def init(self, main_window):
        """
        Finalize this simulator's initialization, owned by the passed main
        window widget.

        This method connects all relevant signals and slots of *all* widgets
        (including the main window, top-level widgets of that window, and leaf
        widgets distributed throughout this application) whose internal state
        pertains to the high-level state of this simulator.

        To avoid circular references, this method is guaranteed to *not* retain
        references to this main window on returning. References to child
        widgets (e.g., actions) of this window may be retained, however.

        Parameters
        ----------
        main_window : QBetseeMainWindow
            Initialized application-specific parent :class:`QMainWindow` widget
            against which to initialize this object.
        """
        super().init(main_window)
        logs.log_debug('Sanitizing simulator proactor state...')
        self._p = main_window.sim_conf.p
        self._action_toggle_work = main_window.action_sim_run_toggle_work
        self._progress_bar = main_window.sim_run_player_progress
        self._progress_status = main_window.sim_run_player_status
        self._progress_substatus = main_window.sim_run_player_substatus
        self.phaser.init(main_window=main_window,
          set_state_from_phase=(self._set_state_from_phase))

    def halt_workers(self) -> None:
        """
        Coercively (i.e., non-gracefully) halt the current simulator worker if
        any *and* dequeue all subsequently queued workers in a thread-safe
        manner, reverting the simulator to the idle state... **by any means
        necessary.**

        This high-level method subsumes the lower-level :meth:`stop_workers`
        slot by (in order):

        #. If no worker is currently working, silently reducing to a noop.
        #. Attempting to gracefully halt the currently working worker, dequeue
           all subsequently queued workers if any, and unblock this worker's
           parent thread if currently blocked.
        #. If this worker fails to gracefully halt within a reasonable window
           of time (e.g., 30 seconds), coerce this worker to immediately halt.

        Design
        ----------
        This method *must* called at application shutdown (e.g., by the parent
        main window). If this is not done *and* a previously running simulator
        worker is currently paused and hence indefinitely blocking its parent
        thread, this application will itself indefinitely block rather than
        actually shutdown. Which, of course, would be catastrophic.

        Caveats
        ----------
        This method may induce data loss or corruption in simulation output.
        In theory, this should only occur in edge cases in which the current
        simulator worker fails to gracefully stop within a sensible window of
        time. In practice, this implies that this method should *only* be
        called when otherwise unavoidable (e.g., at application shutdown).
        """
        WAIT_MAX_MILLISECONDS = 30000
        logs.log_debug('Finalizing simulator workers...')
        if not self.is_worker:
            return
        worker = self.worker
        self.stop_workers()
        guipoolthread.halt_workers(workers=(
         worker,),
          milliseconds=WAIT_MAX_MILLISECONDS)

    @property
    def is_queued(self) -> bool:
        return any(phase.is_queued for phase in self.phaser.PHASES)

    @property
    def is_worker(self) -> bool:
        """
        ``True`` only if one or more simulator workers currently exist.

        Equivalently, this property returns ``True`` only if the simulator
        worker queue is currently non-empty.

        Design
        ----------
        For safety, this property should be tested *before* attempting to
        access the :meth:`worker` property, which raises an exception when no
        simulator workers currently exist.
        """
        return bool(self._workers_queued)

    @property
    def is_idle(self) -> bool:
        """
        ``True`` only if this proactor is **idle** (i.e., *no* proactor
        worker is either working, stopping, or recently finished, implying this
        proactor to be in either the queued or unqueued states).

        Equivalently, this property returns ``True`` only if this proactor is
        currently performing no work such that the user has either queued or
        unqueued at least one phase since the last work performed by this
        proactor (if any) completed. In this case, this proactor has no
        meaningful data or metadata concerning current or recently completed
        work to display to the user and hence is genuinely "idle."
        """
        return self.state in SIMMER_STATES_IDLE

    @property
    def is_workable(self) -> bool:
        """
        ``True`` only if this proactor is **workable** (i.e., currently capable
        of performing work).

        This property returns ``True`` only if this proactor is guaranteed to
        be safely startable, resumable, or pausable and hence "workable."
        Equivalently, this property returns ``True`` only if the current state
        of this proactor is neither of the following states:

        * Unqueued. In this state, this proactor is required to wait until the
          user queues at least one simulation subcommand.
        * Stopping. In this state, this proactor is required to wait until the
          currently stopping worker does so gracefully.

        In either case, this proactor is incapable of performing work until its
        state changes to any other state -- all of which support work.
        """
        return self.state not in SIMMER_STATES_UNWORKABLE

    @property
    def is_working(self) -> bool:
        """
        ``True`` only if the simulator is **working** (i.e., some proactor
        worker is either running or paused from running some queued proactor
        phase and hence is *not* finished).

        If this fine-grained property is ``True``, note that it is necessarily
        the case that the coarse-grained :attr:`is_workable` property is also
        ``True`` but that the reverse is *not* necessarily the case.
        Equivalently, this proactor is *always* workable when it is working but
        *not* necessarily working when it is workable (e.g., due to currently
        being queued but unstarted).
        """
        return self.state in SIMMER_STATES_WORKING

    @property
    def is_running(self) -> bool:
        """
        ``True`` only if the simulator is **running** (i.e., some simulator
        worker is currently modelling or exporting some queued simulator phase
        and hence is neither paused nor finished).

        If this fine-grained property is ``True``, note that it is necessarily
        the case that the coarse-grained :attr:`is_working` and
        :attr:`is_workable` properties are also ``True`` but that the reverse
        is *not* necessarily the case.  Equivalently, the simulator is *always*
        working when it is running but *not* necessarily running when it is
        working (e.g., due to currently being paused).
        """
        return self.state in SIMMER_STATES_RUNNING

    @property
    def worker(self) -> QBetseeSimmerPhaseWorker:
        """
        **Currently working worker** (i.e., :class:`QRunnable` instance
        currently modelling or exporting a previously queued simulation phase
        in another thread) if any *or* raise an exception otherwise (i.e., if
        no workers are currently working).

        Raises
        ----------
        BetseeSimmerException
            If no worker is currently working.
        """
        self._die_unless_working()
        return self._workers_queued[0]

    @property
    def _is_paused(self) -> bool:
        """
        ``True`` only if the simulator is **paused** (i.e., some simulator
        worker is currently paused while previously modelling or exporting some
        queued simulator phase and hence is neither running nor finished).
        """
        return self.state is SimmerState.PAUSED

    @property
    def _worker_phase_state(self) -> SimmerState:
        """
        State of the queued simulator phase that is currently **running**
        (i.e., either being modelled or exported by this simulator) if any *or*
        raise an exception otherwise.

        Caveats
        ----------
        For safety, this property should *only* be accessed when this queue is
        guaranteed to be non-empty (i.e., when the :meth:`is_worker` property
        is ``True``).

        Design
        ----------
        This property getter trivially reduces to a direct access of the
        :attr:`_worker.phase.state` instance variable, but exists to define the
        corresponding non-trivial property setter.

        Raises
        ----------
        BetseeSimmerException
            If no simulator phase is currently running (i.e.,
            :attr:`_workers_cls` is either ``None`` or empty).
        """
        return self.worker.phase.state

    @_worker_phase_state.setter
    @type_check
    def _worker_phase_state(self, state: SimmerState) -> None:
        """
        Set the state of the queued simulator phase that is currently
        **running** (i.e., either being modelled or exported by this simulator)
        if any to the passed state *or* raise an exception otherwise.

        This property setter may additionally set the state of this simulator
        to the passed state (depending on the current state of this simulator
        and the passed state). Doing so avoids subtle desynchronization issues
        between the state of this phase and this simulator. In particular, if a
        queued simulator phase is currently running, this simulator's state is
        guaranteed to be *always* the state of that phase.

        Caveats
        ----------
        For safety, this property should *only* be accessed when this queue is
        guaranteed to be non-empty (i.e., when the :meth:`is_worker` property
        is ``True``).

        Parameters
        ----------
        state : SimmerState
            New state to set this phase to.

        Raises
        ----------
        BetseeSimmerException
            If no simulator phase is currently running (i.e.,
            :attr:`_workers_cls` is either ``None`` or empty).
        """
        worker_phase = self.worker.phase
        logs.log_debug('Updating simulator phase "%s" state from "%s" to "%s"...', worker_phase.name, enums.get_member_name_lowercase(worker_phase.state), enums.get_member_name_lowercase(state))
        worker_phase.state = state
        self._set_state_from_phase(worker_phase)

    @Slot(QObject)
    def _set_state_from_phase(self, phase: QBetseeSimmerPhase) -> None:
        """
        Context-sensitively set the current state of this proactor to the
        current state of the passed proactor phase.

        Parameters
        ----------
        phase : QBetseeSimmerPhase
            Proactor phase whose current state has been previously set.
        """
        state_new = None
        if phase.state in SIMMER_STATES_INTO_FIXED or self.state in SIMMER_STATES_FROM_FLUID:
            if phase.state is SimmerState.UNQUEUED:
                if self.is_queued:
                    pass
                else:
                    state_new = SimmerState.UNQUEUED
            else:
                state_new = phase.state
        else:
            if state_new is None:
                logs.log_debug('Preserving simulator state as "%s"...', enums.get_member_name_lowercase(self.state))
                state_new = self.state
            else:
                logs.log_debug('Updating simulator proactor state from "%s" to "%s"...', enums.get_member_name_lowercase(self.state), enums.get_member_name_lowercase(state_new))
        self.state = state_new

    def _die_unless_workable(self) -> None:
        """
        Raise an exception unless the simulator is **workable** (i.e.,
        currently capable of performing work).

        Raises
        ----------
        BetseeSimmerException
            If the simulator is unworkable.

        See Also
        ----------
        :meth:`is_workable`
            Further details.
        """
        if not self.is_workable:
            raise BetseeSimmerException(QCoreApplication.translate('QBetseeSimmerProactor', 'Simulator not workable (i.e., not currently working and no phases queued).'))

    def _die_unless_running(self) -> None:
        """
        Raise an exception unless the simulator is **running** (i.e., some
        simulator worker is currently modelling or exporting some queued
        simulation phase and hence is neither paused nor finished).

        Raises
        ----------
        BetseeSimmerException
            If the simulator is *not* running, in which case the simulator is
            either paused or finished.

        See Also
        ----------
        :meth:`is_running`
            Further details.
        """
        if not self.is_running:
            raise BetseeSimmerException(QCoreApplication.translate('QBetseeSimmerProactor', 'Simulator not running (i.e., either paused, finished, or not started).'))

    def _die_unless_paused(self) -> None:
        """
        Raise an exception unless the simulator is **paused** (i.e., some
        simulator worker is currently paused while previously modelling or
        exporting some queued simulation phase and hence is neither running nor
        finished).

        Raises
        ----------
        BetseeSimmerException
            If the simulator is *not* paused, in which case the simulator is
            either running or finished.

        See Also
        ----------
        :meth:`_is_paused`
            Further details.
        """
        if not self._is_paused:
            raise BetseeSimmerException(QCoreApplication.translate('QBetseeSimmerProactor', 'Simulator not paused (i.e., either running, finished, or not started).'))

    def _die_if_working(self) -> None:
        """
        Raise an exception if some simulator worker is currently working.

        Raises
        ----------
        BetseeSimmerException
            If some simulator worker is currently working.

        See Also
        ----------
        :meth:`is_worker`
            Further details.
        """
        if self.is_worker:
            raise BetseeSimmerException(QCoreApplication.translate('QBetseeSimmerProactor', 'Simulation currently working.'))

    def _die_unless_working(self) -> None:
        """
        Raise an exception unless some simulator worker is currently working.

        Raises
        ----------
        BetseeSimmerException
            If no simulator worker is currently working.

        See Also
        ----------
        :meth:`is_worker`
            Further details.
        """
        if not self.is_worker:
            raise BetseeSimmerException(QCoreApplication.translate('QBetseeSimmerProactor', 'No simulation currently working.'))

    @Slot(bool)
    def toggle_work(self, is_playing: BoolOrNoneTypes=None) -> None:
        """
        Slot signalled on either the user interactively *or* the codebase
        programmatically pushing the :class:`QPushButton` widget corresponding
        to the :attr:`_action_toggle_work` variable.

        This slot runs the currently queued phase by either:

        * If this phase is currently paused, resuming this phase.
        * Else, starting this phase.

        Parameters
        ----------
        is_playing : BoolOrNoneTypes
            ``True`` only if the corresponding :class:`QPushButton` widget is
            toggled, implying the user to have requested that the simulator be
            either started or resumed, contextually depending on the current
            state of the simulator; conversely, ``False`` implies a request
            that the simulator be paused. Defaults to ``None``, in which case
            this defaults to the negation of the current simulator state (i.e.,
            ``True`` if the simulator is currently paused and ``False``
            otherwise).
        """
        guithread.log_debug_thread_main('Toggling simulator work by user request...')
        self._die_unless_workable()
        if is_playing is None:
            is_playing = self._action_toggle_work.isChecked()
        else:
            if is_playing:
                if self.is_worker:
                    self._resume_worker()
                else:
                    self._start_workers()
            else:
                self._pause_worker()

    def _start_workers(self) -> None:
        """
        Enqueue one simulator worker for each simulation subcommand whose
        corresponding checkbox in a simulator phase is currently checked *and*
        iteratively start each such worker in a thread-safe manner.

        Raises
        ----------
        BetseeSimmerException
            If either:

            * No simulator phase is currently queued (i.e., no such checkboxes
              are currently checked).
            * One or more workers are already working.
        """
        guithread.log_debug_thread_main('Starting simulator work by user request...')
        self._die_unless_queued()
        guipoolthread.die_if_working()
        self._enqueue_workers()
        self._loop_worker()

    def _pause_worker(self) -> None:
        """
        Pause the currently running simulator.

        This method temporarily pauses the current simulator worker in a
        thread-safe manner safely resumable at any time by calling the
        :meth:`_resume_worker` method.

        Raises
        ----------
        BetseeSimmerException
            If the simulator is *not* currently running.
        """
        guithread.log_debug_thread_main('Pausing simulator work by user request...')
        self._die_unless_running()
        self._worker_phase_state = SimmerState.PAUSED
        self.worker.pause()

    def _resume_worker(self) -> None:
        """
        Resume the currently paused simulator.

        This method resumes the current simulator worker in a thread-safe
        manner after having been previously paused by a call to the
        :meth:`_pause_worker` method.

        Raises
        ----------
        BetseeSimmerException
            If the simulator is *not* currently paused.
        """
        guithread.log_debug_thread_main('Resuming simulator work by user request...')
        self._die_unless_paused()
        self._worker_phase_state = self.worker.simmer_state
        self.worker.resume()

    @Slot()
    def stop_workers(self) -> None:
        """
        Slot signalled on the user interactively (but *not* the codebase
        programmatically) clicking the :class:`QPushButton` widget associated
        with the :attr:`_actionstop_workers` action.

        This method effectively reverts the simulator to the idle state in a
        thread-safe manner by (in order):

        #. Unpausing the current simulator worker if currently paused, thus
           unblocking this worker's parent thread if currently blocked.
        #. Gracefully halting this worker.
        #. Dequeueing all subsequently queued workers.

        Raises
        ----------
        BetseeSimmerException
            If no simulator worker is currently working.
        """
        guithread.log_debug_thread_main('Stopping simulator work by user request...')
        self._die_unless_working()
        worker = self.worker
        self._worker_phase_state = SimmerState.STOPPING
        self._workers_queued = deque((worker,))
        worker.stop()

    def _enqueue_workers(self) -> None:
        """
        Create the **simulator worker queue** (i.e., :attr:`_workers_queued`
        variable) as specified by the pair of checkboxes associated with each
        simulator phase.

        This method enqueues (i.e., pushes onto this queue) workers in
        simulation phase order, defined as the ordering of the members of the
        :class:`betse.science.enum.enumphase.SimPhaseKind` enumeration.
        Callers may safely run the simulation phases performed by these workers
        merely by sequentially assigning each worker enqueued in this queue to
        a thread via the
        :func:`betsee.util.thread.pool.guipoolthread.start_worker` function.

        For example:

        #. The :class:`QBetseeSimmerSubcommandWorkerModelSeed` worker (if any)
           is guaranteed to be queued *before*...
        #. The :class:`QBetseeSimmerSubcommandWorkerModelInit` worker (if any)
           is guaranteed to be queued *before*...
        #. The :class:`QBetseeSimmerSubcommandWorkerModelSim` worker (if any).

        Raises
        ----------
        BetseeSimmerException
            If either:

            * No simulator phase is currently queued.
            * Some simulator phase is currently running (i.e.,
              :attr:`_workers_queued` is already defined to be non-``None``).
        """
        guithread.log_debug_thread_main('Enqueueing simulator workers...')
        self._die_unless_queued()
        self._die_if_working()
        self._workers_queued = self.phaser.enqueue_phase_workers()

    def _dequeue_workers(self) -> None:
        """
        Revert the :attr:`_workers_queued` to ``None``, effectively dequeueing
        (i.e., popping) all previously queued simulator workers.
        """
        guithread.log_debug_thread_main('Dequeueing simulator workers...')
        self._die_unless_working()
        self._workers_queued = None

    def _loop_worker(self) -> None:
        """
        Iteratively run the next enqueued simulator worker if any *or* cleanup
        after this iteration otherwise (i.e., if no workers remain to be run).

        This method perform the equivalent of the body of the abstract loop
        iteratively starting and running all enqueued simulator workers.
        Specifically, this method iteratively starts the next simulator worker
        (i.e., head item of the :attr:`_workers_queued`) enqueued by a prior call
        to the :meth:`_enqueue_workers` method if this queue is non-empty
        *or* garbage-collects this queue otherwise (i.e., if already empty).

        Design
        ----------
        Ideally, the body of this method would be the body of a simple loop
        over all enqueued simulator workers. Since the
        :meth:`_handle_worker_completion` slot calling this method is only
        iteratively signalled by Qt on the completion of each worker, however,
        "rolling" this method into a loop is effectively infeasible.

        Technically, refactoring this method into a continuation-based
        generator would probably suffice to "roll" this method into a loop.
        Doing so, however, would require the use of an asynchronous
        Python-based event loop *and* a heavyweight architectural redesign. In
        short, the current approach stands as the most reasonable.
        """
        if not self.is_worker:
            guithread.log_debug_thread_main('Ceasing simulator worker iteration...')
            return
        worker = self.worker
        guithread.log_debug_thread_main('Iterating simulator worker...')
        self._worker_phase_state = worker.simmer_state
        worker.init(conf_filename=(self._p.conf_filename),
          progress_bar=(self._progress_bar),
          progress_label=(self._progress_substatus),
          handler_failed=(self._handle_worker_exception),
          handler_finished=(self._handle_worker_completion))
        guipoolthread.start_worker(worker)

    @Slot(Exception)
    def _handle_worker_exception(self, exception: Exception) -> None:
        """
        Slot signalled on the currently running simulator worker erroneously
        raising an unexpected exception.

        This slot trivially handles this exception by re-raising this
        exception.  Since the only means of explicitly re-raising an exception
        exposed by Python 3.x is to encapsulate that exception inside another
        exception, this slot unconditionally raises a
        :class:`BetseeSimmerBetseException` exception encapsulating the passed
        exception.

        Parameters
        ----------
        exception : Exception
            Exception raised by this worker.

        Raises
        ----------
        BetseeSimmerBetseException
            Unconditionally encapsulates the passed exception.
        """
        guithread.log_debug_thread_main('Catching simulator worker exception "%s"...', objects.get_class_name_unqualified(exception))
        if isinstance(exception, BetseSimUnstableException):
            raise BetseeSimmerBetseException(synopsis=(QCoreApplication.translate('QBetseeSimmerProactor', 'Simulation halted prematurely due to computational instability.'))) from exception
        else:
            raise BetseeSimmerBetseException(synopsis=(QCoreApplication.translate('QBetseeSimmerProactor', 'Simulation halted prematurely with unexpected error:')),
              exegesis=(str(exception))) from exception

    @Slot(bool)
    def _handle_worker_completion(self, is_success: bool) -> None:
        """
        Handle the completion of the most recently working simulator worker.

        Specifically, this method:

        * Sets the state of the corresponding simulator phase to finished.
        * Pops this worker from the :attr:`_workers_queued`.
        * If this queue is non-empty, starts the next enqueued worker.

        Parameters
        ----------
        is_success : bool
            ``True`` only if this worker completed successfully.
        """
        if not self.is_worker:
            guithread.log_debug_thread_main('Ignoring simulator worker closure...')
            return
        guithread.log_debug_thread_main('Handling simulator worker closure...')
        self._worker_phase_state = SimmerState.FINISHED
        self.worker.delete_later()
        self._workers_queued.popleft()
        self._loop_worker()