# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/convert2-project/convert2/__init__.py
# Compiled at: 2018-01-23 14:39:41
# Size of source mod 2**32: 558 bytes
__version__ = '0.0.3'
__short_description__ = 'Convert anything to any type.'
__license__ = 'MIT'
__author__ = 'Sanhe Hu'
__author_email__ = 'husanhe@gmail.com'
__maintainer__ = 'Sanhe Hu'
__maintainer_email__ = 'husanhe@gmail.com'
__github_username__ = 'MacHu-GWU'
try:
    from .parse_int import any2int
    from .parse_float import any2float
    from .parse_str import any2str
    from .parse_datetime import any2datetime
    from .parse_date import any2date
except ImportError:
    pass