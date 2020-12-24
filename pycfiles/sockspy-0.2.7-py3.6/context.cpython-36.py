# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/sockspy/core/context.py
# Compiled at: 2017-07-31 04:34:43
# Size of source mod 2**32: 1532 bytes
import signal, sys
from sockspy.core import pool
from sockspy.socket import raw
import logging, traceback

class AppContext(object):
    __doc__ = '\n    IOC/DI implementation. Use this class as the application context to configure components.\n    '

    def __init__(self, engine_constructor, config):
        self.pool = pool.EndpointPool()
        self.engine = engine_constructor(config, self.pool)
        self.config = config
        self.logger = logging.getLogger(__name__)

    def run(self):

        def handle_signal(sig, _):
            self.logger.debug('destroy engine with signal: ' + str(sig))
            raise KeyboardInterrupt('interrupt by signal!')

        signal.signal(signal.SIGINT, handle_signal)
        signal.signal(signal.SIGTERM, handle_signal)
        result_code = 0
        try:
            try:
                self.pool.set_listener(raw.server_socket(self.config.address, self.config.backlog))
                self.pool.poll(self.engine, self.config.timeout)
            except SystemExit:
                pass
            except KeyboardInterrupt:
                pass
            except InterruptedError:
                pass
            except:
                self.logger.error('<<< context error!\n' + traceback.format_exc())
                result_code = 1

        finally:
            self.engine.destroy()
            sys.exit(result_code)