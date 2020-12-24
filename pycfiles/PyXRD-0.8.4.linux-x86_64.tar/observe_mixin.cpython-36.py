# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/mvc/models/properties/observe_mixin.py
# Compiled at: 2020-03-07 03:51:49
# Size of source mod 2**32: 1768 bytes


class ObserveMixin(object):
    __doc__ = '\n    A descriptor mixin that will make the instance observe and relieve the\n    objects set.\n    '

    def __relieve_old(self, instance, old, new):
        if old is not None:
            instance.relieve_model(old)

    def __observe_new(self, instance, old, new):
        if new is not None:
            instance.observe_model(new)

    def _set(self, instance, value):
        old = getattr(instance, self.label)
        if old != value:
            self._ObserveMixin__relieve_old(instance, old, value)
            super(ObserveMixin, self)._set(instance, value)
            self._ObserveMixin__observe_new(instance, old, value)