# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-armv6l/egg/barobo/demo/with_BaroboCtx_sfp/driveTo_multi.py
# Compiled at: 2014-09-16 14:39:13
from barobo import Linkbot, Dongle
import time
if __name__ == '__main__':
    linkbot = Linkbot()
    linkbot2 = Linkbot()
    linkbot.connect()
    linkbot2.connect()
    linkbot.resetToZero()
    linkbot2.resetToZero()
    print('Moving joints to 90 degrees...')
    linkbot.driveToNB(90, 90, 90)
    linkbot2.driveToNB(90, 90, 90)
    time.sleep(1)
    print('Moving joints to 0 degrees...')
    linkbot.driveToNB(0, 0, 0)
    linkbot2.driveToNB(0, 0, 0)