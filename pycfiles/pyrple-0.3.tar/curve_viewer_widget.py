# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyrpl/widgets/module_widgets/curve_viewer_widget.py
# Compiled at: 2017-08-29 09:44:06
from qtpy import QtCore, QtWidgets
from .base_module_widget import ReducedModuleWidget

class CurveViewerWidget(ReducedModuleWidget):

    def init_gui(self):
        """
        To be overwritten in derived class
        :return:
        """
        self.top_level_layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.top_level_layout)
        self.main_layout = QtWidgets.QHBoxLayout()
        self.top_level_layout.addLayout(self.main_layout)
        self.bottom_layout = QtWidgets.QHBoxLayout()
        self.top_level_layout.addLayout(self.bottom_layout)
        self.init_attribute_layout()

    def init_attribute_layout(self):
        super(CurveViewerWidget, self).init_attribute_layout()
        self.textbox = QtWidgets.QHBoxLayout()
        self.bottom_layout.addLayout(self.textbox)
        curve = self.attribute_widgets['curve']
        for name in ['pk', 'curve', 'params']:
            widget = self.attribute_widgets[name]
            self.main_layout.removeWidget(widget)
            self.textbox.addWidget(widget)
            widget.children()[2].setMinimumHeight(500)
            widths = {'pk': 100, 'params': 200}
            if name in widths:
                widget.children()[2].setMinimumWidth(widths[name])