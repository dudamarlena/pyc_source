# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tpDcc/libs/python/dcc.py
# Compiled at: 2020-05-02 23:38:35
# Size of source mod 2**32: 1092 bytes
"""
Module that contains utility functions related with apps
"""
from __future__ import print_function, division, absolute_import
import sys

def is_nuke():
    """
    Checks if Nuke is available or not
    :return: bool
    """
    try:
        import nuke
        return True
    except ImportError:
        return False


def is_maya():
    """
    Checks if Maya is available or not
    :return: bool
    """
    return 'maya.exe' in sys.executable.lower()


def is_mayapy():
    """
    Checks if Maya is available or not
    :return: bool
    """
    return 'mayapy.exe' in sys.executable.lower()


def is_max():
    """
    Checks if Max is available or not
    :return: bool
    """
    return '3dsmax' in sys.executable.lower()


def is_houdini():
    """
    Checks if Houdini is available or not
    :return: bool
    """
    return 'houdini' in sys.executable


def is_motionbuilder():
    """
    Checks if MotionBuilder is available or not
    :return: bool
    """
    return 'motionbuilder' in sys.executable.lower()