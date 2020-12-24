# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tpPyUtils/debug.py
# Compiled at: 2020-01-16 14:56:47
# Size of source mod 2**32: 1468 bytes
"""
Module that contains utility functions related with debugging purposes
"""
from __future__ import print_function, division, absolute_import

def format_message(fname, expected, actual, flag):
    """
    Convenience function that returns nicely formatted error/warning messages
    """
    format = lambda types: ', '.join([str(t).split("'")[1] for t in types])
    expected, actual = format(expected), format(actual)
    msg = "'{}' method ".format(fname) + ('accepts', 'returns')[flag] + ' ({}), but '.format(expected) + ('was given',
                                                                                                          'result is')[flag] + ' ({})'.format(actual)
    return msg


def debug_object_string(obj, msg):
    """
    Returns a debug string depending of the type of the object
    :param obj: Python object
    :param msg: message to log
    :return: str, debug string
    """
    import inspect
    if inspect.ismodule(obj):
        return '[%s module] :: %s' % (obj.__name__, msg)
    if inspect.isclass(obj):
        return '[%s.%s class] :: %s' % (obj.__module__, obj.__name__, msg)
    if inspect.ismethod(obj):
        return '[%s.%s.%s method] :: %s' % (obj.im_class.__module__, obj.im_class.__name__, obj.__name__, msg)
    if inspect.isfunction(obj):
        return '[%s.%s function] :: %s' % (obj.__module__, obj.__name__, msg)