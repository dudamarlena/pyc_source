# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-zr3xXj/pytest/_pytest/__init__.py
# Compiled at: 2019-02-14 00:35:47
__all__ = [
 '__version__']
try:
    from ._version import version as __version__
except ImportError:
    __version__ = 'unknown'