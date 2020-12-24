# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/layouts/SplitPanelBasicExample.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.api import VerticalLayout, VerticalSplitPanel, Label, HorizontalSplitPanel, CheckBox
from muntjac.ui.button import IClickListener
from muntjac.terminal.sizeable import ISizeable

class SplitPanelBasicExample(VerticalLayout):
    brownFox = 'The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. '

    def __init__(self):
        super(SplitPanelBasicExample, self).__init__()
        vert = VerticalSplitPanel()
        vert.setHeight('450px')
        vert.setWidth('100%')
        vert.setSplitPosition(150, ISizeable.UNITS_PIXELS)
        self.addComponent(vert)
        vert.addComponent(Label(self.brownFox))
        horiz = HorizontalSplitPanel()
        horiz.setSplitPosition(50)
        vert.addComponent(horiz)
        horiz.addComponent(Label(self.brownFox))
        horiz.addComponent(Label(self.brownFox))
        toggleLocked = CheckBox('Splits locked', LockListener(vert, horiz))
        toggleLocked.setImmediate(True)
        self.addComponent(toggleLocked)


class LockListener(IClickListener):

    def __init__(self, vert, horiz):
        self._vert = vert
        self._horiz = horiz

    def buttonClick(self, event):
        self._vert.setLocked(event.getButton().booleanValue())
        self._horiz.setLocked(event.getButton().booleanValue())