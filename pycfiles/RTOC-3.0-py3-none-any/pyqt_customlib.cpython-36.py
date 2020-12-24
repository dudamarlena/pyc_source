# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Benutzer\haschtl\Dokumente\GIT\kellerlogger\RTOC\lib\pyqt_customlib.py
# Compiled at: 2019-06-12 19:19:09
# Size of source mod 2**32: 11239 bytes
"""
This module contains some helper functions for PyQT4 or PyQT5 (and pyqtgraph)
"""
import time, datetime as dt, pyqtgraph as pg
from PyQt5 import QtCore
from PyQt5 import QtWidgets, QtGui, Qt
translate = QtCore.QCoreApplication.translate

def _(text):
    return translate('rtoc', text)


try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:

    def _fromUtf8(s):
        return s


import logging as log
log.basicConfig(level=(log.INFO))
logging = log.getLogger(__name__)

class QHLine(QtWidgets.QFrame):
    __doc__ = '\n    This class creates a horizontal line. Inherited from PyQt5.QtWidgets.QFrame\n\n    Args:\n        width (int): The pixel-width of the horizontal line\n    '

    def __init__(self, width=2):
        super(QHLine, self).__init__()
        self.setFrameShape(QtWidgets.QFrame.HLine)
        self.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.setLineWidth(width)
        self.setStyleSheet('color: black; background-color: black;')


class QVLine(QtWidgets.QFrame):
    __doc__ = '\n    This class creates a vertical line. Inherited from PyQt5.QtWidgets.QFrame\n\n    Args:\n        width (int): The pixel-width of the vertical line\n    '

    def __init__(self, width=2):
        super(QVLine, self).__init__()
        self.setFrameShape(QtWidgets.QFrame.VLine)
        self.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.setLineWidth(width)
        self.setStyleSheet('color: black; background-color: black;')


def getListWidgets(QListWidget):
    """
    Get all items of a QListWidget

    Args:
        QListWidget (QListWidget): A QListWidget

    Returns:
        A list containing all QListWidgetItems
    """
    items = []
    for x in range(QListWidget.count()):
        items.append(QListWidget.itemWidget(QListWidget.item(x)))

    return items


def alert_message(title, text, info, stylesheet='', okbutton=None, cancelbutton=None):
    """
    Creates an alert message. Can be accepted or canceled

    Args:
        title (str): Dialog title
        text (str): Message text
        info (str): Description text
        stylesheet (str): A stylesheet for the dialog
        okbutton (str): Accept-button string
        cancelbutton (str): Cancel-button string

    Returns:
        bool
    """
    if okbutton is None:
        okbutton = translate('lib', 'Ok')
    if cancelbutton is None:
        cancelbutton = translate('lib', 'Cancel')
    msg = QtWidgets.QMessageBox()
    msg.setIcon(QtWidgets.QMessageBox.Warning)
    msg.setText(text)
    msg.setInformativeText(info)
    msg.setWindowTitle(title)
    msg.addButton(okbutton, QtWidgets.QMessageBox.YesRole)
    msg.addButton(cancelbutton, QtWidgets.QMessageBox.NoRole)
    msg.setStyleSheet(stylesheet)
    msg.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
    retval = msg.exec_()
    if retval is 0:
        return True
    else:
        return False


def tri_message(title, text, info, stylesheet='', okbutton=None, nobutton=None, cancelbutton=None):
    """
    Creates an tri-state message. Has three buttons the user can click

    Args:
        title (str): Dialog title
        text (str): Message text
        info (str): Description text
        stylesheet (str): A stylesheet for the dialog
        okbutton (str): Accept-button string
        nobutton (str): Decline-button string
        cancelbutton (str): Cancel-button string

    Returns:
        bool
    """
    if okbutton is None:
        okbutton = translate('lib', 'Yes')
    else:
        if nobutton is None:
            nobutton = translate('lib', 'No')
        if cancelbutton is None:
            cancelbutton = translate('lib', 'Cancel')
    msg = QtWidgets.QMessageBox()
    msg.setIcon(QtWidgets.QMessageBox.Warning)
    msg.setText(text)
    msg.setInformativeText(info)
    msg.setWindowTitle(title)
    msg.addButton(okbutton, QtWidgets.QMessageBox.YesRole)
    msg.addButton(nobutton, QtWidgets.QMessageBox.NoRole)
    msg.addButton(cancelbutton, QtWidgets.QMessageBox.NoRole)
    msg.setStyleSheet(stylesheet)
    msg.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
    retval = msg.exec_()
    if retval is 0:
        return True
    else:
        if retval is 1:
            return False
        return


def info_message(title, text, info, stylesheet=''):
    """
    Creates an info message. Can only be accepted by user.

    Args:
        title (str): Dialog title
        text (str): Message text
        info (str): Description text
        stylesheet (str): A stylesheet for the dialog

    Returns:
        None
    """
    msg = QtWidgets.QMessageBox()
    msg.setIcon(QtWidgets.QMessageBox.Information)
    msg.setText(text)
    msg.setInformativeText(info)
    msg.setWindowTitle(title)
    msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
    msg.setStyleSheet(stylesheet)
    msg.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
    retval = msg.exec_()
    return retval


def item_message(self, title, text, items, stylesheet=''):
    """
    Creates an item-select message. The user can select one item from a list.

    Args:
        self: The parent module calling this function
        title (str): Dialog title
        text (str): Message text
        items (list): Description text
        stylesheet (str): A stylesheet for the dialog

    Returns:
        item (str): Selected item
        ok (bool): Is true, if dialog was not cancelled
    """
    item, ok = QtWidgets.QInputDialog.getItem(self, title, text, items, 0, False)
    return (item, ok)


def text_message(self, title, text, placeholdertext, stylesheet=''):
    """
    Creates a text-input message. The user can enter some text.

    Args:
        self: The parent module calling this function
        title (str): Dialog title
        text (str): Message text
        placeholdertext (str): Placeholder text
        stylesheet (str): A stylesheet for the dialog

    Returns:
        text (str): Submitted text
        ok (bool): Is true, if dialog was not cancelled
    """
    text, ok = QtWidgets.QInputDialog.getText(self, title, text, QtWidgets.QLineEdit.Normal, placeholdertext)
    return (
     text, ok)


def int_message(self, title, text, stylesheet=''):
    """
    Creates a int-input message. The user can enter some text.

    Args:
        self: The parent module calling this function
        title (str): Dialog title
        text (str): Message text
        stylesheet (str): A stylesheet for the dialog

    Returns:
        num (int): Selected number
        ok (bool): Is true, if dialog was not cancelled
    """
    num, ok = QtWidgets.QInputDialog.getInt(self, title, text)
    return (
     num, ok)


def clearLayout(layout):
    """
    Clears all elements from a QLayout (like horizontal or vertical layout)

    Args:
        layout (QLayout): The layout you want to clear

    Returns:
        None
    """
    while layout.count():
        child = layout.takeAt(0)
        if child.widget():
            child.widget().deleteLater()


def setHorScaleCursor():
    """
    Sets the mouse-cursor to 'Horizontal select cursor'
    """
    Qt.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.SizeHorCursor))


def setVerScaleCursor():
    """
    Sets the mouse-cursor to 'Vertical select cursor'
    """
    Qt.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.SizeVerCursor))


def restoreCursor():
    """
    Sets the mouse-cursor to default cursor
    """
    Qt.QApplication.restoreOverrideCursor()


class TimeAxisItem(pg.AxisItem):
    __doc__ = '\n    A custom AxisItem for pyqtgraph.\n    Formats elapsed seconds to readable text\n    '

    def __init__(self, relative=True, *args, **kwargs):
        (super().__init__)(*args, **kwargs)
        self.setLabel(text='Time', units=None)
        self.enableAutoSIPrefix(False)
        self._relative = relative

    def tickStrings(self, values, scale, spacing):
        list = []
        for value in values:
            if value < 0:
                sign = '-'
            else:
                sign = ''
            if self._relative:
                list.append(sign + str(dt.timedelta(seconds=(abs(value)))))
            else:
                list.append(self.formatTime(value))

        return list

    def formatTime(self, value):
        if value <= 86400:
            return '-->'
        else:
            if int(value) == value:
                try:
                    format = dt.datetime.fromtimestamp(float(value))
                    format = format.strftime('%d.%m.%Y %H:%M:%S')
                    return format
                except:
                    print(value)

            else:
                format = dt.datetime.fromtimestamp(float(value))
                format = format.strftime('%H:%M:%S.%f')
            return format

    def attachToPlotItem(self, plotItem):
        """Add this axis to the given PlotItem
        :param plotItem: (PlotItem)
        """
        self.setParentItem(plotItem)
        viewBox = plotItem.getViewBox()
        self.linkToView(viewBox)
        self._oldAxis = plotItem.axes[self.orientation]['item']
        self._oldAxis.hide()
        plotItem.axes[self.orientation]['item'] = self
        pos = plotItem.axes[self.orientation]['pos']
        (plotItem.layout.addItem)(self, *pos)
        self.setZValue(-1000)