# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/inspect_mate-project/inspect_mate/__init__.py
# Compiled at: 2018-09-06 20:36:09
# Size of source mod 2**32: 255 bytes
__version__ = '0.0.1'
__short_description__ = 'Extend the ``inspect`` standard library.'
__license__ = 'MIT'
__author__ = 'Sanhe Hu'
try:
    from .getter import *
    from .tester import *
except:
    pass