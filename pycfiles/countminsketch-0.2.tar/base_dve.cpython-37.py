# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/countmemaybe/base_dve.py
# Compiled at: 2019-12-09 06:49:28
# Size of source mod 2**32: 716 bytes
__doc__ = "\nBase functions for all DVE's in the package\n\nmicha gorelick, mynameisfiber@gmail.com\nhttp://micha.gd/\n"
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