# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/mvc/adapters/model_adapter.py
# Compiled at: 2020-03-07 03:51:49
# Size of source mod 2**32: 8301 bytes
from contextlib import contextmanager
from ..support.utils import not_none
from ..observers import Observer
from ..models import Model
from ..models.properties import LabeledProperty
from .abstract_adapter import AbstractAdapter

class ModelAdapter(Observer, AbstractAdapter):
    __doc__ = '\n        Model-side implementation of the _AbstractAdapter interface.\n    '
    _prop_read = None
    _prop_write = None
    _value_error = None

    @property
    def property_name(self):
        """Returns the property name the adapter is connected to"""
        return self._prop.label

    _ignoring_notifs = False

    @contextmanager
    def _ignore_notifications(self):
        """Context manager to temporarily (and exception-safe) ignore
        property changed notifications (e.g. when we're setting the model
        from the widget and vice versa)"""
        self._ignoring_notifs = True
        yield
        self._ignoring_notifs = False

    def __init__(self, *args, **kwargs):
        controller = args[0]
        prop = args[1]
        widget = args[2]
        prop_read = kwargs.pop('prop_read', None)
        prop_write = kwargs.pop('prop_write', None)
        value_error = kwargs.pop('value_error', None)
        spurious = kwargs.get('spurious', False)
        prop, self._model = self._parse_prop(prop, controller.model)
        (super(ModelAdapter, self).__init__)(*args, **kwargs)
        self._prop_read = not_none(prop_read, self._prop_read)
        self._prop_write = not_none(prop_write, self._prop_write)
        self._value_error = not_none(value_error, self._value_error)
        self._connect_model()

    def _parse_prop(self, prop, model):
        """Parses (optional) prop strings for the given model"""
        if not isinstance(prop, LabeledProperty):
            parts = prop.split('.')
            if len(parts) > 1:
                models = parts[:-1]
                for name in models:
                    model = getattr(model, name)
                    if not isinstance(model, Model):
                        raise TypeError("Attribute '%s' was expected to be a " + "Model, but found: '%s'" % (name, model))

                prop = getattr(type(model), parts[(-1)])
            else:
                prop = parts[0]
        return (
         prop, model)

    def _connect_model(self):
        """Used internally to connect the property into the model, and
        register self as a value observer for that property"""
        if not hasattr(self._model, self._prop.label):
            raise ValueError("Attribute '" + self._prop.label + "' not found in model " + str(self._model))
        if self._prop.observable:
            self.observe((self._on_prop_changed), (self._prop.label), assign=True)
            self.observe_model(self._model)

    def _on_prop_changed(self, *args, **kwargs):
        """Called by the observation code, when the value in the
        observed property is changed"""
        if not self._ignoring_notifs:
            self.update_widget()

    def _disconnect_model(self, model=None):
        model = not_none(self._model, model)
        if model is not None:
            self.relieve_model(self._model)
            self._model = None

    def _get_property_value(self):
        """Private method that returns the property value currently stored
        in the model, without transformations."""
        return getattr(self._model, self._prop.label)

    def _set_property_value(self, val):
        """Private method that sets the property value stored in the model,
        without transformations."""
        return setattr(self._model, self._prop.label, val)

    def _read_property(self, *args):
        """Returns the (possibly transformed) property value stored in the 
        model"""
        if self._prop_read:
            return self._prop_read((self._get_property_value)(*args))
        else:
            return (self._get_property_value)(*args)

    def _write_property(self, value, *args):
        """Sets the value of property. The given value is transformed
        using the prop_write function passed to the constructor.
        An attempt at casting the value to the property type is also made."""
        raw_value = value
        try:
            if self._prop_write:
                value = self._prop_write(value)
            with self._ignore_notifications():
                (self._set_property_value)(value, *args)
        except ValueError:
            if self._value_error:
                self._value_error(self, self._prop.label, raw_value)
            else:
                raise