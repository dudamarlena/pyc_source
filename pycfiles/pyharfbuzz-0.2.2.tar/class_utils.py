# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\pyhardware\utils\class_utils.py
# Compiled at: 2013-10-05 04:00:20
from collections import OrderedDict

def class_to_str(cls):
    """serializes the class name + module name"""
    return cls.__module__ + '.' + cls.__name__


def _list_all_child_classes(parent, dictionnary):
    """function to be called in the recursive loop (private)"""
    depth = []
    for i, cls in enumerate(parent.__subclasses__()):
        depth.append(_list_all_child_classes(cls, dictionnary))
        dictionnary['' * depth[i] + class_to_str(cls)] = cls

    if len(depth) > 0:
        maxdepth = max(depth) + 1
    else:
        maxdepth = 0
    return maxdepth


def list_all_child_classes(parent):
    """returns an ordered dictionnary d with d[class_name] = class.
    The classes are ordered in a depth-first-search way"""
    dictionnary = OrderedDict()
    _list_all_child_classes(parent, dictionnary)
    return dictionnary