# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/betsee/gui/simtab/guisimtab.py
# Compiled at: 2019-08-01 01:03:54
# Size of source mod 2**32: 6341 bytes
"""
High-level **tabbed simulation results** (i.e., partitioning of the
simulation results into multiple pages, each displaying and controlling all
settings associated with a single result of the current simulation) facilities.
"""
from PySide2.QtWidgets import QMainWindow, QTabWidget
from betse.util.type.types import type_check
from betsee.util.widget.mixin.guiwdgmixin import QBetseeObjectMixin

class QBetseeSimmerTabWidget(QBetseeObjectMixin, QTabWidget):
    __doc__ = '\n    :mod:`PySide2`-based tab widget containing multiple tabs, each displaying\n    and controlling all settings associated with a single simulation result\n    (e.g., pickled file, plot, animation) of the current simulation created by\n    a single CLI-oriented simulation subcommand (e.g., ``betse plot init``).\n\n    Attributes (Public)\n    ----------\n    simmer : QBetseeSimmer\n        **Simulator** (i.e., :mod:`PySide2`-based object both displaying *and*\n        controlling the execution of simulation-specific subcommands).\n\n    Attributes (Private: Non-widgets)\n    ----------\n\n    Attributes (Private: Widgets)\n    ----------\n    '

    @type_check
    def __init__(self, *args, **kwargs):
        """
        Initialize this simulator.
        """
        from betsee.gui.simtab.run.guisimrun import QBetseeSimmer
        (super().__init__)(*args, **kwargs)
        self.simmer = QBetseeSimmer()

    @type_check
    def init(self, main_window):
        """
        Finalize this widget's initialization, owned by the passed main window
        widget.

        This method connects all relevant signals and slots of *all* widgets
        (including the main window, top-level widgets of that window, and leaf
        widgets distributed throughout this application) whose internal state
        pertains to the high-level state of this simulation subcommander.

        To avoid circular references, this method is guaranteed to *not* retain
        references to this main window on returning. References to child
        widgets (e.g., actions) of this window may be retained, however.

        Parameters
        ----------
        main_window : QMainWindow
            Initialized application-specific parent :class:`QMainWindow` widget
            against which to initialize this object.
        """
        super().init()
        self._init_widgets(main_window)
        self._init_connections(main_window)

    @type_check
    def _init_widgets(self, main_window: QMainWindow) -> None:
        """
        Create all widgets owned directly by this object *and* initialize all
        other widgets (not necessarily owned by this object) whose internal
        state pertains to the high-level state of simulation subcommands.

        Parameters
        ----------
        main_window : QMainWindow
            Initialized parent :class:`QMainWindow` widget.
        """
        self.simmer.init(main_window=main_window)

    @type_check
    def _init_connections(self, main_window: QMainWindow) -> None:
        """
        Connect all relevant signals and slots of *all* widgets (including the
        main window, top-level widgets of that window, and leaf widgets
        distributed throughout this application) whose internal state pertains
        to the high-level state of simulation subcommands.

        Parameters
        ----------
        main_window : QMainWindow
            Initialized parent :class:`QMainWindow` widget.
        """
        pass

    def halt_work(self) -> None:
        """
        Schedule all currently running simulation work if any for immediate
        and thus possibly non-graceful termination *or* silently reduce to a
        noop otherwise (i.e., if no simulation work is currently running).

        Caveats
        ----------
        This method may induce data loss or corruption in simulation output.
        In theory, this should only occur in edge cases in which the current
        simulator worker fails to gracefully stop within a sensible window of
        time. In practice, this implies that this method should *only* be
        called when otherwise unavoidable (e.g., at application shutdown).

        See Also
        ----------
        :meth:`QBetseeSimmer.halt_work`
            Further details.
        """
        self.simmer.halt_work()