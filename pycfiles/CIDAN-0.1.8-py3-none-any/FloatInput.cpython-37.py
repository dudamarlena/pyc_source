# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/CIDAN/GUI/Inputs/FloatInput.py
# Compiled at: 2020-04-29 15:57:49
# Size of source mod 2**32: 988 bytes
from PySide2.QtWidgets import *
import CIDAN.GUI.Inputs.Input as Input

class FloatInput(Input):

    def __init__(self, display_name, program_name, on_change_function, default_val, tool_tip, min, max, step, display_tool_tip=False):
        super().__init__(display_name, program_name, on_change_function, default_val, tool_tip, display_tool_tip)
        self.input_box = QDoubleSpinBox()
        self.input_box.setMinimum(min)
        self.input_box.setMaximum(max)
        self.input_box.setMaximumWidth(50)
        self.input_box.setSingleStep(step)
        self.input_box.setValue(self.default_val)
        self.input_box.valueChanged.connect(self.on_change)
        self.input_box.setToolTip(self.tool_tip)
        self.layout_h.addWidget(self.input_box)

    def current_state(self):
        return self.input_box.value()

    def set_default_val(self):
        self.input_box.setValue(self.default_val)