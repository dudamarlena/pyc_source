# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyrpl/widgets/module_widgets/pyrpl_config_widget.py
# Compiled at: 2017-08-29 09:44:06
from qtpy import QtCore, QtWidgets
from .base_module_widget import ReducedModuleWidget

class PyrplConfigWidget(ReducedModuleWidget):

    def init_attribute_layout(self):
        super(PyrplConfigWidget, self).init_attribute_layout()
        textwidget = self.attribute_widgets['text']
        self.main_layout.removeWidget(textwidget)
        self.textbox = QtWidgets.QHBoxLayout()
        self.main_layout.addLayout(self.textbox)
        self.textbox.addWidget(textwidget)