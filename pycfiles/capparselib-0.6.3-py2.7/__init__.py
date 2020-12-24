# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/capparselib/__init__.py
# Compiled at: 2020-04-01 06:58:04
__author__ = 'knichols'
name = 'capparselib'
try:
    from ._version import version as __version__
except ImportError:
    __version__ = 'unknown'

__all__ = ['parsers', 'schema']