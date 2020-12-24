# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/ramjet/tasks/email_proxy.py
# Compiled at: 2018-03-07 05:04:13
# Size of source mod 2**32: 937 bytes
from aiohttp import web
from kipp.utils import EmailSender
from functools import partial
from ramjet.settings import logger as root_logger
from ramjet.engines import thread_executor, ioloop
logger = root_logger.getChild('tasks.email_proxy')

def bind_task():
    logger.info('run email proxy')


def bind_handle(add_route):
    logger.info('bind handle')
    add_route('/', EmailProxyHandle)


class EmailProxyHandle(web.View):

    async def get(self):
        return web.Response(text='email proxy')

    async def post(self):
        data = await self.request.json()
        sender = EmailSender(host=(data.pop('host')),
          username=(data.pop('username')),
          passwd=(data.pop('passwd')),
          use_tls=(data.pop('use_tls', None)))
        runner = partial((sender.send_email), **data)
        r = await ioloop.run_in_executor(thread_executor, runner)
        return web.Response(text=(str(r)))