# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/betsee/gui/simconf/stack/widget/mixin/guisimconfwdgeditscalar.py
# Compiled at: 2019-08-01 01:03:54
# Size of source mod 2**32: 20810 bytes
"""
Abstract base classes of all editable scalar simulation configuration widget
subclasses instantiated in pages of the top-level stack.
"""
from PySide2.QtCore import Signal, Slot
from PySide2.QtWidgets import QUndoCommand
from betse.exceptions import BetseMethodUnimplementedException
from betse.util.io.log import logs
from betse.util.type.types import type_check
from betsee.guiexception import BetseePySideWidgetException
from betsee.gui.simconf.stack.widget.mixin.guisimconfwdgedit import QBetseeSimConfEditWidgetMixin
from betsee.util.widget.abc.guiundocmdabc import QBetseeWidgetUndoCommandABC

class QBetseeSimConfEditScalarWidgetMixin(QBetseeSimConfEditWidgetMixin):
    __doc__ = '\n    Abstract base class of all **editable scalar simulation configuration\n    widget** (i.e., widget interactively editing scalar simulation\n    configuration values stored in external YAML files) subclasses.\n\n    In this context, the term "scalar" encompasses all widget subclasses whose\n    contents reduce to a single displayed value (e.g., integer, floating point\n    number, string).\n\n    Attributes\n    ----------\n    _widget_value_last : object\n        Previously displayed value of this widget cached on the completion of\n        the most recent user edit (i.e., :meth:`editingFinished` signal),\n        possibly but *not* necessarily reflecting this widget\'s current state.\n    '

    def __init__(self, *args, **kwargs):
        """
        Initialize this editable scalar widget mixin.
        """
        (super().__init__)(*args, **kwargs)
        self._widget_value_last = None

    def _init_safe(self, *args, **kwargs):
        (super()._init_safe)(*args, **kwargs)
        self._finalize_widget_change_signal.connect(self._set_alias_to_widget_value_if_safe)

    @property
    def undo_synopsis(self) -> str:
        """
        Human-readable string synopsizing the operation performed by this
        scalar widget, preferably as a single translated sentence fragment.
        """
        raise BetseMethodUnimplementedException()

    @property
    def widget_value(self) -> object:
        """
        High-level :mod:`PySide2`-specific scalar value currently displayed by
        this scalar widget.

        Each subclass typically implements this Python property in terms of an
        unprefixed getter method of this widget (e.g., :meth:`QLineEdit.text`).

        Caveats
        ----------
        If this value is neither of the exact type(s) required by the
        simulation configuration alias associated with this widget *nor* of a
        similar type safely convertible into such a type, the subclass *must*
        redefine both the :meth:`_get_alias_from_widget_value` and
        :meth:`_get_widget_from_alias_value` methods to convert this value to
        and from such a type.

        This high-level value is purely :mod:`PySide2`-specific and hence
        distinct from the associated low-level scalar value defined by the
        simulation configuration. In particular, these two values are typically
        but *not* necessarily of the same type.

        For example, for the :class:`QBetseeSimConfComboBoxEnum` subclass:

        * The high-level :meth:`QBetseeSimConfComboBoxEnum.widget_value`
          property returns an integer (i.e., the 0-based index of the currently
          selected item in that combo box).
        * The low-level :meth:`QBetseeSimConfComboBoxEnum._sim_conf_alias.get`
          getter returns the enumeration member corresponding to this item.
        """
        raise BetseMethodUnimplementedException()

    @widget_value.setter
    def widget_value(self, widget_value: object) -> None:
        """
        Set the high-level :mod:`PySide2`-specific scalar value currently
        displayed by this scalar widget to the passed value.

        Each subclass typically implements this Python property in terms of a
        ``set``-prefixed setter method of this widget (e.g.,
        :meth:`QLineEdit.setText`).

        Caveats
        ----------
        To avoid infinite recursion, the superclass rather than subclass
        implementation of this setter method should typically be called
        (e.g., ``super().setText()`` rather than ``self.setText()``). For the
        :class:`QBetseeSimConfLineEdit` subclass, for example, erroneously
        calling this subclass implementation would ensure that:

        #. Each call to the :meth:`QBetseeSimConfLineEdit.setValue` method...
        #. Which pushes an undo command onto the undo stack...
        #. Whose :meth:`QUndoCommand.redo` method is called by that stack...
        #. Which calls the :meth:`QBetseeSimConfLineEdit.setValue` method...
        #. Induces infinite recursion.
        """
        raise BetseMethodUnimplementedException()

    @property
    def _finalize_widget_change_signal(self) -> Signal:
        """
        Signal signalled on each finalized interactive user (but *not*
        programmatic) edit of the contents of this widget.

        The :meth:`_init_safe` method implicitly connects this signal to the
        :meth:`_set_alias_to_widget_value_if_safe` slot.
        """
        raise BetseMethodUnimplementedException()

    def _reset_widget_value(self) -> None:
        """
        Reset the scalar value currently displayed by this scalar widget, thus
        reverting this widget to its default state divorced from an underlying
        model.

        For example, if this widget displays:

        * A string value, this method should set this value to the empty
          string.
        * A float value, this method should set this value to 0.0.
        * An integer value, this method should set this value to 0.
        """
        raise BetseMethodUnimplementedException()

    @Slot(str)
    def _set_filename(self, filename):
        super()._set_filename(filename)
        self._set_widget_to_alias_value(filename)

    @type_check
    def _set_widget_to_alias_value(self, filename: str) -> None:
        """
        Set this widget's displayed value to the current value of the
        simulation configuration alias associated with this widget if a
        simulation configuration is currently open *or* clear this displayed
        value otherwise.

        This method is currently only called by the :meth:`_set_filename` slot
        on opening and closing a simulation configuration, thus initializing
        this widget's value to that of this configuration.

        Parameters
        ----------
        filename : str
            Absolute path of the currently open YAML-formatted simulation
            configuration file if any *or* the empty string otherwise (i.e., if
            no such file is open).
        """
        if filename:
            if self._is_sim_open:
                self.widget_value = self._get_widget_from_alias_value()
                if self.widget_value is None:
                    raise BetseePySideWidgetException('Editable scalar widget "{}" value "None" invalid.'.format(self.obj_name))
                logs.log_debug('Setting widget "%s" display value to %r...', self.obj_name, self.widget_value)
                self._widget_value_last = self.widget_value
        else:
            self._reset_widget_value()
            self._widget_value_last = None

    def _get_widget_from_alias_value(self) -> object:
        """
        Value of the simulation configuration alias associated with this
        widget, coerced into a type displayable by this widget.

        This method is typically called *only* once per open simulation
        configuration file on the first loading of that file.

        See Also
        ----------
        :meth:`_get_alias_from_widget_value`
            Further details.
        """
        return self._sim_conf_alias.get()

    @Slot()
    def _set_alias_to_widget_value_if_safe(self) -> None:
        """
        Slot signalled on each finalized interactive user edit (and possibly
        but *not* necessarily each non-interactive programmatic change) to the
        value displayed by this widget, setting the current value of the
        simulation configuration alias associated with this widget to this
        widget's displayed value if a simulation configuration is currently
        open *or* silently reduce to a noop otherwise.

        Design
        ----------
        If Qt signals the :meth:`_finalize_widget_change_signal` connected to
        this slot *only* on each finalized interactive user edit (rather than
        both each such edit *and* each non-interactive programmatic change),
        the subclass *must* explicitly call this method on each non-interactive
        programmatic change -- typically in the subclass implementation of this
        widget's main setter method (e.g., :meth:`QLineEdit.setText`),
        guaranteed to be called on each such change.
        """
        widget_value = self.widget_value
        if widget_value == self._widget_value_last or not self._is_sim_open:
            return
        alias_value = self._get_alias_from_widget_value()
        logs.log_debug('Setting widget "%s" alias value to %r...', self.obj_name, alias_value)
        self._sim_conf_alias.set(alias_value)
        if self._widget_value_last is not None:
            undo_cmd = QBetseeSimConfEditScalarWidgetUndoCommand(widget=self,
              value_old=(self._widget_value_last))
            self._push_undo_cmd_if_safe(undo_cmd)
            self._update_sim_conf_dirty()
        self._widget_value_last = widget_value

    def _get_alias_from_widget_value(self) -> object:
        """
        Value displayed by this widget, coerced into a type expected by this
        simulation configuration alias.

        Design
        ----------
        The default implementation should suffice for most subclasses. However,
        subclasses for which the following test fails to validate that the
        value displayed by this widget is of the type required by this
        simulation configuration alias must override this method to do so in a
        subclass-specific manner:

            >>> isinstance(self.widget_value, self._sim_conf_alias_type)
        """
        alias_value = self.widget_value
        alias_type = self._sim_conf_alias_type
        if not isinstance(alias_value, alias_type):
            if alias_type is tuple:
                alias_type = alias_type[0]
            alias_value = alias_type(alias_value)
        return alias_value


class QBetseeSimConfEditScalarWidgetUndoCommand(QBetseeWidgetUndoCommandABC):
    __doc__ = '\n    Undo command generically applicable to all editable scalar simulation\n    configuration widgets, implementing the application and restoration of the\n    scalar contents (e.g., float, integer, string) of a single such widget.\n\n    This subclass provides functionality specific to scalar widgets, including:\n\n    * Automatic merging of adjacent undo commands associated with the same\n      scalar widget.\n\n    Attributes\n    ----------\n    _value_new : object\n        New value replacing the prior value of the scalar widget associated\n        with this undo command.\n    _value_old : object\n        Prior value of the scalar widget associated with this undo command.\n    '

    @type_check
    def __init__(self, widget, value_old, *args, **kwargs):
        """
        Initialize this undo command.

        Parameters
        ----------
        widget : QBetseeSimConfEditScalarWidgetMixin
            Scalar widget operated upon by this undo command.
        value_old : object
            Prior value of the scalar widget associated with this undo command.

        All remaining parameters are passed as is to the superclass method.
        """
        (super().__init__)(args, widget=widget, synopsis=widget.undo_synopsis, **kwargs)
        self._value_old = value_old
        self._value_new = widget.widget_value

    def undo(self):
        super().undo()
        with self._widget.ignoring_undo_cmds():
            self._widget.widget_value = self._value_old

    def redo(self):
        super().redo()
        with self._widget.ignoring_undo_cmds():
            self._widget.widget_value = self._value_new

    def mergeWith(self, prior_undo_cmd: QUndoCommand) -> bool:
        """
        Attempt to merge this undo command with the passed undo command
        immediately preceding this undo command on the parent undo stack,
        returning ``True`` only if this method performed this merge.

        Specifically, this method returns:

        * ``True`` if this method successfully merged both the undo and redo
          operations applied by the prior undo command into those applied by
          this undo command, in which case the prior undo command is safely
          removable from the parent undo stack.
        * ``False`` otherwise, in which case both the prior undo command and
          this undo command *must* be preserved as is the parent undo stack.

        Parameters
        ----------
        prior_undo_cmd : QUndoCommand
            Undo command immediately preceding this undo command on the parent
            undo stack.

        Returns
        ----------
        bool
            ``True`` only if these undo commands were successfully merged.
        """
        if not (self.id() == prior_undo_cmd.id() and self._widget == prior_undo_cmd._widget):
            return False
        else:
            self._value_old = prior_undo_cmd._value_old
            return True