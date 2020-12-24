# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/mvc/adapters/gtk_support/treemodels/object_tree_store.py
# Compiled at: 2020-03-07 03:51:49
# Size of source mod 2**32: 6090 bytes
from traceback import print_exc
import logging
logger = logging.getLogger(__name__)
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject
from .base_models import BaseObjectListStore
from ....observers import TreeObserver

class ObjectTreeStore(BaseObjectListStore):
    __doc__ = '\n        GenericTreeModel implementation that holds a tree with objects.\n        It expects all objects to be of a certain type, which needs to be\n        passed to the __init__ as the first argument. \n    '
    _object_node_map = None

    @property
    def _root_node(self):
        return getattr(self._model, self._prop_name, None)

    def is_wrapping(self, model, prop_name):
        return self._model == model and self._prop_name == prop_name

    def __init__(self, model, prop):
        _root = getattr(model, prop.label, None)
        try:
            BaseObjectListStore.__init__(self, prop.data_type)
        except ValueError as err:
            msg = "ValueError (%r) was raised when initializing ObjectTreeStore for model '%s' and data type '%s'" % (err, model, prop.data_type)
            msg += "\n Did you forget to set the data_type on the list property '%s'?" % prop.label
            raise ValueError(msg)

        self._model = model
        self._prop_name = prop.label
        self._object_node_map = dict()
        self._observer = TreeObserver((self.on_item_inserted),
          (self.on_item_deleted), on_deleted_before=(self.on_item_deleted_before),
          prop_name=(self._prop_name),
          model=(self._model))

    def on_item_inserted(self, item):
        try:
            itr = self.create_tree_iter(item)
            path = self.get_path(itr)
            self.row_inserted(path, itr)
        except ValueError:
            logger.debug('Invalid rowref passed: %s', item)

    _deleted_paths = []

    def on_item_deleted_before(self, item):
        self._deleted_paths.append(self.on_get_path(item))

    def on_item_deleted(self, item):
        for path in self._deleted_paths:
            self.row_deleted(path)

        self._deleted_paths = []

    def on_get_flags(self):
        return Gtk.TreeModelFlags.ITERS_PERSIST

    def on_get_iter(self, path):
        try:
            if hasattr(path, 'split'):
                path = list(map(int, path.split(':')))
            return (self._root_node.get_child_node)(*path)
        except IndexError as err:
            err.args = 'IndexError in on_get_iter of %s caused by %s' % (self, path)
            print_exc()
            return

    def on_get_path(self, node):
        try:
            return ':'.join(map(str, node.get_indices()))
        except ValueError as err:
            err.args = 'ValueError in on_get_path of %s caused by %s' % (self, node)
            print_exc()
            return

    def set_value(self, itr, column, value):
        user_data = self.get_tree_node_object(itr)
        setattr(user_data, self._columns[column][0], value)
        self.row_changed(self.get_path(itr), itr)

    def on_get_value(self, node, column):
        try:
            return getattr(node.object, self._columns[column][0])
        except:
            return ''

    def on_iter_next(self, node):
        return node.get_next_node()

    def on_iter_children(self, node):
        node = node or self._root_node
        return node.get_first_child_node()

    def on_iter_has_child(self, node):
        node = node or self._root_node
        return node.has_children

    def on_iter_n_children(self, node):
        node = node or self._root_node
        return node.child_count

    def on_iter_nth_child(self, parent, n):
        node = parent or self._root_node
        try:
            return node.get_child_node(n)
        except:
            return

    def on_iter_parent(self, node):
        return node.parent

    def iter_objects(self):
        for node in self._root_node.iter_children():
            yield node.object

    def get_tree_node(self, itr):
        return BaseObjectListStore.get_user_data(self, itr)

    def get_tree_node_from_path(self, path):
        return BaseObjectListStore.get_user_data_from_path(self, path)

    def get_tree_node_object(self, itr):
        return self.get_tree_node(itr).object

    def get_tree_node_object_from_path(self, path):
        return self.get_tree_node_from_path(path).object


GObject.type_register(ObjectTreeStore)