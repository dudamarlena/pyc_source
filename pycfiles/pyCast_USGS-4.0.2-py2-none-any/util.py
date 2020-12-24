# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dan/dev/pyCast/shakecast/sc/app/util.py
# Compiled at: 2017-04-21 05:20:51
import math, os

def get_delim():
    """
    Returns which delimeter is appropriate for the operating system
    """
    return os.sep


def sc_dir():
    """
    Returns the path of the sc directory for the shakecast application
    """
    path = os.path.dirname(os.path.abspath(__file__))
    delim = get_delim()
    path = path.split(delim)
    del path[-1]
    directory = os.path.normpath(delim.join(path))
    return directory


def root_dir():
    """
    Returns the path of the root directory for the shakecast application
    """
    path = sc_dir().split(get_delim())
    del path[-1]
    directory = os.path.normpath(get_delim().join(path))
    return directory


def lognorm_opt(med=0, spread=0, step=0.01, just_norm=False, shaking=False):
    p_norm = (math.erf((shaking - med) / (math.sqrt(2) * spread)) + 1) / 2
    return p_norm * 100