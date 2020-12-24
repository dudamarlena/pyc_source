# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/neox/commons/forms.py
# Compiled at: 2020-02-26 23:29:03
# Size of source mod 2**32: 8903 bytes
import locale
from PyQt5.QtWidgets import QLineEdit, QLabel, QComboBox, QGridLayout, QTextEdit, QTreeView, QCompleter
from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QRegExpValidator, QDoubleValidator
from neox.commons.qt_models import get_simple_model
from neox.commons.model import Modules
regex_ = QRegExp('^\\d{1,3}(([.]\\d{3})*),(\\d{2})$')
validator = QRegExpValidator(regex_)
try:
    locale.setlocale(locale.LC_ALL, str('es_CO.UTF-8'))
except:
    print('Warning: Error setting locale')

__all__ = ['Label', 'Field', 'ComboBox', 'GridForm', 'FieldMoney']

def set_object_name(obj, type_, value):
    size = 'small'
    color = 'gray'
    if value.get('size'):
        size = value.get('size')
    if value.get('color'):
        color = value.get('color')
    name = type_ + size + '_' + color
    obj.setObjectName(name)


class Completer(QCompleter):

    def __init__(self, parent, records, fields):
        super(Completer, self).__init__()
        self.parent = parent
        self.treeview_search = QTreeView()
        col_headers = self.treeview_search.header()
        col_headers.hide()
        self.setPopup(self.treeview_search)
        self.fields = fields
        self._set_model(records, fields)
        self.activated.connect(self.on_accept)
        self.setFilterMode(Qt.MatchContains)
        self.setCaseSensitivity(Qt.CaseInsensitive)
        self.setWrapAround(True)
        self.setCompletionColumn(1)
        self.treeview_search.setColumnWidth(1, 300)
        self.treeview_search.setColumnHidden(0, True)
        self.id = None

    def get_values(self, records):
        vkeys = [f[0] for f in self.fields]
        values = []
        for r in records:
            row = []
            for key in vkeys:
                row.append(r[key])

            values.append(row)

        return values

    def _set_model(self, records, headers):
        headers = [f[1] for f in self.fields]
        values = self.get_values(records)
        self.model = get_simple_model(self.parent, values, headers)
        self.setModel(self.model)

    def on_accept(self):
        model_index = self._get_model_index()
        idx = self.model.index(model_index.row(), 0)
        self.id = idx.data()

    def _get_model_index(self):
        item_view = self.popup()
        index = item_view.currentIndex()
        proxy_model = self.completionModel()
        model_index = proxy_model.mapToSource(index)
        return model_index


class Label(QLabel):

    def __init__(self, obj, key, value, align='right'):
        super(Label, self).__init__()
        self.setText(value['name'] + ':')
        set_object_name(self, 'label_', value)
        if align == 'left':
            self.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        else:
            self.setAlignment(Qt.AlignRight | Qt.AlignVCenter)


class Field(QLineEdit):

    def __init__(self, obj, key, value, type=None):
        super(Field, self).__init__()
        setattr(obj, 'field_' + key, self)
        self.parent = obj
        set_object_name(self, 'field_', value)
        if value.get('type') == 'numeric':
            self.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        else:
            if value.get('type') == 'relation':
                self.set_completer(value.get('model'), value.get('fields'), value.get('domain'))

    def set_completer(self, tryton_model, fields, domain=[]):
        records = tryton_model.find(domain)
        self.completer = Completer(self.parent, records, fields)
        self.setCompleter(self.completer)

    def get_id(self):
        return self.completer.id

    def _get_tryton_model(self, model, fields):
        modules = Modules(self, self.conn)
        modules.set_models([
         {'name':'_Model', 
          'model':model, 
          'fields':fields}])


class TextField(QTextEdit):

    def __init__(self, obj, key, value):
        super(Field, self).__init__()
        setattr(obj, 'field_' + key, self)
        set_object_name(self, 'field_', value)
        self.value_changed = False
        self.setValidator(validator)

    def textChanged(self, text):
        self.value_changed = True


class FieldMoney(QLineEdit):

    def __init__(self, obj, key, value, amount=None, digits=2, readonly=True):
        super(FieldMoney, self).__init__()
        setattr(obj, 'field_' + key, self)
        set_object_name(self, 'field_', value)
        self.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.digits = 2
        self.value_changed = False
        self.textEdited.connect(self.value_edited)
        self._text = '0'
        self.amount = 0
        self.setReadOnly(readonly)
        validator = QDoubleValidator()
        validator.setDecimals(2)
        self.setValidator(validator)
        if not amount:
            self.zero()

    def __str__(self):
        return self.format_text()

    def format_text(self, text_):
        amount = float(text_)
        return '{:,}'.format(round(amount, self.digits))

    def setText(self, amount):
        if not amount:
            text = ''
        else:
            text = self.format_text(amount)
        super(FieldMoney, self).setText(str(text))

    def zero(self):
        self.setText(str(0))

    def value_edited(self, amount):
        self.value_changed = True

    def show(self):
        pass


class ComboBox(QComboBox):

    def __init__(self, obj, key, data):
        super(ComboBox, self).__init__()
        setattr(obj, 'field_' + key, self)
        self.parent = obj
        self.setFrame(True)
        self.setObjectName('field_' + key)
        values = []
        if data.get('values'):
            values = data.get('values')
        heads = []
        if data.get('heads'):
            heads = data.get('heads')
        selection_model = get_simple_model(obj, values, heads)
        self.setModel(selection_model)
        self.setModelColumn(1)
        selection_model.findItems((str(3)), column=0)
        if data.get('on_change'):
            self.method_on_change = getattr(self.parent, data.get('on_change'))
            self.currentIndexChanged.connect(self.on_change)

    def on_change(self, index):
        self.method_on_change(index)

    def set_editable(self, value=True):
        self.setEditable(value)

    def set_enabled(self, value=True):
        self.setEnabled(value)

    def get_id(self):
        model = self.model()
        row = self.currentIndex()
        column = 0
        res = model.item(row, column)
        return res.text()

    def get_label(self):
        model = self.model()
        row = self.currentIndex()
        column = 1
        res = model.item(row, column)
        return res.text()

    def set_from_id(self, id_):
        model = self.model()
        items = model.findItems((str(id_)), column=0)
        idx = model.indexFromItem(items[0])
        self.setCurrentIndex(idx.row())


class GridForm(QGridLayout):
    __doc__ = "\n    Add a simple form Grid Style to screen,\n    from a data dict with set of {values, attributes}\n    example:\n        (field_name, {\n            'name': string descriptor,\n            'readonly': Bool,\n            'type': type_widget,\n            'placeholder': True or False,\n        }),\n    col:: is number of columns\n    type_widget :: field or selection\n    "

    def __init__(self, obj, values, col=1):
        super(GridForm, self).__init__()
        row = 1
        cols = 0
        align = 'right'
        if col == 0:
            align = 'left'
        for key, value in list(values.items()):
            if not value.get('placeholder'):
                _label = Label(obj, key, value, align)
            if value.get('type') == 'selection':
                _field = ComboBox(obj, key, value)
            else:
                if value.get('type') == 'money':
                    _field = FieldMoney(obj, key, value)
                else:
                    _field = Field(obj, key, value)
                    if value.get('password') is True:
                        _field.setEchoMode(QLineEdit.Password)
                    else:
                        if value.get('placeholder'):
                            _field.setPlaceholderText(value['name'])
                        else:
                            self.setRowStretch(row, 0)
                            column1 = cols * col + 1
                            column2 = column1 + 1
                            if value.get('invisible') is True:
                                continue
                            value.get('placeholder') or self.addWidget(_label, row, column1)
                        if col == 0:
                            row = row + 1
                            self.addWidget(_field, row, column1)
                        else:
                            self.addWidget(_field, row, column2)
                    if value.get('readonly') is True:
                        _field.setReadOnly(True)
                        _field.setFocusPolicy(Qt.NoFocus)
            if cols < col - 1:
                cols += 1
            else:
                row += 1
                cols = 0