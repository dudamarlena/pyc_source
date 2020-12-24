# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyrpl/widgets/module_widgets/asg_widget.py
# Compiled at: 2017-08-29 09:44:06
"""
A widget for the scope module
"""
from .base_module_widget import ModuleWidget
from qtpy import QtCore, QtWidgets

class AsgWidget(ModuleWidget):

    def __init__(self, *args, **kwds):
        super(AsgWidget, self).__init__(*args, **kwds)
        self.attribute_widgets['trigger_source'].value_changed.connect(self.module.setup)