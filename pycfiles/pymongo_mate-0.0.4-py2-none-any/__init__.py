# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/pymongo_mate-project/pymongo_mate/__init__.py
# Compiled at: 2017-10-12 14:43:38
__version__ = '0.0.4'
__short_description__ = 'A library extend pymongo module, makes CRUD easier, and more.'
__license__ = 'MIT'
__author__ = 'Sanhe Hu'
__author_email__ = 'husanhe@gmail.com'
__maintainer__ = 'Sanhe Hu'
__maintainer_email__ = 'husanhe@gmail.com'
__github_username__ = 'MacHu-GWU'
try:
    from .crud.insert import *
    from .crud.select import *
    from .crud.update import *
    from .query_builder import *
except ImportError:
    pass