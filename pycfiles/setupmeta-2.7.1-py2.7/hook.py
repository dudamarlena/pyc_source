# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/setupmeta/hook.py
# Compiled at: 2020-04-30 15:23:01
"""
Hook for setuptools/distutils
"""
import distutils.dist
from setupmeta.model import MetaDefs, SetupMeta
dd_original = distutils.dist.Distribution.parse_command_line

def distutils_hook(dist, *args, **kwargs):
    """ distutils.dist.Distribution.parse_command_line replacement

    distutils calls this right after having processed 'setup_requires'
    It really calls self.parse_command_line(command), we jump in
    so we can decorate the 'dist' object appropriately for our own commands
    """
    if dist.script_args and not hasattr(dist, '_setupmeta'):
        dist._setupmeta = SetupMeta(dist)
        MetaDefs.fill_dist(dist, dist._setupmeta.to_dict())
    return dd_original(dist, *args, **kwargs)


def register(dist, name, value):
    """ Hook into distutils in order to do our magic

    We use this as a 'distutils.setup_keywords' entry point
    We don't need to do anything specific here (in this function)
    But we do need distutils to import this module
    """
    if name == 'setup_requires':
        value = value if isinstance(value, list) else [value]
        if any(item.startswith('setupmeta') for item in value):
            distutils.dist.Distribution.parse_command_line = distutils_hook
        else:
            distutils.dist.Distribution.parse_command_line = dd_original