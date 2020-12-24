# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyxrd/scripts/tools.py
# Compiled at: 2020-03-07 03:51:50
# Size of source mod 2**32: 1131 bytes
"""
    Tools for making scripting easier
"""

def reload_settings(clear_script=True):
    """
        This will reload the PyXRD settings after clearing the script path from
        the command line arguments. This allows to run the GUI when needed.
    """
    import sys
    from copy import copy
    args = copy(sys.argv)
    for i, arg in enumerate(args):
        if arg == '-s':
            del sys.argv[i + 1]
            del sys.argv[i]
            break

    from pyxrd.data import settings
    settings.SETTINGS_APPLIED = False
    settings.initialize()


def launch_gui(project=None):
    """ Launches the GUI, you should run reload_settings before calling this! """
    from pyxrd.core import _run_gui
    _run_gui(project=project)