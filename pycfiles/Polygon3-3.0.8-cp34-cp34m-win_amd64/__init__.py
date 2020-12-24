# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/Polygon/__init__.py
# Compiled at: 2015-11-05 04:38:20
from cPolygon import *
__version__ = version
__author__ = author
__license__ = license
del version
del author
del license

def __createPolygon(contour, hole):
    """rebuild Polygon from pickled data"""
    p = Polygon()
    map(p.addContour, contour, hole)
    return p


def __tuples(a):
    """map an array or list of lists to a tuple of tuples"""
    return tuple(map(tuple, a))


def __reducePolygon(p):
    """return pickle data for Polygon """
    return (
     __createPolygon, (tuple([ __tuples(x) for x in p ]), p.isHole()))


import copy_reg
copy_reg.constructor(__createPolygon)
copy_reg.pickle(Polygon, __reducePolygon)
del copy_reg