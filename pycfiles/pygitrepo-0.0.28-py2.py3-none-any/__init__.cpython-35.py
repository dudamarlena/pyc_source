# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/pygitrepo-project/pygitrepo/__init__.py
# Compiled at: 2018-08-05 14:29:05
# Size of source mod 2**32: 509 bytes
from .version import __version__
__short_description__ = 'Allow dummies develop Python project like a Pro - Quickly initiate a python project from scratch.'
__license__ = 'MIT'
__author__ = 'Sanhe Hu'
__author_email__ = 'husanhe@gmail.com'
__maintainer__ = 'Sanhe Hu'
__maintainer_email__ = 'husanhe@gmail.com'
__github_username__ = 'MacHu-GWU'
try:
    from .cli import initiate_project as init
except ImportError:
    pass