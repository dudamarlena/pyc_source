# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ohppipeline/__init__.py
# Compiled at: 2020-02-24 04:47:21
# Size of source mod 2**32: 379 bytes
""" package in order to reduce and analyze fits 

:author: Clement Hottier
"""
from .utils import makemasterbias, makemasterflat, processimages, crosscorrelalign
__author__ = 'Clement Hottier, Noel Robichon'
__version__ = '1.0.2'
__all__ = [
 'makemasterbias',
 'makemasterflat',
 'processimages',
 'crosscorrelalign']