# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rinat/project/BasiliskJS/basilisk/__init__.py
# Compiled at: 2018-01-05 05:14:53
__author__ = 'lich666dead'
__title__ = 'BasiliskJS'
__version__ = '0.7'
__copyright__ = 'copyright: (c) 2017 by lich666dead.'
try:
    from .basilisk import PhantomJS
except ImportError:
    from basilisk import PhantomJS