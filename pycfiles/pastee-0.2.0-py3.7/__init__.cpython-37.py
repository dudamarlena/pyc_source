# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\pastee\__init__.py
# Compiled at: 2020-03-27 20:33:17
# Size of source mod 2**32: 279 bytes
__version__ = '0.2.0'
import asyncio
from sys import platform, version_info
from .paste import Client
if platform == 'win32':
    if version_info >= (3, 8):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())