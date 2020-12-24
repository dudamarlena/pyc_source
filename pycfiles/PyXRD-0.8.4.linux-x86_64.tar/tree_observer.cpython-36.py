# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/mvc/observers/tree_observer.py
# Compiled at: 2020-03-07 03:51:49
# Size of source mod 2**32: 2714 bytes
from .base import Observer

class TreeObserver(Observer):
    __doc__ = '\n        An observer that wraps the in-instance changes of a Tree made by\n        TreeNodes to on_inserted and on_deleted handlers.\n    '
    _deleted = []

    def __init__(self, on_inserted, on_deleted, prop_name, on_deleted_before=None, model=None, spurious=False):
        super(TreeObserver, self).__init__(spurious=spurious)
        self.on_inserted = on_inserted
        self.on_deleted = on_deleted
        self.on_deleted_before = on_deleted_before
        self.observe((self.on_prop_mutation_before), prop_name, before=True)
        self.observe((self.on_prop_mutation_after), prop_name, after=True)
        self.observe_model(model)

    def on_prop_mutation_before(self, model, prop_name, info):
        if info.method_name == 'on_grandchild_removed':
            self._deleted = [
             info.args[0]]
        else:
            if info.method_name == 'remove':
                self._deleted = [
                 info.args[0]]
            if callable(self.on_deleted_before):
                for old_item in self._deleted[::-1]:
                    self.on_deleted_before(old_item)

    def on_prop_mutation_after(self, model, prop_name, info):
        if callable(self.on_deleted):
            for old_item in self._deleted[::-1]:
                self.on_deleted(old_item)

            self._deleted = []
        else:
            if info.method_name == 'on_grandchild_removed':
                new_item = info.args[0]
                self.on_inserted(new_item)
            if info.method_name == 'insert':
                new_item = info.args[1]
                self.on_inserted(new_item)