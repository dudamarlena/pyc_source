# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/compress-project/compress/__init__.py
# Compiled at: 2017-11-15 03:05:37
# Size of source mod 2**32: 483 bytes
__version__ = '0.0.2'
__short_description__ = 'All in one data compression library.'
__license__ = 'MIT'
__author__ = 'Sanhe Hu'
__author_email__ = 'husanhe@gmail.com'
__maintainer__ = 'Sanhe Hu'
__maintainer_email__ = 'husanhe@gmail.com'
__github_username__ = 'MacHu-GWU'
try:
    from .compressor import Compressor, CompressAlgorithms
    from .string_encoding import Encoder, EncodingAlgorithms
except:
    pass