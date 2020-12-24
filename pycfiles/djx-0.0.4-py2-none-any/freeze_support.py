# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-zr3xXj/pytest/_pytest/freeze_support.py
# Compiled at: 2019-02-14 00:35:47
"""
Provides a function to report all internal modules for using freezing tools
pytest
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

def freeze_includes():
    """
    Returns a list of module names used by pytest that should be
    included by cx_freeze.
    """
    import py, _pytest
    result = list(_iter_all_modules(py))
    result += list(_iter_all_modules(_pytest))
    return result


def _iter_all_modules(package, prefix=''):
    """
    Iterates over the names of all modules that can be found in the given
    package, recursively.
    Example:
        _iter_all_modules(_pytest) ->
            ['_pytest.assertion.newinterpret',
             '_pytest.capture',
             '_pytest.core',
             ...
            ]
    """
    import os, pkgutil
    if type(package) is not str:
        path, prefix = package.__path__[0], package.__name__ + '.'
    else:
        path = package
    for _, name, is_package in pkgutil.iter_modules([path]):
        if is_package:
            for m in _iter_all_modules(os.path.join(path, name), prefix=name + '.'):
                yield prefix + m

        else:
            yield prefix + name