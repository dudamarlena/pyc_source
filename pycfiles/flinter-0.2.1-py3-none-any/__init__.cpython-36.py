# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dauptain/GITLAB/flint/src/flinter/__init__.py
# Compiled at: 2020-05-13 15:15:08
# Size of source mod 2**32: 343 bytes
"""
Flinter
=======

Flint is a source-code static analyzer and quality checker for
fortran programming language. It intends to follows the coding conventions
mentioned in
`OMS Documentation Wiki page <https://alm.engr.colostate.edu/cb/wiki/16983>`__
"""
from .struct_analysis import *
from .fmt_analysis import *
from .formatting import *