# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sbo/lib/python3.4/site-packages/vaitk/gui/widgets/VProgressBar.py
# Compiled at: 2015-05-02 14:14:14
# Size of source mod 2**32: 3308 bytes
from ... import core
from ..VWidget import VWidget
from ..VPainter import VPainter
from ..VPalette import VPalette

class VProgressBar(VWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._text = ''
        self._minimum = 0
        self._maximum = 100
        self._value = 0

    def paintEvent(self, event):
        painter = VPainter(self)
        w, h = self.size()
        fg_color = self.palette().color(VPalette.ColorGroup.Active, VPalette.ColorRole.WindowText)
        bg_color = self.palette().color(VPalette.ColorGroup.Active, VPalette.ColorRole.Window)
        final_text = ''
        if len(self._text) > 0:
            final_text += self._text + ' '
        percentage = int(100 * (self.value() - self.minimum()) / (self.maximum() - self.minimum()))
        percentage_text = '%d' % percentage + '%'
        bar_total_length = w - len(final_text) - 2
        if bar_total_length < 5:
            bar_text = percentage_text.rjust(4)
        else:
            bar_fill_length = int(bar_total_length * percentage / 100)
            bar_text = '=' * bar_fill_length + ' ' * (bar_total_length - bar_fill_length)
            bar_text = bar_text[:int(bar_total_length / 2) - 1] + percentage_text + bar_text[int(bar_total_length / 2) - 1 + len(percentage_text):]
        final_text += '[' + bar_text + ']'
        painter.drawText((0, 0), final_text, fg_color, bg_color)

    def minimumSize(self):
        if len(self._text) > 0:
            width = len(self._text) + len(' [100%]')
        else:
            width = len('[100%]')
        return (width, 1)

    def setValue(self, value):
        if self._value != value:
            if self._minimum < value < self._maximum:
                self._value = value
                self.update()

    def minimum(self):
        return self._minimum

    def maximum(self):
        return self._maximum

    def setMinimum(self, minimum):
        if self._minimum == minimum:
            return
        self._minimum = minimum
        if self._minimum > self._maximum:
            self._maximum = self._minimum
        if not self._minimum < self._value < self._maximum:
            self.reset()
        else:
            self.update()

    def setMaximum(self, maximum):
        if self._maximum == maximum:
            return
        self._maximum = maximum
        if self._maximum < self._minimum:
            self._minimum = self._maximum
        if not self._minimum < self._value < self._maximum:
            self.reset()
        else:
            self.update()

    def reset(self):
        self._value = self._minimum
        self.update()

    def setRange(self, minimum, maximum):
        if self._minimum == minimum and self._maximum == maximum:
            return
        self._minimum = minimum
        self._maximum = maximum
        if self._maximum < self._minimum:
            self._maximum = self._minimum
        if not self._minimum < self._value < self._maximum:
            self.reset()
        else:
            self.update()

    def setText(self, text):
        self._text = text

    def text(self):
        return self._text

    def value(self):
        return self._value