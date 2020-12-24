# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-armv6l/egg/barobo/demo/with_BaroboCtx_sfp/setJointAcceleration.py
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
    linkbot.resetToZero()
    linkbot.recordAnglesBegin(delay=0.1)
    linkbot.setJointStates([
     barobo.ROBOT_BACKWARD, barobo.ROBOT_NEUTRAL, barobo.ROBOT_NEUTRAL], [
     120, 0, 0])
    time.sleep(1)
    linkbot.startJointAcceleration(1, 120)
    time.sleep(5)
    linkbot.stop()
    linkbot.recordAnglesEnd()
    linkbot.recordAnglesPlot()