# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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