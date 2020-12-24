# uncompyle6 version 3.6.7
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: C:\Users\shu\Documents\PythonWorkSpace\py3\py33_projects\potplayer-project\potplayer\__init__.py
# Compiled at: 2016-10-03 17:19:25
# Size of source mod 2**32: 251 bytes
__version__ = '0.0.3'
__author__ = 'Sanhe Hu'
__license__ = 'MIT'
__short_description__ = 'A tools to manipulate potplayer playlist'
from .playlist import PlayList
from .execute import run, kill