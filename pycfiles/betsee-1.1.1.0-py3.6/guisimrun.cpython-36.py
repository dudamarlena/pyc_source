# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/betsee/gui/simtab/run/guisimrun.py
# Compiled at: 2019-08-01 01:03:54
# Size of source mod 2**32: 24960 bytes
"""
High-level **simulator** (i.e., :mod:`PySide2`-based object both displaying
*and* controlling the execution of simulation phases) functionality.
"""
from PySide2.QtCore import Slot
from betse.science.enum.enumphase import SimPhaseKind
from betse.util.io.log import logs
from betse.util.type.text.string import strs
from betse.util.type.types import type_check
from betsee.gui.window.guiwindow import QBetseeMainWindow
from betsee.gui.simtab.run.guisimrunact import QBetseeSimmerProactor
from betsee.gui.simtab.run.guisimrunenum import SimmerState, SimmerModelState
from betsee.gui.simtab.run.guisimrunstate import SIM_PHASE_KIND_TO_NAME, SIMMER_STATES_IDLE, SIMMER_STATE_TO_PROACTOR_STATUS, SIMMER_STATE_TO_PROACTOR_SUBSTATUS, SIMMER_STATES_HALTING
from betsee.util.widget.abc.control.guictlabc import QBetseeControllerABC

class QBetseeSimmer(QBetseeControllerABC):
    __doc__ = '\n    High-level **simulator** (i.e., :mod:`PySide2`-based object both displaying\n    *and* controlling the execution of simulation phases).\n\n    Attributes (Private)\n    ----------\n    _progress_status_text_prior : str\n        Most recent textual contents of the\n        :attr:`QBetseeMainWindow.sim_run_player_status` label, preserved so as\n        to permit this text to be transparently reused without localization\n        concerns (particularly on repeatedly switching between the paused,\n        stopped, and finished simulator states).\n\n    Attributes (Private: Controllers)\n    ----------\n    _proactor : QBetseeSimmerProactor\n        **Simulator proactor** (i.e., lower-level :mod:`PySide2`-based\n        delegate controlling but *not* displaying the execution of simulation\n        phases). In standard model-view-controller (MVC) parlance:\n\n        * BETSE itself is the model (M) that runs simulation phases.\n        * This proactor is the controller (C) for running simulation phases.\n        * This parent object is the view (V) into running simulation phases.\n\n    Attributes (Private: Widgets)\n    ----------\n    _action_stop_workers : QAction\n        Alias of the :attr:`QBetseeMainWindow.action_sim_run_stop_workers`\n        action.\n    _action_toggle_work : QAction\n        Alias of the :attr:`QBetseeMainWindow.action_sim_run_toggle_work`\n        action.\n    _player_toolbar : QFrame\n        Alias of the :attr:`QBetseeMainWindow.sim_run_player_toolbar_frame`\n        frame containing only the :class:`QToolBar` containing buttons for\n        controlling the currently running simulation.\n    _progress_bar : QProgressBar\n        Alias of the :attr:`QBetseeMainWindow.sim_run_player_progress` widget.\n    _progress_status : QLabel\n        Alias of the :attr:`QBetseeMainWindow.sim_run_player_status` label,\n        synopsizing the current state of this simulator.\n    _progress_substatus : QLabel\n        Alias of the :attr:`QBetseeMainWindow.sim_run_player_substatus` label,\n        detailing the current state of this simulator.\n    '

    def __init__(self, *args, **kwargs):
        """
        Initialize this simulator.
        """
        (super().__init__)(*args, **kwargs)
        self._proactor = QBetseeSimmerProactor(self)
        self._action_toggle_work = None
        self._action_stop_workers = None
        self._player_toolbar = None
        self._progress_bar = None
        self._progress_status = None
        self._progress_substatus = None
        self._progress_status_text_prior = None

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
        logs.log_debug('Sanitizing simulator state...')
        self._init_widgets(main_window)
        self._init_connections(main_window)

    @type_check
    def _init_widgets(self, main_window: QBetseeMainWindow) -> None:
        """
        Create all widgets owned directly by this object *and* initialize all
        other widgets (*not* always owned by this object) concerning this
        simulator.

        Parameters
        ----------
        main_window : QBetseeMainWindow
            Initialized application-specific parent :class:`QMainWindow`
            widget.
        """
        self._action_toggle_work = main_window.action_sim_run_toggle_work
        self._action_stop_workers = main_window.action_sim_run_stop_work
        self._player_toolbar = main_window.sim_run_player_toolbar_frame
        self._progress_bar = main_window.sim_run_player_progress
        self._progress_status = main_window.sim_run_player_status
        self._progress_substatus = main_window.sim_run_player_substatus
        self._progress_substatus_group = main_window.sim_run_player_substatus_group

    @type_check
    def _init_connections(self, main_window: QBetseeMainWindow) -> None:
        """
        Connect all relevant signals and slots of *all* widgets (including the
        main window, top-level widgets of that window, and leaf widgets
        distributed throughout this application) whose internal state pertains
        to the high-level state of this simulator.

        Parameters
        ----------
        main_window : QBetseeMainWindow
            Initialized application-specific parent :class:`QMainWindow`
            widget.
        """
        self._action_toggle_work.triggered.connect(self._proactor.toggle_work)
        self._action_stop_workers.triggered.connect(self._proactor.stop_workers)
        self._proactor.state_changed.connect(self._sync_widgets_to_proactor_state)
        self._progress_bar.valueChanged.connect(self._sync_widgets_to_proactor_state_current)
        self._proactor.init(main_window)

    def halt_work(self) -> None:
        """
        Schedule the currently running simulation phase if any for immediate
        and thus possibly non-graceful termination *or* silently reduce to a
        noop otherwise (i.e., if no simulation phase is currently running).

        Caveats
        ----------
        This method may induce data loss or corruption in simulation output.
        In theory, this should only occur in edge cases in which the current
        simulator worker fails to gracefully stop within a sensible window of
        time. In practice, this implies that this method should *only* be
        called when otherwise unavoidable (e.g., at application shutdown).

        See Also
        ----------
        :meth:`QBetseeSimmerProactor.halt_workers`
            Further details.
        """
        self._proactor.halt_workers()

    @Slot(SimmerState, SimmerState)
    def _sync_widgets_to_proactor_state(self, state_new: SimmerState, state_old: SimmerState) -> None:
        """
        Slot signalled on each transition of the proactor from the passed
        previous state into the passed current state.

        This slot synchronizes all widgets owned or otherwise controlled by
        this simulator to reflect this transition.

        Parameters
        ----------
        state_new : SimmerState
            Current state of the proactor.
        state_old : SimmerState
            Previous state of the proactor.
        """
        logs.log_debug('Synchronizing widgets to proactor state transition...')
        if state_new in SIMMER_STATES_IDLE or state_new is SimmerState.MODELLING and state_old is not SimmerState.MODELLING:
            logs.log_debug('Resetting simulator progress bar...')
            self._progress_bar.reset()
        self._sync_widgets_to_proactor_state_current()

    @Slot()
    def _sync_widgets_to_proactor_state_current(self) -> None:
        """
        Slot signalled on each transition of the proactor from its previous
        into its current state.

        This slot synchronizes all widgets owned or otherwise controlled by
        this simulator to reflect the current state of the proactor.
        """
        logs.log_debug('Synchronizing widgets to proactor state...')
        self._sync_toolbar()
        self._sync_progress()

    def _sync_toolbar(self) -> None:
        """
        Update the contents of the **simulator toolbar** (i.e.,
        :class:`QToolBar` instance containing buttons controlling the currently
        running simulation).
        """
        self._player_toolbar.setEnabled(self._proactor.is_queued)
        self._action_toggle_work.setEnabled(self._proactor.is_workable)
        self._action_toggle_work.setChecked(self._proactor.is_running)
        self._action_stop_workers.setEnabled(self._proactor.is_working)

    def _sync_progress(self) -> None:
        """
        Update the contents of all simulator widgets to reflect the current
        progress of the simulation subcommand being run by the proactor (if
        any).
        """
        self._sync_progress_status()
        self._sync_progress_substatus()

    def _sync_progress_status(self) -> None:
        """
        Update the text displayed by the :attr:`_progress_status` label,
        synopsizing the current state of this simulator.
        """
        status_text_template = SIMMER_STATE_TO_PROACTOR_STATUS[self._proactor.state]
        phase_type_name = SIM_PHASE_KIND_TO_NAME[self._proactor.worker.phase.kind] if self._proactor.is_worker else 'the nameless that shall not be named'
        if self._progress_status_text_prior is None:
            self._progress_status_text_prior = self._progress_status.text()
        status_text = status_text_template.format(phase_type=phase_type_name,
          status_prior=(self._progress_status_text_prior))
        if self._proactor.state not in SIMMER_STATES_HALTING:
            self._progress_status_text_prior = status_text
            self._progress_status_text_prior = strs.lowercase_char_first(strs.remove_suffix_if_found(text=(self._progress_status_text_prior),
              suffix='...'))
        self._progress_status.setText(status_text)

    def _sync_progress_substatus(self) -> None:
        """
        Update the text displayed by the :attr:`_progress_substatus` label,
        detailing the current state of this simulator.
        """
        substatus_value = SIMMER_STATE_TO_PROACTOR_SUBSTATUS[self._proactor.state]
        substatus_text_template = None
        if self._proactor.state is SimmerState.MODELLING:
            phase_kind = self._proactor.worker.phase.kind
            if phase_kind is SimPhaseKind.SEED:
                return
            model_state = None
            if self._progress_bar.is_reset:
                model_state = SimmerModelState.PREPARING
            else:
                if self._progress_bar.is_done:
                    model_state = SimmerModelState.FINISHING
                else:
                    model_state = SimmerModelState.MODELLING
            model_state_to_substatus_text_template = substatus_value[phase_kind]
            substatus_text_template = model_state_to_substatus_text_template[model_state]
        else:
            if self._proactor.state is SimmerState.EXPORTING:
                return
            substatus_text_template = substatus_value
        substatus_text_prior = self._progress_substatus.text()
        proactor_metadata = self._proactor.phaser.get_metadata()
        substatus_text = substatus_text_template.format(progress_current=(self._progress_bar.value()),
          progress_maximum=(self._progress_bar.maximum()),
          queued_modelling=(proactor_metadata.phases_queued_modelling_count),
          queued_exporting=(proactor_metadata.phases_queued_exporting_count),
          substatus_prior=substatus_text_prior)
        self._progress_substatus.setText(substatus_text)