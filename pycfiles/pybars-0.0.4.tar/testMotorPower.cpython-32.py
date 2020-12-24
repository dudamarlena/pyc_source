# uncompyle6 version 3.6.7
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-armv6l/egg/barobo/demo/with_BaroboCtx_sfp/testMotorPower.py
# Compiled at: 2014-09-16 14:39:13
from barobo import Linkbot, Dongle
import time, sys
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
    linkbot.stop()
    linkbot.setMotorPowers(0, 255, 255)
    time.sleep(1)
    startAngles = linkbot.getJointAngles()
    time.sleep(5)
    endAngles = linkbot.getJointAngles()
    linkbot.stop()
    for start, end in zip(startAngles, endAngles):
        print('Forward Speed: {}'.format((end - start) / 5.0))

    linkbot.setMotorPowers(0, -255, -255)
    time.sleep(1)
    startAngles = linkbot.getJointAngles()
    time.sleep(5)
    endAngles = linkbot.getJointAngles()
    linkbot.stop()
    for start, end in zip(startAngles, endAngles):
        print('Backward Speed: {}'.format((end - start) / 5.0))