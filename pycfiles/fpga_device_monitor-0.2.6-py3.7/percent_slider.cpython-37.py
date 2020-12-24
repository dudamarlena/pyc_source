# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fpga_device_monitor/widgets/percent_slider.py
# Compiled at: 2020-04-09 04:27:42
# Size of source mod 2**32: 1069 bytes
from qtpy.QtCore import Slot
from qtpy.QtWidgets import QSlider
from fpga_device_monitor.windows.base import BaseWidget

class PercentSlider(BaseWidget):
    __doc__ = "A combination of a slider and a label for selecting a percentage value.\n\n    The label automatically updates to display the slider's state.\n    "

    def __init__(self, parent, default=0, v_min=0, v_max=100, *args, **kwargs):
        (super(PercentSlider, self).__init__)('label_slider.ui', *args, **kwargs)
        self
        self.value = default
        self.slider.setMinimum(v_min)
        self.slider.setMaximum(v_max)
        self.slider.setValue(default)
        self.refresh()

    def refresh(self) -> None:
        """Updates the label to reflect the currently chosen value."""
        self.label.setText(f"{self.value} %")

    @Slot(int)
    def on_slider_valueChanged(self, new_value: int):
        """Handler for choosing a new value on the slider.

        :param new_value: New value
        """
        self.value = new_value
        self.refresh()