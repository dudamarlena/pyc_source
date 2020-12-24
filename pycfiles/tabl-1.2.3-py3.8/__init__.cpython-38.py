# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/tabl/__init__.py
# Compiled at: 2020-03-12 15:31:38
# Size of source mod 2**32: 376 bytes
"""
.. module:: tabl
.. moduleauthor:: Bastiaan Bergman <Bastiaan.Bergman@gmail.com>

"""
from .tabl import Tbl, read_tabl, transpose, T
from .hashjoin import first
from ._version import __version__
__all__ = [
 'Tbl', 'first', 'transpose', 'T', 'read_tabl', '__version__']
name = 'tabl'