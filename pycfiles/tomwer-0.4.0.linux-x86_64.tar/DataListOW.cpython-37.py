# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/orangecontrib/tomwer/widgets/control/DataListOW.py
# Compiled at: 2020-01-23 09:41:29
# Size of source mod 2**32: 4094 bytes
__authors__ = [
 'C. Nemoz', 'H. Payno']
__license__ = 'MIT'
__date__ = '01/12/2016'
from Orange.widgets import widget, gui
from silx.gui import qt
from tomwer.core.utils import logconfig
from tomwer.gui.datalist import DataListDialog
from tomwer.core.process.scanlist import _ScanList
from tomwer.core.scan.scanfactory import ScanFactory
from tomwer.web.client import OWClient
from Orange.widgets.settings import Setting
from Orange.widgets.widget import Output
import logging
logger = logging.getLogger(__name__)

class DataListOW(widget.OWWidget, OWClient):
    name = 'data list'
    id = 'orange.widgets.tomwer.scanlist'
    description = 'List path to reconstructions/scans. Those path will be send to the next box once validated.'
    icon = 'icons/scanlist.svg'
    priority = 50
    category = 'esrfWidgets'
    keywords = ['tomography', 'file', 'tomwer', 'folder']
    want_main_area = True
    resizing_enabled = True
    compress_signal = False
    _scanIDs = Setting(list())
    assert len(_ScanList.outputs) == 1

    class Outputs:
        data_out = Output(name=(_ScanList.outputs[0].name), type=(_ScanList.outputs[0].type),
          doc=(_ScanList.outputs[0].doc))

    def __init__(self, parent=None):
        """A simple annuary which register all folder containing completed scan

        .. warning: the widget won't check for scan validity and will only
            emit the path to folders to the next widgets

        :param parent: the parent widget
        """
        widget.OWWidget.__init__(self, parent)
        OWClient.__init__(self, logger)
        self.widget = DataListDialog(parent=self)
        self.widget.setScanIDs(self._scanIDs)
        layout = gui.vBox(self.mainArea, self.name).layout()
        layout.addWidget(self.widget)
        self.widget._sendButton.clicked.connect(self._sendList)
        self.size = self.widget.size
        self.add = self.widget.add
        self.start = self._sendList

    def _sendList(self):
        """Send a signal for each list to the next widget"""
        for d in self.widget.datalist.items:
            try:
                scan = ScanFactory.create_scan_object(d)
            except:
                logger.error('Fail to create an instance of TomoBase from', d)
            else:
                mess = 'sending one scan %s' % d
                logger.debug(mess, extra={logconfig.DOC_TITLE: self.widget._scheme_title, 
                 logconfig.SCAN_ID: d})
                self.Outputs.data_out.send(scan)


def main():
    app = qt.QApplication([])
    s = DataListOW()
    s.show()
    app.exec_()


if __name__ == '__main__':
    main()