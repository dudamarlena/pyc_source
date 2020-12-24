# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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