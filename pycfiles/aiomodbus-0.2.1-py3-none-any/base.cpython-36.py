# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/denny/project/picme/aiommy/build/lib/aiommy/permissions/base.py
# Compiled at: 2017-11-20 03:41:06
# Size of source mod 2**32: 188 bytes
from aiohttp import web

class BasePermission(object):

    async def check_permission(self, request):
        pass

    async def get_response(self):
        return web.HTTPForbidden()