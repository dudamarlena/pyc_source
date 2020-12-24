# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/qt/qtgui/util/qdraganddropdebug.py
# Compiled at: 2019-08-19 15:09:30
__all__ = [
 'DropDebugger']
__docformat__ = 'restructuredtext'
from taurus.external.qt import Qt

class DropDebugger(Qt.QLabel):
    """A simple utility for debugging drag&drop.
    This widget will accept drops and show a pop-up with the contents
    of the MIME data passed in the drag&drop"""

    def __init__(self, parent=None):
        Qt.QLabel.__init__(self, parent)
        self.setAcceptDrops(True)
        self.setText('Drop something here')
        self.setMinimumSize(300, 200)
        self.setWindowTitle('Drag&Drop Debugger')

    def dragEnterEvent(self, event):
        event.acceptProposedAction()

    def dropEvent(self, event):
        """reimplemented to support drag&drop of models. See :class:`QWidget`"""
        msg = '<b>MIMETYPE</b>: DATA. <ul>'
        mimedata = event.mimeData()
        for format in mimedata.formats():
            data = mimedata.data(format)
            msg += ('<li><b>{0}</b>: "{1}"</li>').format(format, data)

        msg += '</ul>'
        Qt.QMessageBox.information(self, 'Drop event received', msg)


if __name__ == '__main__':
    import sys
    from taurus.qt.qtgui.application import TaurusApplication
    app = TaurusApplication(cmd_line_parser=None)
    w = DropDebugger()
    w.show()
    sys.exit(app.exec_())