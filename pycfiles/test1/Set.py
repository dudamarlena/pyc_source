# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Ft\Lib\Set.py
# Compiled at: 2006-12-26 13:41:49


def __bootstrap__():
    global __bootstrap__
    global __file__
    global __loader__
    import imp, pkg_resources
    __file__ = pkg_resources.resource_filename(__name__, 'Set.pyd')
    del __bootstrap__
    del __loader__
    imp.load_dynamic(__name__, __file__)


__bootstrap__()