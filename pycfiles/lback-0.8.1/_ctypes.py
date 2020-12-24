# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: _ctypes.pyc
# Compiled at: 2014-10-30 14:52:35


def __load():
    import imp, os, sys
    try:
        dirname = os.path.dirname(__loader__.archive)
    except NameError:
        dirname = sys.prefix

    path = os.path.join(dirname, '_ctypes.pyd')
    mod = imp.load_dynamic(__name__, path)


__load()
del __load