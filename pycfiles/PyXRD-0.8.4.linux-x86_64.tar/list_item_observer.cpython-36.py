# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/mvc/observers/list_item_observer.py
# Compiled at: 2020-03-07 03:51:49
# Size of source mod 2**32: 2702 bytes
import weakref
from .base import Observer

class ListItemObserver(Observer):
    __doc__ = "\n        An observer that observes a single item in a list and informs us of changes.\n        The observed properties are defined in the list type's meta class by\n        setting their property descriptors 'tabular' attribute to True.\n    "
    _previous_model_ref = None

    @property
    def _previous_model(self):
        if self._previous_model_ref is not None:
            return self._previous_model_ref()
        else:
            return

    @_previous_model.setter
    def _previous_model(self, value):
        self._previous_model_ref = weakref.ref(value, self.clear)

    def __init__(self, on_changed, model=None, spurious=False):
        super(ListItemObserver, self).__init__(spurious=spurious)
        self.on_changed = on_changed
        self.observe_model(model)

    def observe_model(self, model):
        if self._previous_model is not None:
            self.relieve_model(self._previous_model)
        if model is not None:
            for prop_name, data_type in model.Meta.get_column_properties():
                self.observe((self.on_prop_mutation), prop_name, assign=True)

            self._previous_model = model
            super(ListItemObserver, self).observe_model(model)

    def clear(self, *args):
        self.on_changed = None
        if len(args) == 0:
            self.observe_model(None)

    def on_prop_mutation(self, model, prop_name, info):
        if callable(self.on_changed):
            self.on_changed(model)