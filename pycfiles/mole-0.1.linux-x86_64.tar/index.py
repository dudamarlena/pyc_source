# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ajdiaz/env/mole/lib/python2.7/site-packages/mole/server/index.py
# Compiled at: 2012-11-19 05:22:20
import os
from setproctitle import setproctitle
from mole.server import Server
from mole.planner import Planner
from mole.event import EventError
from mole.helper.log import getLogger
from mole.helper.process import ProcessPool

class ServerIndex(Server):
    """Create an Index server thread"""

    def _server_index_cb_flush(self, input, index):
        offset = input.tell()
        if offset > self.offset:
            self.log.debug('%-15s: saving a restore point in offset %x' % (self.name, offset))
            index.set_metadata('offset', offset)
            self.offset = offset
        if index.count > 0:
            self.log.debug('%-15s: lat loop got %d new items' % (self.name, index.count))

    def __init__(self, config, logger=None):
        if logger:
            self.log = logger
        else:
            self.log = getLogger('mole: indexer')
        self.config = config
        self.plan = None
        self.name = None
        self.offset = 0
        return

    def execute(self, name, config):
        setproctitle('indexer: %s' % name)
        self.plan = Planner()
        self.name = name
        map(self.plan.add, config.values())
        self.log.info('%-15s: start index plan: %s' % (name, repr(self.plan)))
        try:
            _in = self.plan.get_input()
            _out = self.plan.get_output()
            _out.callback_flush = lambda x: ServerIndex._server_index_cb_flush(self, _in, _out)
            _off = _out.get_metadata('offset')
            if _off is not None:
                _in.seek(_off)
                self.log.info('%-15s: seek forward to last restore point at %x' % (name, _off))
        except ValueError:
            self.log.warning('%-15s: unable seek position, so we cannot resume index', name)

        try:
            self.plan(False)
        except EventError as e:
            self.log.error('%-15s: event error: %s' % (name, str(e)))

        return

    def __call__(self, config):
        return self.execute(config)

    def run(self):
        pool = ProcessPool(len(self.config))
        for k, v in self.config:
            pool.apply_async(func=self.execute, name='mole: indexer - %s' % k, args=[
             k, v])

        setproctitle('mole: indexer')

    def cancel(self):
        self.log.warning('[MASTER]: stopping indexer due to cancel interrupt')
        if self.plan:
            self.plan.cancel()