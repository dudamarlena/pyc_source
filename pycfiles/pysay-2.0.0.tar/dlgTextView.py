# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: C:\Anaconda2\lib\site-packages\pySAXS\guisaxs\qt\dlgTextView.py
# Compiled at: 2018-08-28 08:06:51
__doc__ = '\nproject : pySAXS\ndescription : function to print a message from a txt file to a dialog box\nauthors : Olivier Tache  \n\n'
from PyQt5 import QtGui, QtCore, uic, QtWidgets
import os, sys, pySAXS, codecs

class ViewMessage(QtWidgets.QDialog):

    def __init__(self, file, title='test', parent=None):
        QtWidgets.QDialog.__init__(self)
        self.ui = uic.loadUi(pySAXS.UI_PATH + 'dlgTextView.ui', self)
        f = codecs.open(file, mode='r', encoding='utf8', errors='ignore')
        msg = f.read()
        f.close()
        msgu = str(msg)
        self.textBrowser.setText(msgu)
        self.setWindowTitle(title)
        if parent is not None:
            self.move(parent.x(), parent.y())
        return


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    file = os.path.dirname(pySAXS.__file__) + os.sep + 'LICENSE.txt'
    myapp = ViewMessage(file, 'LICENCE')
    myapp.show()
    sys.exit(app.exec_())