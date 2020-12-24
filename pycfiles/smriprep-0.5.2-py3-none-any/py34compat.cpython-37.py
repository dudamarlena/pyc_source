# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-pti7pv2_/setuptools/setuptools/py34compat.py
# Compiled at: 2020-02-14 17:24:43
# Size of source mod 2**32: 245 bytes
import importlib
try:
    import importlib.util
except ImportError:
    pass

try:
    module_from_spec = importlib.util.module_from_spec
except AttributeError:

    def module_from_spec(spec):
        return spec.loader.load_module(spec.name)