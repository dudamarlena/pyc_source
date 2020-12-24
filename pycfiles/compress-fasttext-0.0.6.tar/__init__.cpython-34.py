# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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