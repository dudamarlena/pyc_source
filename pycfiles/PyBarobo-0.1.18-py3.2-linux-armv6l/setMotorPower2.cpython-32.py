# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-armv6l/egg/barobo/demo/with_AutoConnect/setMotorPower2.py
# Compiled at: 2014-09-16 14:39:13
from barobo import Linkbot, Dongle
import time, sys, math
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: {0} [Linkbot Serial ID]'.format(sys.argv[0]))
        quit()
    serialID = sys.argv[1]
    dongle = Dongle()
    dongle.connect()
    linkbot = dongle.getLinkbot(serialID)
    for i in range(0, 1000, 1):
        linkbot.setBuzzerFrequency(int((math.sin(i / 100) + 1) * 1000))

    linkbot.stop()