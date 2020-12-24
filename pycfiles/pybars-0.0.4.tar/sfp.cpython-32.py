# uncompyle6 version 3.6.7
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-armv6l/egg/sfp.py
# Compiled at: 2014-09-18 14:11:51


def __bootstrap__():
    global __bootstrap__
    global __file__
    global __loader__
    import sys, pkg_resources, imp
    __file__ = pkg_resources.resource_filename(__name__, 'sfp.cpython-32mu.so')
    __loader__ = None
    del __bootstrap__
    del __loader__
    imp.load_dynamic(__name__, __file__)
    return


__bootstrap__()