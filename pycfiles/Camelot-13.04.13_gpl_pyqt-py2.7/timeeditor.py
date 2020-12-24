# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/camelot/view/controls/editors/timeeditor.py
# Compiled at: 2013-04-11 17:47:52
import datetime
from PyQt4 import QtGui
from customeditor import AbstractCustomEditor, set_background_color_palette, draw_tooltip_visualization
from camelot.core import constants

class TimeEditor(QtGui.QTimeEdit, AbstractCustomEditor):

    def __init__(self, parent, editable=True, field_name='time', format=constants.camelot_time_format, **kwargs):
        QtGui.QTimeEdit.__init__(self, parent)
        AbstractCustomEditor.__init__(self)
        self.setObjectName(field_name)
        self.setDisplayFormat(format)
        self.setEnabled(editable)

    def set_value(self, value):
        value = AbstractCustomEditor.set_value(self, value)
        if value:
            self.setTime(value)
        else:
            self.setTime(self.minimumTime())

    def get_value(self):
        value = self.time()
        value = datetime.time(hour=value.hour(), minute=value.minute(), second=value.second())
        return AbstractCustomEditor.get_value(self) or value

    def set_field_attributes(self, editable=True, background_color=None, tooltip=None, **kwargs):
        self.set_enabled(editable)
        self.set_background_color(background_color)
        self.setToolTip(unicode(tooltip or ''))

    def set_enabled(self, editable=True):
        self.setEnabled(editable)

    def paintEvent(self, event):
        super(TimeEditor, self).paintEvent(event)
        if self.toolTip():
            draw_tooltip_visualization(self)

    def set_background_color(self, background_color):
        set_background_color_palette(self.lineEdit(), background_color)