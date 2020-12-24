# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/bibolamazi_gui/sourcelisteditor.py
# Compiled at: 2015-05-11 05:40:29
import os, os.path, logging
logger = logging.getLogger(__name__)
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import bibolamazi.init
from .qtauto.ui_sourcelisteditor import Ui_SourceListEditor

class SourceListEditor(QWidget):

    def __init__(self, parent):
        super(SourceListEditor, self).__init__(parent)
        self.ui = Ui_SourceListEditor()
        self.ui.setupUi(self)
        self.ui.btnAddFavorite.clicked.connect(self.requestAddToFavorites)
        QObject.connect(self.ui.lstSources.model(), SIGNAL('layoutChanged()'), self.update_stuff_moved)
        self._is_updating = False
        self._ref_dir = None
        return

    sourceListChanged = pyqtSignal('QStringList')
    requestAddToFavorites = pyqtSignal()

    def sourceList(self):
        return [ str(self.ui.lstSources.item(i).text()) for i in xrange(self.ui.lstSources.count()) ]

    def setRefDir(self, refdir):
        """Sets the "reference" directory, which is the directory in which the bibolamazi
        file being edited resides. This is used to decide on whether to refer to a file with
        an absolute or a relative path.
        """
        self._ref_dir = refdir

    @pyqtSlot(QStringList, bool)
    @pyqtSlot(QStringList)
    def setSourceList(self, sourcelist, noemit=False):
        sourcelist = [ str(x) for x in list(sourcelist) ]
        if sourcelist == self.sourceList():
            return
        self._is_updating = True
        self.ui.lstSources.clear()
        for src in sourcelist:
            self.ui.lstSources.addItem(src)

        self.on_lstSources_currentRowChanged(self.ui.lstSources.currentRow())
        self._is_updating = False
        if not noemit:
            self.emitSourceListChanged()

    @pyqtSlot()
    def emitSourceListChanged(self):
        if self._is_updating:
            return
        logger.debug('emitting sourceListChanged()!')
        self.sourceListChanged.emit(QStringList(self.sourceList()))

    @pyqtSlot()
    def on_btnAddSource_clicked(self):
        self.ui.lstSources.addItem('')
        self.ui.lstSources.setCurrentRow(self.ui.lstSources.count() - 1)
        self.ui.txtFile.setFocus()
        self.emitSourceListChanged()

    @pyqtSlot()
    def on_btnRemoveSource_clicked(self):
        row = self.ui.lstSources.currentRow()
        if row < 0:
            logger.debug('No row selected')
            return
        logger.debug('removing row %d', row)
        item = self.ui.lstSources.takeItem(row)
        self.emitSourceListChanged()

    @pyqtSlot()
    def update_stuff_moved(self):
        logger.debug('Stuff moved around!')
        self.emitSourceListChanged()

    @pyqtSlot('QListWidgetItem*')
    def on_lstSources_itemDoubleClicked(self, item):
        logger.debug('double-clicked!!')
        self.ui.txtFile.setFocus()

    @pyqtSlot(int)
    def on_lstSources_currentRowChanged(self, row):
        logger.debug('current row changed.. row=%d', row)
        if self.ui.lstSources.count() == 0 or row < 0:
            self.ui.txtFile.setText('')
            self.ui.btnRemoveSource.setEnabled(False)
            self.ui.gbxEditSource.setEnabled(False)
        else:
            self.ui.btnRemoveSource.setEnabled(True)
            self.ui.gbxEditSource.setEnabled(True)
            self.ui.txtFile.setText(self.ui.lstSources.item(row).text())

    @pyqtSlot(QString)
    def on_txtFile_textChanged(self, text):
        row = self.ui.lstSources.currentRow()
        if row < 0:
            logger.debug('No row selected')
            return
        item = self.ui.lstSources.item(row)
        if item.text() != text:
            item.setText(text)
            self.emitSourceListChanged()

    @pyqtSlot()
    def on_btnBrowse_clicked(self):
        row = self.ui.lstSources.currentRow()
        if row < 0:
            logger.debug('No row selected')
            return
        fname = str(QFileDialog.getOpenFileName(self, 'Select BibTeX File', QString(), 'BibTeX Files (*.bib);;All Files (*)'))
        logger.debug('fname=%r.', fname)
        if not fname:
            return
        if self._ref_dir:
            relpath = os.path.relpath(os.path.realpath(fname), os.path.realpath(self._ref_dir))
            if '..' in relpath.split(os.sep) or '..' in relpath.split(os.altsep):
                pass
            else:
                fname = relpath
        self.ui.txtFile.setText(fname)