# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/heatshrink/__init__.py
# Compiled at: 2016-11-09 11:18:15
from .core import encode, decode
from .streams import open, EncodedFile
__all__ = ['encode', 'decode', 'open', 'EncodedFile']