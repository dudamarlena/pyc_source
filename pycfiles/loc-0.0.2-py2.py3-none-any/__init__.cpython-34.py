# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/loc-project/loc/__init__.py
# Compiled at: 2018-10-18 18:25:40
# Size of source mod 2**32: 454 bytes
"""
"""
__version__ = '0.0.2'
__short_description__ = 'Software Localization Tool.'
__license__ = 'MIT'
__author__ = 'Sanhe Hu'
__author_email__ = 'husanhe@gmail.com'
__maintainer__ = 'Sanhe Hu'
__maintainer_email__ = 'husanhe@gmail.com'
__github_username__ = 'MacHu-GWU'
try:
    from .locales import Locale, locale_list
    from .loc_dict import LocDict
except ImportError:
    pass