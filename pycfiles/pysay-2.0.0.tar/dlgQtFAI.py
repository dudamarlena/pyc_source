# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: C:\Anaconda2\lib\site-packages\pySAXS\guisaxs\qt\dlgQtFAI.py
# Compiled at: 2018-08-23 04:00:44
from PyQt5 import QtGui, QtCore, uic, QtWidgets
import sys
from pyFAI import azimuthalIntegrator
from numpy import *
import numpy, sys, os.path
from pySAXS.tools import FAIsaxs
from pySAXS.tools import filetools
from pySAXS.guisaxs import dataset
import time, fabio
from pySAXS.LS import SAXSparametersXML
from pySAXS.guisaxs.qt import dlgQtFAITest
import pySAXS

class FAIDialog(QtWidgets.QDialog):

    def __init__(self, parent=None, parameterfile=None, outputdir=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = uic.loadUi(pySAXS.UI_PATH + 'dlgQtFAI.ui', self)
        self.setWindowTitle('Radial averaging tool for SAXS')
        if parent is not None:
            self.setWindowIcon(parent.windowIcon())
        self.ui.paramFileButton.clicked.connect(self.OnClickparamFileButton)
        self.ui.paramViewButton.clicked.connect(self.OnClickparamViewButton)
        self.ui.addButton.clicked.connect(self.OnAddButton)
        self.ui.changeOutputDirButton.clicked.connect(self.OnClickchangeOutputDirButton)
        self.ui.RADButton.clicked.connect(self.OnClickRADButton)
        self.ui.buttonRemove.clicked.connect(self.OnClickRemove)
        self.ui.buttonClearList.clicked.connect(self.OnClickClearList)
        self.ui.listWidget.setAcceptDrops(True)
        self.parent = parent
        self.workingdirectory = ''
        self.printout = None
        if parent is not None:
            self.printout = parent.printTXT
            self.workingdirectory = parent.workingdirectory
        if parameterfile is not None:
            self.ui.paramTxt.setText(parameterfile)
        if outputdir is not None:
            self.ui.outputDirTxt.setText(outputdir)
        self.imageToolWindow = None
        return

    def dragEnterEvent(self, event):
        event.acceptProposedAction()

    def dropEvent(self, event):
        mimeData = event.mimeData()
        if mimeData.hasUrls():
            for url in mimeData.urls():
                f = str(url.path())
                li = QtWidgets.QListWidgetItem(f)
                self.ui.listWidget.addItem(li)

    def OnClickparamFileButton(self):
        fd = QtWidgets.QFileDialog(self)
        filename, truc = fd.getOpenFileName(directory=self.workingdirectory, filter='XML files (*.xml)')
        self.workingdirectory = filename
        self.ui.paramTxt.setText(filename)

    def OnClickparamViewButton(self):
        filename = str(self.ui.paramTxt.text())
        if filename is not None and filename != '':
            self.dlgFAI = dlgQtFAITest.FAIDialogTest(self.parent, filename, None)
            self.dlgFAI.show()
        return

    def OnAddButton(self):
        fd = QtWidgets.QFileDialog(self)
        filenames, truc = fd.getOpenFileNames(directory=self.workingdirectory)
        for f in filenames:
            li = QtWidgets.QListWidgetItem(f)
            self.ui.listWidget.addItem(li)
            self.workingdirectory = f

    def OnClickViewImage(self):
        """itemList=self.ui.listWidget.selectedItems()
        if len(itemList)<0:
            return #no item selected
        
        if self.imageToolWindow is None:
            #oprn a new window
            self.imageToolWindow = QtImageTool.MainWindow(self.parent)
        
        for item in itemList:
            filename=str(item.text())
            self.imageToolWindow.open_image(filename)
        
        self.imageToolWindow.show()"""
        pass

    def OnClickRemove(self):
        itemList = self.ui.listWidget.selectedItems()
        print itemList
        if len(itemList) < 0:
            return
        for item in itemList:
            self.ui.listWidget.takeItem(self.ui.listWidget.row(item))

    def OnClickClearList(self):
        """
        erase list
        """
        self.ui.listWidget.clear()

    def OnClickchangeOutputDirButton(self):
        fd = QtWidgets.QFileDialog(self, directory=self.workingdirectory)
        fd.setFileMode(QtWidgets.QFileDialog.DirectoryOnly)
        if fd.exec_() == 1:
            direc = str(fd.selectedFiles()[0])
            self.ui.outputDirTxt.setText(direc)
            self.workingdirectory = direc

    def OnClickRADButton(self):
        items = []
        for index in range(self.ui.listWidget.count()):
            items.append(self.ui.listWidget.item(index))

        l = [ str(i.text()) for i in items ]
        n = len(l)
        if n <= 0:
            return
        else:
            self.ui.progressBar.setMaximum(n)
            self.ui.progressBar.setValue(0)
            fai = FAIsaxs.FAIsaxs()
            filename = self.ui.paramTxt.text()
            if not os.path.exists(filename):
                self.printTXT(filename + ' does not exist')
                return
            outputdir = self.ui.outputDirTxt.text()
            fai.setGeometry(filename)
            mad = fai.getIJMask()
            maskfilename = fai.getMaskFilename()
            self.printTXT('Image mask opened in ', maskfilename)
            for ind in range(len(l)):
                self.ui.progressBar.setValue(ind + 1)
                imageFilename = l[ind]
                t0 = time.time()
                im, q, i, s, newname = fai.integratePySaxs(l[ind], mad, self.printTXT)
                t1 = time.time()
                if im is not None:
                    self.printTXT('data averaged in ' + str(t1 - t0) + ' s for ' + imageFilename + ' and saved as ' + newname)
                    if self.parent is not None:
                        name = filetools.getFilename(imageFilename)
                        if 'Comment' in im.header:
                            comment = im.header['Comment']
                            if comment != '':
                                name += '-' + comment
                        self.parent.data_dict[name] = dataset.dataset(name, q, i, imageFilename, error=s, type='saxs', image='Image')

            self.parent.redrawTheList()
            self.parent.Replot()
            self.ui.progressBar.setValue(0)
            if self.parent is not None:
                self.parent.pref.set('outputdir', section='pyFAI', value=str(self.ui.outputDirTxt.text()))
                self.parent.pref.set('parameterfile', section='pyFAI', value=str(self.ui.paramTxt.text()))
                self.parent.pref.save()
            return

    def printTXT(self, txt='', par=''):
        """
        for printing messages
        """
        if self.printout == None:
            print str(txt) + str(par)
        else:
            self.printout(txt, par)
        return


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    myapp = FAIDialog()
    myapp.show()
    sys.exit(app.exec_())