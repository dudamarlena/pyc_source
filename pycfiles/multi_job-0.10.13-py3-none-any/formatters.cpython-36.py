# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/joel/Workspace/multi-job/multi_job/interface/formatters.py
# Compiled at: 2020-02-19 11:54:34
# Size of source mod 2**32: 564 bytes
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
    lines = [f"    --{opt}" for opt in options]
    return '\n' + '\n'.join(lines)