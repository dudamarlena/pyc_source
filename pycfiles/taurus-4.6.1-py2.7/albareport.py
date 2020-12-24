# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/qt/qtgui/panel/report/albareport.py
# Compiled at: 2019-08-19 15:09:30
"""This module provides a panel to display taurus messages"""
from taurus.external.qt import Qt
from taurus.qt.qtgui.panel.report.basicreport import SendMailDialog, SMTPReportHandler
__package__ = 'taurus.qt.qtgui.panel.report'
__all__ = [
 'TicketReportHandler']
__docformat__ = 'restructuredtext'

class SendTicketDialog(SendMailDialog):

    def __init__(self, parent=None):
        SendMailDialog.__init__(self, parent=parent)
        self.ui.editTo.setParent(None)
        self.ui.editTo = Qt.QComboBox(self)
        self.ui.editTo.setEditable(True)
        self.ui.editTo.addItems(['controls', 'mis', 'electronics',
         'systems'])
        self.ui.editTo.setCurrentIndex(0)
        self.ui.mainLayout.addWidget(self.ui.editTo, 1, 1, 1, 1)
        return

    def getTo(self):
        return str(self.ui.editTo.currentText() + '@rt.cells.es')


class TicketReportHandler(SMTPReportHandler):
    """Report a message by sending an ALBA ticket"""
    Label = 'Send ticket'

    def getDialogClass(self):
        return SendTicketDialog


def main():
    app = Qt.QApplication([])
    w = SendTicketDialog()
    w.exec_()


if __name__ == '__main__':
    main()