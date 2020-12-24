# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: rstobj/__init__.py
# Compiled at: 2019-05-24 23:16:42
"""
Construct RestructuredText markup and directives from Python Code.
"""
from ._version import __version__
__short_description__ = 'Construct RestructuredText markup and directives from Python Code.'
__license__ = 'MIT'
__author__ = 'Sanhe Hu'
__author_email__ = 'husanhe@gmail.com'
__maintainer__ = 'Sanhe Hu'
__maintainer_email__ = 'husanhe@gmail.com'
__github_username__ = 'MacHu-GWU'
try:
    from . import directives, markup
    from .directives import *
    from .markup import *
except:
    pass