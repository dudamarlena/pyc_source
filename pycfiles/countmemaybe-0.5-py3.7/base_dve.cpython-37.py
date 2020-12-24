# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/countmemaybe/base_dve.py
# Compiled at: 2019-12-09 06:49:28
# Size of source mod 2**32: 716 bytes
"""
Base functions for all DVE's in the package

micha gorelick, mynameisfiber@gmail.com
http://micha.gd/
"""
import mmh3

class BaseDVE(object):
    hasher = mmh3.hash

    def add(self, item):
        raise NotImplemented

    def cardinality(self):
        raise NotImplemented

    def cardinality_union(self):
        raise NotImplemented

    def cardinality_intersection(self):
        raise NotImplemented

    def relative_error(self):
        raise NotImplemented

    def __add__(self, item):
        self.add(item)
        return self

    def update(self, items):
        for item in items:
            self.add(item)

    def __len__(self):
        return self.cardinality()