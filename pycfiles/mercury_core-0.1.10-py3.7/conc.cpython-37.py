# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/common/adhoc/conc.py
# Compiled at: 2018-01-29 12:10:54
# Size of source mod 2**32: 757 bytes
import logging, multiprocessing
from mercury.common.transport import get_ctx_and_connect_req_socket, full_req_transceiver
log = logging.getLogger(__name__)
logging.basicConfig(level=(logging.DEBUG))
ZURL = 'tcp://localhost:9090'

def transmit(action):
    r = full_req_transceiver(ZURL, action)
    log.info('Return: {}'.format(r))


t1 = multiprocessing.Process(target=transmit, args=({'action': 'sleep'},))
t2 = multiprocessing.Process(target=transmit, args=({'action': 'fast'},))
t3 = multiprocessing.Process(target=transmit, args=(
 {'action': 'self-destruct'},))
t1.start()
t2.start()
t3.start()
input('Press enter')