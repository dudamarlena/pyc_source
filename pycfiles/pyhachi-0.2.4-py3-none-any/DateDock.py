# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pyhacc/DateDock.py
# Compiled at: 2013-09-08 13:48:31
from qtalchemy.dialogs import *
from qtalchemy.widgets import *
from PySide import QtCore, QtGui
from .PyHaccSchema import *

class DateObject(ModelObject):
    date = UserAttr(datetime.date, 'Transaction Date')


class DateWidget(QtGui.QWidget, MapperMixin):
    """
    >>> app, Session = qtappsession()
    >>> a = DateWidget(None, Session)
    >>> a.dateSettings.date = datetime.date(2012, 2, 4)
    >>> Session.date
    datetime.date(2012, 2, 4)
    """
    title = 'Date'
    factory = 'Date'

    def __init__(self, parent, Session):
        QtGui.QWidget.__init__(self, parent)
        self.setWindowTitle('Date')
        self.setObjectName('DateDock')
        self.Session = Session
        self.dateSettings = DateObject()
        if self.Session.date is None:
            self.dateSettings.date = datetime.date.today()
        else:
            self.dateSettings.date = self.Session.date
        box = QtGui.QHBoxLayout(self)
        self.mm = self.mapClass(DateObject)
        self.mm.addBoundField(box, 'date')
        self.mm.connect_instance(self.dateSettings)
        instanceEvent(self.dateSettings, 'set', 'date')(self.setDate)
        return

    def setDate(self, obj, attr, value):
        self.Session.date = self.dateSettings.date