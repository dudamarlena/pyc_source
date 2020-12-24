# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/neox/commons/model.py
# Compiled at: 2020-02-26 23:29:02
# Size of source mod 2**32: 7543 bytes
from PyQt5.QtCore import Qt, QAbstractTableModel, QModelIndex
__all__ = [
 'Modules', 'TableModel', 'TrytonModel']

class Modules(object):
    __doc__ = 'Load/Set target modules on context of mainwindow'

    def __init__(self, parent=None, connection=None):
        self.parent = parent
        self.conn = connection

    def set_models(self, mdict):
        for val in mdict:
            if val:
                model = TrytonModel(self.conn, val['model'], val['fields'], val.get('methods'))
                setattr(self.parent, val['name'], model)

    def set_model(self, mdict):
        model = TrytonModel(self.conn, mdict['model'], mdict['fields'], mdict.get('methods'))
        return model

    def permission_delete(self, target, ctx_groups):
        """ Check if the user has permissions for delete records """
        model_data = TrytonModel(self.conn, 'ir.model', ('values', 'fs_id'), [])
        groups_ids = model_data.setDomain([
         (
          'fs_id', '=', target)])
        if groups_ids:
            group_id = eval(groups_ids[0]['values'])[0][1]
            if group_id in ctx_groups:
                return True
        return False


class TableModel(QAbstractTableModel):

    def __init__(self, model, fields):
        super(TableModel, self).__init__()
        self._fields = fields
        self.model = model
        self._data = []

    def reset(self):
        self.beginResetModel()
        self._data = []
        self.endResetModel()

    def add_record(self, rec):
        length = len(self._data)
        self.beginInsertRows(QModelIndex(), length, length)
        self._data.append(rec)
        self.endInsertRows()
        return rec

    def get_id(self):
        pass

    def removeId(self, row, mdl_idx):
        self.beginRemoveRows(mdl_idx, row, row)
        id_ = self._data[row].get('id')
        self._data.pop(row)
        self.endRemoveRows()
        return id_

    def deleteRecords(self, ids):
        pass

    def rowCount(self, parent=None):
        return len(self._data)

    def columnCount(self, parent=None):
        return len(self._fields)

    def get_data(self, index):
        raw_value = self._data[index.row()]
        return raw_value

    def data(self, index, role, field_name='name'):
        field = self._fields[index.column()]
        if role == Qt.DisplayRole:
            index_row = self._data[index.row()]
            if not index_row.get(field.get(field_name)):
                return
            raw_value = index_row[field[field_name]]
            digits = None
            if field.get('digits'):
                digits = 0
                target_field = field.get('digits')[0]
                if index_row.get(target_field):
                    target = index_row[target_field]
                    group_digits = field.get('digits')[1]
                    if group_digits.get(target):
                        digits = group_digits.get(target)
            if not raw_value:
                return
            if field.get('format'):
                field_format = field['format']
                if digits or digits == 0:
                    field_format = field['format'] % str(digits)
                if isinstance(raw_value, str):
                    raw_value = float(raw_value)
                fmt_value = field_format.format(raw_value)
            else:
                fmt_value = raw_value
            return fmt_value
        if role == Qt.TextAlignmentRole:
            align = Qt.AlignmentFlag(Qt.AlignVCenter | field['align'])
            return align
        return

    def get_sum(self, field_target):
        res = sum([d[field_target] for d in self._data])
        return res

    def update_record(self, rec, pos=None):
        if pos is None:
            pos = 0
            for d in self._data:
                if d['id'] == rec['id']:
                    break
                pos += 1

        self._data.pop(pos)
        self._data.insert(pos, rec)
        start_pos = self.index(pos, 0)
        end_pos = self.index(pos, len(self._fields) - 1)
        self.dataChanged.emit(start_pos, end_pos)
        return rec

    def headerData(self, section, orientation, role):
        """ Set the headers to be displayed. """
        if role != Qt.DisplayRole:
            return
        elements = [f['description'] for f in self._fields]
        if orientation == Qt.Horizontal:
            for i in range(len(elements)):
                if section == i:
                    return elements[i]


class TrytonModel(object):
    __doc__ = 'Model interface for Tryton'

    def __init__(self, connection, model, fields, methods=None):
        self._fields = fields
        self._methods = methods
        self._proxy = connection.get_proxy(model)
        self._context = connection.context
        self._data = []
        if self._methods:
            self.setMethods()

    def setFields(self, fields):
        self._fields = fields

    def setMethods(self):
        for name in self._methods:
            if not hasattr(self._proxy, name):
                continue
            setattr(self, name, getattr(self._proxy, name))

    def find(self, domain, limit=None, order=None, context=None):
        if context:
            self._context.update(context)
        return self._setDomain(domain, limit, order)

    def _setDomain(self, domain, limit=None, order=None):
        if domain:
            if isinstance(domain[0], int):
                operator = 'in'
                operand = domain
                if len(domain) == 1:
                    operator = '='
                    operand = domain[0]
                domain = [
                 (
                  'id', operator, operand)]
        if not order:
            order = [
             ('id', 'ASC')]
        self._data = self._search_read(domain, fields_names=(self._fields),
          limit=limit,
          order=order)
        return self._data

    def _search_read(self, domain, offset=0, limit=None, order=None, fields_names=None):
        if order:
            ids = self._proxy.search(domain, offset, limit, order, self._context)
            records = self._proxy.read(ids, fields_names, self._context)
            rec_dict = {}
            for rec in records:
                rec_dict[rec['id']] = rec

            res = []
            for id_ in ids:
                res.append(rec_dict[id_])

        else:
            res = self._proxy.search_read(domain, offset, limit, order, fields_names, self._context)
        return res

    def read(self, ids, fields_names=None):
        records = self._proxy.read(ids, fields_names, self._context)
        return records

    def _search(self, domain, offset=0, limit=None, order=None):
        pass

    def deleteRecords(self, ids):
        self._proxy.delete(ids, self._context)

    def getRecord(self, id_):
        records = self.setDomain([('id', '=', id_)])
        if records:
            return records[0]

    def update(self, id, pos=False):
        rec, = self._search_read([('id', '=', id)], fields_names=[x['name'] for x in self._fields])
        return rec

    def create(self, values):
        records = self._proxy.create([values], self._context)
        return records[0]

    def write(self, ids, values):
        self._proxy.write(ids, values, self._context)

    def method(self, name):
        print(('Se ejecuta este metodo...', name))
        return getattr(self._proxy, name)