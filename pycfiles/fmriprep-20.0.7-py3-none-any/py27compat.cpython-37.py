# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-vxs8l7gu/setuptools/setuptools/py27compat.py
# Compiled at: 2020-05-05 12:41:36
# Size of source mod 2**32: 1504 bytes
"""
Compatibility Support for Python 2.7 and earlier
"""
import sys, platform
from setuptools.extern import six

def get_all_headers(message, key):
    """
    Given an HTTPMessage, return all headers matching a given key.
    """
    return message.get_all(key)


if six.PY2:

    def get_all_headers(message, key):
        return message.getheaders(key)


linux_py2_ascii = platform.system() == 'Linux' and six.PY2
rmtree_safe = str if linux_py2_ascii else (lambda x: x)
try:
    from ._imp import find_module, PY_COMPILED, PY_FROZEN, PY_SOURCE
    from ._imp import get_frozen_object, get_module
except ImportError:
    import imp
    from imp import PY_COMPILED, PY_FROZEN, PY_SOURCE

    def find_module(module, paths=None):
        """Just like 'imp.find_module()', but with package support"""
        parts = module.split('.')
        while parts:
            part = parts.pop(0)
            f, path, (suffix, mode, kind) = info = imp.find_module(part, paths)
            if kind == imp.PKG_DIRECTORY:
                parts = parts or ['__init__']
                paths = [path]
            elif parts:
                raise ImportError("Can't find %r in %s" % (parts, module))

        return info


    def get_frozen_object(module, paths):
        return imp.get_frozen_object(module)


    def get_module(module, paths, info):
        (imp.load_module)(module, *info)
        return sys.modules[module]