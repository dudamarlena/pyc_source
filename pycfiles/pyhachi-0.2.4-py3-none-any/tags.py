# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pyhacc/tags.py
# Compiled at: 2013-09-08 13:48:31
from qtalchemy import *
from PySide import QtCore, QtGui
from qtalchemy.dialogs import *
from .PyHaccSchema import *

class TagEditor(BoundDialog):
    """
    >>> app, Session = qtappsession()
    >>> s = Session()
    >>> a=TagEditor(None,row=s.query(Tags).filter(Tags.name==Tags.Names.BankReconciled).one())
    """

    def __init__(self, parent, row=None, Session=None, row_id=None, flush=True):
        BoundDialog.__init__(self, parent)
        self.setWindowTitle('Tags')
        self.setDataReader(Session, Tags, 'id')
        main = QtGui.QVBoxLayout(self)
        grid = LayoutLayout(main, QtGui.QFormLayout())
        self.mm = self.mapClass(Tags)
        self.mm.addBoundField(grid, 'name')
        self.mm.addBoundField(grid, 'description')
        buttonbox = LayoutWidget(main, QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel))
        buttonbox.accepted.connect(self.accept)
        buttonbox.rejected.connect(self.reject)
        self.readData(row, row_id)

    def load(self):
        self.mm.connect_instance(self.main_row)