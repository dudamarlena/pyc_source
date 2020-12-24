# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/mvc/adapters/gtk_support/treemodels/object_list_store.py
# Compiled at: 2020-03-07 03:51:49
# Size of source mod 2**32: 6069 bytes
import logging
logger = logging.getLogger(__name__)
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GObject
from ....observers import ListObserver, ListItemObserver
from .base_models import BaseObjectListStore
from weakref import WeakKeyDictionary

class ObjectListStore(BaseObjectListStore):
    __doc__ = '\n        GenericTreeModel implementation that wraps a python list of \n        mvc model objects. In addition, it expects all objects \n        to be of a certain type, which needs to be passed to the __init__ as \n        the first argument.This way, the wrapper can inspect the type and\n        find out what properties can be represented as columns and report this\n        to Gtk.\n    '
    _deleted_paths = None

    @property
    def _data(self):
        if self._model is not None:
            return getattr(self._model, self._prop_name, None)
        else:
            return []

    def is_wrapping(self, model, prop_name):
        return self._model == model and self._prop_name == prop_name

    def __init__(self, model, prop):
        BaseObjectListStore.__init__(self, prop.data_type)
        self._model = model
        self._prop_name = prop.label
        self._deleted_paths = []
        self._observer = ListObserver((self.on_item_inserted),
          (self.on_item_deleted), on_deleted_before=(self.on_item_deleted_before),
          prop_name=(self._prop_name),
          model=(self._model))
        self._list_item_observers = WeakKeyDictionary()
        for item in self._data:
            self._observe_item(item)

    def _observe_item(self, item):
        obs = ListItemObserver((self.on_item_changed), model=item)
        self._list_item_observers[item] = obs

    def _unobserve_item(self, item):
        observer = self._list_item_observers.get(item, None)
        if observer is not None:
            observer.clear()

    def on_item_changed(self, item):
        itr = self.create_tree_iter(item)
        path = self.get_path(itr)
        try:
            self.row_changed(path, itr)
        except TypeError as err:
            err.args += ('when emitting row_changed using:', path, itr)
            raise

    def on_item_inserted(self, item):
        try:
            itr = self.create_tree_iter(item)
            path = self.get_path(itr)
            self._observe_item(item)
            self.row_inserted(path, itr)
        except ValueError:
            logger.debug('Invalid rowref passed: %s', item)

    def on_item_deleted_before(self, item):
        self._unobserve_item(item)
        self._deleted_paths.append((self._data.index(item),))

    def on_item_deleted(self, item):
        for path in self._deleted_paths:
            self.row_deleted(path)

        self._deleted_paths = []

    def on_get_iter(self, path):
        try:
            return self._data[path[0]]
        except IndexError:
            return

    def on_get_path(self, rowref):
        try:
            return (
             self._data.index(rowref),)
        except ValueError:
            logger.exception('ValueError in on_get_path of %s caused by %s' % (self, rowref))

    def set_value(self, itr, column, value):
        user_data = self.get_user_data(itr)
        setattr(user_data, self._columns[column][0], value)
        self.row_changed(self.get_path(itr), itr)

    def on_get_value(self, rowref, column):
        value = getattr(rowref, self._columns[column][0])
        try:
            default = self._columns[column][1]()
        except TypeError:
            default = ''

        if value is not None:
            return value
        else:
            return default

    def on_iter_next(self, rowref):
        n, = self.on_get_path(rowref)
        try:
            return self._data[(n + 1)]
        except IndexError:
            pass

    def on_iter_children(self, rowref):
        if rowref:
            return
        if self._data:
            return self.on_get_iter((0, ))

    def on_iter_has_child(self, rowref):
        if rowref:
            return False
        else:
            if len(self._data) > 0:
                return True
            return False

    def on_iter_n_children(self, rowref):
        if rowref:
            return 0
        else:
            return len(self._data)

    def on_iter_nth_child(self, parent, n):
        if parent:
            return
        else:
            if n < 0 or n >= len(self._data):
                return
            return self._data[n]

    def on_iter_parent(self, rowref):
        pass


GObject.type_register(ObjectListStore)