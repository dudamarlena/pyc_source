# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nicfit/aio.py
# Compiled at: 2019-08-02 01:55:02
# Size of source mod 2**32: 1565 bytes
import asyncio
from .app import AsyncApplication
from .command import Command as BaseCommand
from .command import SubCommandCommand as BaseSubCommandCommand

class Application(AsyncApplication):

    def __init__(self, main_func=None, *, event_loop=None, **kwargs):
        (super().__init__)(main_func, **kwargs)
        self.event_loop = event_loop or asyncio.get_event_loop()
        self._main_task = None
        self._exit_status = None

    def _run(self, args_list=None):
        self.log.debug(('aio.Application: {args_list}'.format)(**locals()))
        self._main_task = self.event_loop.create_task(self.main(args_list=args_list))
        try:
            self._exit_status = self.event_loop.run_until_complete(self._main_task)
        except asyncio.CancelledError as ex:
            try:
                self.log.debug('aio.Application: Cancelled: {}'.format(ex))
            finally:
                ex = None
                del ex

        else:
            return self._exit_status

    def stop(self, exit_status=0):
        self.log.debug('Application::stop(exit_status=%d)' % exit_status)
        self._exit_status = exit_status
        self._main_task.cancel()


class Command(BaseCommand):

    async def run(self, args):
        self.args = args
        return await self._run()

    async def _run(self):
        raise NotImplementedError('Must implement a _run function')


class SubCommandCommand(BaseSubCommandCommand):

    async def run(self, args):
        self.args = args
        return await self._run()

    async def _run(self):
        return await self.args.command_func(self.args)