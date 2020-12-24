# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/guyskk/anyant/weirb/src/weirb/project-template/echo/services/hello.py
# Compiled at: 2018-06-30 08:52:59
# Size of source mod 2**32: 258 bytes
from validr import T

class HelloService:
    __doc__ = 'A Simple Hello'

    async def method_say(self, name: T.str.maxlen(10).default('world')) -> T.dict(message=(T.str)):
        """Say Hello"""
        return dict(message=f"hello {name}!")