# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: invsearch/__init__.py
# Compiled at: 2018-11-03 10:39:44
"""
Search Document by Field and Value.
"""
__version__ = '0.0.2'
__short_description__ = 'Search Document by Field and Value.'
__license__ = 'MIT'
__author__ = 'Sanhe Hu'
__author_email__ = 'husanhe@gmail.com'
__maintainer__ = 'Sanhe Hu'
__maintainer_email__ = 'husanhe@gmail.com'
__github_username__ = 'MacHu-GWU'
try:
    from .inv_index import InvIndex
except:
    pass