# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/joel/Workspace/dev/interface/formatters.py
# Compiled at: 2020-02-01 10:25:30
# Size of source mod 2**32: 570 bytes
"""
Formatting functions for docopts
"""
from sys import argv

def fmt_uses(uses):
    """
    TODO
    
    Args:
        uses ([type]): [description]
    
    Returns:
        [type]: [description]
    """
    lines = [f"    {argv[0]} <config_path> [options] " + l for l in uses]
    return 'Usage:\n' + '\n'.join(lines)


def fmt_options(options):
    """
    TODO
    
    Args:
        options ([type]): [description]
    
    Returns:
        [type]: [description]
    """
    lines = [f"    --{opt}" for opt, desc in options]
    return '\n' + '\n'.join(lines)