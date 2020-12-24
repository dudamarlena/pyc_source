# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/sh2dis/__init__.py
# Compiled at: 2017-12-04 18:02:15
"""A disassembler for SuperH SH2 ROMs."""
from __future__ import print_function
from . import __main__
from . import mitsubishi
from . import segment
from . import sh2
from . import sh7052
from . import sh7055
__author__ = 'Ed Marshall'
__email__ = 'esm@logic.net'
__url__ = 'http://github.com/logic/sh2dis'
__version__ = '1.0'
__copyright__ = 'Copyright (C) 2010-2017, Ed Marshall'
__license__ = 'GPL3'

class ROMError(Exception):
    """An error related to parsing the supplied ROM data."""
    pass