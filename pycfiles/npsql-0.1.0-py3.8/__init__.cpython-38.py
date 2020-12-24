# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/npsql/__init__.py
# Compiled at: 2020-03-13 15:13:35
# Size of source mod 2**32: 383 bytes
"""
.. module:: npsql
.. moduleauthor:: Bastiaan Bergman <Bastiaan.Bergman@gmail.com>

"""
from .npsql import Nptab, read_tabl, transpose, T
from .hashjoin import first
from ._version import __version__
__all__ = [
 'Nptab', 'first', 'transpose', 'T', 'read_tabl', '__version__']
name = 'npsql'