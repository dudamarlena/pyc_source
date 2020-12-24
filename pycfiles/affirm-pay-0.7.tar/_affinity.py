# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-ppc/egg/affinity/_affinity.py
# Compiled at: 2006-03-22 22:49:50


def __bootstrap__():
    global __bootstrap__
    global __file__
    global __loader__
    import sys, pkg_resources, imp
    __file__ = pkg_resources.resource_filename(__name__, '_affinity.so')
    del __bootstrap__
    del __loader__
    imp.load_dynamic(__name__, __file__)


__bootstrap__()