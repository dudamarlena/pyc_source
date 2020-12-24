# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/CIDAN/GUI/Inputs/Int3DInput.py
# Compiled at: 2020-04-29 15:57:49
# Size of source mod 2**32: 1854 bytes
from PySide2.QtWidgets import *
import CIDAN.GUI.Inputs.Input as Input

class Int3DInput(Input):

    def __init__(self, display_name, program_name, on_change_function, default_val, tool_tip, min, max, step, display_tool_tip=False):
        super().__init__(display_name, program_name, on_change_function, default_val, tool_tip, display_tool_tip)
        self.input_box_1 = QSpinBox()
        self.input_box_1.setMinimum(min)
        self.input_box_1.setMaximumWidth(50)
        self.input_box_1.setMaximum(max)
        self.input_box_1.setSingleStep(step)
        self.input_box_1.setValue(self.default_val)
        self.input_box_1.setToolTip(self.tool_tip)
        self.layout_h.addWidget(self.input_box_1)
        self.input_box_1.valueChanged.connect(self.on_change)
        self.input_box_2 = QSpinBox()
        self.input_box_2.setMinimum(min)
        self.input_box_2.setMaximumWidth(50)
        self.input_box_2.setMaximum(max)
        self.input_box_2.setSingleStep(step)
        self.input_box_2.setValue(self.default_val)
        self.input_box_2.setToolTip(self.tool_tip)
        self.layout_h.addWidget(self.input_box_2)
        self.input_box_2.valueChanged.connect(self.on_change)
        self.input_box_3 = QSpinBox()
        self.input_box_3.setMinimum(min)
        self.input_box_3.setMaximumWidth(50)
        self.input_box_3.setMaximum(max)
        self.input_box_3.setSingleStep(step)
        self.input_box_3.setValue(self.default_val)
        self.input_box_3.setToolTip(self.tool_tip)
        self.layout_h.addWidget(self.input_box_3)
        self.input_box_3.valueChanged.connect(self.on_change)

    def current_state(self):
        return self.input_box_1.value()

    def set_default_val(self):
        self.input_box_1.setValue(self.default_val)