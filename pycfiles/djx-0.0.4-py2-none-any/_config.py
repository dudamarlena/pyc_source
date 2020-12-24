# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-zr3xXj/attrs/attr/_config.py
# Compiled at: 2019-02-14 00:35:48
from __future__ import absolute_import, division, print_function
__all__ = [
 'set_run_validators', 'get_run_validators']
_run_validators = True

def set_run_validators(run):
    """
    Set whether or not validators are run.  By default, they are run.
    """
    global _run_validators
    if not isinstance(run, bool):
        raise TypeError("'run' must be bool.")
    _run_validators = run


def get_run_validators():
    """
    Return whether or not validators are run.
    """
    return _run_validators