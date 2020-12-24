# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/widgets/DataTreeWidget.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 2886 bytes
from ..Qt import QtGui, QtCore
from ..pgcollections import OrderedDict
import types, traceback, numpy as np
try:
    import metaarray
    HAVE_METAARRAY = True
except:
    HAVE_METAARRAY = False

__all__ = ['DataTreeWidget']

class DataTreeWidget(QtGui.QTreeWidget):
    """DataTreeWidget"""

    def __init__(self, parent=None, data=None):
        QtGui.QTreeWidget.__init__(self, parent)
        self.setVerticalScrollMode(self.ScrollPerPixel)
        self.setData(data)
        self.setColumnCount(3)
        self.setHeaderLabels(['key / index', 'type', 'value'])

    def setData(self, data, hideRoot=False):
        """data should be a dictionary."""
        self.clear()
        self.buildTree(data, (self.invisibleRootItem()), hideRoot=hideRoot)
        self.expandToDepth(3)
        self.resizeColumnToContents(0)

    def buildTree(self, data, parent, name='', hideRoot=False):
        if hideRoot:
            node = parent
        else:
            typeStr = type(data).__name__
            if typeStr == 'instance':
                typeStr += ': ' + data.__class__.__name__
            node = QtGui.QTreeWidgetItem([name, typeStr, ''])
            parent.addChild(node)
        if isinstance(data, types.TracebackType):
            data = list(map(str.strip, traceback.format_list(traceback.extract_tb(data))))
        elif HAVE_METAARRAY:
            if hasattr(data, 'implements'):
                if data.implements('MetaArray'):
                    data = {'data':data.view(np.ndarray), 
                     'meta':data.infoCopy()}
        if isinstance(data, dict):
            for k in data.keys():
                self.buildTree(data[k], node, str(k))

        elif isinstance(data, list) or isinstance(data, tuple):
            for i in range(len(data)):
                self.buildTree(data[i], node, str(i))

        else:
            node.setText(2, str(data))