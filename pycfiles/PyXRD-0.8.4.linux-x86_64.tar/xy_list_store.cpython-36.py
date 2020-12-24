# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/mvc/adapters/gtk_support/treemodels/xy_list_store.py
# Compiled at: 2020-03-07 03:51:49
# Size of source mod 2**32: 7627 bytes
from collections import namedtuple
from ....observers import Observer
from ....models.xydata import XYData
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib, GObject
from .base_models import BaseObjectListStore

class PointMeta:

    @classmethod
    def get_column_properties(cls):
        return [
         (
          'x', float),
         (
          'y', float)]


Point = namedtuple('Point', ['x', 'y'])
Point.Meta = PointMeta

class XYListStore(BaseObjectListStore, Observer):
    __doc__ = '\n        GenericTreeModel implementation that wraps an XYData model.\n    '
    _model = None
    _prop_name = None
    _last_lenght = 0
    __gsignals__ = {'columns-changed': (GObject.SignalFlags.RUN_LAST, None, ())}

    @property
    def _data(self):
        return getattr(self._model, self._prop_name, None)

    def is_wrapping(self, model, prop_name):
        return self._model == model and self._prop_name == prop_name

    def __init__(self, model, prop):
        BaseObjectListStore.__init__(self, Point)
        self._flush()
        self._model = model
        self._prop_name = prop.label
        _data = getattr(self._model, self._prop_name, None)
        assert isinstance(_data, XYData), 'Can only wrap XYData (or subclasses) instances to a XYListStore,' + "but got '%s' instead from property '%s' on model '%s'." % (
         _data, self._prop_name, self._model)
        Observer.__init__(self, model=(self._data))
        self.set_property('leak-references', False)
        self._last_length = len(self)
        self._last_num_col = self._data.num_columns
        self._emit_update()

    @Observer.observe('data_changed', signal=True)
    def on_data_changed(self, model, name, info):
        if model == self._data:
            self._emit_update()

    def _emit_update(self):
        self._schedule_flush()
        if self._last_num_col != self._data.num_columns:
            self.emit('columns-changed')
            self._last_num_col = self._data.num_columns
        row_diff = len(self._data) - self._last_length
        if row_diff > 0:
            for i in range(self._last_length, self._last_length + row_diff, 1):
                path = self.on_get_path(i)
                itr = self.get_iter(path)
                self.row_inserted(path, itr)

        else:
            if row_diff < 0:
                for i in range(self._last_length, self._last_length + row_diff - 1, -1):
                    path = self.on_get_path(i)
                    self.row_deleted(path)

        self._last_length = len(self._data)
        for i in range(0, len(self._data)):
            path = self.on_get_path(i)
            itr = self.get_iter(path)
            self.row_changed(path, itr)

    def on_get_flags(self):
        return Gtk.TreeModelFlags.LIST_ONLY

    def on_get_iter(self, path):
        if hasattr(path, 'get_indices'):
            path = path.get_indices()
        sp = ':'.join(map(lambda i: '%d' % i, path))
        if sp not in self._cache:
            try:
                i = path[0]
                if i >= 0:
                    if i < len(self):
                        self._cache[sp] = [
                         i]
            except IndexError:
                pass

        return self._cache.get(sp, None)

    def _schedule_flush(self):
        if not self._flush_scheduled:

            def idle_add():
                GLib.idle_add(self._flush)
                return False

            GLib.timeout_add(500, idle_add)
            self._flush_scheduled = True

    def _flush(self):
        self.invalidate_iters()
        self._cache = {}
        self._flush_scheduled = False
        return False

    def on_get_value(self, rowref, column):
        if column == self.c_x:
            return self._data.data_x[rowref[0]]
        if column >= self.c_y:
            return self._data.data_y[(rowref[0], column - 1)]
        raise AttributeError

    def on_get_path(self, rowref):
        if rowref is None:
            return
        else:
            if isinstance(rowref, tuple):
                return rowref
            if isinstance(rowref, list):
                return tuple(rowref)
            return (rowref,)

    def on_iter_next(self, rowref):
        if rowref is not None:
            itr = self.on_get_iter((rowref[0] + 1,))
            return itr
        else:
            return

    def on_iter_children(self, rowref):
        if rowref is not None:
            return
        if len(self) > 0:
            return self.on_get_iter((0, ))

    def on_iter_has_child(self, rowref):
        if rowref is not None:
            return False
        else:
            if len(self) > 0:
                return True
            return False

    def on_iter_n_children(self, rowref):
        if rowref is not None:
            return 0
        else:
            return len(self)

    def on_iter_nth_child(self, rowref, n):
        if rowref is not None:
            return
        else:
            if n < 0 or n >= len(self):
                return
            return self.on_get_iter((n,))

    def on_iter_parent(self, rowref):
        pass

    def on_get_n_columns(self):
        return self._data.num_columns

    def on_get_column_type(self, index):
        return float

    def __len__(self):
        return self._data.size


GObject.type_register(XYListStore)