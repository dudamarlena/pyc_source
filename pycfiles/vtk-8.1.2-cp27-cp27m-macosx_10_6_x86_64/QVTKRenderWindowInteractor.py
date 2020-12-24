# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/prabhu/src/git/VTKPythonPackage/VTK-osx_2.7/Wrapping/Python/vtk/qt4/QVTKRenderWindowInteractor.py
# Compiled at: 2018-11-28 17:07:58
import vtk.qt
try:
    import PyQt4
    vtk.qt.PyQtImpl = 'PyQt4'
except ImportError:
    try:
        import PySide
        vtk.qt.PyQtImpl = 'PySide'
    except ImportError:
        raise ImportError('Cannot load either PyQt or PySide')

from vtk.qt.QVTKRenderWindowInteractor import *
if __name__ == '__main__':
    print PyQtImpl
    QVTKRenderWidgetConeExample()