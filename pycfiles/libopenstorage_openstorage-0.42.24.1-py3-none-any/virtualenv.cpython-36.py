# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/pip/pip/_internal/utils/virtualenv.py
# Compiled at: 2020-01-10 16:25:21
# Size of source mod 2**32: 891 bytes
import os.path, site, sys

def running_under_virtualenv():
    """
    Return True if we're running inside a virtualenv, False otherwise.

    """
    if hasattr(sys, 'real_prefix'):
        return True
    else:
        if sys.prefix != getattr(sys, 'base_prefix', sys.prefix):
            return True
        return False


def virtualenv_no_global():
    """
    Return True if in a venv and no system site packages.
    """
    site_mod_dir = os.path.dirname(os.path.abspath(site.__file__))
    no_global_file = os.path.join(site_mod_dir, 'no-global-site-packages.txt')
    if running_under_virtualenv():
        if os.path.isfile(no_global_file):
            return True
    return False