# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/qt/qtgui/dialog/taurusconfigurationdialog.py
# Compiled at: 2019-08-19 15:09:29
"""This module provides a set of dialog based widgets"""
__all__ = [
 'TaurusConfigurationDialog']
__docformat__ = 'restructuredtext'
from taurus.external.qt import Qt
from taurus.qt.qtgui.panel.taurusconfigurationpanel import TaurusConfigurationPanel

class TaurusConfigurationDialog(Qt.QDialog):

    def __init__(self, parent=None, designMode=False):
        Qt.QDialog.__init__(self, parent)
        self.setWindowTitle('TaurusConfigurationDialog')
        layout = Qt.QVBoxLayout()
        self.setLayout(layout)
        ConfigPanel = TaurusConfigurationPanel
        self._panel = ConfigPanel(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self._panel)
        self._panel._ui.pushButtonOk.setVisible(True)
        self._panel._ui.pushButtonCancel.setVisible(True)
        self._panel._ui.pushButtonOk.clicked.connect(self._onOk)
        self._panel._ui.pushButtonCancel.clicked.connect(self._onCancel)
        self.adjustSize()
        self.show()

    def _onOk(self):
        self._panel._onOk()
        self._onCancel()

    def _onCancel(self):
        self.close()

    def setModel(self, model):
        self._panel.setModel(model)


def main():
    import sys
    attr_name = sys.argv[1]
    a = Qt.QApplication([])
    d = TaurusConfigurationDialog()
    d.setModel(attr_name)
    return a.exec_()


if __name__ == '__main__':
    import sys
    sys.exit(main())