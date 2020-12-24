# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\chirp\compare\base_storage.py
# Compiled at: 2013-12-11 23:17:46
__doc__ = "\nBase class for storage systems.  The storage classes serve two\nfunctions.  The primary purpose is to provide a mechanism for storing\ncomparison results.  The secondary purpose is to provide a list of\nsignals that will be compared.  It's convenient to link these because\nRDBMS-based backends will typically use an integer ID to index signals\nand the comparisons between pairs of signals.\n\nCopyright (C) 2012 Daniel Meliza <dmeliza@dylan.uchicago.edu>\nCreated 2012-02-16\n"

class base_storage(object):

    def __init__(self, comparator):
        self.file_pattern = comparator.file_extension
        self.compare_stat_fields = comparator.compare_stat_fields
        self.symmetric = comparator.symmetric

    @property
    def nsignals(self):
        """ The number of signals stored in the object """
        return len(self.signals)

    def pairs(self):
        """ Yields the keys for the pairs of signals to be compared """
        from itertools import product
        items = [ k for k, v in self.signals ]
        if self.symmetric:
            for i, v1 in enumerate(items):
                for v2 in items[i:]:
                    yield (v1, v2)

        else:
            for v1, v2 in product(items, items):
                yield (v1, v2)