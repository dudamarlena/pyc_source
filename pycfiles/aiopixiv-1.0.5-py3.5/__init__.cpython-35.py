# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/aiopixiv/__init__.py
# Compiled at: 2017-03-30 14:45:02
# Size of source mod 2**32: 272 bytes
"""
aiopixiv - an async way to access the pixiv API.
"""
from aiopixiv.wrapper import BaseAPI, PixivError, PixivAuthFailed
from aiopixiv.v5 import PixivAPIv5
__version__ = '1.0.5'
__author__ = 'Laura Dickinson'
__all__ = ('PixivError', 'PixivAuthFailed', 'PixivAPIv5')