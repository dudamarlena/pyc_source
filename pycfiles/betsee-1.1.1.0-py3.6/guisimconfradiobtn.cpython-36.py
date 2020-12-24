# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/betsee/gui/simconf/stack/widget/guisimconfradiobtn.py
# Compiled at: 2019-08-01 01:03:54
# Size of source mod 2**32: 5714 bytes
"""
:class:`QRadioButton`-based simulation configuration widget subclasses.
"""
from PySide2.QtCore import QCoreApplication, Signal
from PySide2.QtWidgets import QButtonGroup, QRadioButton
from betse.util.type.iterable import iterget
from betse.util.type.obj import objtest
from betse.util.type.types import type_check
from betsee.guiexception import BetseePySideRadioButtonException
from betsee.gui.simconf.stack.widget.mixin.guisimconfwdgeditenum import QBetseeSimConfEditEnumWidgetMixin

class QBetseeSimConfEnumRadioButtonGroup(QBetseeSimConfEditEnumWidgetMixin, QButtonGroup):
    __doc__ = '\n    Simulation configuration-specific radio button group widget, permitting\n    high-level enumeration members backed by low-level raw strings in external\n    simulation configuration files to be interactively edited.\n\n    Caveats\n    ----------\n    **Qt (Creator|Designer) provides no means of promoting\n    :class:`QButtonGroup` widgets to instances of this subclass,** a\n    longstanding deficiency with no short-term official solution. Instead,\n    button groups *must* be manually "promoted" via the admittedly hackish\n    :attr:`betsee.lib.pyside2.cache.guipsdcache._PROMOTE_OBJ_NAME_TO_TYPE`\n    dictionary.\n\n    See Also\n    ----------\n    :class:`QBetseeSimConfComboBox`\n        Alternative simulation configuration-specific widget subclass similarly\n        permitting high-level enumeration members to be interactively edited.\n        While more cumbersome to initialize, that subclass is preferable from\n        the user experience (UX) perspective for sufficiently large\n        enumerations (e.g., containing ten or more members).\n    '

    def _init_safe(self, *args, **kwargs):
        (super()._init_safe)(*args, **kwargs)
        for radio_btn in self.buttons():
            objtest.die_unless_instance(obj=radio_btn, cls=QRadioButton)
            if radio_btn not in self._widget_value_to_enum_member:
                raise BetseePySideRadioButtonException(QCoreApplication.translate('QBetseeSimConfEnumRadioButtonGroup', 'Button group "{1}" radio button "{0}" not a value of "enum_member_to_widget_value".'.format(radio_btn.objectName(), self.objectName())))

    @property
    def undo_synopsis(self) -> str:
        return QCoreApplication.translate('QBetseeSimConfEnumRadioButtonGroup', 'changes to a radio button')

    @property
    def _finalize_widget_change_signal(self) -> Signal:
        return self.buttonClicked

    @property
    def widget_value(self) -> QRadioButton:
        return self.checkedButton()

    @widget_value.setter
    @type_check
    def widget_value(self, widget_value: QRadioButton) -> None:
        widget_value.setChecked(True)

    def _reset_widget_value(self) -> None:
        self.widget_value = iterget.get_item_first(self.buttons())