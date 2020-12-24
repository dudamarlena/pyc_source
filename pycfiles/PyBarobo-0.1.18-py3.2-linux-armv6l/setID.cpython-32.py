# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-armv6l/egg/barobo/demo/util/setID.py
# Compiled at: 2014-09-16 14:39:13
from barobo import Linkbot, BaroboCtx
import time, sys
if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: {0} <Com_Port> [New Linkbot Serial ID]'.format(sys.argv[0]))
        quit()
    ctx = BaroboCtx()
    ctx.connectDongleSFP(sys.argv[1])
    linkbot = ctx.getLinkbot()
    linkbot._setSerialID(sys.argv[2])