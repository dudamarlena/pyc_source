# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/betsee/util/widget/mixin/guiwdgeditmixin.py
# Compiled at: 2019-08-01 01:03:54
# Size of source mod 2**32: 12340 bytes
"""
**Application-specific editable widget** (i.e., widget whose content is
interactively editable by end users and whose implementation is specific to
this application) hierarchy.
"""
from PySide2.QtWidgets import QUndoStack
from betse.util.io.log import logs
from betse.util.type.types import type_check, GeneratorType
from betsee.util.widget.mixin.guiwdgmixin import QBetseeObjectMixin
from contextlib import contextmanager

class QBetseeEditWidgetMixin(QBetseeObjectMixin):
    __doc__ = "\n    Abstract mixin of most application-specific **editable widget** (i.e.,\n    widget interactively editing one or more values in an undoable manner)\n    subclasses.\n\n    This class is suitable for use as a multiple-inheritance mixin. To preserve\n    the expected method resolution order (MRO) semantics, this class should\n    typically be inherited *first* rather than *last* in subclasses.\n\n    Attributes\n    ----------\n    _is_undo_cmd_pushable : bool\n        ``True`` only if undo commands are safely pushable from this widget\n        onto the undo stack *or* ``False`` when either:\n\n        * This widget's content is currently being programmatically populated.\n        * A previous undo command is already being applied to this widget.\n\n        In both cases, changes to this widget's content are program- rather\n        than user-driven and hence are *NOT* safely undoable. If ``False``,\n        widget subclass slots intending to push an undo commands onto the undo\n        stack should instead (in order):\n\n        #. Temporarily avoid doing so for the duration of the current slot\n           call, as doing so *could* induce infinite recursion.\n        #. Set ``self._is_undo_cmd_pushable = True`` to permit all subsequent\n           slot calls to push undo commands onto the undo stack.\n    _undo_stack : QUndoStack\n        Undo stack to which this widget pushes undo commands.\n    "

    def __init__(self, *args, **kwargs):
        (super().__init__)(*args, **kwargs)
        self._undo_stack = None
        self._is_undo_cmd_pushable = True

    @type_check
    def _init_safe(self, undo_stack: QUndoStack) -> None:
        """
        Finalize the initialization of this editable widget in a safe manner
        guaranteed *not* to induce infinite recursion in common edge cases.

        Unlike the :meth:`init` method, this method is intended to be
        overridden by subclasses.

        Parameters
        ----------
        undo_stack : QUndoStack
            Undo stack to which this widget pushes undo commands.

        See Also
        ----------
        :meth:`init`
            Further details.
        """
        self._undo_stack = undo_stack

    @type_check
    def init(self, is_reinitable=False, *args, **kwargs):
        """
        Finalize the initialization of this editable widget.

        Parameters
        ----------
        The ``is_reinitable`` parameter is passed as is to the
        :meth:`QBetseeObjectMixin.init` method. All remaining parameters are
        passed as is to the :meth:`_init_safe` method.

        Caveats
        ----------
        **Subclasses should override the abstract :meth:`_init_safe` method
        rather than this concrete method.** While :meth:`_init_safe` is
        explicitly designed for that sole purpose, this method is instead
        explicitly designed to *not* be overridden. Why? Because only the
        former method is protected against infinite recursion in edge cases
        (e.g., setting the initial value of this widget, which recursively
        pushes undo commands onto the undo stack associated with this widget).

        See Also
        ----------
        :meth:`QBetseeObjectMixin.init`
            Further details.
        """
        super().init(is_reinitable=is_reinitable)
        with self.ignoring_undo_cmds():
            (self._init_safe)(*args, **kwargs)

    @contextmanager
    @type_check
    def ignoring_undo_cmds(self) -> GeneratorType:
        """
        Context manager temporarily disabling this widget's
        :attr:`QBetseeEditWidgetMixin._is_undo_cmd_pushable` boolean for the
        duration of this context, guaranteeably restoring this boolean to its
        prior state immediately *before* returning.

        This context manager prevents this widget from recursively pushing
        additional undo commands onto the undo stack at inopportune moments
        (e.g., during (re)initialization or when already applying an undo
        command). Allowing this induces infinite recursion, which is bad.

        Returns
        -----------
        contextlib._GeneratorContextManager
            Context manager instrumenting this widget as described above.

        Yields
        -----------
        None
            Since this context manager yields no values, the ``with`` statement
            encapsulating this manager must *not* be suffixed by an ``as``
            clause.
        """
        if not self._is_undo_cmd_pushable:
            logs.log_debug('Disabling editable widget "%s" undo command push request handling via noop...', self.obj_name)
            yield
            return
        try:
            logs.log_debug('Disabling editable widget "%s" undo command push request handling via setter...', self.obj_name)
            self._is_undo_cmd_pushable = False
            yield
        finally:
            logs.log_debug('Restoring editable widget "%s" undo command push request handling...', self.obj_name)
            self._is_undo_cmd_pushable = True

    def _is_undo_stack_dirty(self) -> bool:
        """
        ``True`` only if this widget is associated with an undo stack (i.e., if
        the :meth:`_set_undo_stack` method has been called more recently than
        the :meth:`_unset_undo_stack` method) *and* that undo stack is in the
        **dirty state** (i.e., contains at least one undo command to be
        subsequently undone).
        """
        return self._undo_stack is not None and not self._undo_stack.isClean()

    @type_check
    def _push_undo_cmd_if_safe(self, undo_cmd: 'betsee.util.widget.abc.guiundocmdabc.QBetseeWidgetUndoCommandABC') -> None:
        """
        Non-recursively push the passed widget-specific undo command onto the
        undo stack associated with this widget if doing so is currently safe
        *or* silently reduce to a noop otherwise (i.e., if doing so is
        currently unsafe).

        Parameters
        ----------
        undo_cmd : QBetseeWidgetUndoCommandABC
            Widget-specific undo command to be pushed onto this stack.
        """
        if self._is_undo_cmd_pushable:
            if self._undo_stack is not None:
                with self.ignoring_undo_cmds():
                    self._undo_stack.push_undo_cmd_if_safe(undo_cmd)
        else:
            logs.log_debug('Ignoring editable widget "%s" undo command "%s" push request (e.g., to prevent infinite recursion)...', self.obj_name, undo_cmd.actionText())