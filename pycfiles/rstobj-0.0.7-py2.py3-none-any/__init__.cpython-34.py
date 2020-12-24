# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/rstobj-project/rstobj/__init__.py
# Compiled at: 2018-12-02 17:44:27
# Size of source mod 2**32: 506 bytes
"""
Construct RestructuredText markup and directives from Python Code.
"""
__version__ = '0.0.5'
__short_description__ = 'Construct RestructuredText markup and directives from Python Code.'
__license__ = 'MIT'
__author__ = 'Sanhe Hu'
__author_email__ = 'husanhe@gmail.com'
__maintainer__ = 'Sanhe Hu'
__maintainer_email__ = 'husanhe@gmail.com'
__github_username__ = 'MacHu-GWU'
try:
    from . import directives, markup
except:
    pass