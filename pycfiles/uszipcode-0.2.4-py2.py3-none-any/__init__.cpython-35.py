# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/uszipcode-project/uszipcode/__init__.py
# Compiled at: 2019-05-20 14:26:06
# Size of source mod 2**32: 633 bytes
"""
``uszipcode`` is awesome!
"""
from __future__ import print_function
try:
    from .search import SearchEngine, SimpleZipcode, Zipcode, ZipcodeType, SORT_BY_DIST
except Exception as e:
    print(e)

from ._version import __version__
__short_description__ = 'USA zipcode programmable database, includes up-to-date census and geometry information.'
__license__ = 'MIT'
__author__ = 'Sanhe Hu'
__author_email__ = 'husanhe@gmail.com'
__maintainer__ = 'Sanhe Hu'
__maintainer_email__ = 'husanhe@gmail.com'
__github_username__ = 'MacHu-GWU'