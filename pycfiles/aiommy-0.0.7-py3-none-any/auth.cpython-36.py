# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/denny/project/picme/aiommy/build/lib/aiommy/permissions/auth.py
# Compiled at: 2017-11-20 03:41:06
# Size of source mod 2**32: 389 bytes
from aiohttp import web
from aiommy.permissions.base import BasePermission

class AuthPermission(BasePermission):

    async def check_permission(self, request):
        if hasattr(request, 'user'):
            if request.user is not None:
                if request.user.get('id'):
                    return
        return await self.get_response()

    async def get_response(self):
        return web.HTTPUnauthorized()