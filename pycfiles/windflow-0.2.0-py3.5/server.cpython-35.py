# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/windflow/commands/server.py
# Compiled at: 2018-04-18 11:33:58
# Size of source mod 2**32: 722 bytes
from windflow.commands.base import Command
from windflow.commands.mixins import EventLoopCommandMixin

class ServerCommand(EventLoopCommandMixin, Command):
    name = 'server'

    def __init__(self, app_factory, host='0.0.0.0', port=8081, **kwargs):
        self.app_factory = app_factory
        self.host = host
        self.port = port
        self.kwargs = kwargs

    def handle(self, logger, options):
        self.kwargs['debug'] = bool(self.kwargs.pop('debug', False))
        loop = self.get_event_loop(self.kwargs['debug'])
        self.app_factory(**self.kwargs).listen(self.port, self.host)
        logger.info('Listening to {}:{} - {}'.format(self.host, self.port, self.kwargs))
        loop.run_forever()