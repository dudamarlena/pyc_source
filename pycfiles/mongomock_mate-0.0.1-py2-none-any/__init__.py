# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/mongomock_mate-project/mongomock_mate/__init__.py
# Compiled at: 2018-07-30 23:07:59
"""
Package Description.
"""
__version__ = '0.0.1'
__short_description__ = 'Add additional feature for mongomock.'
__license__ = 'MIT'
__author__ = 'Sanhe Hu'
__author_email__ = 'husanhe@gmail.com'
__maintainer__ = 'Sanhe Hu'
__maintainer_email__ = 'husanhe@gmail.com'
__github_username__ = 'MacHu-GWU'
try:
    from . import patch_write_concern
    from . import patch_collection
    from . import patch_database
except:
    pass