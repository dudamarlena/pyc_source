# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sage/fatedoc/FATE/federatedml/param/pearson_param.py
# Compiled at: 2020-04-29 05:13:12
# Size of source mod 2**32: 2101 bytes
from federatedml.param.base_param import BaseParam

class PearsonParam(BaseParam):

    def __init__(self, column_names=None, column_indexes=None):
        super().__init__()
        self.column_names = column_names
        self.column_indexes = column_indexes
        if column_names is None:
            self.column_names = []
        if column_indexes is None:
            self.column_indexes = []

    def check(self):
        if not isinstance(self.column_names, list):
            raise ValueError(f"type mismatch, column_names with type {type(self.column_names)}")
        else:
            for name in self.column_names:
                if not isinstance(name, str):
                    raise ValueError(f"type mismatch, column_names with element {name}(type is {type(name)})")

            if isinstance(self.column_indexes, list):
                for idx in self.column_indexes:
                    if not isinstance(idx, int):
                        raise ValueError(f"type mismatch, column_indexes with element {idx}(type is {type(idx)})")

            if isinstance(self.column_indexes, int):
                if self.column_indexes != -1:
                    raise ValueError(f"column_indexes with type int and value {self.column_indexes}(only -1 allowed)")
            if isinstance(self.column_indexes, list):
                if isinstance(self.column_names, list):
                    if len(self.column_indexes) == 0 and len(self.column_names) == 0:
                        raise ValueError('provide at least one column')