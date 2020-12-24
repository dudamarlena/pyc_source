# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/makegms.py
# Compiled at: 2018-11-10 09:21:52
# Size of source mod 2**32: 302 bytes


def __bootstrap__():
    global __bootstrap__
    global __file__
    global __loader__
    import sys, pkg_resources, imp
    __file__ = pkg_resources.resource_filename(__name__, 'makegms.cpython-36m-darwin.so')
    __loader__ = None
    del __bootstrap__
    del __loader__
    imp.load_dynamic(__name__, __file__)


__bootstrap__()