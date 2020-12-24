# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/mvc/models/properties/signal_property.py
# Compiled at: 2020-03-07 03:51:49
# Size of source mod 2**32: 1901 bytes
from mvc.support.observables.signal import Signal
from .labeled_property import LabeledProperty

class SignalProperty(LabeledProperty):
    __doc__ = '\n    A descriptor for signals.\n    Expects a single additional keyword argument (or not for default of Signal):\n        - data_type: the type of signal to initialize this property with.\n    '
    data_type = Signal

    def _get(self, instance):
        signal = getattr(instance, self._get_private_label(), None)
        if signal is None:
            signal = self.data_type()
            setattr(instance, self._get_private_label(), signal)
        return signal

    def __set__(self, instance, value):
        raise AttributeError('Cannot set a Signal property!')