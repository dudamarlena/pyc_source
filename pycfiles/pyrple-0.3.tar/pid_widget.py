# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyrpl/widgets/module_widgets/pid_widget.py
# Compiled at: 2017-08-29 09:44:06
__doc__ = '\nA widget for pid modules.\n'
from .base_module_widget import ModuleWidget
from qtpy import QtCore, QtWidgets

class PidWidget(ModuleWidget):
    """
    Widget for a single PID.
    """

    def init_gui(self):
        self.init_main_layout(orientation='vertical')
        self.init_attribute_layout()
        input_filter_widget = self.attribute_widgets['inputfilter']
        self.attribute_layout.removeWidget(input_filter_widget)
        self.main_layout.addWidget(input_filter_widget)
        for prop in ['p', 'i']:
            self.attribute_widgets[prop].widget.set_log_increment()

    def update_ival(self):
        widget = self.attribute_widgets['ival']
        if self.isVisible() and not widget.editing():
            widget.write_attribute_value_to_widget()