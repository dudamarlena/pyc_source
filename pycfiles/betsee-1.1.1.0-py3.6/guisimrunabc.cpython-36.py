# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/betsee/gui/simtab/run/guisimrunabc.py
# Compiled at: 2019-08-01 01:03:54
# Size of source mod 2**32: 11843 bytes
"""
High-level **simulator** (i.e., :mod:`PySide2`-based object both displaying
*and* controlling the execution of simulation phases) functionality.
"""
from PySide2.QtCore import QCoreApplication, Signal
from betse.util.type.decorator.deccls import abstractproperty
from betse.util.type.types import type_check
from betsee.guiexception import BetseeSimmerException
from betsee.gui.simtab.run.guisimrunstate import SimmerState
from betsee.util.widget.abc.control.guictlabc import QBetseeControllerABC

class QBetseeSimmerStatefulABC(QBetseeControllerABC):
    __doc__ = '\n    Abstract base class of all **stateful simulator controller** (i.e.,\n    :mod:`PySide2`-based object controlling the internal and possibly external\n    state of some aspect of the simulator) subclasses.\n\n    Attributes (Private: Non-widgets)\n    ----------\n    _state : SimmerState\n        Current state of this simulator controller, exactly analogous to the\n        current state of a finite state automata. For safety, this variable\n        should *only* be set by the public :meth:`state` setter.\n    '
    state_changed = Signal(object, object)

    def __init__(self, *args, **kwargs):
        """
        Initialize this stateful simulator controller.
        """
        (super().__init__)(*args, **kwargs)
        self._state = SimmerState.UNQUEUED

    @property
    def state(self) -> SimmerState:
        """
        Current state of this simulator controller, exactly analogous to the
        current state of a finite state automata.
        """
        return self._state

    @state.setter
    @type_check
    def state(self, state: SimmerState) -> None:
        """
        Set the current state of this simulator controller to the passed state
        *and* signal all slots connected to the :attr:`state_changed` of
        this state change.
        """
        state_new = state
        state_old = self._state
        self._state = state_new
        self._update_state()
        self.state_changed.emit(state_new, state_old)

    def _die_unless_queued(self) -> None:
        """
        Raise an exception unless this stateful simulator controller is
        currently queued for modelling and/or exporting one or more simulator
        phases.

        Equivalently, this method raises an exception if *no* such phase is
        currently queued.

        See Also
        ----------
        :meth:`is_queued`
            Further details.
        """
        if not self.is_queued:
            raise BetseeSimmerException(QCoreApplication.translate('QBetseeSimmerStatefulABC', 'Simulator controller not queued.'))

    @abstractproperty
    def is_queued(self) -> bool:
        """
        ``True`` only if this stateful simulator controller is currently queued
        for modelling and/or exporting one or more simulator phases.
        """
        pass

    def _update_state(self) -> None:
        """
        Update the internal state of this stateful simulator controller and the
        contents of widgets controlled by this controller to reflect the
        current external state of this controller.

        The :meth:`state` setter property method internally calls this method
        to perform subclass-specific business logic on either the user
        interactively *or* the codebase programmatically interacting with any
        widget relevant to the current state of this controller (e.g., a
        checkbox queueing a simulation phase for exporting).

        Design
        ----------
        The default implementation of this method reduces to a noop and is thus
        intended (but *not* required) to be overridden by subclasses requiring
        subclass-specific business logic to be performed when this controller's
        :meth:`state` property is set. Overriding setter property methods in a
        manner internally calling the superclass method is highly non-trivial;
        hence, the :meth:`state` setter property method internally calls this
        method instead.
        """
        pass