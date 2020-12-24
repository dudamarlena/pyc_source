# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/etheno/truffle.py
# Compiled at: 2019-06-27 23:49:12
# Size of source mod 2**32: 1561 bytes
from collections.abc import Sequence
import shlex, time
from typing import Iterable
from .logger import EthenoLogger, PtyLogger

def make_list(args: Iterable):
    if isinstance(args, str):
        return shlex.split(args)
        if isinstance(args, Sequence) and not isinstance(args, bytes):
            if isinstance(args, list):
                return args
            return list(args)
    else:
        return [
         args]


class Truffle(object):

    def __init__(self, truffle_cmd='truffle', parent_logger=None, log_level=None):
        self._running = False
        self.logger = EthenoLogger('Truffle', log_level=log_level, parent=parent_logger)
        self.truffle_cmd = make_list(truffle_cmd)

    def terminate(self):
        self._running = False

    def run_tests(self):
        return self.run('test')

    def run_migrate(self):
        return self.run('migrate')

    def run(self, args):
        self._running = True
        args = make_list(args)
        p = PtyLogger(self.logger, ['/usr/bin/env'] + self.truffle_cmd + args)
        p.start()
        try:
            try:
                while p.isalive():
                    if not self._running:
                        self.logger.info('Etheno received a shutdown signal; terminating truffle %s' % ' '.join(args))
                        break
                    time.sleep(1.0)

            except KeyboardInterrupt as e:
                try:
                    self.logger.info('Caught keyboard interrupt; terminating truffle %s' % ' '.join(args))
                    raise e
                finally:
                    e = None
                    del e

        finally:
            p.close(force=True)

        return p.wait()