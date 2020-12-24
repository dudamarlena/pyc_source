# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/gui/qfolderdialog.py
# Compiled at: 2019-12-12 10:30:45
# Size of source mod 2**32: 4327 bytes
__author__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '08/02/2017'
from silx.gui import qt
import logging, os
_logger = logging.getLogger()

class QScanDialog(qt.QFileDialog):
    __doc__ = 'docstring for QFolderDialog'

    def __init__(self, parent, multiSelection=False):
        qt.QFileDialog.__init__(self, parent)
        self.setFileMode(qt.QFileDialog.ExistingFiles)
        self.setOption(qt.QFileDialog.ShowDirsOnly)
        self.multiSelection = multiSelection
        idir = False
        f_cd_last = os.environ['HOME'] + '/.octave/mylastpwd.txt'
        if os.path.isfile(f_cd_last) is True:
            with open(f_cd_last, 'r') as (fcdl):
                d_cd_last = fcdl.readlines()
                d_cd_last = d_cd_last[0][0:d_cd_last[0].rfind('/')]
                idir = os.path.isdir(d_cd_last)
        else:
            if idir is True:
                self.setDirectory(d_cd_last)
            else:
                self.setDirectory('/data')
            if self.multiSelection is True:
                self.file_view = self.findChild(qt.QListView, 'listView')
                if self.file_view:
                    self.file_view.setSelectionMode(qt.QAbstractItemView.MultiSelection)
                    self.file_view.setSelectionMode(qt.QAbstractItemView.ExtendedSelection)
                self.f_tree_view = self.findChild(qt.QTreeView)
                if self.f_tree_view:
                    self.f_tree_view.setSelectionMode(qt.QAbstractItemView.MultiSelection)
                    self.f_tree_view.setSelectionMode(qt.QAbstractItemView.ExtendedSelection)
                btns = self.findChildren(qt.QPushButton)
                if len(btns) is 0:
                    _logger.error('Cannot retrieve open button. Multiple selection not available. Might came from an issue with some PyQt(5) version. Had this issue with PyQt5 5.9.2')
                else:
                    self.openBtn = [x for x in btns if 'open' in str(x.text()).lower()][0]
                    self.openBtn.clicked.disconnect()
                    self.openBtn.hide()
                    parent = self.openBtn.parent()
                    self.openBtn = qt.QPushButton('Select', parent=parent)
                    self.openBtn.clicked.connect(self.openClicked)
                    parent.layout().insertWidget(0, self.openBtn)

    def openClicked(self):
        inds = self.f_tree_view.selectionModel().selectedIndexes()
        files = []
        for i in inds:
            if i.column() == 0:
                files.append(os.path.join(str(self.directory().absolutePath()), str(i.data())))

        self.selectedFiles = files
        self.accept()
        self.done(1)

    def filesSelected(self):
        return self.selectedFiles