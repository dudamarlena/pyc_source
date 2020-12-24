# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/utf8config-project/utf8config/__init__.py
# Compiled at: 2017-10-14 19:53:13
# Size of source mod 2**32: 419 bytes
__version__ = '0.0.2'
__short_description__ = 'A utf8 charset config file parser'
__license__ = 'MIT'
__author__ = 'Sanhe Hu'
__author_email__ = 'husanhe@gmail.com'
__maintainer__ = 'Sanhe Hu'
__maintainer_email__ = 'husanhe@gmail.com'
__github_username__ = 'MacHu-GWU'
try:
    from .core import Config, Section, Field
except ImportError:
    pass