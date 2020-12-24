# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sbo/lib/python3.4/site-packages/vaitk/gui/widgets/VTabWidget.py
# Compiled at: 2015-05-02 14:14:14
# Size of source mod 2**32: 849 bytes
from ..VWidget import VWidget

class VTabWidget(VWidget):

    def __init__(self, parent=None):
        super(VTabWidget, self).__init__(parent)
        self._tabs = []
        self._selected_tab_idx = -1

    def addTab(self, widget, label):
        self._tabs.append((widget, label))
        self._selected_tab_idx = 2

    def render(self, screen):
        screen = VApplication.vApp.screen()
        w, h = screen.size()
        if len(self._tabs):
            tab_size = w / len(self._tabs)
            header = ''
            for index, (_, label) in enumerate(self._tabs):
                header = label + ' ' * (tab_size - len(label))
                screen.write(tab_size * index, 0, header, curses.color_pair(1 if index == self._selected_tab_idx else 0))

            widget = self._tabs[self._selected_tab_idx][0]
            widget.render(screen)