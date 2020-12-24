# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/panels/PanelLightExample.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.api import VerticalLayout, Panel, Label, Button
from muntjac.ui.button import IClickListener
from muntjac.ui.themes import Reindeer

class PanelLightExample(VerticalLayout, IClickListener):

    def __init__(self):
        super(PanelLightExample, self).__init__()
        self.setSpacing(True)
        self.setSpacing(True)
        self._panel = Panel('This is a light Panel')
        self._panel.setStyleName(Reindeer.PANEL_LIGHT)
        self._panel.setHeight('200px')
        layout = self._panel.getContent()
        layout.setMargin(True)
        layout.setSpacing(True)
        self.addComponent(self._panel)
        for _ in range(20):
            l = Label('The quick brown fox jumps over the lazy dog.')
            self._panel.addComponent(l)

        b = Button('Toggle caption')
        b.addListener(self, IClickListener)
        self.addComponent(b)

    def buttonClick(self, event):
        if self._panel.getCaption() is None:
            self._panel.setCaption('This is a light Panel')
        else:
            self._panel.setCaption(None)
        return