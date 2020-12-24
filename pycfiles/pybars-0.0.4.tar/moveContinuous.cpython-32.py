# uncompyle6 version 3.6.7
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-armv6l/egg/barobo/demo/with_BaroboCtx_sfp/moveContinuous.py
# Compiled at: 2014-09-16 14:39:13
import barobo
from barobo import Linkbot, Dongle
import time, sys
if sys.version_info[0] == 3:
    raw_input = input
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
    linkbot.resetToZero()
    print('Moving joints forwards for 4 seconds...')
    linkbot.setJointSpeeds(120, 120, 120)
    linkbot.moveContinuous(barobo.ROBOT_BACKWARD, barobo.ROBOT_BACKWARD, barobo.ROBOT_BACKWARD)
    raw_input('Press enter to stop.')
    linkbot.resetToZero()
    linkbot.stop()