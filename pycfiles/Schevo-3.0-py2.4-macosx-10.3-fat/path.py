# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/schevo/script/path.py
# Compiled at: 2007-03-21 14:34:41
"""Path-handling functions for Schevo script commands.

For copyright, license, and warranty, see bottom of file.
"""
import sys
from schevo.lib import optimize
import os

def package_path(pkg_or_path):
    """If pkg_or_path is a module, return its path; otherwise,
    return pkg_or_path."""
    from_list = pkg_or_path.split('.')[:1]
    try:
        pkg = __import__(pkg_or_path, {}, {}, from_list)
    except ImportError:
        return os.path.abspath(pkg_or_path)

    if '__init__.py' in pkg.__file__:
        return os.path.abspath(os.path.dirname(pkg.__file__))
    else:
        return os.path.abspath(pkg.__file__)


optimize.bind_all(sys.modules[__name__])