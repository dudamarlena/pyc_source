# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\xicam\dialogs.py
# Compiled at: 2018-08-27 17:21:07
from PySide import QtGui, QtCore
from fabio import edfimage, tifimage
import numpy as np, os

def savedatadialog(guesspath='', caption='Save data to EDF', headers=None):
    if headers is None:
        headers = dict()
    dialog = QtGui.QFileDialog(parent=None, caption=caption, directory=os.path.dirname(guesspath), filter='EDF (*.edf);;PNG (*.png);;TIFF (*.tif)')
    dialog.selectFile(os.path.basename(guesspath))
    filename, ok = dialog.getSaveFileName()
    return (
     filename, ok)


def infodialog(msg, shortmsg):
    msgBox = QtGui.QMessageBox()
    msgBox.setText(msg)
    msgBox.setInformativeText(shortmsg)
    msgBox.setStandardButtons(QtGui.QMessageBox.Close)
    msgBox.setDefaultButton(QtGui.QMessageBox.Close)
    response = msgBox.exec_()


def checkoverwrite(path):
    msgBox = QtGui.QMessageBox()
    msgBox.setText(('Are you sure you want to overwrite {}?').format(path))
    msgBox.setStandardButtons(QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel)
    msgBox.setDefaultButton(QtGui.QMessageBox.Cancel)
    response = msgBox.exec_()
    return response == QtGui.QMessageBox.Ok