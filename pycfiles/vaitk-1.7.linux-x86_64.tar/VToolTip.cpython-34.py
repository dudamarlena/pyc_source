# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sbo/lib/python3.4/site-packages/vaitk/gui/widgets/VToolTip.py
# Compiled at: 2015-05-02 14:14:14
# Size of source mod 2**32: 1251 bytes
from .VLabel import VLabel
from ..VPainter import VPainter
from ..VPalette import VPalette
from ..VPalette import VPalette

class VToolTip(VLabel):
    _instance = None

    @classmethod
    def showText(cls, pos, text):
        """
        Shows the tooltip text at screen position pos.
        Only one tooltip is allowed. If another tooltip is already present,
        it will be moved and the text changed.
        """
        if cls._instance is None:
            cls._instance = VToolTip(text, parent=None)
        cls._instance.setText(text)
        cls._instance.resize((len(text), 1))
        cls._instance.move(pos)
        cls._instance.show()

    @classmethod
    def hideText(cls):
        """Hides the tooltip if present"""
        if cls._instance is not None:
            VLabel.hide(cls._instance)

    def paintEvent(self, event):
        painter = VPainter(self)
        w, h = self.size()
        painter.fg_color = self.palette().color(VPalette.ColorGroup.Active, VPalette.ColorRole.ToolTipText)
        painter.bg_color = self.palette().color(VPalette.ColorGroup.Active, VPalette.ColorRole.ToolTipBase)
        painter.drawText((0, 0), self._label)