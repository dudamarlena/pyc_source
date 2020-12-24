# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/mvc/observers/list_observer.py
# Compiled at: 2020-03-07 03:51:49
# Size of source mod 2**32: 3498 bytes
from .base import Observer
import types

class ListObserver(Observer):
    __doc__ = '\n        An observer that wraps the in-instance changes of a list to on_inserted\n        and on_deleted handlers.\n    '
    _deleted = []

    def __init__(self, on_inserted, on_deleted, prop_name, on_deleted_before=None, model=None, spurious=False):
        super(ListObserver, self).__init__(spurious=spurious)
        self.on_inserted = on_inserted
        self.on_deleted = on_deleted
        self.on_deleted_before = on_deleted_before
        self.observe((self.on_prop_mutation_before), prop_name, before=True)
        self.observe((self.on_prop_mutation_after), prop_name, after=True)
        self.observe_model(model)

    def on_prop_mutation_before(self, model, prop_name, info):
        if info.method_name in ('__setitem__', '__delitem__'):
            i = info.args[0]
            if isinstance(i, slice):
                self._deleted = info.instance[i]
            else:
                if i <= len(info.instance):
                    self._deleted = [
                     info.instance[i]]
            if info.method_name == 'pop':
                if len(info.instance) > 0:
                    self._deleted = [
                     info.instance[(-1)]]
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
            if info.method_name == '__setitem__':
                i = info.args[0]
                if type(i) is slice:
                    for item in info.instance[i]:
                        self.on_inserted(item)

                else:
                    new_item = info.args[1]
                    self.on_inserted(new_item)
            else:
                if info.method_name == 'append':
                    new_item = info.args[0]
                    self.on_inserted(new_item)
                if info.method_name == 'extend':
                    items = info.args[0]
                    for new_item in items:
                        self.on_inserted(new_item)

            if info.method_name == 'insert':
                new_item = info.args[1]
                self.on_inserted(new_item)