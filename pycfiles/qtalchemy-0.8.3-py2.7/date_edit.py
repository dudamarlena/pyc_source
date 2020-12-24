# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/qtalchemy/widgets/date_edit.py
# Compiled at: 2013-09-07 09:08:02
"""
The PBDateEdit provides a date input box with more flexible entry.

It also supports null dates which is something QDateEdit does not.
"""
import datetime, fuzzyparsers
from PySide import QtCore, QtGui
from qtalchemy import fromQType, toQType
from .button_edit import PBButtonEdit, Property

class DateValidator(QtGui.QValidator):

    def __init__(self, parent=None):
        QtGui.QValidator.__init__(self, parent)

    def fixup(self, input):
        if input == '':
            return ''
        try:
            date = fuzzyparsers.parse_date(input)
        except:
            return ''

        return date.strftime('%x')

    def validate(self, input, pos):
        try:
            date = fuzzyparsers.parse_date(input)
            return (QtGui.QValidator.Acceptable, input, pos)
        except Exception as e:
            return (
             QtGui.QValidator.Intermediate, input, pos)


class PBDateEdit(PBButtonEdit):
    """
    PBDateEdit is a QLineEdit derivative that parses input strings into dates 
    with the fuzzyparsers python package.  A QCalendarWidget is available 
    by clicking a button to the right of the edit or pressing F4.
    """

    def __init__(self, parent=None):
        PBButtonEdit.__init__(self, parent)
        self.setValidator(DateValidator())
        self.button.setIcon(QtGui.QIcon(':/qtalchemy/widgets/view-calendar.ico'))
        self.editingFinished.connect(self.transform)
        x = self.sizePolicy()
        self.setSizePolicy(QtGui.QSizePolicy.Minimum, x.verticalPolicy())

    def minimumSizeHint(self):
        buttonWidth = self.style().pixelMetric(QtGui.QStyle.PM_ScrollBarExtent)
        x = PBButtonEdit.minimumSizeHint(self)
        x.setWidth(len(datetime.date.today().strftime('%x')) * 9 + buttonWidth)
        return x

    def sizeHint(self):
        buttonWidth = self.style().pixelMetric(QtGui.QStyle.PM_ScrollBarExtent)
        x = PBButtonEdit.sizeHint(self)
        x.setWidth(len(datetime.date.today().strftime('%x')) * 9 + buttonWidth)
        return x

    def date(self):
        x = self.text()
        if x == '':
            return
        else:
            return toQType(fuzzyparsers.parse_date(x))
            return

    def setDate(self, v):
        v = fromQType(v)
        if v is None:
            self.setText('')
        else:
            self.setText(v.strftime('%x'))
        return

    date = Property('QDate', date, setDate)

    def transform(self):
        x = self.text()
        if x != '':
            self.setDate(toQType(fuzzyparsers.parse_date(x)))

    def date_selected(self, date):
        self.setDate(date)
        self.calendar.close()

    def buttonPress(self):
        PBButtonEdit.buttonPress(self)
        self.calendar = QtGui.QCalendarWidget()
        self.calendar.setWindowFlags(QtCore.Qt.Popup)
        if self.date is not None:
            self.calendar.setSelectedDate(self.date)
        self.calendar.activated.connect(self.date_selected)
        self.calendar.clicked.connect(self.date_selected)
        self.calendar.move(self.mapToGlobal(self.rect().bottomLeft()))
        self.calendar.show()
        self.calendar.setFocus(QtCore.Qt.PopupFocusReason)
        return