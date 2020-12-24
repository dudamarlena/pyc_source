# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/mvc/observers/dict_observer.py
# Compiled at: 2020-03-07 03:51:49
# Size of source mod 2**32: 2888 bytes
from .base import Observer

class DictObserver(Observer):
    __doc__ = '\n        An observer that wraps the in-instance changes of a dict to on_inserted\n        and on_deleted handlers.\n    '
    _deleted = []

    def __init__(self, on_inserted, on_deleted, prop_name, model=None, spurious=False):
        super(DictObserver, self).__init__(model=model, spurious=spurious)
        self.on_inserted = on_inserted
        self.on_deleted = on_deleted
        self.observe((self.on_prop_mutation_before), prop_name, before=True)
        self.observe((self.on_prop_mutation_after), prop_name, after=True)

    def on_prop_mutation_before(self, model, prop_name, info):
        if info.method_name in ('__setitem__', '__delitem__', 'pop', 'setdefault'):
            key = info.args[0]
            if key in info.instance:
                self._deleted.append(info.instance[key])
        else:
            if info.method_name == 'update':
                if len(info.args) == 1:
                    iterable = info.args[0]
                else:
                    if len(info.kwargs) > 0:
                        iterable = info.kwargs
                if hasattr(iterable, 'iteritems'):
                    iterable = iter(iterable.items())
                for key, value in iterable:
                    if key in info.instance:
                        self._deleted.append(info.instance[key])

            if info.method_name == 'clear':
                self._deleted.extend(list(info.instances.values()))

    def on_prop_mutation_after(self, model, prop_name, info):
        if self._deleted:
            for old_item in self._deleted:
                self.on_deleted(old_item)

            self._deleted = []
        if info.method_name == 'popitem':
            old_item = info.result[1]
            self.on_deleted(old_item)