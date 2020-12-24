# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/betsee/gui/simtab/run/phase/guisimrunphase.py
# Compiled at: 2019-08-01 01:03:54
# Size of source mod 2**32: 13195 bytes
"""
Low-level **simulator phase** (i.e., simulation phase to be queued for
modelling and/or exporting by this simulator) functionality.
"""
from PySide2.QtCore import QObject, Signal, Slot
from betse.science.enum.enumphase import SimPhaseKind
from betse.util.io.log import logs
from betse.util.type import enums
from betse.util.type.decorator.decmemo import property_cached
from betse.util.type.types import type_check
from betsee.gui.simtab.run.guisimrunabc import QBetseeSimmerStatefulABC
from betsee.gui.simtab.run.guisimrunenum import SimmerState
from betsee.gui.simtab.run.guisimrunstate import SIMMER_STATE_TO_PHASE_STATUS, SIMMER_STATES_FROM_FLUID
from betsee.gui.window.guiwindow import QBetseeMainWindow

class QBetseeSimmerPhase(QBetseeSimmerStatefulABC):
    __doc__ = '\n    **Simulator phase controller** (i.e., :mod:`PySide2`-based object wrapping\n    a simulator phase to be queued for modelling and/or exporting by this\n    simulator).\n\n    This controller maintains all state required to interactively manage this\n    simulator phase.\n\n    Attributes (Private: Non-widgets)\n    ----------\n    _kind : SimPhaseKind\n        Type of simulation phase controlled by this controller.\n\n    Attributes (Private: Widgets)\n    ----------\n    _queue_modelling_lock : QCheckBox\n        Checkbox toggling whether this phase is queueable for modelling.\n    _queue_modelling : QCheckBox\n        Checkbox toggling whether this phase is queued for modelling.\n    _queue_exporting : QCheckBoxOrNoneTypes\n        Checkbox toggling whether this phase is queued for exporting if this\n        phase supports exporting *or* ``None`` otherwise. While most phases\n        support exporting, some (e.g., the seed phase) do *not*.\n    _status : QLabel\n        Label synopsizing the current state of this phase.\n    '
    queue_changed = Signal(QObject)

    def __init__(self, *args, **kwargs):
        """
        Initialize this simulator phase.
        """
        (super().__init__)(*args, **kwargs)
        self._kind = None
        self._queue_modelling_lock = None
        self._queue_modelling = None
        self._queue_exporting = None
        self._status = None

    @type_check
    def init(self, main_window, kind):
        """
        Finalize the initialization of this simulator phase, owned by the
        passed main window widget.

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
        kind : SimPhaseKind:
            Type of simulation phase controlled by this controller.
        """
        super().init(main_window)
        self._kind = kind
        logs.log_debug('Sanitizing simulator phase "%s" state...', self.name)
        self._init_widgets(main_window)
        self._init_connections(main_window)

    @type_check
    def _init_widgets(self, main_window: QBetseeMainWindow) -> None:
        """
        Create all widgets owned directly by this object *and* initialize all
        other widgets (*not* always owned by this object) concerning this
        simulator phase.

        Parameters
        ----------
        main_window : QBetseeMainWindow
            Initialized application-specific parent :class:`QMainWindow`
            widget.
        """
        is_unqueueable_model_name = 'sim_run_queue_{}_model_lock'.format(self.name)
        is_queued_model_name = 'sim_run_queue_{}_model'.format(self.name)
        is_queued_export_name = 'sim_run_queue_{}_export'.format(self.name)
        status_name = 'sim_run_queue_{}_status'.format(self.name)
        self._queue_modelling_lock = main_window.get_widget(widget_name=is_unqueueable_model_name)
        self._queue_modelling = main_window.get_widget(widget_name=is_queued_model_name)
        self._status = main_window.get_widget(widget_name=status_name)
        self._queue_exporting = main_window.get_widget_or_none(widget_name=is_queued_export_name)

    @type_check
    def _init_connections(self, main_window: QBetseeMainWindow) -> None:
        """
        Connect all relevant signals and slots of *all* widgets (including the
        main window, top-level widgets of that window, and leaf widgets
        distributed throughout this application) whose internal state pertains
        to the high-level state of this simulator phase.

        Parameters
        ----------
        main_window : QBetseeMainWindow
            Initialized application-specific parent :class:`QMainWindow`
            widget.
        """
        self._queue_modelling.toggled.connect(self._toggle_queue_subkind)
        if self._queue_exporting is not None:
            self._queue_exporting.toggled.connect(self._toggle_queue_subkind)
        self._queue_modelling_lock.toggled.connect(self._toggle_queue_modelling_lock)
        self._queue_modelling.setChecked(True)

    @property
    def is_queued(self) -> bool:
        """
        ``True`` only if this simulator phase is currently queued (i.e., for
        modelling and/or exporting).
        """
        return self.is_queued_modelling or self.is_queued_exporting

    @property
    def is_queued_modelling(self) -> bool:
        """
        ``True`` only if this simulator phase is currently queued for
        modelling.
        """
        return self._queue_modelling.isChecked()

    @property
    def is_queued_exporting(self) -> bool:
        """
        ``True`` only if this simulator phase is currently queued for
        exporting.
        """
        return self._queue_exporting is not None and self._queue_exporting.isChecked()

    @property
    def kind(self) -> SimPhaseKind:
        """
        Type of simulation phase controlled by this controller.
        """
        return self._kind

    @property_cached
    def name(self) -> str:
        """
        Machine-readable alphabetic lowercase name of the type of simulation
        phase controlled by this controller (e.g., ``seed``, ``init``).
        """
        return enums.get_member_name_lowercase(self._kind)

    @Slot(bool)
    def _toggle_queue_subkind(self, is_queued: bool) -> None:
        """
        Slot signalled on either the user interactively *or* the codebase
        programmatically toggling the :class:`QCheckBox` widget corresponding
        to either the :attr:`_queue_modelling` *or* :attr:`_queue_exporting`
        variables.

        If this slot changes the state of this simulator phase to either
        :attr:`SimmerState.QUEUED` or :attr:`SimmerState.UNQUEUED`, this slot
        notifies interested parties of this fact by signalling the
        :attr:`queue_changed` with this simulator phase.

        Parameters
        ----------
        is_queued : bool
            ``True`` only if this :class:`QCheckBox` is currently checked.
        """
        logs.log_debug('Enqueueing simulator phase "%s"...' if is_queued else 'Dequeueing simulator phase "%s"...', self.name)
        if self.state in SIMMER_STATES_FROM_FLUID:
            self.state = SimmerState.QUEUED if self.is_queued else SimmerState.UNQUEUED
            self.queue_changed.emit(self)

    @Slot(bool)
    def _toggle_queue_modelling_lock(self, is_unqueueable_model: bool) -> None:
        """
        Slot signalled on either the user interactively *or* the codebase
        programmatically toggling the checkable :class:`QToolButton` widget
        corresponding to the :attr:`_queue_modelling_lock` variable.

        Specifically, if:

        * This button is checked, this slot locks (i.e., disables) the
          :class:`QCheckBox` widget corresponding to the
          :attr:`_queue_modelling` variable.
        * This button is unchecked, this slot unlocks (i.e., enables) that
          :class:`QCheckBox` widget.

        Parameters
        ----------
        is_unqueueable_model : bool
            ``True`` only if this :class:`QToolButton` is currently checked.
        """
        self._queue_modelling.setEnabled(not is_unqueueable_model)

    def _update_state(self) -> None:
        status_text = SIMMER_STATE_TO_PHASE_STATUS[self.state]
        self._status.setText(status_text)