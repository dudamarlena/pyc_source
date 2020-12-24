# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Python27\lib\site-packages\pySAXS\guisaxs\qt\testQtFAI.py
# Compiled at: 2012-11-20 09:14:47
from PyQt4 import QtGui, QtCore
import sys
from pySAXS.guisaxs.qt import FAIDialogui
import numpy, sys, os.path, dircache
from pySAXS.tools import FAIsaxs
import pyFAI
from pyFAI import azimuthalIntegrator
from pySAXS.tools import filetools
from pySAXS.guisaxs import dataset
import time
from pyFAI import azimuthalIntegrator
import fabio

class FAIDialog(QtGui.QMainWindow):

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = FAIDialogui.Ui_FAIDialog()
        self.ui.setupUi(self)
        QtCore.QObject.connect(self.ui.paramFileButton, QtCore.SIGNAL('clicked()'), self.OnClickparamFileButton)
        QtCore.QObject.connect(self.ui.addButton, QtCore.SIGNAL('clicked()'), self.OnAddButton)
        QtCore.QObject.connect(self.ui.changeOutputDirButton, QtCore.SIGNAL('clicked()'), self.OnClickchangeOutputDirButton)
        QtCore.QObject.connect(self.ui.RADButton, QtCore.SIGNAL('clicked()'), self.OnClickRADButton)
        self.printout = None
        return

    def OnClickparamFileButton(self):
        fd = QtGui.QFileDialog(self)
        filename = fd.getOpenFileName()
        self.ui.paramTxt.setText(filename)

    def OnAddButton(self):
        fd = QtGui.QFileDialog(self)
        filenames = fd.getOpenFileNames()
        print filenames
        for f in filenames:
            li = QtGui.QListWidgetItem(f)
            self.ui.listWidget.addItem(li)

    def OnClickchangeOutputDirButton(self):
        fd = QtGui.QFileDialog(self)
        fd.setFileMode(QtGui.QFileDialog.DirectoryOnly)
        if fd.exec_() == 1:
            dir = str(fd.selectedFiles().first())
            self.ui.outputDirTxt.setText(dir)

    def OnClickRADButton(self):
        items = []
        for index in range(self.ui.listWidget.count()):
            items.append(self.ui.listWidget.item(index))

        l = [ str(i.text()) for i in items ]
        print l
        n = len(l)
        self.ui.progressBar.setMaximum(n)
        self.ui.progressBar.setValue(0)
        fai = azimuthalIntegrator.AzimuthalIntegrator()
        filename = self.ui.paramTxt.text()
        if os.path.exists(filename):
            d = FAIsaxs.getIJxml(filename)
        else:
            printTXT(filename + ' does not exist')
            return
        outputdir = self.ui.outputDirTxt.text()
        FAIsaxs.setGeometry(fai, d)
        if d.has_key('user.qDiv'):
            qDiv = d['user.qDiv']
        else:
            qDiv = 1000
        mad, maskfilename = FAIsaxs.getIJMask(d)
        self.printTXT('Image mask opened in ', maskfilename)
        for i in range(len(l)):
            self.ui.progressBar.setValue(i + 1)
            time.sleep(1.1)
            imageFilename = l[i]
            name = filetools.getFilename(imageFilename)
            newname = outputdir + os.sep + name + '.rgr'
            try:
                im = fabio.open(imageFilename)
            except:
                self.printTXT('error in opening ', imageFilename)
                im = None

            if im is not None:
                t0 = time.time()
                q, i, s = fai.saxs(im.data, qDiv, filename=newname, mask=mad, correctSolidAngle=False)
                t1 = time.time()
                self.printTXT('data averaged in ' + str(t1 - t0) + ' s for ' + imageFilename + ' and saved as ' + newname)
                continue

        self.ui.progressBar.setValue(0)
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
    app = QtGui.QApplication(sys.argv)
    myapp = FAIDialog()
    myapp.show()
    sys.exit(app.exec_())