# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyxrd/generic/gtk_tools/dummy_gtk.py
# Compiled at: 2020-03-07 03:51:50
# Size of source mod 2**32: 2123 bytes
from mvc.support.utils import get_new_uuid
__all__ = [
 'gobject',
 'GtkTreeIter',
 'GenericTreeModelTREE_MODEL_LIST_ONLY']
TREE_MODEL_LIST_ONLY = 0
TREE_MODEL_ITERS_PERSIST = 0
events_pending = lambda : False

class GtkTreeIter:

    def __init__(self, user_data, path=None):
        self.user_data = user_data
        self.path = path


class GenericTreeModel(object):
    __connected_signals__ = None

    def __init__(self):
        self.__connected_signals__ = {}

    def connect(self, signal_name, handler, *args):
        handlers = self.__connected_signals__.get(signal_name, {})
        handler_id = get_new_uuid()
        handlers[handler_id] = (handler, args)
        self.__connected_signals__[signal_name] = handlers
        return handler_id

    def disconnect(self, signal_name, handler_id):
        try:
            handlers = self.__connected_signals__.get(signal_name, {})
            del handlers[handler_id]
        except KeyError:
            pass

    def emit(self, signal_name, args=()):
        handlers = self.__connected_signals__.get(signal_name, {})
        for id, (handler, user_args) in handlers.items():
            handler(self, *(args,) + user_args)

    def set_property(self, *args, **kwargs):
        pass

    def create_tree_iter(self, user_data):
        return GtkTreeIter(user_data)

    def get_path(self, itr):
        return self.on_get_path(itr.user_data)

    def get_iter(self, path):
        return self.create_tree_iter(self.on_get_iter(path))

    def row_inserted(self, path, itr):
        self.emit('row-inserted', (path, itr))

    def row_deleted(self, indeces):
        self.emit('row-deleted', (indeces,))

    def invalidate_iters(self):
        pass

    def iter_is_valid(self, itr):
        return True

    def __len__(self):
        return len(self._model_data)