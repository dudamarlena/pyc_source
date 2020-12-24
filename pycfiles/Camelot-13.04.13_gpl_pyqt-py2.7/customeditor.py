# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/camelot/view/controls/editors/customeditor.py
# Compiled at: 2013-04-11 17:47:52
from PyQt4 import QtGui
from PyQt4 import QtCore
from camelot.view.proxy import ValueLoading

def set_background_color_palette(widget, background_color):
    """
    Set the palette of a widget to have a cerain background color.
    :param widget: a QWidget
    :param background_color: a QColor
    """
    if background_color not in (None, ValueLoading):
        palette = QtGui.QPalette(widget.palette())
        for x in [QtGui.QPalette.Active, QtGui.QPalette.Inactive, QtGui.QPalette.Disabled]:
            for y in [widget.backgroundRole(), QtGui.QPalette.Window, QtGui.QPalette.Base]:
                palette.setColor(x, y, background_color)

        widget.setPalette(palette)
    else:
        widget.setPalette(QtGui.QApplication.palette())
    return


def draw_tooltip_visualization(widget):
    """
    Draws a small visual indication in the top-left corner of a widget.
    :param widget: a QWidget
    """
    painter = QtGui.QPainter(widget)
    painter.drawPixmap(QtCore.QPoint(0, 0), QtGui.QPixmap(':/tooltip_visualization_7x7_glow.png'))


class AbstractCustomEditor(object):
    """
    Helper class to be used to build custom editors.
    This class provides functionality to store and retrieve 
    `ValueLoading` as an editor's value.

    Guidelines for implementing CustomEditors :

    * When an editor consists of multiple widgets, one widget must be the focusProxy
      of the editor, to have that widget immediately activated when the user single
      clicks in the table view.
    
    * When an editor has widgets that should not get selected when the user tabs
      through the editor, setFocusPolicy(Qt.ClickFocus) should be called on those
      widgets.
      
    * Editor should set their size policy, for most editor this means their
      vertical size policy should be  `QtGui.QSizePolicy.Fixed`
      
    """

    def __init__(self):
        self._value_loading = True
        self.value_is_none = False

    def set_value(self, value):
        if value == ValueLoading:
            self._value_loading = True
            return
        else:
            self._value_loading = False
            if value is None:
                self.value_is_none = True
            else:
                self.value_is_none = False
            return value
            return

    def get_value(self):
        if self._value_loading:
            return ValueLoading
        else:
            return

    def set_field_attributes(self, editable=True, background_color=None, tooltip='', **kwargs):
        self.set_background_color(background_color)

    def get_height(self):
        height = [
         QtGui.QLineEdit().sizeHint().height(),
         QtGui.QDateEdit().sizeHint().height(),
         QtGui.QDateTimeEdit().sizeHint().height(),
         QtGui.QSpinBox().sizeHint().height(),
         QtGui.QDateEdit().sizeHint().height(),
         QtGui.QComboBox().sizeHint().height()]
        finalHeight = max(height)
        return finalHeight

    def set_background_color(self, background_color):
        set_background_color_palette(self, background_color)


class CustomEditor(QtGui.QWidget, AbstractCustomEditor):
    """
    Base class for implementing custom editor widgets.
    This class provides dual state functionality.  Each 
    editor should have the posibility to have `ValueLoading`
    as its value, specifying that no value has been set yet.
    """
    editingFinished = QtCore.pyqtSignal()
    valueChanged = QtCore.pyqtSignal()

    def __init__(self, parent):
        QtGui.QWidget.__init__(self, parent)
        AbstractCustomEditor.__init__(self)

    def paintEvent(self, event):
        super(CustomEditor, self).paintEvent(event)
        if self.toolTip():
            draw_tooltip_visualization(self)