# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/CIDAN/GUI/Inputs/BoolInput.py
# Compiled at: 2020-04-29 15:58:09
# Size of source mod 2**32: 815 bytes
from PySide2.QtWidgets import *
import CIDAN.GUI.Inputs.Input as Input

class BoolInput(Input):

    def __init__(self, display_name, program_name, on_change_function, default_val, tool_tip, display_tool_tip=False):
        super().__init__(display_name, program_name, on_change_function, default_val, tool_tip, display_tool_tip)
        self.input_box = QRadioButton()
        self.input_box.setMaximumWidth(50)
        self.input_box.setChecked(self.default_val)
        self.input_box.toggled.connect(self.on_change)
        self.input_box.setToolTip(self.tool_tip)
        self.layout_h.addWidget(self.input_box)

    def current_state(self):
        return self.input_box.isChecked()

    def set_default_val(self):
        self.input_box.setChecked(self.default_val)