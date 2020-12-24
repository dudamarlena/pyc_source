# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/g/projects/superhelp/build/lib/superhelp/code_execution.py
# Compiled at: 2020-04-14 20:07:24
# Size of source mod 2**32: 997 bytes
import logging

def get_val(pre_block_code_str, block_code_str, name):
    """
    Executing supplied code from end users - nope - nothing to see here from a
    security point of view ;-) Needs addressing if this code is ever used as a
    service for other users.

    Note - can be the source of mysterious output in stdout (e.g. exec a print
    function).
    """
    exp_dets = {}
    try:
        exec(pre_block_code_str + block_code_str, exp_dets)
    except ImportError as e:
        try:
            logging.debug(f"Import problem running {__file__} (specifically {__name__}): {e}")
            raise ImportError('SuperHELP only has modules from the Python standard library installed - it looks like your snippet relies on a module from outside the standard library.')
        finally:
            e = None
            del e

    try:
        val = exp_dets[name]
    except KeyError:
        val = None

    return val