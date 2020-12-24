# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/flawless/server/stub.py
# Compiled at: 2014-11-13 17:37:22
from flawless.server.api import Flawless

class FlawlessServiceStub(Flawless.Iface):

    def __init__(self):
        for func in [ f for f in dir(self) if not f.startswith('_') ]:
            getattr(self, func).__dict__['result'] = None
            getattr(self, func).__dict__['last_args'] = None
            getattr(self, func).__dict__['args_list'] = list()

        return

    def _handle_stub(self, func, args):
        last_args = dict((k, v) for k, v in args.items() if k != 'self')
        getattr(self, func).__dict__['last_args'] = last_args
        getattr(self, func).__dict__['args_list'].append(last_args)
        return getattr(self, func).__dict__['result']

    def record_error(self, request):
        return self._handle_stub('record_error', locals())