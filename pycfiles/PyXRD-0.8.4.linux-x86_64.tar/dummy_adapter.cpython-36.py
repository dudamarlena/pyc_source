# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/mvc/adapters/dummy_adapter.py
# Compiled at: 2020-03-07 03:51:48
# Size of source mod 2**32: 1963 bytes
from .abstract_adapter import AbstractAdapter

class DummyAdapter(AbstractAdapter):
    __doc__ = '\n        An adapter that does nothing. Really nothing.\n    '

    def __init__(self, controller=None, prop=None, widget=None):
        super(DummyAdapter, self).__init__(controller, prop, widget)

    def _connect_widget(self):
        pass

    def _disconnect_widget(self, widget=None):
        pass

    def _connect_model(self):
        pass

    def _disconnect_model(self, model=None):
        pass

    def _read_widget(self):
        pass

    def _write_widget(self, val):
        pass

    def _read_property(self, *args):
        pass

    def _write_property(self, value, *args):
        pass