# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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
    __doc__ = '\n    Widget for displaying hierarchical python data structures\n    (eg, nested dicts, lists, and arrays)\n    '

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
        else:
            if HAVE_METAARRAY:
                if hasattr(data, 'implements'):
                    if data.implements('MetaArray'):
                        data = {'data':data.view(np.ndarray), 
                         'meta':data.infoCopy()}
        if isinstance(data, dict):
            for k in data.keys():
                self.buildTree(data[k], node, str(k))

        else:
            if isinstance(data, list) or isinstance(data, tuple):
                for i in range(len(data)):
                    self.buildTree(data[i], node, str(i))

            else:
                node.setText(2, str(data))