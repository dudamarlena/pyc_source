# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tpHoudiniLib/core/helpers.py
# Compiled at: 2020-01-16 21:52:53
# Size of source mod 2**32: 738 bytes
"""
Module that contains Houdini utility functions and classes
"""
from __future__ import print_function, division, absolute_import
import hou, hdefereval

def get_houdini_version(as_string=True):
    """
    Returns version of the executed Houdini
    :param as_string: bool, Whether to return the stiring version or not
    :return: variant, int or str
    """
    if as_string:
        return hou.applicationVersionString()
    else:
        return hou.applicationVersion()


def get_houdini_pass_main_thread_function():
    """
    Return Houdini function to execute function in Houdini main thread
    :return: fn
    """
    return hdefereval.executeInMainThreadWithResult