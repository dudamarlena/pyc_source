# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/colin/Projects/pyqode.cobol/pyqode/cobol/modes/pic_offset.py
# Compiled at: 2016-12-29 05:32:02
# Size of source mod 2**32: 1987 bytes
import os
from pyqode.qt import PYQT4_API, PYSIDE_API
from pyqode.qt.QtCore import QObject, Signal, Slot
from pyqode.qt.QtGui import QIcon
from pyqode.qt.QtWidgets import QAction
from pyqode.cobol.api import get_field_infos
from pyqode.core.api import Mode, TextHelper

class OffsetCalculatorMode(QObject, Mode):
    __doc__ = '\n    This modes computes the selected PIC fields offsets.\n\n    It adds a "Calculate PIC offsets" action to the editor context menu and\n    emits the signal |pic_infos_available| when the the user triggered the\n    action and the pic infos have been computed.\n    '
    pic_infos_available = Signal(list)

    def __init__(self):
        if os.environ['QT_API'] in PYQT4_API + PYSIDE_API:
            QObject.__init__(self)
            Mode.__init__(self)
        else:
            super().__init__()

    def on_install(self, editor):
        super().on_install(editor)
        self.action = QAction(editor)
        self.action.setText(_('Calculate PIC offsets'))
        self.action.setIcon(QIcon.fromTheme('accessories-calculator'))
        self.action.setShortcut('Ctrl+Shift+O')
        self.action.setToolTip(_('Compute the PIC offset of the fields in the selected text'))
        editor.add_action(self.action, sub_menu='COBOL')
        self.action.triggered.connect(self._compute_offsets)

    def _compute_offsets(self):
        original_tc = self.editor.textCursor()
        tc = self.editor.textCursor()
        start = tc.selectionStart()
        end = tc.selectionEnd()
        tc.setPosition(start)
        start_line = tc.blockNumber()
        tc.setPosition(end)
        end_line = tc.blockNumber()
        th = TextHelper(self.editor)
        th.select_lines(start=start_line, end=end_line, apply_selection=True)
        source = th.selected_text()
        results = get_field_infos(source, self.editor.free_format)
        self.editor.setTextCursor(original_tc)
        self.pic_infos_available.emit(results)