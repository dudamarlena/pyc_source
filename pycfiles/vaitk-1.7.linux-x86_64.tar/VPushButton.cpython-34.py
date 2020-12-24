# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sbo/lib/python3.4/site-packages/vaitk/gui/widgets/VPushButton.py
# Compiled at: 2015-05-02 14:14:14
# Size of source mod 2**32: 489 bytes
from ..VWidget import VWidget

class VPushButton(VWidget):

    def __init__(self, label, parent=None):
        super(VPushButton, self).__init__(parent)
        self._label = label

    def render(self, painter):
        super(VPushButton, self).render(painter)
        for i in range(0, h / 2):
            painter.write(0, i, ' ' * w)

        painter.write(0, h / 2, '[ ' + self._label + ' ]' + ' ' * (w - len(self._label) - 4))
        for i in range(1 + h / 2, h):
            painter.write(0, i, ' ' * w)