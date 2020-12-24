# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/ramjet/tasks/webdemo.py
# Compiled at: 2018-03-07 03:59:08
# Size of source mod 2**32: 637 bytes
"""
Web HTTP Hanle 的示例

访问：/webdemo/
"""
from aiohttp import web
from aiohttp_session import get_session
from ramjet.settings import logger
logger = logger.getChild('tasks.web_demo')

def bind_task():
    logger.info('run web_demo')


def bind_handle(add_route):
    logger.info('bind_handle')
    add_route('/', DemoHandle)


class DemoHandle(web.View):

    async def get(self):
        logger.info('get DemoHandle')
        s = await get_session(self.request)
        if 'skey' in s:
            logger.info('session work ok')
        else:
            s['skey'] = '123'
        return web.Response(text='New hope')