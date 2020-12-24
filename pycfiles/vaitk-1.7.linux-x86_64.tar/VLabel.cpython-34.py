# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sbo/lib/python3.4/site-packages/vaitk/gui/widgets/VLabel.py
# Compiled at: 2015-05-02 14:14:14
# Size of source mod 2**32: 1087 bytes
from ... import core
from ..VWidget import VWidget
from ..VPainter import VPainter
from ..VPalette import VPalette

class VLabel(VWidget):

    def __init__(self, label='', parent=None):
        super().__init__(parent)
        self._label = label

    def paintEvent(self, event):
        painter = VPainter(self)
        w, h = self.size()
        painter.fg_color = self.palette().color(VPalette.ColorGroup.Active, VPalette.ColorRole.WindowText)
        painter.bg_color = self.palette().color(VPalette.ColorGroup.Active, VPalette.ColorRole.Window)
        string = ' ' * w
        for i in range(0, int(h / 2)):
            painter.drawText((0, i), string)

        painter.drawText((0, int(h / 2)), self._label + ' ' * (w - len(self._label)))
        for i in range(1 + int(h / 2), h):
            painter.drawText((0, i), string)

    def minimumSize(self):
        return (len(self._label), 1)

    def setText(self, text):
        if text != self._label:
            self._label = text
            self.update()