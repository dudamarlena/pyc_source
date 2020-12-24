# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/progrid/progrid.py
# Compiled at: 2015-03-22 17:32:36
import pdb, sys
from functools import partial
from kivy.adapters.dictadapter import DictAdapter
from kivy.adapters.listadapter import ListAdapter
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.lang import Builder
from kivy.metrics import dp, sp
from kivy.properties import *
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.listview import ListItemButton, ListView
from kivy.uix.selectableview import SelectableView
from kivy.uix.scrollview import ScrollView
from kivy.uix.stacklayout import StackLayout
from kivy.uix.textinput import TextInput
import pdb
from material_ui.flatui.flatui import FlatButton, FlatTextInput, FloatingAction
from material_ui.flatui.labels import BindedLabel, ResizeableLabel
from material_ui.flatui.layouts import ColorBoxLayout
from material_ui.flatui.popups import AlertPopup, FlatPopup, OkButtonPopup
from pkg_resources import resource_filename
path = resource_filename(__name__, 'progrid.kv')
Builder.load_file(path)
icon_settings_32 = resource_filename(__name__, 'images/settings-32.png')

class ProGrid(BoxLayout):
    """
    Data to display, array of dictionaries.
    """
    data = ListProperty([])
    headers = DictProperty({})
    columns = ListProperty([])
    col_order = ListProperty([])
    row_filters = DictProperty({})
    row_filters_names = DictProperty({})
    records_readonly = BooleanProperty(True)
    row_sorting = ListProperty([])
    data_len_limit = NumericProperty(1000)
    coltypes = DictProperty({})
    text_no_data = StringProperty('No data found.')
    content = ObjectProperty(None)
    selection_color = ListProperty([0.6, 0.6, 1, 1])
    content_background_color = ListProperty([0.98, 0.98, 0.98, 1])
    content_font_name = StringProperty('')
    content_font_size = NumericProperty(dp(15))
    content_align = OptionProperty('left', options=['left', 'center', 'right'])
    header = ObjectProperty(None)
    header_background_color = ListProperty([0.93, 0.93, 0.93, 1])
    header_font_name = StringProperty('')
    header_font_size = NumericProperty(dp(17))
    header_height = NumericProperty(dp(52))
    header_align = OptionProperty('left', options=['left', 'center', 'right'])
    footer = ObjectProperty(None)
    footer_background_color = ListProperty([0.93, 0.93, 0.93, 1])
    footer_height = NumericProperty(dp(30))
    footer_align = OptionProperty('left', options=['left', 'center', 'right'])
    footer_text = StringProperty('www.github.com/Cuuuurzel/kivy-pro-grid ')
    footer_text_color = ListProperty([0, 0, 0, 0.9])
    footer_text_halign = OptionProperty('right', options=['left', 'center', 'right'])
    footer_text_font_name = StringProperty(None)
    footer_text_font_size = NumericProperty(dp(12))
    text_color = ListProperty([0, 0, 0, 0.9])
    grid_color = ListProperty([0.93, 0.93, 0.93, 1])
    padding_h = NumericProperty(dp(5))
    padding_v = NumericProperty(dp(0))
    row_height = NumericProperty(dp(42))
    on_double_tap = ObjectProperty(None)
    on_long_press = ObjectProperty(None)
    on_select = ObjectProperty(None)
    _data = ListProperty([])
    _rows = ListProperty([])
    _coltypes = DictProperty({})

    def __init__(self, **kargs):
        super(ProGrid, self).__init__(**kargs)
        self.___grid = {}
        self.bind(data=self._render)
        self.bind(columns=self._render)
        self.bind(row_filters=self._render)
        self.bind(row_sorting=self._render)
        self.bind(data_len_limit=self._render)
        self.bind(content_font_size=lambda o, v: self.setter('row_height')(o, v * 2))
        self._render(self.data)

    def _render(self, *args):
        if len(self.data) > self.data_len_limit:
            self._raise_too_much_data(len(self.data))
        self._setup_data(self.data)
        self._build_coltypes()
        for col in self.columns:
            self.___grid[col] = []

        self._gen_header()
        self._gen_footer()
        self.content.clear_widgets()
        self.content.height = 0
        self._rows = []
        for n, line in enumerate(self._data):
            row = self._gen_row(line, n)
            self._rows.append(row)
            self.content.add_widget(row)
            self.content.height += row.height

    def on_row_select(self, gridrow):
        if self.on_select:
            datarow = self._data[gridrow]['_progrid_order']
            self.on_select(gridrow, datarow, self._data[gridrow])

    def on_row_double_tap(self, gridrow):
        if self.on_double_tap:
            datarow = self._data[gridrow]['_progrid_order']
            self.on_double_tap(gridrow, datarow, self._data[gridrow])

    def on_row_long_press(self, gridrow):
        if self.on_long_press:
            datarow = self._data[gridrow]['_progrid_order']
            self.on_long_press(gridrow, datarow, self._data[gridrow])

    def _gen_header(self):
        self.header.clear_widgets()
        args = self._build_header_args()
        first_col = True
        for column in self.columns:
            text = self.headers[column]
            text = text.encode('utf-8')
            text = ' ' + text if first_col else text
            lbl = ColumnHeader(text=text, meta=column, **args)
            first_col = False
            self.header.add_widget(lbl)
            self.___grid[column].append(lbl)

    def _gen_footer(self):
        lbl = BindedLabel(text=self.footer_text, halign=self.footer_text_halign, color=self.footer_text_color, font_size=self.footer_text_font_size)
        if self.footer_text_font_name:
            lbl.font_name = self.footer_text_font_name
        self.footer.add_widget(lbl)

    def _gen_row(self, line, n):
        b = RowLayout(height=self.row_height, orientation='horizontal', rowid=n, grid=self, padding=[
         self.padding_h, self.padding_v], background_color=self.content_background_color)
        args = self._build_content_args()
        first_col = True
        for column in self.columns:
            val = self._coltypes[column](line[column] if column in line.keys() else '')
            if self._coltypes[column] == bool:
                w = BoxLayout()
                c = CheckBox(active=val, size_hint=(None, 1), width=sp(32), **args)
                s = BoxLayout(size_hint=(1, 1))
                w.add_widget(c)
                w.add_widget(s)
            else:
                text = val if val not in ('None', 'None') else ''
                text = text.encode('utf-8')
                w = BindedLabel(text=text, **args)
            b.add_widget(w)
            first_col = False
            self.___grid[column].append(w)

        return b

    def _setup_data(self, data):
        if len(self.col_order) == 0:
            self.col_order = self.columns
        for i in range(len(self.data)):
            self.data[i]['_progrid_order'] = i

        self._data = []
        if len(data) > 0:
            self._all_columns = self.data[0].keys()
            self._data = filter(self._validate_line, data)
            if len(self.row_sorting) > 0:
                field, mode = self.row_sorting[0]
                reverse = False if mode == 'asc' else True
                self._data = sorted(self._data, key=lambda o: o[field], reverse=reverse)
        else:
            self.add_widget(Label(text=self.text_no_data, color=self.text_color))

    def _validate_line(self, line):
        for k in self.row_filters:
            if not self.row_filters[k](line[k]):
                return False

        return True

    def _raise_too_much_data(self, n):
        msg = "data_len_limit: %d - Len of data feed: %d\nYou've got this exception because you did feed too much data.\nYou can bypass this exception by changing the value of the data_len_limit property.\nBe aware of performance issues.\n" % (self.data_len_limit, n)
        raise ValueError(msg)

    def _build_dict(self, *args):
        result = {}
        for d in args:
            result.update(d)

        return result

    def _build_header_args(self):
        font_name = {'font_name': self.header_font_name} if self.header_font_name else {}
        font_size = {'font_size': self.header_font_size} if self.header_font_size else {}
        h_align = {'halign': self.header_align} if self.header_align else {}
        v_align = {'valign': 'middle'}
        color = {'color': self.text_color} if self.text_color else {}
        root_layout = {'root_layout': self}
        hover_color = {'hover_color': [0, 0, 1, 0.5]}
        grid = {'grid': self}
        return self._build_dict(v_align, h_align, font_name, font_size, color, root_layout, hover_color, grid)

    def _build_content_args(self):
        v_align = {'valign': 'middle'}
        font_name = {'font_name': self.content_font_name} if self.content_font_name else {}
        font_size = {'font_size': self.content_font_size} if self.content_font_size else {}
        h_align = {'halign': self.content_align} if self.content_align else {}
        color = {'color': self.text_color} if self.text_color else {}
        b_color = {'fill_color': self.content_background_color} if self.content_background_color else {}
        return self._build_dict(v_align, h_align, font_name, font_size, color, b_color)

    def on_column_resize(self, oldsize, newsize, column):
        print (
         oldsize, newsize, column)
        newwidth = newsize[0]
        for widget in self.___grid[column]:
            widget.width = newwidth
            widget.size_hint[0] = None

        return

    def _build_coltypes(self):
        columns = set(self.headers.keys()) - set(self.coltypes)
        self._coltypes = self.coltypes
        if len(self._data) > 0:
            line = self._data[0]
        else:
            line = [ '' for c in columns ]
        for column in columns:
            obj = line[column] if column in line.keys() else ''
            if isinstance(obj, bool):
                self._coltypes[column] = bool
            else:
                self._coltypes[column] = str

    def update_single_row(self, rowid, data):
        self.data[rowid] = data
        self.content.remove_widget(self._rows[rowid])
        self._rows[rowid] = self._gen_row(data, rowid)
        self.content.add_widget(self._rows[rowid], len(self.content.children))


class ProGridCustomizator(FloatingAction):
    """
    String properties to be translated eventually.
    """
    popup_title = StringProperty('Customize your grid')
    hint_filter = StringProperty('No filter')
    cannot_use_expression_for_field = StringProperty("\nCannot use filter for field %s.\nPress on '?' for more information.\n")
    filters_help = StringProperty('\nThree kind of filters are supported :\n\n  1) Simple text filter, for example, \'ar\' will match \'aron\' and \'mario\'.\n\n  2) Expressions starting comparison operators ( <, <=, =>, >, == and != ).\n  For example, \'> 14\' or \'== 0\'.\n\n  3) Expressions containing \'$VAL\'.\n  For example, \'$VAL == "M"\'.\n\nPlease quote ( \'\' ) any text in your filters.')
    grid = ObjectProperty(None)
    popup = ObjectProperty(None)

    def __init__(self, **kargs):
        super(ProGridCustomizator, self).__init__(icon=icon_settings_32, **kargs)
        self._help_popup = OkButtonPopup(text=self.filters_help)
        if 'grid' not in kargs.keys():
            raise ValueError('You need to provide a pointer to your grid using the "grid" parameter.')
        else:
            self.grid = kargs['grid']

    def exit_customizer(self, *args):
        self.popup.dismiss()

    def save_and_exit(self, *args):
        self._filter_error_occur = False
        self.grid.columns = self._get_columns()
        self.grid.row_filters, self.grid.row_filters_names = self._get_row_filters()
        if not self._filter_error_occur:
            self.exit_customizer()

    def _get_row_filters(self):
        filters = {}
        filters_names = {}
        comparators = ('< <= => > == != and or').split(' ')
        startswith = lambda v: expression.startswith(v)
        for column in self._columns.keys():
            chk, lbl, fil = self._columns[column]
            if len(fil.text.strip()) > 0:
                expression = fil.text.strip()
                if len(list(filter(startswith, comparators))) > 0:
                    foo = 'lambda VAL: %s' % ('_format_val(VAL) ' + expression)
                else:
                    if '$VAL' in expression:
                        foo = 'lambda VAL: %s' % expression.replace('$VAL', '_format_val(VAL)')
                    else:
                        foo = "lambda VAL: _format_val(VAL) == _format_val('" + expression + "')"
                    try:
                        filters[column] = eval(foo)
                        filters_names[column] = expression
                    except Exception as e:
                        AlertPopup(text=self.cannot_use_expression_for_field % lbl.text.lower()).open()
                        self._filter_error_occur = True
                        print e

        return (
         filters, filters_names)

    def _get_columns(self):
        columns = []
        for column in self._columns.keys():
            chk, lbl, fil = self._columns[column]
            if chk.active:
                columns.append(column)

        return sorted(columns, key=lambda o: self.grid.col_order.index(o))

    def customize(self):
        self.popup = FlatPopup(size_hint=(0.95, 0.7), title=self.popup_title, title_size=dp(20), title_color=[
         0, 0, 0, 0.8], content=self._build_content())
        self.popup.open()

    def _build_footer(self):
        footer = BoxLayout(orientation='horizontal', spacing=dp(10), size_hint=(1,
                                                                                None), height=dp(35))
        args = {'size_hint': (0.2, 1), 'color': [0, 0.59, 0.53, 1], 'color_down': [0, 0, 0, 0.7]}
        txt = '[ref=main][b]       ?       [/b][/ref]'
        lbl = Label(text=txt, markup=True, color=[0, 0, 0, 0.8], font_size=dp(18))
        lbl.bind(on_ref_press=self._help_popup.open)
        cancel_button = FlatButton(markup=True, text='Cancel', **args)
        cancel_button.bind(on_press=self.exit_customizer)
        ok_button = FlatButton(markup=True, text='[b]OK[/b]', **args)
        ok_button.bind(on_press=self.save_and_exit)
        footer.add_widget(lbl)
        footer.add_widget(cancel_button)
        footer.add_widget(ok_button)
        return footer

    def _build_content_row(self, column):
        row = BoxLayout(orientation='horizontal', size_hint=(1, None), height=dp(30))
        chk = CheckBox(active=column in self.grid.columns)
        fil = FlatTextInput(text=self.grid.row_filters_names[column] if column in self.grid.row_filters_names.keys() else '', hint_text=self.hint_filter, multiline=False, valign='middle')
        lbl = Label(text=self.grid.headers[column], color=[
         0, 0, 0, 0.8], halign='left', valign='middle')
        lbl.bind(size=lbl.setter('text_size'))
        row.add_widget(chk)
        row.add_widget(lbl)
        row.add_widget(fil)
        return (row, chk, lbl, fil)

    def _build_content(self):
        s = ScrollView()
        x = BoxLayout(orientation='vertical')
        content = GridLayout(cols=1, size_hint=(1, None))
        content.height = 0
        self._columns = {}
        for column in sorted(self.grid.headers.keys()):
            row, chk, lbl, fil = self._build_content_row(column)
            content.add_widget(row)
            content.height += row.height
            self._columns[column] = (chk, lbl, fil)

        s.add_widget(content)
        x.add_widget(s)
        x.add_widget(self._build_footer())
        return x


class ColumnHeader(ResizeableLabel):
    grid = ObjectProperty(None)

    def __init__(self, **kargs):
        super(ColumnHeader, self).__init__(**kargs)
        self.on_new_size = self.grid.on_column_resize


class RowLayout(ColorBoxLayout):
    rowid = NumericProperty(None)
    grid = ObjectProperty(None)

    def __init__(self, **kargs):
        super(RowLayout, self).__init__(**kargs)

    def _create_clock(self, touch):
        Clock.schedule_once(self.on_long_press, 0.5)

    def _delete_clock(self, touch):
        Clock.unschedule(self.on_long_press)

    def on_long_press(self, time):
        if self.grid:
            self.grid.on_row_long_press(self.rowid)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if touch.is_double_tap:
                return self.on_double_tap(touch)
            self._create_clock(touch)
            return self.grid.records_readonly or super(RowLayout, self).on_touch_down(touch)
        return False

    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos):
            self._delete_clock(touch)
            if self.grid:
                self.grid.on_row_select(self.rowid)
            return self.grid.records_readonly or super(RowLayout, self).on_touch_up(touch)
        return False

    def on_double_tap(self, touch):
        if self.grid:
            self.grid.on_row_double_tap(self.rowid)
        return self.grid.records_readonly


def _format_val(v):
    return str(v).lower()