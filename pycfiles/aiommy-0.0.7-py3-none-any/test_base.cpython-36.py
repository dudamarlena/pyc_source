# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/denny/project/picme/aiommy/build/lib/tests/test_permissions/test_base.py
# Compiled at: 2017-11-20 03:41:06
# Size of source mod 2**32: 657 bytes
from aiohttp.test_utils import make_mocked_request, unittest_run_loop
from aiommy.permissions.base import BasePermission
from aiommy.unittest import AioTestCase

class BasePermissionTestCase(AioTestCase):

    @unittest_run_loop
    async def test_check_permission(self):
        request = make_mocked_request('GET', '/')
        permission = BasePermission()
        result = await permission.check_permission(request)
        self.assertTrue(result is None)

    @unittest_run_loop
    async def test_get_response(self):
        permission = BasePermission()
        result = await permission.get_response()
        self.assertTrue(result.status == 403)