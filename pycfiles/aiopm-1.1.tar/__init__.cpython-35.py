# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/aiopixiv/__init__.py
# Compiled at: 2017-03-30 14:45:02
# Size of source mod 2**32: 272 bytes
__doc__ = '\naiopixiv - an async way to access the pixiv API.\n'
from aiopixiv.wrapper import BaseAPI, PixivError, PixivAuthFailed
from aiopixiv.v5 import PixivAPIv5
__version__ = '1.0.5'
__author__ = 'Laura Dickinson'
__all__ = ('PixivError', 'PixivAuthFailed', 'PixivAPIv5')