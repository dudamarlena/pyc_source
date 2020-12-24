# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-armv6l/egg/barobo/demo/with_BaroboCtx_sfp/setBuzzerFrequency.py
# Compiled at: 2014-09-16 14:39:13
from barobo import Linkbot, Dongle
import barobo, time, sys
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: {0} <Com_Port> [Linkbot Serial ID]'.format(sys.argv[0]))
        quit()
    if len(sys.argv) == 3:
        serialID = sys.argv[2]
    else:
        serialID = None
    dongle = Dongle()
    dongle.connectDongleSFP(sys.argv[1])
    linkbot = dongle.getLinkbot(serialID)
    linkbot.setBuzzerFrequency(440.5)
    time.sleep(0.1)
    linkbot.setBuzzerFrequency(880.2)
    time.sleep(0.1)
    linkbot.setBuzzerFrequency(440.2)
    time.sleep(0.1)
    linkbot.setBuzzerFrequency(0)