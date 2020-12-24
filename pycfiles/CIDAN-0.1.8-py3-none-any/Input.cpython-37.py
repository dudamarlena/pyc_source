# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/CIDAN/GUI/Inputs/Input.py
# Compiled at: 2020-04-29 16:29:45
# Size of source mod 2**32: 1315 bytes
from PySide2.QtWidgets import *

class Input(QFrame):

    def __init__(self, display_name, program_name, on_change_function, default_val, tool_tip, display_tool_tip=False):
        super().__init__()
        self.program_name = program_name
        self.input_box_1 = None
        self.tool_tip = tool_tip
        self.default_val = default_val
        self.display_name = display_name
        self.layout_main = QVBoxLayout()
        self.layout_h = QHBoxLayout()
        temp_lable = QLabel()
        temp_lable.setText(display_name)
        temp_lable.setToolTip(tool_tip)
        self.layout_h.addWidget(temp_lable)
        self.on_change_function = on_change_function
        self.layout_main.addLayout(self.layout_h)
        if display_tool_tip:
            temp_lable_2 = QLabel()
            temp_lable_2.setText(tool_tip)
            self.layout_main.addWidget(temp_lable_2)
        self.setLayout(self.layout_main)

    def on_change(self, *args, **kwargs):
        try:
            self.on_change_function(self.program_name, self.current_state())
        except AssertionError as e:
            try:
                print(e)
                self.set_default_val()
            finally:
                e = None
                del e

    def current_state(self):
        pass

    def set_default_val(self):
        pass