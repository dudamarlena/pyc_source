# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/external/qt/QtCore.py
# Compiled at: 2019-08-19 15:09:29
"""
Provides QtCore classes and functions.
"""
from builtins import str as __str
from taurus.core.util.log import deprecation_decorator as __deprecation
from . import PYQT5, PYSIDE2, PYQT4, PYSIDE, PythonQtError

@__deprecation(rel='4.0.1', alt='str')
class QString(__str):
    pass


@__deprecation(rel='4.0.1', alt='python objects directly')
def from_qvariant(qobj=None, convfunc=None):
    return qobj


@__deprecation(rel='4.0.1', alt='python objects directly')
def to_qvariant(pyobj=None):
    return pyobj


if PYQT5:
    from PyQt5.QtCore import *
    from PyQt5.QtCore import pyqtSignal as Signal
    from PyQt5.QtCore import pyqtSlot as Slot
    from PyQt5.QtCore import pyqtProperty as Property
    from PyQt5.QtCore import QT_VERSION_STR as __version__
    from PyQt5.QtCore import QDateTime
    QDateTime.toPython = QDateTime.toPyDateTime
elif PYSIDE2:
    from PySide2.QtCore import *
    from PySide2.QtCore import Signal as pyqtSignal
    from PySide2.QtCore import Slot as pyqtSlot
    from PySide2.QtCore import Property as pyqtProperty
    try:
        from PySide2.QtGui import QStringListModel
    except:
        pass

elif PYQT4:
    from PyQt4.QtCore import *
    from PyQt4.QtCore import QCoreApplication
    from PyQt4.QtCore import Qt
    from PyQt4.QtCore import pyqtSignal as Signal
    from PyQt4.QtCore import pyqtSlot as Slot
    from PyQt4.QtCore import pyqtProperty as Property
    from PyQt4.QtGui import QItemSelection, QItemSelectionModel, QItemSelectionRange, QSortFilterProxyModel, QStringListModel
    from PyQt4.QtCore import QT_VERSION_STR as __version__
    from PyQt4.QtGui import QDesktopServices as _QDesktopServices

    class QStandardPaths:
        StandardLocation = _QDesktopServices.StandardLocation
        displayName = _QDesktopServices.displayName
        DesktopLocation = _QDesktopServices.DesktopLocation
        DocumentsLocation = _QDesktopServices.DocumentsLocation
        FontsLocation = _QDesktopServices.FontsLocation
        ApplicationsLocation = _QDesktopServices.ApplicationsLocation
        MusicLocation = _QDesktopServices.MusicLocation
        MoviesLocation = _QDesktopServices.MoviesLocation
        PicturesLocation = _QDesktopServices.PicturesLocation
        TempLocation = _QDesktopServices.TempLocation
        HomeLocation = _QDesktopServices.HomeLocation
        DataLocation = _QDesktopServices.DataLocation
        CacheLocation = _QDesktopServices.CacheLocation
        writableLocation = _QDesktopServices.storageLocation


    @__deprecation(rel='4.0.1', alt='python objects directly')
    def QVariant(pyobj=None):
        return pyobj


elif PYSIDE:
    from PySide.QtCore import *
    from PySide.QtCore import Signal as pyqtSignal
    from PySide.QtCore import Slot as pyqtSlot
    from PySide.QtCore import Property as pyqtProperty
    from PySide.QtGui import QItemSelection, QItemSelectionModel, QItemSelectionRange, QSortFilterProxyModel, QStringListModel
    from PySide.QtGui import QDesktopServices as _QDesktopServices

    class QStandardPaths:
        StandardLocation = _QDesktopServices.StandardLocation
        displayName = _QDesktopServices.displayName
        DesktopLocation = _QDesktopServices.DesktopLocation
        DocumentsLocation = _QDesktopServices.DocumentsLocation
        FontsLocation = _QDesktopServices.FontsLocation
        ApplicationsLocation = _QDesktopServices.ApplicationsLocation
        MusicLocation = _QDesktopServices.MusicLocation
        MoviesLocation = _QDesktopServices.MoviesLocation
        PicturesLocation = _QDesktopServices.PicturesLocation
        TempLocation = _QDesktopServices.TempLocation
        HomeLocation = _QDesktopServices.HomeLocation
        DataLocation = _QDesktopServices.DataLocation
        CacheLocation = _QDesktopServices.CacheLocation
        writableLocation = _QDesktopServices.storageLocation


    import PySide.QtCore
    __version__ = PySide.QtCore.__version__
else:
    raise PythonQtError('No Qt bindings could be found')