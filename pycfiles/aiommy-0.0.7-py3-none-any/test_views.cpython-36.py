# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/denny/project/picme/aiommy/build/lib/tests/test_views.py
# Compiled at: 2017-11-20 03:41:06
# Size of source mod 2**32: 1100 bytes
import json
from aiohttp import web
from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop
from aiommy.views import JsonifyResponseView

class JsonifyResponseViewTestCase(AioHTTPTestCase):

    def get_app(self):
        app = web.Application()
        body = {'body': 'ok'}

        class TestView(JsonifyResponseView):

            async def post(self):
                response = await self.request.json()
                return web.Response(text=(json.dumps(response)))

            async def get(self):
                return self.json_response(body)

        app.router.add_route('*', '/', TestView)
        return app

    @unittest_run_loop
    async def test_body_json(self):
        result = '{"body": "ok"}'
        response = await self.client.post('/', data=result)
        text = await response.text()
        self.assertTrue(text == result)

    @unittest_run_loop
    async def test_json_response(self):
        response = await self.client.get('/')
        text = await response.text()
        self.assertTrue(text == '{\n    "body": "ok"\n}' or text == '{"body": "ok"}')