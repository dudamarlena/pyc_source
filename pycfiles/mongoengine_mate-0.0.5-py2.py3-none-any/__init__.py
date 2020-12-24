# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: mongoengine_mate/__init__.py
# Compiled at: 2019-09-17 23:00:10
"""
Utility methods for MongoDB ORM, built on top of mongoengine.
"""
from ._version import __version__
__short_description__ = 'Utility methods for MongoDB ORM, built on top of mongoengine.'
__license__ = 'MIT'
__author__ = 'Sanhe Hu'
__author_email__ = 'husanhe@gmail.com'
__maintainer__ = 'Sanhe Hu'
__maintainer_email__ = 'husanhe@gmail.com'
__github_username__ = 'MacHu-GWU'
try:
    from .document import ExtendedDocument
except ImportError:
    pass