# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/pytq_crawlib-project/pytq_crawlib/__init__.py
# Compiled at: 2018-01-26 14:28:48
# Size of source mod 2**32: 452 bytes
"""
Sanhe's private crawler tool.
"""
__version__ = '0.0.5'
__short_description__ = ''
__license__ = 'MIT'
__author__ = 'Sanhe Hu'
__author__ = 'Sanhe Hu'
__author_email__ = 'husanhe@gmail.com'
__maintainer__ = 'Sanhe Hu'
__maintainer_email__ = 'husanhe@gmail.com'
__github_username__ = 'MacHu-GWU'
try:
    from .scheduler import BaseScheduler, OneToOne, OneToMany
except:
    pass