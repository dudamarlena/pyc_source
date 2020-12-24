# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/neil/Scripts/random_name/build/lib/censusname/__init__.py
# Compiled at: 2015-02-15 13:50:46
# Size of source mod 2**32: 273 bytes
__title__ = 'censusname'
__version__ = '0.2'
__author__ = 'Neil Freeman'
__license__ = 'GPL'
__all__ = [
 'censusname', 'formatters']
from .censusname import Censusname, generate, NAMEFILES, SURNAME2000, SURNAME1990, MALEFIRST1990, FEMALEFIRST1990
from . import formatters