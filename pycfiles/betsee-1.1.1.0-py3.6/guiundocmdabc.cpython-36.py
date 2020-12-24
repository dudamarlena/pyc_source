# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/betsee/util/widget/abc/guiundocmdabc.py
# Compiled at: 2019-08-01 01:03:54
# Size of source mod 2**32: 6729 bytes
"""
Abstract base classes of all widget-specific undo command subclasses.
"""
from PySide2.QtWidgets import QUndoCommand
from betse.util.io.log import logs
from betse.util.type.types import type_check
from betsee.util.widget.mixin.guiwdgeditmixin import QBetseeEditWidgetMixin

class QBetseeWidgetUndoCommandABC(QUndoCommand):
    __doc__ = '\n    Abstract base class of all widget-specific undo command subclasses,\n    encapsulating both the application and restoration of the contents of a\n    specific type of widget.\n\n    Attributes\n    ----------\n    _id : int\n        Integer uniquely identifying the concrete subclass implementing this\n        abstract base class of this undo command.\n    _widget : QBetseeEditWidgetMixin\n        Application-specific widget operated upon by this undo command.\n    _synopsis : str\n        Human-readable string synopsizing the operation performed by this\n        undo command, preferably as a single translated sentence fragment.\n        This string is identical to that returned by the :meth:`actionString`\n        method, but is stored as an instance variable purely for readability.\n    '

    @type_check
    def __init__(self, widget, synopsis):
        """
        Initialize this undo command.

        Parameters
        ----------
        widget : QBetseeEditWidgetMixin
            Application-specific widget operated upon by this undo command.
        synopsis : str
            Human-readable string synopsizing the operation performed by this
            undo command, preferably as a single translated sentence fragment.
        """
        super().__init__(synopsis)
        self._synopsis = synopsis
        self._widget = widget
        self._id = id(type(self))

    def undo(self) -> None:
        logs.log_debug('Undoing %s for widget "%s"...', self._synopsis, self._widget.obj_name)

    def redo(self) -> None:
        logs.log_debug('Redoing %s for widget "%s"...', self._synopsis, self._widget.obj_name)

    def id(self) -> int:
        """
        Integer uniquely identifying the concrete subclass implementing this
        abstract base class.

        Our pure-C++ :class:`QUndoCommand` superclass requires this integer to
        transparently support **command compression** (i.e., automatic merging
        of adjacent undo commands of the same type).
        """
        return self._id


class QBetseeUndoCommandNull(QUndoCommand):
    __doc__ = '\n    Placeholder undo command intended solely to simplify testing.\n    '

    def undo(self) -> None:
        logs.log_debug('Undoing %s...', self.actionText())

    def redo(self) -> None:
        logs.log_debug('Redoing %s...', self.actionText())