# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-armv6l/egg/barobo/demo/with_BaroboCtx_sfp/jointEventTest3.py
# Compiled at: 2014-09-16 14:39:13
from barobo import Linkbot, Dongle
import sys

def jointcb(millis, j1, j2, j3, mask):
    print('joint: {} {} {} {} {}'.format(millis, j1, j2, j3, mask))


def accelcb(millis, j1, j2, j3):
    print('accel: {} {} {} {}'.format(millis, j1, j2, j3))


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
    instr = 'c'
    jointThresh = 1
    accelThresh = 0.1
    jointCBEnabled = False
    accelCBEnabled = False
    while instr != 'q':
        instr = input('Commands:\n1 : Enable/Disable joint callback\n2 : Enable/Disable accel callback\n3 : Increase joint threshold\n4 : Decrease joint threshold\n5 : Increase accel threshold\n6 : Decrease accel threshold\nq : quit')
        if instr == '1':
            if jointCBEnabled:
                linkbot.disableJointEventCallback()
                jointCBEnabled = False
                print('Joint callback disabled.')
            else:
                linkbot.enableJointEventCallback(jointcb)
                jointCBEnabled = True
                print('Joint callback enabled.')
        elif instr == '2':
            if accelCBEnabled:
                linkbot.disableAccelEventCallback()
                accelCBEnabled = False
                print('Accel callback disabled.')
            else:
                linkbot.enableAccelEventCallback(accelcb)
                accelCBEnabled = True
                print('Accel callback enabled.')
        elif instr == '3':
            jointThresh += 1
            linkbot.setJointEventThreshold(jointThresh)
            print('Joint threshold set to {}'.format(jointThresh))
        elif instr == '4':
            jointThresh -= 1
            linkbot.setJointEventThreshold(jointThresh)
            print('Joint threshold set to {}'.format(jointThresh))
        elif instr == '5':
            accelThresh += 0.1
            linkbot.setAccelEventThreshold(accelThresh)
            print('Accel threshold set to {}'.format(accelThresh))
        elif instr == '6':
            accelThresh -= 0.1
            linkbot.setAccelEventThreshold(accelThresh)
            print('Accel threshold set to {}'.format(accelThresh))
            continue