# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fpga_device_monitor/widgets/switch_ctrl.py
# Compiled at: 2020-04-09 04:27:42
# Size of source mod 2**32: 1083 bytes
from typing import Any
from qtpy.QtCore import Slot
from qtpy.QtWidgets import QPushButton
from fpga_device_monitor.widgets.device_ctrl import DeviceControlWidget

class SwitchControlWidget(DeviceControlWidget):
    __doc__ = "A widget for controlling a FPGA Switch. Provides a button that controls the Switch's state."

    def __init__(self, *args, **kwargs):
        (super(SwitchControlWidget, self).__init__)(args, ui_file='out_switch.ui', **kwargs)

    def update_widget(self) -> None:
        """Sets the current state of the button, based on the Switch's state."""
        self
        self.btn_toggle.setChecked(self.state)

    def get_state_from_widget(self) -> bool:
        """Returns the state of the Switch, based on the state of the widget's button."""
        return self.btn_toggle.isChecked()

    @Slot(bool)
    def on_btn_toggle_toggled(self, state: bool):
        """Handler for toggling the widget's button. This sends the update to the Switch."""
        self.btn_toggle.setText('On' if state else 'Off')
        self.send_device_state()