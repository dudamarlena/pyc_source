# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/kdsearch/__init__.py
# Compiled at: 2017-03-03 07:35:05
# Size of source mod 2**32: 428 bytes
"""Search k-dimensional datasets efficiently using KDTrees 
"""
from . import kdtree
from . import statistics
KDTree = kdtree.KDTree
Statistics = statistics.Statistics
__all__ = [
 'KDTree',
 'Statistics']

def load_tests(loader, tests, ignore):
    import unittest, doctest
    for module in (kdtree, statistics):
        tests.addTests(doctest.DocTestSuite(module))

    return tests