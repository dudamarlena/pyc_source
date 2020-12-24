# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tgfastdata\datawidgets.py
# Compiled at: 2007-08-13 18:20:11
import turbogears
from turbogears import widgets, validators
from turbogears.widgets.datagrid import DataGrid
from sqlobject import SQLObject
from turbogears.database import so_columns, so_joins

class EditForm(widgets.TableForm):
    __module__ = __name__
    template = 'tgfastdata.templates.editform'


class FastDataGrid(DataGrid):
    """Grid that displays SQLObject's SelectResults with add/edit/delete controls.
    """
    __module__ = __name__
    css = [
     widgets.CSSLink(widgets.static, 'grid.css')]
    template = 'tgfastdata.templates.datagrid'
    params = ['show_actions', 'show_add_link', 'add_link_title', 'delete_link_msg', 'get_edit_url', 'get_delete_url', 'get_add_url']
    add_link_title = 'Add a record'
    show_actions = True
    show_add_link = True
    delete_link_msg = 'Are you sure you want to delete this?'

    def __init__(self, fields=None, **kw):
        """Ctor.
        You can pass fields to control what and how is displayed to override sqlmeta.
        """
        super(FastDataGrid, self).__init__([], **kw)
        self.fields = fields

    def get_add_url():
        return lambda row=None: turbogears.url('add')
        return

    get_add_url = staticmethod(get_add_url)

    def get_edit_url():

        def _get_edit_url(row):
            return turbogears.url([str(row.id), 'edit'])

        return _get_edit_url

    get_edit_url = staticmethod(get_edit_url)

    def get_delete_url():

        def _get_delete_url(row):
            return turbogears.url([str(row.id), 'delete'])

        return _get_delete_url

    get_delete_url = staticmethod(get_delete_url)

    def update_params(self, d):
        """Sets up headers based on the select results columns"""
        fields = d.get('fields') or self.fields
        d['fields'] = self._prepare_fields(d['value'], fields)
        super(FastDataGrid, self).update_params(d)

    def _prepare_fields(self, value, fields):
        if hasattr(value, 'sourceClass'):
            columns_meta = so_columns(value.sourceClass)
        else:
            columns_meta = {}
        collist_raw = fields or columns_meta.keys()
        if not collist_raw:
            raise ValueError, 'no fields information can be found'
        if columns_meta:

            def f(col):
                if not (isinstance(col, tuple) or isinstance(col, DataGrid.Column)):
                    name = col
                    if columns_meta.has_key(name):
                        column = columns_meta[name]
                        header = column.title or column.name.capitalize()
                    elif columns_meta.has_key(name + 'ID'):
                        column = columns_meta[(name + 'ID')]
                        header = column.title or column.name[:-2].capitalize()
                    else:
                        header = name
                    col = DataGrid.Column(name=name, title=header)
                return col

            collist_raw = [ f(col) for col in collist_raw ]
        return collist_raw


class EmptyStringConverter(validators.FancyValidator):
    """
    Converts empty string to None value. Doesn't change any other values.
    """
    __module__ = __name__

    def _to_python(self, value, state):
        if isinstance(value, basestring) and len(value) == 0:
            return None
        if isinstance(value, unicode):
            try:
                return value.encode()
            except:
                return value

        else:
            return value
        return


class SaneDateConverter(validators.DateConverter):
    """Converts string to dates and vice versa for DataCol columns.
    
    FIXME: This is crudely hacked to work in conjunction with 
           CalendarDatePicker widget. Should really implement a proper 
           DateConverter and submit it to FormEncode.
    """
    __module__ = __name__
    month_style = 'dd.mm.yyy'
    format = '%d.%m.%Y'

    def __init__(self, format=None, **kw):
        if format:
            self.format = format
        super(SaneDateConverter, self).__init__(**kw)

    def _from_python(self, value, state):
        if self.if_empty is not validators.NoDefault and not value:
            return ''
        return value.strftime(self.format)


class SaneCalendarDatePicker(widgets.CalendarDatePicker):
    """DatePicker wiget with nicer date format."""
    __module__ = __name__
    format = '%d.%m.%Y'

    def __init__(self, format=None, **kw):
        if format:
            self.format = format
        super(SaneCalendarDatePicker, self).__init__(**kw)


def option_selected(input_value, option_value):
    if hasattr(input_value, '__getitem__') and not isinstance(input_value, basestring):
        return option_value in [ row.id for row in input_value ]
    elif isinstance(input_value, SQLObject):
        return option_value == input_value.id
    else:
        return option_value == input_value


class DataCheckBoxList(widgets.CheckBoxList):
    __module__ = __name__
    validator = validators.Set()

    def checked(self, input_value, option_value):
        return self._is_option_selected(option_value, input_value)

    def _is_option_selected(self, option_value, value):
        if option_selected(value, option_value):
            return True
        return False


class JoinSelect(widgets.MultipleSelectField):
    __module__ = __name__
    validator = validators.Set()

    def checked(self, input_value, option_value):
        return self._is_option_selected(option_value, input_value)

    def _is_option_selected(self, option_value, value):
        if option_selected(value, option_value):
            return True
        return False


class DataSelectField(widgets.SingleSelectField):
    __module__ = __name__

    def selected(self, input_value, option_value):
        return self._is_option_selected(option_value, input_value)

    def _is_option_selected(self, option_value, value):
        if option_selected(value, option_value):
            return True
        return False