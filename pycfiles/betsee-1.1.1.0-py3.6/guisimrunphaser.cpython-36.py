# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/betsee/gui/simtab/run/phase/guisimrunphaser.py
# Compiled at: 2019-08-01 01:03:54
# Size of source mod 2**32: 10619 bytes
"""
High-level **simulator phaser** (i.e., :mod:`PySide2`-based object containing
each simulator phase controller on behalf of higher-level parent controllers)
functionality.
"""
from betse.science.enum.enumphase import SimPhaseKind
from betse.util.io.log import logs
from betse.util.type.iterable import tuples
from betse.util.type.types import type_check, CallableTypes, QueueType
from betsee.gui.window.guiwindow import QBetseeMainWindow
from betsee.gui.simtab.run.phase.guisimrunphase import QBetseeSimmerPhase
from betsee.gui.simtab.run.work.guisimrunwork import QBetseeSimmerPhaseWorker
from betsee.gui.simtab.run.work.guisimrunworkenum import SimmerPhaseSubkind
from betsee.util.widget.abc.control.guictlabc import QBetseeControllerABC
from collections import deque
SimmerProactorMetadata = tuples.make_named_subclass(class_name='SimmerProactorMetadata',
  item_names=('phases_queued_modelling_count', 'phases_queued_exporting_count'),
  doc='\n    Named tuple created and returned by the\n    :meth:`QBetseeSimmerProactor.get_metadata` method, aggregating metadata\n    synopsizing the current state of the simulator proactor.\n\n    Attributes\n    ----------\n    phases_queued_modelling_count : int\n        Number of simulator phases currently queued for modelling.\n    phases_queued_exporting_count : int\n        Number of simulator phases currently queued for exporting.\n    ')

class QBetseeSimmerPhaser(QBetseeControllerABC):
    __doc__ = '\n    High-level **simulator proactor phaser** (i.e., :mod:`PySide2`-based\n    object containing each simulator phase controller on behalf of\n    higher-level parent controllers).\n\n    Attributes (Public)\n    ----------\n    PHASES : SequenceTypes\n        Immutable sequence of all simulator phase controllers (e.g.,\n        :attr:`_phase_seed`), needed for iteration over these controllers. For\n        sanity, these phases are ordered is simulation order such that:\n\n        * The seed phase is listed *before* the initialization phase.\n        * The initialization phase is listed *before* the simulation phase.\n\n    Attributes (Private)\n    ----------\n    _phase_seed : QBetseeSimmerPhase\n        Controller for all simulator widgets pertaining to the seed phase.\n    _phase_init : QBetseeSimmerPhase\n        Controller for all simulator widgets pertaining to the initialization\n        phase.\n    _phase_sim : QBetseeSimmerPhase\n        Controller for all simulator widgets pertaining to the simulation\n        phase.\n    '

    def __init__(self, *args, **kwargs):
        """
        Initialize this simulator proactor phaser.
        """
        (super().__init__)(*args, **kwargs)
        self._phase_seed = QBetseeSimmerPhase(self)
        self._phase_init = QBetseeSimmerPhase(self)
        self._phase_sim = QBetseeSimmerPhase(self)
        self.PHASES = (
         self._phase_seed, self._phase_init, self._phase_sim)

    @type_check
    def init(self, main_window, set_state_from_phase):
        """
        Finalize this phaser's initialization, owned by the passed main window
        widget.

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
        set_state_from_phase : CallableTypes
            Slot of the parent proactor setting the current state of the
            proactor to the current state of the passed simulator phase. For
            simplicity, this method iteratively for all simulator phases:

            * Connects the queueing signal emitted by this phase to this slot.
            * Calls this slot with this phase, ensuring that the proactor
              derive its initial state from the initial state of each phase.
        """
        super().init(main_window)
        logs.log_debug('Sanitizing simulator proactor phaser state...')
        self._phase_seed.init(kind=(SimPhaseKind.SEED), main_window=main_window)
        self._phase_init.init(kind=(SimPhaseKind.INIT), main_window=main_window)
        self._phase_sim.init(kind=(SimPhaseKind.SIM), main_window=main_window)
        for phase in self.PHASES:
            phase.queue_changed.connect(set_state_from_phase)
            set_state_from_phase(phase)

    def get_metadata(self) -> SimmerProactorMetadata:
        """
        Named tuple aggregating metadata synopsizing the current state of this
        proactor, typically for displaying this metadata to the end user.

        Design
        ----------
        This method is intentionally designed as a getter rather than read-only
        property to inform callers of the non-negligible cost of each call to
        this getter, whose return value should thus be stored in a
        caller-specific variable rather than recreated silently on each access
        of such a property.
        """
        phases_queued_modelling_count = 0
        phases_queued_exporting_count = 0
        for phase in self.PHASES:
            if phase.is_queued_modelling:
                phases_queued_modelling_count += 1
            if phase.is_queued_exporting:
                phases_queued_exporting_count += 1

        return SimmerProactorMetadata(phases_queued_modelling_count=phases_queued_modelling_count,
          phases_queued_exporting_count=phases_queued_exporting_count)

    def enqueue_phase_workers(self) -> QueueType:
        """
        Create and return a new **simulator worker queue** (i.e., double-ended
        queue of each simulator worker to be subsequently run in a
        multithreaded manner by the parent proactor to run a simulation
        subcommand whose corresponding checkbox was checked at the time this
        method was called).

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

        Caveats
        ----------
        **This queue is double- rather than single-ended.** Why? Because the
        Python stdlib fails to provide the latter. Since the former generalizes
        the latter, however, leveraging the former in a single-ended manner
        replicates the behaviour of the latter. Ergo, a double-ended queue
        remains the most space- and time-efficient data structure for doing so.

        Returns
        ----------
        QueueType
            If either:

            * No simulator phase is currently queued.
            * Some simulator phase is currently running (i.e.,
              :attr:`_workers_queued` is already defined to be non-``None``).
        """
        workers_queued = deque()
        for phase in self.PHASES:
            if phase.is_queued_modelling:
                worker = QBetseeSimmerPhaseWorker(phase=phase,
                  phase_subkind=(SimmerPhaseSubkind.MODELLING))
                workers_queued.append(worker)
            if phase.is_queued_exporting:
                worker = QBetseeSimmerPhaseWorker(phase=phase,
                  phase_subkind=(SimmerPhaseSubkind.EXPORTING))
                workers_queued.append(worker)

        return workers_queued