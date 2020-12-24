# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: pygitrepo/__init__.py
# Compiled at: 2018-09-12 23:19:03
from .version import __version__
__short_description__ = 'Allow beginner to develop Python project like a Pro - Quickly initiate a python project from scratch.'
__license__ = 'MIT'
__author__ = 'Sanhe Hu'
__author_email__ = 'husanhe@gmail.com'
__maintainer__ = 'Sanhe Hu'
__maintainer_email__ = 'husanhe@gmail.com'
__github_username__ = 'MacHu-GWU'
try:
    from .initiate_project import initiate_project as init
    from .validation import DocService
except ImportError:
    pass