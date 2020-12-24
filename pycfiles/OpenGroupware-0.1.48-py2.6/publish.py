# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/foundation/services/publish.py
# Compiled at: 2012-10-12 07:02:39
from coils.core import *

class Publish(Command):
    __domain__ = 'service'
    __operation__ = 'publish'

    def __init__(self):
        Command.__init__(self)

    def parse_parameters(self, **params):
        self._source = params.get('source', 'NULL')
        self._target = params.get('target', None)
        self._data = params.get('data', None)
        return

    def run(self, **params):
        self._result = False
        if self._target is None:
            raise CoilsException('Publish command missing target')
        if self._ctx.amq_available:
            self._ctx.send(self._source, ('coils.pubsub/publish:{0}').format(self._target), self._data)
            self._result = True
        else:
            self.log.warn('Non-service context, cannot send messages')
        return