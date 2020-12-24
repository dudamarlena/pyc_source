# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyrpl/widgets/module_widgets/asg_widget.py
# Compiled at: 2017-08-29 09:44:06
__doc__ = '\nA widget for the scope module\n'
from .base_module_widget import ModuleWidget
from qtpy import QtCore, QtWidgets

class AsgWidget(ModuleWidget):

    def __init__(self, *args, **kwds):
        super(AsgWidget, self).__init__(*args, **kwds)
        self.attribute_widgets['trigger_source'].value_changed.connect(self.module.setup)