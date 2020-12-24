# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/denny/project/picme/aiommy/build/lib/aiommy/permissions/base.py
# Compiled at: 2017-11-20 03:41:06
# Size of source mod 2**32: 188 bytes
from aiohttp import web

class BasePermission(object):

    async def check_permission(self, request):
        pass

    async def get_response(self):
        return web.HTTPForbidden()