# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/ramjet/tasks/webapps.py
# Compiled at: 2017-11-06 21:55:23
# Size of source mod 2**32: 519 bytes
"""
Web HTTP Hanle 的示例

访问：/apps/
"""
from aiohttp import web
from aiohttp_session import get_session
import aiohttp_jinja2
from ramjet.settings import logger
logger = logger.getChild('tasks.webapps')

def bind_task():
    logger.info('run webapps')


def bind_handle(add_route):
    logger.info('bind_handle')
    add_route('/', WebApps)


class WebApps(web.View):

    @aiohttp_jinja2.template('static/dist/index.html')
    async def get(self):
        logger.info('get WebApps')