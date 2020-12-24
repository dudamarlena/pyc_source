# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Anaconda2\lib\site-packages\pySAXS\guisaxs\qt\dlgTextView.py
# Compiled at: 2018-08-28 08:06:51
"""
project : pySAXS
description : function to print a message from a txt file to a dialog box
authors : Olivier Tache  

"""
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