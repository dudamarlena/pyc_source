# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/betsee/gui/simconf/stack/widget/guisimconfcheckbox.py
# Compiled at: 2019-08-01 01:03:54
# Size of source mod 2**32: 2017 bytes
"""
:class:`QCheckBox`-based simulation configuration widget subclasses.
"""
from PySide2.QtCore import QCoreApplication, Signal
from PySide2.QtWidgets import QCheckBox
from betse.util.type.types import type_check, ClassOrNoneTypes
from betsee.gui.simconf.stack.widget.mixin.guisimconfwdgeditscalar import QBetseeSimConfEditScalarWidgetMixin

class QBetseeSimConfCheckBox(QBetseeSimConfEditScalarWidgetMixin, QCheckBox):
    __doc__ = '\n    Simulation configuration-specific check box widget, permitting booleans\n    backed by external simulation configuration files to be interactively\n    edited.\n    '

    @property
    def undo_synopsis(self) -> str:
        return QCoreApplication.translate('QBetseeSimConfCheckBox', 'edits to a check box')

    @property
    def _finalize_widget_change_signal(self) -> Signal:
        return self.toggled

    @property
    def _sim_conf_alias_type_strict(self) -> ClassOrNoneTypes:
        return bool

    @property
    def widget_value(self):
        return super().isChecked()

    @widget_value.setter
    @type_check
    def widget_value(self, widget_value):
        super().setChecked(widget_value)

    def _reset_widget_value(self) -> None:
        self.widget_value = False