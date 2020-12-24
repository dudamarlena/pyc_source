# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/layouts/LayoutSpacingExample.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.api import VerticalLayout, GridLayout, CheckBox, Button
from muntjac.ui.button import IClickListener

class LayoutSpacingExample(VerticalLayout, IClickListener):

    def __init__(self):
        super(LayoutSpacingExample, self).__init__()
        self.grid = GridLayout(3, 3)
        self.grid.setSpacing(False)
        self.sp = CheckBox('Spacing enabled')
        self.sp.setImmediate(True)
        self.sp.addListener(self, IClickListener)
        self.addComponent(self.sp)
        self.addComponent(self.grid)
        for i in range(9):
            self.grid.addComponent(Button('Component %d' % (i + 1)))

        self.setSpacing(True)

    def buttonClick(self, event):
        enabled = self.sp.booleanValue()
        self.grid.setSpacing(enabled)