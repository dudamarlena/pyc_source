# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: C:\Users\shu\PycharmProjects\py34\cazipcode-project\cazipcode\__init__.py
# Compiled at: 2017-07-13 17:04:38
# Size of source mod 2**32: 298 bytes
__doc__ = '\n\n'
__version__ = '0.0.2'
__short_description__ = 'Powerful Canada zipcode search engine.'
__license__ = 'MIT'
__author__ = 'Sanhe Hu'
try:
    from .search import great_circle, fields, PostalCode, SearchEngine
except:
    pass