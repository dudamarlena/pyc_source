# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/capparselib/__init__.py
# Compiled at: 2020-04-01 06:58:04
__author__ = 'knichols'
name = 'capparselib'
try:
    from ._version import version as __version__
except ImportError:
    __version__ = 'unknown'

__all__ = ['parsers', 'schema']