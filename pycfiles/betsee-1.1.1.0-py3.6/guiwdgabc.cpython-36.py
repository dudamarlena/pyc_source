# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/betsee/util/widget/abc/guiwdgabc.py
# Compiled at: 2019-01-16 01:51:30
# Size of source mod 2**32: 12817 bytes
"""
Abstract base classes of most application-specific widget subclasses.
"""
from PySide2.QtWidgets import QUndoStack
from betse.util.io.log import logs
from betse.util.py import pyident
from betse.util.type.cls import classes
from betse.util.type.text import strs
from betse.util.type.types import type_check
from betsee.guiexception import BetseePySideEditWidgetException
_OBJ_NAME_DEFAULT = 'N/A'

class QBetseeObjectMixin(object):
    __doc__ = "\n    Abstract base class of most application-specific Qt object subclasses.\n\n    This class is suitable for use as a multiple-inheritance mixin. To preserve\n    the expected method resolution order (MRO) semantics, this class should\n    typically be inherited *first* rather than *last* in subclasses.\n\n    Attributes (Private)\n    ----------\n    _is_initted : bool\n        ``True`` only if this object's :meth:`init` method has been called.\n    "

    def __init__(self, *args, **kwargs):
        """
        Initialize this application-specific Qt object.

        Parameters
        ----------
        All parameters are passed as is to the superclass this mixin is mixed
        into (e.g., :class:`QObject` or a subclass thereof).

        Caveats
        ----------
        **Subclasses overriding this method should not attempt to accept
        subclass-specific parameters.** Due to the semantics of Python's
        method-resolution order (MRO), accidentally violating this constraint is
        guaranteed to raise non-human-readable exceptions at subclass
        instantiation time.

        Abstract base subclasses may trivially circumvent this constraint by
        defining abstract properties which concrete subclasses then define. When
        doing so, note that abstract methods should raise the
        :class:`BetseMethodUnimplementedException` exception rather than be
        decorated by the usual :meth:`abstractmethod` decorator -- which is
        *not* safely applicable to subclasses of this class.

        For example:

            >>> from betse.exceptions import BetseMethodUnimplementedException
            >>> @property
            ... def muh_subclass_property(self) -> MuhValueType:
            ...     raise BetseMethodUnimplementedException()
        """
        (super().__init__)(*args, **kwargs)
        self._is_initted = False
        if not self.obj_name:
            self.obj_name = _OBJ_NAME_DEFAULT

    def init(self) -> None:
        """
        Finalize the initialization of this Qt object.

        This method is principally intended to simplify the implementation of
        subclasses overriding this method with subclass-specific finalization.

        Raises
        ----------
        BetseePySideEditWidgetException
            If this method has already been called for this object, preventing
            objects from being erroneously refinalized.
        """
        if self.obj_name != _OBJ_NAME_DEFAULT:
            logs.log_debug('Initializing object "%s"...', self.obj_name)
        if self._is_initted:
            raise BetseePySideEditWidgetException('Object "{}" already initialized.'.format(self.obj_name))
        self._is_initted = True

    def init_if_needed(self, *args, **kwargs) -> None:
        """
        Finalize the initialization of this object if needed (i.e., if this
        object's initialization has *not* already been finalized by a call to
        the :meth:`init` method).

        This method safely wraps the :meth:`init` method, effectively squelching
        the exception raised by that method when this object's initialization
        has already been finalized.

        Parameters
        ----------
        All parameters are passed as is to the :meth:`init` method if called.
        """
        if self._is_initted:
            (self.init)(*args, **kwargs)

    @property
    def is_initted(self) -> bool:
        """
        ``True`` only if this object's :meth:`init` method has been called.
        """
        return self._is_initted

    @property
    def obj_name(self) -> str:
        """
        Qt-specific name of this object.

        This property getter is a convenience alias of the non-Pythonic
        :meth:`objectName` method.
        """
        return self.objectName()

    @obj_name.setter
    @type_check
    def obj_name(self, obj_name: str) -> None:
        """
        Set the Qt-specific name of this object to the passed string.

        This property setter is a convenience alias of the non-Pythonic
        :meth:`setObjectName` method.
        """
        self.setObjectName(obj_name)

    def set_obj_name_from_class_name(self) -> None:
        """
        Set the Qt-specific name of this object to the unqualified name of this
        subclass, altered to comply with object name standards (e.g., from
        ``QBetseeSimmerWorkerSeed`` to ``simmer_worker_seed``).

        Specifically, this function (in order):

        #. Obtains the unqualified name of this subclass.
        #. Removes any of the following prefixes from this name:

           * ``QBetsee``, the string prefixing the names of all
             application-specific :class:`QObject` subclasses.
           * ``Q``, the string prefixing the names of all
             application-agnostic :class:`QObject` subclasses.

        #. Converts this name from CamelCase to snake_case.
        #. Sets this object's name to this name.

        Design
        ----------
        This method is intentionally *not* called by the :meth:`__init__` method
        to set this object's name to a (seemingly) sane default. Why? Because
        numerous subclasses prefer to manually set this name. Unconditionally
        calling this method for every subclass would have the undesirable side
        effect of preventing this and other subclasses from detecting when the
        object name has yet to be set (e.g., via a comparison against the
        :data:`_OBJ_NAME_DEFAULT` default).
        """
        cls = type(self)
        cls_name = classes.get_name_unqualified(cls)
        cls_name = strs.remove_prefix_if_found(text=cls_name, prefix='QBetsee')
        cls_name = strs.remove_prefix_if_found(text=cls_name, prefix='Q')
        self.obj_name = pyident.convert_camelcase_to_snakecase(cls_name)


class QBetseeEditWidgetMixin(QBetseeObjectMixin):
    __doc__ = "\n    Abstract base class of most application-specific **editable widget** (i.e.,\n    widget interactively editing one or more values in an undoable manner)\n    subclasses.\n\n    Attributes\n    ----------\n    is_undo_cmd_pushable : bool\n        ``True`` only if undo commands are safely pushable from this widget onto\n        the undo stack *or* ``False`` when either:\n        * This widget's content is currently being programmatically populated.\n        * A previous undo command is already being applied to this widget.\n        In both cases, changes to this widget's content are program- rather than\n        user-driven and hence are *NOT* safely undoable. If ``False``, widget\n        subclass slots intending to push an undo commands onto the undo stack\n        should instead (in order):\n        * Temporarily avoid doing so for the duration of the current slot call,\n          as doing so *could* induce infinite recursion.\n        * Set ``self.is_undo_cmd_pushable = False`` to permit all subsequent\n          slot calls to push undo commands onto the undo stack.\n    _undo_stack : QUndoStack\n        Undo stack to which this widget pushes undo commands if any *or*\n        ``None`` otherwise.\n    "

    def __init__(self, *args, **kwargs):
        (super().__init__)(*args, **kwargs)
        self._unset_undo_stack()

    @type_check
    def _set_undo_stack(self, undo_stack: QUndoStack) -> None:
        """
        Set the undo stack to which this widget pushes undo commands, permitting
        the :meth:`_push_undo_cmd_if_safe` method to pushing undo commands from
        this widget onto this stack.
        """
        self._undo_stack = undo_stack
        self.is_undo_cmd_pushable = True

    def _unset_undo_stack(self) -> None:
        """
        Unset the undo stack to which this widget pushes undo commands,
        preventing the :meth:`_push_undo_cmd_if_safe` method from pushing undo
        commands from this widget.
        """
        self._undo_stack = None
        self.is_undo_cmd_pushable = False

    def _is_undo_stack_dirty(self) -> bool:
        """
        ``True`` only if the undo stack associated with this widget is in the
        **dirty state** (i.e., contains at least one undo command to be undone).
        """
        return not self._undo_stack.isClean()

    @type_check
    def _push_undo_cmd_if_safe(self, undo_cmd: 'betsee.util.widget.abc.guiundocmdabc.QBetseeWidgetUndoCommandABC') -> None:
        """
        Push the passed widget-specific undo command onto the undo stack
        associated with this widget.

        Parameters
        ----------
        undo_cmd : QBetseeWidgetUndoCommandABC
            Widget-specific undo command to be pushed onto this stack.
        """
        if not self.is_undo_cmd_pushable:
            return
        self._sim_conf.undo_stack.push(undo_cmd)