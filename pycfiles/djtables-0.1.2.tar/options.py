# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/adammck/projects/djtables/example/djtables/options.py
# Compiled at: 2010-08-05 02:56:47
from django.core.paginator import Paginator
from .row import Row
from .cell import Cell

class Options(object):
    _defaults = {}

    def __init__(self, options=None, **kwargs):
        options = options is not None and options.__dict__.copy() or {}
        options.update(kwargs)
        for key in options.keys():
            if not key.startswith('_'):
                value = options.pop(key)
                setattr(self, key, value)

        for key, value in self._defaults.items():
            if not hasattr(self, key):
                setattr(self, key, value)

        return

    def __setattr__(self, name, value):
        if name in self._defaults:
            object.__setattr__(self, name, value)
        else:
            raise AttributeError('Invalid option: %s' % name)

    def fork(self, **kwargs):
        return self.__class__(self, **kwargs)


class TableOptions(Options):
    _defaults = {'paginator_class': Paginator, 
       'row_class': Row, 
       'cell_class': Cell, 
       'prefix': '', 
       'order_by': None, 
       'per_page': 20, 
       'page': 1, 
       'template': 'djtables/table.html', 
       'columns': []}