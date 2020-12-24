# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\despres\Desktop\reaper\scripts\reapy\reapy\__main__.py
# Compiled at: 2019-02-22 02:22:46
# Size of source mod 2**32: 1162 bytes
"""Get setup infos."""
from reapy.reascripts import enable_dist_api, disable_dist_api
import os, sys

def get_config_scripts():
    """
    Return paths to configuration ReaScripts.
    """
    return (
     os.path.abspath(enable_dist_api.__file__),
     os.path.abspath(disable_dist_api.__file__))


def get_python_dll():
    """
    Return path to Python DLL (if it can be found).
    """
    dir = os.path.dirname(sys.executable)
    file = os.path.basename(dir).lower() + '.dll'
    path = os.path.join(dir, file)
    if os.path.isfile(path):
        return path
    raise FileNotFoundError("Can't find python DLL...")


string = '\n======================\n  reapy config infos\n======================\n\nPython DLL\n----------\n    {}\n\nEnable or disable reapy dist API\n--------------------------------\nEnable dist API\n    {}\n\nDisable dist API\n    {}\n'
if __name__ == '__main__':
    try:
        dll = get_python_dll()
    except FileNotFoundError as e:
        try:
            dll = e.args[0]
        finally:
            e = None
            del e

    enable, disable = get_config_scripts()
    print(string.format(dll, enable, disable))