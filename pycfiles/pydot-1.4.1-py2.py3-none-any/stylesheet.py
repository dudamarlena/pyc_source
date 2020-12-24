# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/pydosh/stylesheet.py
# Compiled at: 2013-12-19 02:01:18
from PySide import QtGui, QtCore
__styleNames = ['Default', 'Dark']

def styleSheetNames():
    return __styleNames


def setStylesheet(name=None):
    """ Set the stylesheet from the resource settings.
                If no stylesheet name is supplied then the value from the
                config is read
        """
    settings = QtCore.QSettings()
    if name is None:
        name = settings.value('options/stylesheet', __styleNames[0])
    if name not in __styleNames:
        QtGui.QMessageBox.warning(None, 'Stylesheet Error', 'Stylesheet %r not recognised - must be one of %r' % (
         name, (', ').join(__styleNames)), QtGui.QMessageBox.Ok)
        name = __styleNames[0]
    styleSheetFile = QtCore.QFile(':/style/%s' % name)
    styleSheetFile.open(QtCore.QIODevice.ReadOnly)
    styleSheet = styleSheetFile.readAll()
    QtGui.QApplication.instance().setStyleSheet(str(styleSheet))
    settings.setValue('options/stylesheet', name)
    return