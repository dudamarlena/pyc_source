# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/Qt.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 6154 bytes
"""
This module exists to smooth out some of the differences between PySide and PyQt4:

* Automatically import either PyQt4 or PySide depending on availability
* Allow to import QtCore/QtGui pyqtgraph.Qt without specifying which Qt wrapper
  you want to use.
* Declare QtCore.Signal, .Slot in PyQt4  
* Declare loadUiType function for Pyside

"""
import sys, re
from .python2_3 import asUnicode
PYSIDE = 'PySide'
PYQT4 = 'PyQt4'
PYQT5 = 'PyQt5'
QT_LIB = None
libOrder = [
 PYQT4, PYSIDE, PYQT5]
for lib in libOrder:
    if lib in sys.modules:
        QT_LIB = lib
        break

if QT_LIB is None:
    for lib in libOrder:
        try:
            __import__(lib)
            QT_LIB = lib
            break
        except ImportError:
            pass

if QT_LIB == None:
    raise Exception('PyQtGraph requires one of PyQt4, PyQt5 or PySide; none of these packages could be imported.')
if QT_LIB == PYSIDE:
    from PySide import QtGui, QtCore, QtOpenGL, QtSvg
    try:
        from PySide import QtTest
    except ImportError:
        pass

    import PySide
    try:
        from PySide import shiboken
        isQObjectAlive = shiboken.isValid
    except ImportError:

        def isQObjectAlive(obj):
            try:
                if hasattr(obj, 'parent'):
                    obj.parent()
                else:
                    if hasattr(obj, 'parentItem'):
                        obj.parentItem()
                    else:
                        raise Exception('Cannot determine whether Qt object %s is still alive.' % obj)
            except RuntimeError:
                return False
            else:
                return True


    VERSION_INFO = 'PySide ' + PySide.__version__

    class StringIO(object):
        __doc__ = 'Alternative to built-in StringIO needed to circumvent unicode/ascii issues'

        def __init__(self):
            self.data = []

        def write(self, data):
            self.data.append(data)

        def getvalue(self):
            return ''.join(map(asUnicode, self.data)).encode('utf8')


    def loadUiType(uiFile):
        """
        Pyside "loadUiType" command like PyQt4 has one, so we have to convert the ui file to py code in-memory first    and then execute it in a special frame to retrieve the form_class.
        """
        import pysideuic
        import xml.etree.ElementTree as xml
        parsed = xml.parse(uiFile)
        widget_class = parsed.find('widget').get('class')
        form_class = parsed.find('class').text
        with open(uiFile, 'r') as (f):
            o = StringIO()
            frame = {}
            pysideuic.compileUi(f, o, indent=0)
            pyc = compile(o.getvalue(), '<string>', 'exec')
            exec(pyc, frame)
            form_class = frame[('Ui_%s' % form_class)]
            base_class = eval('QtGui.%s' % widget_class)
        return (form_class, base_class)


else:
    if QT_LIB == PYQT4:
        from PyQt4 import QtGui, QtCore, uic
        try:
            from PyQt4 import QtSvg
        except ImportError:
            pass

        try:
            from PyQt4 import QtOpenGL
        except ImportError:
            pass

        try:
            from PyQt4 import QtTest
        except ImportError:
            pass

        VERSION_INFO = 'PyQt4 ' + QtCore.PYQT_VERSION_STR + ' Qt ' + QtCore.QT_VERSION_STR
    else:
        if QT_LIB == PYQT5:
            from PyQt5 import QtGui, QtCore, QtWidgets, Qt, uic
            try:
                from PyQt5 import QtSvg
            except ImportError:
                pass

            try:
                from PyQt5 import QtOpenGL
            except ImportError:
                pass

            def scale(self, sx, sy):
                tr = self.transform()
                tr.scale(sx, sy)
                self.setTransform(tr)


            QtWidgets.QGraphicsItem.scale = scale

            def rotate(self, angle):
                tr = self.transform()
                tr.rotate(angle)
                self.setTransform(tr)


            QtWidgets.QGraphicsItem.rotate = rotate

            def translate(self, dx, dy):
                tr = self.transform()
                tr.translate(dx, dy)
                self.setTransform(tr)


            QtWidgets.QGraphicsItem.translate = translate

            def setMargin(self, i):
                self.setContentsMargins(i, i, i, i)


            QtWidgets.QGridLayout.setMargin = setMargin

            def setResizeMode(self, mode):
                self.setSectionResizeMode(mode)


            QtWidgets.QHeaderView.setResizeMode = setResizeMode
            QtGui.QApplication = QtWidgets.QApplication
            QtGui.QGraphicsScene = QtWidgets.QGraphicsScene
            QtGui.QGraphicsObject = QtWidgets.QGraphicsObject
            QtGui.QGraphicsWidget = QtWidgets.QGraphicsWidget
            QtGui.QApplication.setGraphicsSystem = None
            for o in dir(QtWidgets):
                if o.startswith('Q'):
                    setattr(QtGui, o, getattr(QtWidgets, o))

            VERSION_INFO = 'PyQt5 ' + QtCore.PYQT_VERSION_STR + ' Qt ' + QtCore.QT_VERSION_STR
        else:
            if QT_LIB.startswith('PyQt'):
                import sip

                def isQObjectAlive(obj):
                    return not sip.isdeleted(obj)


                loadUiType = uic.loadUiType
                QtCore.Signal = QtCore.pyqtSignal
            versionReq = [
             4, 7]
            USE_PYSIDE = QT_LIB == PYSIDE
            USE_PYQT4 = QT_LIB == PYQT4
            USE_PYQT5 = QT_LIB == PYQT5
            QtVersion = PySide.QtCore.__version__ if QT_LIB == PYSIDE else QtCore.QT_VERSION_STR
            m = re.match('(\\d+)\\.(\\d+).*', QtVersion)
            if m is not None and list(map(int, m.groups())) < versionReq:
                print(list(map(int, m.groups())))
                raise Exception('pyqtgraph requires Qt version >= %d.%d  (your version is %s)' % (versionReq[0], versionReq[1], QtVersion))