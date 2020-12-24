# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/legions/context.py
# Compiled at: 2020-05-07 10:49:55
# Size of source mod 2**32: 781 bytes
from nubia import context
from nubia import exceptions
from nubia import eventbus

class LegionContext(context.Context):

    def on_connected(self, *args, **kwargs):
        pass

    def on_cli(self, cmd, args):
        self.verbose = args.verbose
        self.registry.dispatch_message(eventbus.Message.CONNECTED)

    def on_interactive(self, args):
        self.verbose = args.verbose
        ret = self._registry.find_command('connect').run_cli(args)
        if ret:
            raise exceptions.CommandError('Failed starting interactive mode')
        self.registry.dispatch_message(eventbus.Message.CONNECTED)