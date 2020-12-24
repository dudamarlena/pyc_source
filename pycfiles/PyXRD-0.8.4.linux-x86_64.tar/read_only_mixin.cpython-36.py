# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/mvc/models/properties/read_only_mixin.py
# Compiled at: 2020-03-07 03:51:49
# Size of source mod 2**32: 1460 bytes
from warnings import warn

class ReadOnlyMixin(object):
    __doc__ = '\n    A descriptor mixin that will make the property read only and raise a\n    warning whenever somebody tries to set the property.\n    '

    def __set__(self, instance, value):
        warn('The `%s` property can not be set!' % self.label, RuntimeWarning)