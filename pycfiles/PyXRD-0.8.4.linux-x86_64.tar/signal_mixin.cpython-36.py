# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/mvc/models/properties/signal_mixin.py
# Compiled at: 2020-03-07 03:51:49
# Size of source mod 2**32: 2368 bytes
from mvc.support.utils import rec_getattr
from mvc.support import observables

class SignalMixin(object):
    __doc__ = '\n    A descriptor mixin that will invoke a signal on the instance\n    owning this property when set. \n    \n    Expects two more keyword arguments to be passed to the property constructor:\n        - signal_name: a dotted string describing where to get the signal object\n          from the instance\n    '
    signal_name = 'data_changed'

    def __set__(self, instance, value):
        signal = rec_getattr(instance, self.signal_name, None)
        if signal is not None:
            old = getattr(instance, self.label)
            with signal.ignore():
                super(SignalMixin, self).__set__(instance, value)
            new = getattr(instance, self.label)
            if isinstance(old, observables.ObsWrapperBase) or old != new:
                signal.emit()
        else:
            super(SignalMixin, self).__set__(instance, value)