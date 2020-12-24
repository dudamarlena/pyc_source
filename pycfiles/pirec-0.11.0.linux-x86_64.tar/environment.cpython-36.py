# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jstutters/.virtualenvs/pirec/lib/python3.6/site-packages/pirec/environment.py
# Compiled at: 2017-02-10 11:03:57
# Size of source mod 2**32: 763 bytes
"""Module containing the get_environment function."""
import os
try:
    import pip
except ImportError:
    pass

import socket

def get_environment():
    """Obtain information about the executing environment.

    Captures:
        * installed Python packages using pip (if available),
        * hostname
        * uname
        * environment variables

    Returns:
        dict: a dict with the keys ``python_packages``, ``hostname``, ``uname`` and ``environ``
    """
    env = {}
    try:
        env['python_packages'] = [str(p) for p in pip.get_installed_distributions()]
    except:
        pass

    env['hostname'] = socket.gethostname()
    env['uname'] = os.uname()
    env['environ'] = dict(os.environ)
    return env