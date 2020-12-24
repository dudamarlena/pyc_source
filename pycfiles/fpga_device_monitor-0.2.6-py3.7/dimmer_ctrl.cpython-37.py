# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fpga_device_monitor/widgets/dimmer_ctrl.py
# Compiled at: 2020-04-09 04:27:42
# Size of source mod 2**32: 1143 bytes
from typing import Any
from qtpy.QtCore import Slot, Signal
from fpga_device_monitor.widgets.device_ctrl import DeviceControlWidget
from fpga_device_monitor.widgets.percent_slider import PercentSlider
from fpga_device_monitor.windows.base import BaseWidget

class DimmerControlWidget(DeviceControlWidget, BaseWidget):
    __doc__ = "Control widget for a FPGA Dimmer. Provides a slider that is used to change the Dimmer's brightness."

    def __init__(self, *args, **kwargs):
        (super(DimmerControlWidget, self).__init__)(args, ui_file='out_dimmer.ui', **kwargs)
        self.sld_brightness.slider.valueChanged.connect(self.send_device_state)

    def update_widget(self) -> None:
        """Updates the widget by setting the slider's value to the Dimmer's reported brightness."""
        self
        self.sld_brightness.slider.setValue(self.state * 100)

    def get_state_from_widget(self) -> float:
        """Translates the slider's value (0..100) to the Dimmer device state (0..1).

        :return Dimmer brightness value calculated from slider's value"""
        return self.sld_brightness.value / 100