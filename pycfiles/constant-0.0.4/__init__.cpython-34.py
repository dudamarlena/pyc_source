# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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