# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/attrsmallow-project/attrsmallow/__init__.py
# Compiled at: 2018-01-29 14:31:30
# Size of source mod 2**32: 415 bytes
__version__ = '0.0.1'
__short_description__ = 'Integration of attrs and marshmallow.'
__license__ = 'MIT'
__author__ = 'Sanhe Hu'
__author_email__ = 'husanhe@gmail.com'
__maintainer__ = 'Sanhe Hu'
__maintainer_email__ = 'husanhe@gmail.com'
__github_username__ = 'MacHu-GWU'
try:
    from .model_schema import BaseModel, BaseSchema
except:
    pass