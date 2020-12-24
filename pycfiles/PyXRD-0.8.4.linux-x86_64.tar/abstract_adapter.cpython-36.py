# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/mvc/adapters/abstract_adapter.py
# Compiled at: 2020-03-07 03:51:48
# Size of source mod 2**32: 5534 bytes
import logging
logger = logging.getLogger(__name__)
import weakref
from .metaclasses import MetaAdapter

class AbstractAdapter(object, metaclass=MetaAdapter):
    __doc__ = '\n        An semi-abstract class all Adapters have to derive from.\n    '
    widget_types = []
    _AbstractAdapter__prop = None

    @property
    def _prop(self):
        if callable(self._AbstractAdapter__prop):
            return self._AbstractAdapter__prop()
        else:
            return self._AbstractAdapter__prop

    @_prop.setter
    def _prop(self, value):
        if value is None:
            self._AbstractAdapter__prop = None
        else:
            self._AbstractAdapter__prop = weakref.ref(value, lambda : self.disconnect())

    _AbstractAdapter__controller = None

    @property
    def _controller(self):
        if callable(self._AbstractAdapter__controller):
            return self._AbstractAdapter__controller()
        else:
            return self._AbstractAdapter__controller

    @_controller.setter
    def _controller(self, value):
        if value is None:
            self._AbstractAdapter__controller = None
        else:
            self._AbstractAdapter__controller = weakref.ref(value, lambda c: self.disconnect())

    _AbstractAdapter__widget = None

    @property
    def _widget(self):
        if callable(self._AbstractAdapter__widget):
            return self._AbstractAdapter__widget()
        else:
            return self._AbstractAdapter__widget

    @_widget.setter
    def _widget(self, value):
        if value is None:
            self._AbstractAdapter__widget = None
        else:
            self._AbstractAdapter__widget = weakref.ref(value, lambda w: self.disconnect(widget=(w())))

    def __init__(self, controller, prop, widget, *args, **kwargs):
        (super(AbstractAdapter, self).__init__)(*args, **kwargs)
        self._prop = prop
        self._controller = controller
        self._widget = widget

    def update_model(self):
        """Forces the property to be updated from the value hold by
        the widget. This method should be called directly by the
        user in very unusual conditions."""
        self._write_property(self._read_widget())

    def update_widget(self):
        """Forces the widget to be updated from the property
        value. This method should be called directly by the user
        when the property is not observable, or in very unusual
        conditions."""
        self._write_widget(self._read_property())

    def disconnect(self, model=None, widget=None):
        """Disconnects the adapter from the model and the widget."""
        self._disconnect_model(model=model)
        self._disconnect_widget(widget=widget)

    def _connect_widget(self):
        raise NotImplementedError('Please Implement this method')

    def _disconnect_widget(self, widget=None):
        raise NotImplementedError('Please Implement this method')

    def _connect_model(self):
        raise NotImplementedError('Please Implement this method')

    def _disconnect_model(self, model=None):
        raise NotImplementedError('Please Implement this method')

    def _read_widget(self):
        raise NotImplementedError('Please Implement this method')

    def _write_widget(self, val):
        raise NotImplementedError('Please Implement this method')

    def _read_property(self, *args):
        raise NotImplementedError('Please Implement this method')

    def _write_property(self, value, *args):
        raise NotImplementedError('Please Implement this method')