# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/denny/project/picme/aiommy/build/lib/aiommy/permissions/view_only.py
# Compiled at: 2017-11-20 03:41:06
# Size of source mod 2**32: 280 bytes
from aiohttp import web
from aiommy.permissions.base import BasePermission

class ViewOnly(BasePermission):

    async def check_permission(self, request):
        if request.method == 'GET':
            return
        else:
            return web.HTTPMethodNotAllowed(request.method, ('GET', ))