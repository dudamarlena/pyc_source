# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pydap/__init__.py
# Compiled at: 2011-06-20 14:04:22
try:
    import pkg_resources
    pkg_resources.declare_namespace(__name__)
except ImportError:
    from pkgutil import extend_path
    __path__ = extend_path(__path__, __name__)

import modulefinder
for p in __path__:
    modulefinder.AddPackagePath(__name__, p)