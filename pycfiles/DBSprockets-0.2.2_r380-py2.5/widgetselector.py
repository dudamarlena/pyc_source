# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/dbsprockets/widgetselector.py
# Compiled at: 2008-06-30 11:43:48
"""
widgetselecter Module

this contains the class which allows the ViewConfig to select the appropriate widget for the given field

Classes:
Name                               Description
WidgetSelecter                     Parent Class
SAWidgetSelector                   Selecter Based on sqlalchemy field types
DatabaseViewWidgetSelector         Database View always selects the same widget
TableDefWidgetSelector             Table def fields use the same widget

Exceptions:
None

Functions:
None

Copywrite (c) 2007 Christopher Perkins
Original Version by Christopher Perkins 2007
Released under MIT license.
"""
from sqlalchemy.schema import Column
from sqlalchemy.types import *
from tw.api import Widget
from tw.forms.fields import *
from dbsprockets.widgets.widgets import *
from dbsprockets.saprovider import SAProvider

class WidgetSelector:

    def select(self, field):
        return Widget


class DatabaseViewWidgetSelector(WidgetSelector):

    def select(self, field):
        return TableLabelWidget


class TableDefWidgetSelector(WidgetSelector):

    def select(self, field):
        return TableDefWidget


class RecordViewWidgetSelector(WidgetSelector):

    def select(self, field):
        return RecordFieldWidget


text_field_limit = 100

class SAWidgetSelector(WidgetSelector):
    defaultWidgets = {String: TextField, 
       Integer: TextField, 
       Numeric: TextField, 
       DateTime: DBSprocketsCalendarDateTimePicker, 
       Date: DBSprocketsCalendarDatePicker, 
       Time: DBSprocketsTimePicker, 
       Binary: FileField, 
       PickleType: TextField, 
       Boolean: DBSprocketsCheckBox}
    defaultNameBasedWidgets = {}

    def _getSelectWidget(self, field):
        return ForeignKeySingleSelectField

    def select(self, field):
        if not isinstance(field, Column):
            raise TypeError('arg1 must be a sqlalchemy column, not %s' % type(field))
        if isinstance(field.type, Integer):
            if len(field.foreign_keys) == 1:
                return self._getSelectWidget(field)
        if field.name in self.defaultNameBasedWidgets:
            return self.defaultNameBasedWidgets[field.name]
        if field.name.lower() == 'password':
            return PasswordField
        tipe = String
        for t in self.defaultWidgets.keys():
            if isinstance(field.type, t):
                tipe = t
                break

        widget = self.defaultWidgets[tipe]
        if widget is TextField and hasattr(field.type, 'length') and (field.type.length is None or field.type.length > text_field_limit):
            widget = TextArea
        return widget