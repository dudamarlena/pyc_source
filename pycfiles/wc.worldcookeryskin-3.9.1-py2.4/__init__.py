# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/wc/__init__.py
# Compiled at: 2007-02-23 15:52:17
try:
    import pkg_resources
    pkg_resources.declare_namespace('wc')
except ImportError:
    from pkgutil import extend_path
    __path__ = extend_path(__path__, __name__)