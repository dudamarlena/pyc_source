# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sbo/lib/python3.4/site-packages/vaitk/gui/widgets/VDialog.py
# Compiled at: 2015-05-02 14:14:14
# Size of source mod 2**32: 1879 bytes
from ..VWidget import VWidget
from ..VPalette import VPalette
from ..VPainter import VPainter

class VDialog(VWidget):

    def __init__(self, parent=None):
        super(VDialog, self).__init__(parent)
        self._title = None

    def paintEvent(self, event):
        if self.isEnabled():
            if self.isActive():
                color_group = VPalette.ColorGroup.Active
            else:
                color_group = VPalette.ColorGroup.Inactive
        else:
            color_group = VPalette.ColorGroup.Disabled
        fg, bg = self.colors(color_group)
        w, h = self.size()
        if self._title:
            dash_length = w - 2 - len(self._title) - 2 - 2
            header = '+' + '-' * (dash_length / 2) + '| ' + self._title + ' |' + '-' * (dash_length - dash_length / 2) + '+'
        else:
            header = '+' + '-' * (w - 2) + '+'
        painter = VPainter(self)
        painter.write(0, 0, header, fg, bg)
        for i in range(0, h - 2):
            painter.write(0, i + 1, '|' + ' ' * (len(header) - 2) + '|', fg, bg)

        painter.write(0, h - 1, '+' + '-' * (len(header) - 2) + '+', fg, bg)

    def setTitle(self, title):
        self._title = title

    def minimumSize(self):
        if self._title:
            return (len(self._title) + 8, 2)
        else:
            return (2, 2)

    def contentsMargins(self):
        return (1, 1, 1, 1)