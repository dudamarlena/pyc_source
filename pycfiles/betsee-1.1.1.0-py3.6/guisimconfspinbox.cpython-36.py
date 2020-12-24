# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/betsee/gui/simconf/stack/widget/guisimconfspinbox.py
# Compiled at: 2019-08-01 01:03:54
# Size of source mod 2**32: 10530 bytes
"""
:class:`QAbstractSpinBox`-based simulation configuration widget subclasses.
"""
from PySide2.QtCore import QCoreApplication, Qt, Signal
from PySide2.QtWidgets import QSpinBox
from betse.util.type.numeric import floats
from betse.util.type.types import type_check, ClassOrNoneTypes
from betsee.gui.simconf.stack.widget.mixin.guisimconfwdgeditscalar import QBetseeSimConfEditScalarWidgetMixin
from betsee.util.widget.abc.guiclipboardabc import QBetseeClipboardScalarWidgetMixin
from betsee.util.widget.stock.guispinbox import QBetseeDoubleSpinBox

class QBetseeSimConfSpinBoxWidgetMixin(QBetseeClipboardScalarWidgetMixin, QBetseeSimConfEditScalarWidgetMixin):
    __doc__ = '\n    Abstract base class of all simulation configuration-specific subclasses,\n    permitting numeric values (i.e., integers, floating point values) backed by\n    external simulation configuration files to be interactively edited.\n    '

    def __init__(self, *args, **kwargs):
        (super().__init__)(*args, **kwargs)
        self.setAccelerated(True)
        self.setAlignment(Qt.AlignRight)
        self.setKeyboardTracking(False)

    def setValue(self, value_new):
        super().setValue(value_new)
        self._set_alias_to_widget_value_if_safe()

    @property
    def undo_synopsis(self) -> str:
        return QCoreApplication.translate('QBetseeSimConfSpinBoxWidgetMixin', 'edits to a spin box')

    @property
    def widget_value(self) -> object:
        return self.value()

    @property
    def _finalize_widget_change_signal(self) -> Signal:
        return self.editingFinished


class QBetseeSimConfIntSpinBox(QBetseeSimConfSpinBoxWidgetMixin, QSpinBox):
    __doc__ = '\n    Simulation configuration-specific integer spin box widget, permitting\n    integers backed by external simulation configuration files to be\n    interactively edited.\n    '

    @property
    def _sim_conf_alias_type_strict(self) -> ClassOrNoneTypes:
        return int

    @QBetseeSimConfSpinBoxWidgetMixin.widget_value.setter
    @type_check
    def widget_value(self, widget_value: int) -> None:
        QSpinBox.setValue(self, widget_value)

    def _reset_widget_value(self) -> None:
        self.widget_value = 0


class QBetseeSimConfDoubleSpinBox(QBetseeSimConfSpinBoxWidgetMixin, QBetseeDoubleSpinBox):
    __doc__ = '\n    Simulation configuration-specific floating point spin box widget,\n    permitting floating point numbers backed by external simulation\n    configuration files to be interactively edited.\n    '

    @property
    def _sim_conf_alias_type_strict(self) -> ClassOrNoneTypes:
        return float

    def _get_widget_from_alias_value(self):
        widget_value = super()._get_widget_from_alias_value()
        widget_value_precision = floats.get_base_10_precision(widget_value)
        if self.singleStep() == self.SINGLE_STEP_DEFAULT:
            widget_value_exponent = floats.get_base_10_exponent(widget_value)
            single_step_new = 2.5 * 10 ** (widget_value_exponent - 1)
            self.setSingleStep(single_step_new)
        widget_value_precision = max(widget_value_precision + 1, 3)
        self.setDecimals(widget_value_precision)
        return widget_value

    @QBetseeSimConfSpinBoxWidgetMixin.widget_value.setter
    @type_check
    def widget_value(self, widget_value: float) -> None:
        QBetseeDoubleSpinBox.setValue(self, widget_value)

    def _reset_widget_value(self) -> None:
        self.widget_value = 0.0