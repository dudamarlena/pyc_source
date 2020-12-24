# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: docfly/pkg/picage/helpers.py
# Compiled at: 2020-03-21 11:28:22
"""
Utility functions.
"""
import sys, string

def get_sp_dir():
    """
    Get the absolute path of the ``site-packages`` directory.
    """
    for p in sys.path[::-1]:
        if p.endswith('site-packages'):
            return p

    raise Exception("'site-package' directory not found!")


SP_DIR = get_sp_dir()
_first_letter_for_valid_name = set(string.ascii_lowercase + '_')
_char_set_for_valid_name = set(string.ascii_letters + string.digits + '_-')

def is_valid_package_module_name(name):
    """
    Test whether it's a valid package or module name.

    - a-z, 0-9, and underline
    - starts with underline or alpha letter

    valid:

    - ``a``
    - ``a.b.c``
    - ``_a``
    - ``_a._b._c``

    invalid:

    - ``A``
    - ``0``
    - ``.a``
    - ``a#b``
    """
    if '.' in name:
        for part in name.split('.'):
            if not is_valid_package_module_name(part):
                return False

    elif len(name):
        if name[0] not in _first_letter_for_valid_name:
            return False
        if len(set(name).difference(_char_set_for_valid_name)):
            return False
    else:
        return False
    return True


def assert_is_valid_name(name, error=None):
    if error is None:
        error = ValueError('%r is not a valid package or module name!' % name)
    if not is_valid_package_module_name(name):
        raise error
    return