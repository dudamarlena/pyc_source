# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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