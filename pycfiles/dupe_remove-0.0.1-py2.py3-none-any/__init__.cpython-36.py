# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/dupe_remove-project/dupe_remove/__init__.py
# Compiled at: 2019-03-01 14:21:47
# Size of source mod 2**32: 484 bytes
"""
Solution for clean up duplicate data in database efficiently.
"""
from ._version import __version__
__short_description__ = 'Build Lambda Function to remove duplicate data from Redshift in minutes.'
__license__ = 'MIT'
__author__ = 'Sanhe Hu'
__author_email__ = 'husanhe@gmail.com'
__github_username__ = 'MacHu-GWU'
try:
    from .worker import Worker
    from .scheduler import Scheduler
    from .handler import Handler
except ImportError:
    pass