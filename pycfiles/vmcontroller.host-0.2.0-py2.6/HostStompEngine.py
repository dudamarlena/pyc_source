# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/vmcontroller/host/services/HostStompEngine.py
# Compiled at: 2011-03-04 15:52:41
try:
    import time, pdb, logging, inject, stomper
    from vmcontroller.common import BaseStompEngine
    from vmcontroller.common import support, exceptions
    from vmcontroller.common import destinations
except ImportError, e:
    print 'Import error in %s : %s' % (__name__, e)
    import sys
    sys.exit()

class HostStompEngine(BaseStompEngine):
    logger = logging.getLogger(support.discoverCaller())

    def __init__(self):
        super(HostStompEngine, self).__init__()

    def connected(self, msg):
        return (
         stomper.subscribe(destinations.CONN_DESTINATION),
         stomper.subscribe(destinations.CMD_RES_DESTINATION))