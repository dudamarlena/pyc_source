# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/CIDAN/GUI/Inputs/OptionInput.py
# Compiled at: 2020-04-29 15:59:56
# Size of source mod 2**32: 918 bytes
from PySide2.QtWidgets import *
import CIDAN.GUI.Inputs.Input as Input

class OptionInput(Input):

    def __init__(self, display_name, program_name, on_change_function, default_index, tool_tip, val_list, display_tool_tip=False):
        super().__init__(display_name, program_name, on_change_function, default_index, tool_tip, display_tool_tip)
        self.input_box = QComboBox()
        self.val_list = val_list
        self.input_box.addItems(val_list)
        self.input_box.setCurrentIndex(self.default_val)
        self.input_box.setToolTip(self.tool_tip)
        self.input_box.currentIndexChanged.connect(self.on_change)
        self.layout_h.addWidget(self.input_box)

    def current_state(self):
        return self.val_list[self.input_box.currentIndex()]

    def set_default_val(self):
        self.input_box.setCurrentIndex(self.default_val)