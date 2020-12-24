# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/rpc/helpers/fake_agent_service.py
# Compiled at: 2018-01-08 12:01:55
# Size of source mod 2**32: 449 bytes
import logging
from mercury.common.transport import SimpleRouterReqService
log = logging.getLogger('__name__')

class FakeAgentService(SimpleRouterReqService):

    def process(self, message):
        log.info(f"Received message: {message}")
        return {'message': dict(status=0, data=message)}


if __name__ == '__main__':
    logging.basicConfig(level=(logging.DEBUG))
    service = FakeAgentService('tcp://0.0.0.0:9090')
    service.start()