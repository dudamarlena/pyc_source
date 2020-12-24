# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: C:\Users\shu\PycharmProjects\py34\constant-project\constant\__init__.py
# Compiled at: 2017-04-06 16:11:23
# Size of source mod 2**32: 311 bytes
__version__ = '0.0.4'
__short_description__ = 'Use IDLE autocomplete feature to manage large amount of constants.'
__license__ = 'MIT'
__author__ = 'Sanhe Hu'
try:
    from .tpl.class_def import gencode
    from .const import Constant
except:
    pass