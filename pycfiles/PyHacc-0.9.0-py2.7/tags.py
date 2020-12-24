# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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